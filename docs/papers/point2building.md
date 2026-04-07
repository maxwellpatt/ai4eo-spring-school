# Point2Building: Reconstructing Buildings from Airborne LiDAR Point Clouds

**arXiv:** [2403.02136](https://huggingface.co/papers/2403.02136)
**Session:** Day 1 — Deep Learning for Change Detection in 3D Point Clouds

## Authors
Yujia Liu, Anton Obukhov, Jan Dirk Wegner, Konrad Schindler
ETH Zürich (Photogrammetry and Remote Sensing); University of Zürich

## Overview

A learning-based approach to reconstructing buildings as 3D polygonal meshes directly from airborne LiDAR point clouds, without relying on exhaustive preprocessing steps like plane detection. The key challenge is the large diversity of roof shapes, low/varying point density, and incomplete facade coverage due to vegetation occlusions.

## Key Methods

- **Autoregressive generative model** (Point2Building): iteratively builds up the mesh by generating sequences of vertices and faces
- **No heavy preprocessing**: learns directly from raw point cloud data, reducing error propagation
- **Flexible geometry generation**: adapts to diverse building structures without hand-crafted shape priors
- Architecture uses Transformers for sequence generation over mesh vertex/face tokens

## Datasets

- Airborne LiDAR from **Zurich**, **Berlin**, and **Tallinn** — diverse urban styles used for training and evaluation
- Demonstrates good generalization across European urban morphologies

## Main Contributions

1. First autoregressive model to directly predict 3D polygonal meshes from LiDAR point clouds
2. Eliminates need for plane detection preprocessing — end-to-end learning from raw data
3. Good cross-city generalization despite different architectural styles

## Code
- Available via the paper's project page (ETH Zürich Photogrammetry group)
