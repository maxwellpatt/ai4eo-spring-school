# Catchment Flood Surrogate Model

## Goal

Build a surrogate model that mimics the outputs of a flood model — so we can sweep scenario space (different rainfall events, return periods, antecedent conditions) in milliseconds rather than hours per model run.

```
flood_model(catchment, scenario) → outputs      [expensive: hours per run]
surrogate(catchment_embedding, scenario_params) → outputs   [cheap: ms per run]
```

Catchments are represented using **AlphaEarth Foundation embeddings** — pre-computed 64-dimensional vectors from Google DeepMind that distil a year of multi-source satellite data (optical, radar, climate) per 10m pixel. No model training needed to generate these.

---

## Key Design Decisions

### Pooling Strategy

**Do not use mean pooling.** Per [Corley et al. 2026 (arXiv:2603.02080)](https://arxiv.org/pdf/2603.02080), mean pooling discards within-patch variability and degrades accuracy by >10% under spatial shift — exactly the wrong thing to lose for hydrology where soil/land cover/topography heterogeneity within a catchment matters.

**Recommended approach:**
- **GeM (Generalized Mean Pooling)** — drop-in replacement, same 64-dim output, up to 5% accuracy gain and 40% lower geographic generalization gap
- **Stats pooling** — concat of [min, max, mean, std] over the catchment → 256-dim vector; best performance, 4× larger

Stats pooling is the stronger choice for a surrogate model context where we care about distributional properties of land cover within each catchment.

### Embedding Source

[AlphaEarth Foundations](https://deepmind.google/blog/alphaearth-foundations-helps-map-our-planet-in-unprecedented-detail/) — annual 64-dim embeddings at 10m resolution, 2017–2025.

| Property | Value |
|---|---|
| dtype | int8 (not float32 — check if dequantization needed before stats pooling) |
| Bands | 64 per pixel |
| Resolution | 10m |
| Temporal | Annual composites, 2017–2025 |
| Tile index | **STAC-GeoParquet** on [source.coop/tge-labs/aef](https://source.coop/tge-labs/aef) |

**Access pattern:** STAC-GeoParquet tile index → query by bbox → COG paths. Very similar to how Copernicus DEM is fetched in data-platform (`copernicus_dem_tile_discovery` → tile COG downloads). `pystac-client` + `odc-stac` or `stackstac` should work — the 64-band COG will load as an xarray with 64 variables.

**Sources (in preference order):**
1. [Source Cooperative STAC-GeoParquet index](https://source.coop/tge-labs/aef) — free, STAC-native, no egress billing
2. GCS `gs://alphaearth_foundations` — requester-pays, same COGs
3. [AWS Open Data](https://registry.opendata.aws/aef-source/) — free egress within AWS
4. [HuggingFace — Major-TOM/Core-AlphaEarth-Embeddings](https://huggingface.co/datasets/Major-TOM/Core-AlphaEarth-Embeddings) — pre-chunked, check UK tile coverage

Source Cooperative is the best fit for the data-platform pattern — STAC query → discover tiles → download COGs, identical to DEM ingestion.

**Important limitation — annual composites:** Embeddings are annual averages and wash out everything sub-annual (seasonal vegetation state, wet/dry antecedent conditions). For the flood surrogate this means the embedding captures *persistent* catchment character (land cover type, urbanisation, soil type proxy) but NOT the pre-storm state. Antecedent soil moisture must come from a separate source (CHESS/CEH) and be passed as an explicit scenario parameter.

---

## Components

### 1. Catchment Boundaries — new bronze/silver asset

UK catchment boundaries do not currently exist in the data-platform. Needs ingestion.

**Best sources:**
- **NRFA (National River Flow Archive)** — gauged catchment boundaries for ~1,500 stations in England, Scotland, Wales. WFS endpoint via UKCEH. Comes with peak flow records (training targets).
- **EA WFD River Basin Districts / sub-catchments** — broader administrative catchments, less hydrologically precise
- **SEPA / NRW equivalents** for Scotland and Wales

NRFA is the right starting point — catchment boundaries and observed peak flows in one place.

**Asset pattern:** standard WFS ingestion → bronze GeoParquet → silver Iceberg, consistent with existing infrastructure assets.

### 2. AlphaEarth Embeddings for UK — new gold asset

Read AlphaEarth COG tiles covering UK extent, aggregate each 64-dim embedding raster over each catchment polygon using stats pooling → one 256-dim descriptor vector per catchment per year.

**Tool:** [`exactextract`](https://github.com/isciences/exactextract) — designed for fast zonal statistics over COG rasters, handles partial pixel coverage correctly (important for catchment boundaries that don't align to tile grids).

**Output:** parquet table — `(catchment_id, year, embedding_dim_0 … embedding_dim_255)`

### 3. Scenario Parameters

Per-catchment, per-event inputs to the surrogate alongside the embedding:

| Parameter | Source |
|---|---|
| Rainfall event depth (mm) | CEH GEAR gridded rainfall / NRFA metadata |
| Event duration (hrs) | CEH GEAR |
| Return period (years) | FEH / NRFA flood frequency analysis |
| Antecedent soil moisture | CEH Soil Moisture dataset (CHESS) or proxy from API |
| Season / month | derived |

### 4. Training Targets

**Starting point: NRFA peak flow records** — observed annual maximum flows (AMAX) and peak-over-threshold (POT) series for gauged catchments. Freely available, covers ~1,500 catchments, no data agreement needed.

This gives us: `surrogate(embedding, rainfall_event) → peak_discharge`

**Upgrade path:**
- EA National Flood Map — inundation extents for 1:20, 1:100, 1:1000-year events (static, but spatially explicit)
- JBA / Fathom commercial flood model outputs — need data agreement
- Run synthetic scenarios with a lightweight model (LISFLOOD-FP, unit hydrograph) for ungauged catchments

### 5. Surrogate Model

Starting simple:
- **LightGBM or XGBoost** — fast to train, interpretable feature importance, good baseline
- Input: `[256-dim stats-pooled embedding] + [scenario params]`
- Output: `peak_discharge` (log-transformed) or `inundation_extent_fraction`
- Evaluate on spatial hold-out splits (not random — geographic generalisation is the goal)

Once baseline works, upgrade to a small MLP or even a transformer that attends over the embedding dimensions.

### 6. 3D Embedding Space Visualisation

UMAP-reduce the 256-dim catchment vectors to 3D, build an interactive explorer:
- Each point = one UK catchment
- Colour by: peak flow regime, flashiness index, baseflow index, dominant land cover, geographic region
- Hover: catchment name, area, key statistics, satellite thumbnail
- Spatial clusters should correspond to hydrologically similar catchments — this is the validation

**Tool options:**
- Plotly Dash + `plotly.graph_objects.Scatter3d` — simplest, runs in a notebook or small app
- deck.gl `ScatterplotLayer` — if you want catchments on an actual map
- Three.js / react-three-fiber — if you want a custom 3D globe view

---

## Dagster Pipeline (proposed)

```
bronze/catchment_boundaries        ← NRFA WFS ingestion
         ↓
silver/catchment_boundaries        ← Iceberg, EPSG:4326, H3-indexed

alphaearth_tile_discovery          ← query Source Cooperative STAC-GeoParquet index by UK bbox
                                      (mirrors copernicus_dem_tile_discovery pattern)
         ↓
bronze/alphaearth_uk               ← download intersecting COG tiles (64-band, int8, 10m)
         ↓
gold/catchment_embeddings          ← stats-pool AlphaEarth COGs over each catchment polygon
                                      (exactextract zonal stats → min/max/mean/std per dim)
                                      output: parquet (catchment_id, year, emb_0..255)
         ↓
gold/catchment_scenario_features   ← join embeddings + scenario params (NRFA AMAX events)
         ↓
gold/surrogate_training_dataset    ← (features, targets) ready for model training
         ↓
gold/surrogate_model               ← trained LightGBM artifact, serialised to S3
         ↓
gold/surrogate_predictions         ← predictions on held-out / ungauged catchments
         ↓
gold/catchment_umap_coords         ← 3D UMAP reduction of embedding space
```

---

## Data Gaps to Resolve

- [ ] Query Source Cooperative STAC-GeoParquet index for UK bbox to confirm tile coverage and COG structure
- [ ] Check int8 dtype — determine whether raw int8 or dequantized float values are needed for stats pooling
- [ ] Check NRFA WFS endpoint is still live and accessible without auth
- [ ] Determine whether EA National Flood Map extents are openly accessible (they are, via data.gov.uk)
- [ ] Decide: stats pooling (256-dim, better) vs GeM (64-dim, simpler) — recommend starting with stats pooling

---

## Relevant Papers

| Paper | Why relevant |
|---|---|
| [Foundation-Scale Satellite Embeddings Reframe Hydrological Generalization (GRL 2026)](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025GL121604) | Direct precedent — AlphaEarth embeddings for 455 Australian catchments, outperforms static attributes |
| [From Pixels to Patches: Pooling Strategies for Earth Embeddings (arXiv:2603.02080)](https://arxiv.org/pdf/2603.02080) | Why not to use mean pooling; GeM and stats pooling recommendation |
| [Prithvi-EO-2.0 (arXiv:2412.02732)](../papers/prithvi-eo-2.md) | Alternative embedding source if AlphaEarth coverage is insufficient |
| [DiffusionSat (arXiv:2312.03606)](../papers/diffusionsat.md) | Generative model — potentially useful for synthetic scenario generation downstream |
