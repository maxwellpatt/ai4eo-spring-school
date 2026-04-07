# SSL4EO-L: Datasets and Foundation Models for Landsat Imagery

**arXiv:** [2306.09424](https://huggingface.co/papers/2306.09424)
**Session:** Day 2 — Foundation Models for EO / Day 4 — TorchGeo + MLOps

## Authors
Adam J. Stewart, Nils Lehmann, Isaac A. Corley, Yi Wang, Yi-Chia Chang, Nassim Ait Ali Braham, Shradha Sehgal, Caleb Robinson, Arindam Banerjee
UIUC; TU Munich; UT San Antonio; DLR; Microsoft AI for Good

## Overview

The first SSL dataset and foundation models for the Landsat satellite family — the longest-running EO program (50+ years, 8 satellites). Addresses the gap where most Landsat analysis still uses decision trees / random forests due to lack of labeled data and pretrained models. All datasets and weights are distributed via **TorchGeo**.

## Dataset: SSL4EO-L

| Stat | Value |
|---|---|
| Image patches | 5 million |
| Sensors covered | Landsat 4/5 TM, Landsat 7 ETM+, Landsat 8/9 OLI |
| Product levels | SR (Surface Reflectance) and TOA |
| Status | Largest Landsat dataset in history at time of release |

Also re-releases modernized versions of:
- **L7 Irish**: cloud detection dataset for Landsat 7
- **L8 Biome**: cloud detection dataset for Landsat 8
- New ML benchmarks for Landsats 4–5 TM and Landsat 7 ETM+ SR

## Key Methods

- Self-supervised pretraining (MAE, MoCo) on SSL4EO-L
- Fine-tuning evaluated on multiple **semantic segmentation** benchmarks
- Distributed via TorchGeo — plug-and-play with standard PyTorch training pipelines

## Main Contributions

1. First purpose-built SSL dataset for the entire Landsat family
2. First pretrained foundation models for Landsat imagery
3. Modernized cloud detection benchmarks for Landsat 7 and 8
4. Full TorchGeo integration for reproducibility

## Why It Matters for AI4EO

Directly relevant to Day 4 (TorchGeo session by Adam Stewart, who is also the lead author). Demonstrates the full pipeline: dataset → SSL pretraining → fine-tuning → benchmark evaluation, all through TorchGeo.

## Code & Data
- Available via [TorchGeo](https://github.com/microsoft/torchgeo)
