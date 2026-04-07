# Prithvi-EO-2.0: A Versatile Multi-Temporal Foundation Model for Earth Observation Applications

**arXiv:** [2412.02732](https://huggingface.co/papers/2412.02732)
**Session:** Day 2 — Foundation Models for EO

## Authors
Daniela Szwarcman, Sujit Roy, Paolo Fraccaro, et al.
IBM Research (UK, Ireland, Brazil, Zurich, USA); NASA Marshall Space Flight Center; multiple universities

## Overview

Prithvi-EO-2.0 is a geospatial foundation model that builds on the original Prithvi (NASA/IBM) with improved architecture, stronger benchmark performance, and support for temporal and location-aware embeddings. It is one of the few open-weight EO FMs designed explicitly for multi-temporal satellite imagery tasks.

## Key Methods

- **Temporal embeddings**: encodes time-of-acquisition to handle irregularly-sampled multi-date imagery
- **Location embeddings**: encodes geographic coordinates to improve spatial generalization
- **Backbone**: masked autoencoder (MAE) pretraining on large-scale multi-spectral satellite data
- Evaluated on **GEO-Bench** across multiple downstream tasks at varying resolutions

## Key Tasks Supported

- Disaster response mapping
- Land use and crop mapping
- Ecosystem dynamics monitoring
- Semantic segmentation, scene classification

## Main Contributions

1. First major update to the Prithvi EO FM — improved performance across GEO-Bench tasks
2. Temporal + location embeddings enable better handling of spatio-temporal EO data
3. Open weights released, compatible with fine-tuning pipelines

## Why It Matters for AI4EO

Prithvi-EO-2.0 is a practical, open-access FM representative of the current state of the art. It demonstrates how pretraining design choices (temporal embeddings, location conditioning) directly translate to downstream task performance.

## Code & Weights
- HuggingFace: [ibm-nasa-geospatial/Prithvi-EO-2.0](https://huggingface.co/ibm-nasa-geospatial)
