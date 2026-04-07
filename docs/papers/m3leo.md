# M3LEO: A Multi-Modal, Multi-Label Earth Observation Dataset Integrating Interferometric SAR and Multispectral Data

**arXiv:** [2406.04230](https://huggingface.co/papers/2406.04230)
**Session:** Day 4 — TorchGeo + MLOps

## Authors
Matt Allen (Cambridge), Francisco Dorr, Joseph A. Gallego-Mejia (Drexel), Laura Martínez-Ferrer (Universitat de València), Anna Jungbluth (ESA Climate Office), Freddie Kalaitzis (Oxford), Raúl Ramos-Pollán (U. Antioquia)

## Overview

M3LEO is the first large-scale EO dataset to combine polarimetric SAR, interferometric SAR (InSAR), and coherence data alongside multispectral optical imagery — covering ~14% of Earth's land surface. Paired with a flexible PyTorch Lightning framework and Hydra config management for ML experimentation.

## Dataset

| Stat | Value |
|---|---|
| Total chips | ~17 million (4×4 km each) |
| Land surface covered | 21.05×10⁶ km² (~14.1% of Earth) |
| Geographic regions | 6 (CONUS, Europe, Middle East, Pakistan/India, China, South America) |
| SAR products | Sentinel-1 amplitude, InSAR unwrapped phase, coherence (12/24/36/48-day baselines) |
| Optical | Sentinel-2 L2A (monthly composites, 2018–2020) |
| Auxiliary | ESA WorldCover, AGB biomass, SRTM DEM, MODIS vegetation, GHS built surface |

## Key Methods

### SAR Data Products
- **Amplitude (Polarimetric SAR)**: Sentinel-1 GRD, VV+VH, 10 m/pixel
- **InSAR**: ASF ARIA GUNW unwrapped interferograms, ~90 m/pixel
- **Coherence**: Global Seasonal Sentinel-1 Interferometric Coherence (GSSIC), ~90 m/pixel

### ML Framework
- PyTorch Lightning + Hydra configuration
- Self-supervised methods: MAE, CLIP, DINO
- Geographic band-based train/val/test splits (60/20/20%)

## Key Results

| Input Modality | ESAWC mIoU |
|---|---|
| S1 VV+VH | 0.419 |
| S2 RGB | 0.400 |
| GSSIC coherence | 0.291 |
| **S1+S2 fusion** | **0.463** |

- SAR-optical fusion consistently outperforms any single modality
- Strong distribution shift between geographic regions — important for generalization research

## Why It Matters for AI4EO

Demonstrates SAR+optical multimodal pipelines at scale — a pattern directly relevant to Zora's raster processing work. The PyTorch Lightning + Hydra framework design is a good MLOps template.

## Code & Data
- Dataset: [huggingface.co/M3LEO](https://huggingface.co/M3LEO)
- Miniset (5k tiles/region): [huggingface.co/M3LEO-miniset](https://huggingface.co/M3LEO-miniset)
- Code: [github.com/spaceml-org/M3LEO](https://github.com/spaceml-org/M3LEO)
