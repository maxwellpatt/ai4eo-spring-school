# Sat2Scene: 3D Urban Scene Generation from Satellite Images with Diffusion

**arXiv:** [2401.10786](https://huggingface.co/papers/2401.10786)
**Session:** Day 3 — Generative Models for EO

## Authors
Zuoyue Li, Zhenqiang Li, Zhaopeng Cui, Marc Pollefeys, Martin R. Oswald
ETH Zürich; University of Tokyo; Zhejiang University; Microsoft; University of Amsterdam

## Overview

Sat2Scene generates photo-realistic **street-view scenes** from overhead satellite imagery using a novel architecture combining 3D sparse diffusion models with neural rendering. Solves a hard cross-view synthesis problem: given a satellite image of an urban area, generate how that area would look from ground level — for arbitrary viewpoints.

## Key Methods

### Architecture
1. **3D Sparse Diffusion Model**: generates a sparse 3D scene representation from satellite image features
2. **Neural Rendering**: renders the 3D representation into photorealistic street-view images at arbitrary viewpoints
3. **Feed-forward inference**: no per-scene optimization needed — fully feed-forward at test time

### Why It's Hard
- Extreme viewpoint change (top-down → street-level)
- Cross-view appearance gap (satellite textures ≠ street-level appearance)
- Must generalize across different urban environments

## Datasets

- Evaluated on urban scenes from satellite + street-view paired datasets
- Cross-city generalization evaluated across multiple geographic locations

## Main Results

- Generates photo-realistic, geometrically consistent street-view sequences
- Feed-forward approach enables practical inference speeds
- Outperforms prior top-down-to-street-view synthesis methods

## Why It Matters for AI4EO

Demonstrates the intersection of generative models and 3D scene understanding for EO — a frontier combining Day 1 (3D point clouds), Day 3 (generative models), and novel-view synthesis. Shows how satellite imagery can be the seed for immersive 3D understanding of urban environments.
