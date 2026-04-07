# AI4EO Spring School 2026

Link to course home page: https://www-obelix.irisa.fr/ai4eo-spring-school-2026/

**Hosted by:** OBELIX group at IRISA, Université Bretagne Sud, Vannes
**Dates:** April 8–10, 2026

**Co-organised with:**
- Copernicus Master in Digital Earth
- Cluster SequoIA (PANORAMIX chair)
- ESA Phi-lab

## Schedule Overview

### Day 1
- [Deep learning for change detection in 3D point clouds](notes/day1/point_clouds.md) — Iris de Gélis (Estellus / Paris Observatory)
- [Foundation Models for EO](notes/day1/foundation_models.md) — Stéphane May (CNES) & Pierre Adorni (IRISA)

### Day 2
- [Responsible AI in EO](notes/day2/responsible_ai.md) — Pedram Ghamisi (HZDR / Lancaster University)
- [Introduction to Deep Learning with TorchGeo + MLOps](notes/day2/torchgeo_mlops.md) — Adam Stewart (TU Munich)

### Day 3
- [Generative models for EO](notes/day3/generative_models.md) — Nicolas Audebert (IGN / LASTIG lab)
- [ESA Phi-lab data-driven project](notes/day3/phi_lab_project.md) — Group work

## Repository Structure

```
definitions.py          # Dagster definitions entry point
pyproject.toml          # Project dependencies (uv)
notes/                  # Per-session notes and preparation
  day1/
    foundation_models.md
    point_clouds.md
  day2/
    responsible_ai.md
    torchgeo_mlops.md
  day3/
    generative_models.md
    phi_lab_project.md
assets/                 # Dagster assets for experiments
  foundation_models.py
  point_clouds.py
  generative.py
  torchgeo_tutorial.py  # TorchGeo pipeline (raw_data → geo_dataset → trained_model)
  phi_lab/
data/                   # Downloaded datasets (gitignored)
  torchgeo_tutorial/    # Landsat 7/8 + Cropland Data Layer (CDL)
checkpoints/            # Trained model checkpoints (gitignored)
```

## Setup

```bash
uv sync --extra dagster
uv run --extra dagster dagster dev
```
