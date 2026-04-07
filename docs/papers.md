# AI4EO Spring School 2026 — Paper Reading List

Curated papers by session, sourced from Hugging Face Papers.

---

## Session 1 — Deep Learning for Change Detection in 3D Point Clouds
*Iris de Gélis (Estellus / Paris Observatory)*

| Paper | Summary |
|---|---|
| **SceneEdited** — [2511.15153](https://hf.co/papers/2511.15153) | City-scale benchmark for 3D point cloud updating via image-guided change detection |
| **Point2Building** — [2403.02136](https://hf.co/papers/2403.02136) | Autoregressive model reconstructing 3D building meshes from airborne LiDAR |
| **ECLAIR** — [2404.10699](https://hf.co/papers/2404.10699) | Large-scale aerial LiDAR dataset for point cloud semantic segmentation |
| **P³ Dataset** — [2505.15379](https://hf.co/papers/2505.15379) | Pixels, points, and polygons for multimodal building vectorization |

---

## Session 2 — Foundation Models for EO
*Stéphane May (CNES) & Pierre Adorni (IRISA)*

| Paper | Summary |
|---|---|
| **Prithvi-EO-2.0** — [2412.02732](https://hf.co/papers/2412.02732) | Multi-temporal geospatial FM with temporal/location embeddings; strong benchmark results |
| **REOBench** — [2505.16793](https://hf.co/papers/2505.16793) | Robustness benchmark for EO FMs under corruptions — good critical read |
| **SSL4EO-L** — [2306.09424](https://hf.co/papers/2306.09424) | SSL datasets and FMs for Landsat; by Adam Stewart (the Day 2 speaker) |
| **Efficient SSL for EO via Dynamic Dataset Curation** — [2504.06962](https://hf.co/papers/2504.06962) | Dynamic pruning strategy to improve FM pretraining diversity |
| **GeoLLaVA-8K** — [2505.21375](https://hf.co/papers/2505.21375) | Multimodal LLM for remote sensing at 8K resolution |

---

## Session 3 — Responsible AI in EO
*Pedram Ghamisi (HZDR / Lancaster University)*

| Paper | Summary |
|---|---|
| **Fairness & Bias Mitigation in Computer Vision: A Survey** — [2408.02464](https://hf.co/papers/2408.02464) | Broad survey on bias discovery and mitigation; good foundation for the EO angle |
| **The Quest for Reliable Metrics of Responsible AI** — [2510.26007](https://hf.co/papers/2510.26007) | Assesses robustness of fairness metrics across recommender systems |
| **Change-Agent** — [2403.19646](https://hf.co/papers/2403.19646) | LLM-driven change detection with captioning and cause analysis — intersects interpretability |

> Note: Ghamisi's own papers are not indexed on HF Papers, but his work on **Physics-Aware Machine Learning** and **Explainability in Hyperspectral Image Analysis** is worth searching on arXiv directly.

---

## Session 4 — Introduction to Deep Learning with TorchGeo + MLOps
*Adam Stewart (TU Munich)*

| Paper | Summary |
|---|---|
| **TorchGeo** — [2111.08872](https://hf.co/papers/2111.08872) | The core paper; essential reading before this session |
| **SSL4EO-L** — [2306.09424](https://hf.co/papers/2306.09424) | Follow-up from the same author — SSL + Landsat FMs built on TorchGeo |
| **M3LEO** — [2406.04230](https://hf.co/papers/2406.04230) | Multi-modal SAR+optical EO dataset with PyTorch Lightning framework |

---

## Session 5 — Generative Models for EO
*Nicolas Audebert (IGN / LASTIG)*

| Paper | Summary |
|---|---|
| **DiffusionSat** — [2312.03606](https://hf.co/papers/2312.03606) | Largest generative FM for satellite imagery; metadata-conditioned diffusion |
| **SatDiFuser** — [2503.07890](https://hf.co/papers/2503.07890) | Diffusion-based GFM that outperforms discriminative models on segmentation |
| **Generate Your Own Scotland** — [2308.16648](https://hf.co/papers/2308.16648) | ControlNet conditioned on OpenStreetMap to generate realistic satellite images |
| **Sat2Scene** — [2401.10786](https://hf.co/papers/2401.10786) | 3D diffusion + neural rendering for street-view generation from satellite imagery |
| **Physics-Consistent Satellite Imagery for Climate Viz** — [2104.04785](https://hf.co/papers/2104.04785) | GAN conditioned on physics models for flood/reforestation visualization |
