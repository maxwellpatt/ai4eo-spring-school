# GeoLLaVA-8K: Scaling Remote-Sensing Multimodal Large Language Models to 8K Resolution

**arXiv:** [2505.21375](https://huggingface.co/papers/2505.21375)
**Session:** Day 2 — Foundation Models for EO

## Authors
Fengxiang Wang, Mingshuo Chen, Yueying Li, Di Wang, et al.
National University of Defense Technology; Beijing U. of Posts & Telecom; Wuhan University; Tsinghua University; Beihang University

## Overview

Ultra-high-resolution (UHR) remote sensing imagery is valuable for EO but creates two hard problems for multimodal models: (1) scarcity of UHR training data and (2) **token explosion** from large input images. GeoLLaVA-8K solves both — introducing new UHR datasets and efficient token pruning strategies to handle inputs up to 8K×8K.

## Key Methods

### Token Efficiency
- **Background Token Pruning**: removes tokens from uninformative regions (ocean, forest) — pilot studies show this can *improve* performance by reducing noise
- **Anchored Token Selection**: retains object-centric tokens that carry key semantic information
- Built on the **LLaVA framework**

### Datasets Created
| Dataset | Avg Resolution | Tasks |
|---|---|---|
| **SuperRS-VQA** | 8,376 × 8,376 | 22 real-world dialogue tasks |
| **HighRS-VQA** | 2,000 × 1,912 | High-res vision-language tasks |

Highest-resolution vision-language datasets in remote sensing at time of publication.

## Results

- State-of-the-art on **XLRS-Bench** (extra-large RS benchmark)
- First RS multimodal LLM capable of handling 8K×8K inputs
- Token pruning reduces memory footprint while preserving or improving accuracy

## Why It Matters for AI4EO

Demonstrates that the standard assumption of "resize everything to 224px" breaks down for UHR EO imagery. The token pruning approach is a practical solution with broader applicability to any large-image multimodal pipeline.

## Code & Data
- GitHub: [GeoLLaVA-8K](https://github.com/MiliLong/GeoLLaVA-8K)
