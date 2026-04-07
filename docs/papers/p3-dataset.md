# The P³ Dataset: Pixels, Points and Polygons for Multimodal Building Vectorization

**arXiv:** [2505.15379](https://huggingface.co/papers/2505.15379)
**Session:** Day 1 — Deep Learning for Change Detection in 3D Point Clouds

## Authors
Raphael Sulzer, Liuyun Duan, Nicolas Girard, Florent Lafarge
LuxCarta Technology, Mouans-Sartoux, France; Centre Inria d'Université Côte d'Azur, Sophia Antipolis, France

## Overview

P³ is a large-scale multimodal benchmark for building vectorization combining aerial LiDAR point clouds, high-resolution aerial imagery, and vectorized 2D building outlines collected across three continents. The paper argues that LiDAR serves as a robust modality for building polygon prediction, and that fusion with optical imagery pushes accuracy further.

## Dataset

| Stat | Value |
|---|---|
| LiDAR points | 10+ billion |
| LiDAR accuracy | Decimeter-level |
| Image GSD | 25 cm |
| Geographic coverage | 3 continents |
| Annotations | Vectorized 2D building outlines |

## Key Methods

- **Hybrid frameworks**: combine LiDAR and imagery in separate branches, fuse for prediction
- **End-to-end frameworks**: joint learning directly from both modalities
- Benchmarks three state-of-the-art building polygon prediction models with pretrained weights released

## Key Findings

- LiDAR alone outperforms imagery alone for building polygon prediction
- Fusing LiDAR + aerial imagery achieves the best accuracy and geometric quality
- Multimodal fusion is especially beneficial for complex rooftop geometries

## Main Contributions

1. First large-scale multimodal dataset combining LiDAR, imagery, and building polygons across 3 continents
2. Rigorous comparison of hybrid vs. end-to-end multimodal learning frameworks
3. Public release with code and pretrained model weights

## Code & Data
- GitHub: [raphaelsulzer/PixelsPointsPolygons](https://github.com/raphaelsulzer/PixelsPointsPolygons)
