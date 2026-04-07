# REOBench: Benchmarking Robustness of Earth Observation Foundation Models

**arXiv:** [2505.16793](https://huggingface.co/papers/2505.16793)
**Session:** Day 2 — Foundation Models for EO

## Authors
Xiang Li, Yong Tao, Siyuan Zhang, Siwei Liu, Zhitong Xiong, et al.
Universities of Bristol, Exeter, Aberdeen; South China Normal University; TU Munich; TU Eindhoven

## Overview

The first comprehensive robustness benchmark for EO foundation models (EOFMs). Evaluates how well EOFMs hold up under realistic image corruptions — finding significant performance drops (1–25%) across all model families. Vision-language models prove the most robust due to semantic grounding.

## Key Methods

### Corruption Types (12 total, 5 severity levels each)
- **Appearance**: cloud occlusion, brightness, haze, Gaussian blur, motion blur, noise, compression artifacts, Landsat-7 SLC-off simulation
- **Geometric**: rotation, scale, translation

### Robustness Metric
Relative Task Performance Drop (ℛ_TP) — percentage drop from clean to corrupted performance. Lower = more robust.

### Models Evaluated
- **MIM-based**: SatMAE, ScaleMAE, RVSA, SatMAE++
- **CL-based**: RemoteCLIP, GeoRSCLIP
- **LLM-based**: GeoChat, LHRS-Bot, RS-LLaVA, SkySenseGPT, VHM, Falcon

## Datasets Used

| Dataset | Task |
|---|---|
| AID | Scene Classification |
| ISPRS Potsdam | Semantic Segmentation |
| DIOR-R | Object Detection |
| VRSBench | Captioning, VQA, Visual Grounding |

## Key Findings

- **MIM-based models** suffer most: 25%+ drop in classification tasks
- **CL-based models** more robust: <10% drop across tasks
- **LLM-based models** most robust: <5% drop in vision-language tasks
- **Motion blur** is the most damaging corruption (~60% drop for MIM models)
- **Translation** has the least impact
- Backbone size matters differently by task: ViT-L better for classification, ViT-B better for segmentation

## Why It Matters for AI4EO

A critical read for anyone deploying EO FMs in real-world settings. Robustness is often assumed but rarely tested — REOBench provides standardized tools to audit this before deployment.

## Code & Data
- GitHub: [lx709/REOBench](https://github.com/lx709/REOBench)
- License: CC-BY-4.0
