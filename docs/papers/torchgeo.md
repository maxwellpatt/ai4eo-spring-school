# TorchGeo: Deep Learning With Geospatial Data

**arXiv:** [2111.08872](https://huggingface.co/papers/2111.08872)
**Session:** Day 4 — Introduction to Deep Learning with TorchGeo + MLOps

## Authors
Adam J. Stewart, Caleb Robinson, Isaac A. Corley, Anthony Ortiz, Juan M. Lavista Ferres, Arindam Banerjee
University of Illinois Urbana-Champaign; Microsoft AI for Good Research Lab; UT San Antonio

## Overview

TorchGeo is a Python library that integrates geospatial data into the PyTorch deep learning ecosystem. It addresses the non-trivial challenges of working with remotely sensed data: extra spectral bands beyond RGB, differing coordinate systems, varying resolutions, and the need to join multiple geospatial data sources. **Essential reading before the Day 4 session.**

## Key Challenges Addressed

- Satellite imagery has additional spectral bands (SWIR, NIR, etc.) not supported by standard CV libraries
- Geospatial datasets use different CRS (coordinate reference systems), bounds, and resolutions
- Sampling must be aware of spatial extent, not just image indices
- No standardized benchmark datasets or pretrained models existed for remote sensing

## Key Components

| Component | Description |
|---|---|
| **Datasets** | Data loaders for 40+ benchmark remote sensing datasets |
| **Composable Datasets** | Combine multiple geospatial sources by spatial intersection |
| **Samplers** | Geospatially-aware samplers (random, grid, stratified by class) |
| **Transforms** | Works with multispectral imagery (arbitrary number of channels) |
| **Pretrained Models** | ImageNet-pretrained weights adapted for multispectral use |

## Datasets Included (selection)

Landsat, Sentinel-1/2, NAIP, BigEarthNet, EuroSAT, UC Merced, DOTA, LandCover.ai, Cropland Data Layer (CDL), and many more.

## Main Contributions

1. First unified geospatial data library for PyTorch
2. Composable dataset abstraction for seamlessly joining geospatial data sources
3. Geospatially-aware samplers that respect spatial boundaries
4. Reproducible benchmark results on multiple remote sensing datasets
5. Foundation for SSL4EO-L, GEO-Bench, and many other EO ML works

## Why It Matters for AI4EO

TorchGeo is the Day 4 session topic. Adam Stewart (lead author) is presenting. This is the core infrastructure paper — reading it before the session will make the tutorial significantly more useful.

## Code
- GitHub: [microsoft/torchgeo](https://github.com/microsoft/torchgeo)
- Docs: [torchgeo.readthedocs.io](https://torchgeo.readthedocs.io)
