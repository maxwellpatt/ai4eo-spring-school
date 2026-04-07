# Can Generative Geospatial Diffusion Models Excel as Discriminative Geospatial Foundation Models?

**arXiv:** [2503.07890](https://huggingface.co/papers/2503.07890)
**Session:** Day 3 — Generative Models for EO

## Authors
Yuru Jia, Valerio Marsocci, Ziyang Gong, Xue Yang, Maarten Vergauwen, Andrea Nascetti
KU Leuven; KTH; European Space Agency; Shanghai AI Lab; SJTU

## Overview

Asks and answers a fundamental question: can a **generative** diffusion model — trained to synthesize satellite imagery — also serve as a **discriminative** geospatial foundation model for tasks like segmentation and classification? The answer is yes, via **SatDiFuser**, which extracts and fuses multi-stage diffusion features for discriminative downstream tasks.

## Key Insight

Diffusion models learn rich, multi-grained semantic representations during the denoising process — including local textures, global structure, and semantic content. These representations are underexploited when the model is used only for generation.

## Key Methods

### SatDiFuser Framework
1. Extract diffusion features at multiple **noise levels** (timesteps) and **decoder stages**
2. Analyze which timesteps / stages encode which semantic granularity
3. Apply three **fusion strategies** to combine these diverse representations for downstream tasks:
   - Channel concatenation
   - Attention-based fusion
   - Cross-scale feature pyramid fusion

## Results

| Task | Improvement over SOTA GFMs |
|---|---|
| Semantic Segmentation (mIoU) | +5.7% |
| Scene Classification (F1-score) | +7.9% |

Outperforms leading discriminative GFMs (MAE-based, contrastive) on standard RS benchmarks.

## Benchmarks
- Semantic segmentation: OpenEarthMap, Potsdam, iSAID
- Classification: UCMerced, AID, RESISC45

## Why It Matters for AI4EO

Bridges the gap between generative and discriminative EO models — showing that the two paradigms are complementary, not separate. Strong result for the Day 3 (generative models) and Day 2 (foundation models) sessions.

## Code
- GitHub: [yurujaja/SatDiFuser](https://github.com/yurujaja/SatDiFuser)
