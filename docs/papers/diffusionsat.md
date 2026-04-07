# DiffusionSat: A Generative Foundation Model for Satellite Imagery

**arXiv:** [2312.03606](https://huggingface.co/papers/2312.03606)
**Session:** Day 3 — Generative Models for EO

## Authors
Samar Khanna, Patrick Liu, Linqi Zhou, Chenlin Meng, Robin Rombach, Marshall Burke, David Lobell, Stefano Ermon
Stanford University; Stability AI

## Overview

DiffusionSat is the largest generative foundation model for satellite imagery at time of publication. It addresses the key ways satellite images differ from natural images — multi-spectral channels, irregular temporal sampling, and sparse/unavailable text captions — by using **geospatial metadata as conditioning** instead of captions.

## Key Methods

### Architecture
- Based on latent diffusion models (LDMs)
- Metadata conditioning: geolocation, acquisition time, sensor parameters — replaces text prompts
- Trained on multiple large public remote sensing datasets

### Supported Tasks
| Task | Description |
|---|---|
| **Temporal generation** | Generate future imagery given past acquisitions |
| **Super-resolution** | Upscale multi-spectral imagery given low-res inputs |
| **Inpainting** | Fill missing or cloud-covered regions |

## Datasets Used for Pretraining

Multiple large public remote sensing datasets (Sentinel-2, Landsat, NAIP, fMoW, etc.)

## Main Results

- State-of-the-art on satellite image generation across all three tasks at time of release
- Metadata conditioning outperforms text-based conditioning for EO data
- First model to unify temporal generation, super-resolution, and inpainting in a single framework

## Why It Matters for AI4EO

DiffusionSat is the canonical example of applying diffusion models to EO — directly what Nicolas Audebert's Day 3 session covers. Key paper to read to understand where the field is going with generative models for satellite data.

## Project Page
- [samar-khanna.github.io/DiffusionSat](https://samar-khanna.github.io/DiffusionSat/)
