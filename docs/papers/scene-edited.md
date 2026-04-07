# SceneEdited: A City-Scale Benchmark for 3D HD Map Updating via Image-Guided Change Detection

**arXiv:** [2511.15153](https://huggingface.co/papers/2511.15153)
**Session:** Day 1 — Deep Learning for Change Detection in 3D Point Clouds

## Authors
Chun-Jung Lin, Tat-Jun Chin, Sourav Garg, Feras Dayoub
Australian Institute for Machine Learning (AIML), University of Adelaide

## Overview

Addresses the gap between *detecting* changes and *incorporating* them into updated 3D HD maps — a critical step for urban planning, infrastructure monitoring, and autonomous navigation. SceneEdited is the first city-scale dataset explicitly designed to support research on HD map maintenance through 3D point cloud updating.

## Key Methods

- **Dataset construction**: Synthesized 23,000+ object changes (both manual and automatic) across 2,000+ out-of-date scene versions, simulating realistic urban modifications (missing roadside infrastructure, buildings, overpasses, utility poles)
- **Baseline**: Foundational image-based structure-from-motion (SfM) pipeline for updating outdated 3D scenes
- **Toolkit**: Supports scalability, trackability, and portability for future dataset expansion and annotation unification

## Dataset

| Stat | Value |
|---|---|
| Scenes | 800+ up-to-date scenes |
| Coverage | 73 km driving, ~3 km² urban area |
| Synthesized changes | 23,000+ |
| Out-of-date versions | 2,000+ |
| Per-scene data | Calibrated RGB images, LiDAR scans, change masks |

## Main Contributions

1. First city-scale dataset linking 2D image-based change detection to 3D map updating
2. Realistic simulation of urban object changes with detailed change masks
3. Standardized benchmark for future research on HD map maintenance

## Code & Data
- GitHub: [ChadLin9596/ScenePoint-ETK](https://github.com/ChadLin9596/ScenePoint-ETK)
