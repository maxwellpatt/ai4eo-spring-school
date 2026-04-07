# Generating Physically-Consistent Satellite Imagery for Climate Visualizations

**arXiv:** [2104.04785](https://huggingface.co/papers/2104.04785)
**Session:** Day 3 — Generative Models for EO

## Authors
Björn Lütjens (MIT), Brandon Leshchinskiy (MIT), Océane Boulais, Farrukh Chishtie, Natalia Díaz-Rodríguez, et al.

## Overview

Addresses a key problem with generative satellite imagery: **hallucinations**. Pure deep learning GANs generate photorealistic but physically-inconsistent flood visualizations. This paper proposes conditioning on **physics-based flood model outputs** (segmentation maps from hydraulic simulations) to ensure generated images actually reflect the underlying physics — enabling trustworthy climate change communication.

## Key Methods

### Physics-Informed GAN
- Base model: **pix2pixHD** (1024×1024×4 inputs)
- Inputs: pre-event satellite image + physics-based flood mask (from Fathom hydraulic model)
- Output: post-event satellite image

### Physical Consistency Definition
```
Generated image is physically-consistent if:
||flood_segmentation(I_generated) - flood_mask_physics|| < ε
```

### Novel Evaluation Metric: FVPS
**Flood Visualization Plausibility Score** — harmonic mean of:
- **IoU**: measures physical consistency (does the water appear where physics says it should?)
- **LPIPS**: measures photorealism (does it look like a real satellite image?)

`FVPS = 2 / (1/(IoU + ε) + 1/(1 - LPIPS + ε))`

## Results

| Model | LPIPS ↓ | IoU ↑ | FVPS ↑ |
|---|---|---|---|
| **GAN + physics (ours)** | 0.265 | 0.502 | 0.533 |
| GAN (no physics) | 0.293 | 0.226 | 0.275 |
| Handcrafted baseline | 0.399 | 0.470 | 0.411 |

Physics conditioning dramatically improves IoU while maintaining photorealism.

## Datasets

| Dataset | Events | Resolution |
|---|---|---|
| xbd2xbd | 7 flood events (Harvey, Florence, Michael, etc.) | ~0.5 m/px |
| xbdfathom | Hurricane Harvey (physics-based masks) | ~30 m/px |
| forest | Reforestation in 4 countries | 50 cm/px |
| arctic | Arctic sea ice melt | Variable |

**Total**: 30,000+ labeled HD image triplets (~90 GB), publicly released.

## Key Contributions

1. First physics-conditioned GAN for satellite imagery generation
2. FVPS: new joint metric for photorealism + physical consistency
3. 30k+ open-source labeled image triplets across flood, reforestation, and sea ice events
4. Validates generalization across three different climate phenomena

## Why It Matters for AI4EO

Perfect intersection of generative models (Day 3) and responsible AI (Day 2): demonstrates that photorealism alone is insufficient — generated imagery must be physically consistent to be safe for climate communication and decision-making.

## Code & Demo
- GitHub: [blutjens/eie-earth-public](https://github.com/blutjens/eie-earth-public)
- Interactive demo: [climate-viz.github.io](https://climate-viz.github.io/)
