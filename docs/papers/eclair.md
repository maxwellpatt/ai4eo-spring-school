# ECLAIR: A High-Fidelity Aerial LiDAR Dataset for Semantic Segmentation

**arXiv:** [2404.10699](https://huggingface.co/papers/2404.10699)
**Session:** Day 1 — Deep Learning for Change Detection in 3D Point Clouds

## Authors
Iaroslav Melekhov, Anand Umashankar, Hyeong-Jin Kim, Vladislav Serkov, Dusty Argyle
Sharper Shape; Aalto University

## Overview

ECLAIR (Extended Classification of Lidar for AI Recognition) is a large-scale outdoor aerial LiDAR dataset purpose-built for advancing point cloud semantic segmentation. It is one of the most extensive and diverse datasets of its kind, curated by internal expert annotators for high quality labels.

## Dataset

| Stat | Value |
|---|---|
| Total area | 10 km² |
| Total points | ~600 million |
| Object categories | 11 |
| Labeling | Expert-curated, high-quality semantic labels |

**Categories include:** ground, vegetation, buildings, utility infrastructure, and other urban structures.

## Key Methods

- Benchmark uses a **voxel-based point cloud segmentation** approach based on the **Minkowski Engine**
- Provides both qualitative and quantitative analysis as a baseline for the community

## Applications

Designed to advance:
- 3D urban modeling
- Scene understanding
- Utility infrastructure management (power lines, poles)

## Main Contributions

1. Largest and most diverse aerial LiDAR semantic segmentation dataset at time of release
2. Expert-quality labels across 11 categories — higher fidelity than crowd-sourced alternatives
3. Open-source release with baseline benchmark results

## Code & Data
- GitHub: [SharperShape/eclair-dataset](https://github.com/SharperShape/eclair-dataset)
