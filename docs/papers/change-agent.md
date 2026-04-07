# Change-Agent: Towards Interactive Comprehensive Remote Sensing Change Interpretation and Analysis

**arXiv:** [2403.19646](https://huggingface.co/papers/2403.19646)
**Session:** Day 2 — Responsible AI in EO (interpretability angle)

## Authors
Chenyang Liu, Keyan Chen, Haotian Zhang, Zipeng Qi, Zhengxia Zou, Zhenwei Shi
Beihang University; Shanghai AI Laboratory

## Overview

Change-Agent is an interactive system for comprehensive remote sensing change interpretation. It combines a purpose-built Multi-level Change Interpretation (MCI) vision model as "eyes" with a Large Language Model as "brain" — enabling users to ask natural language questions and receive change detection, captioning, counting, and cause analysis in return.

## Key Methods

### Multi-level Change Interpretation (MCI) Model
Dual-branch Siamese architecture (Segformer-B1 backbone):
- **Change Detection Branch**: pixel-level change masks
- **Change Captioning Branch**: semantic textual descriptions

### BI3 Layer (Bi-temporal Iterative Interaction)
- **LPE (Local Perception Enhancement)**: multi-scale convolutions (1×1, 3×3, 5×1, 1×5 kernels) for capturing changes at different scales
- **GDFA (Global Difference Fusion Attention)**: attention mechanism that uses feature differencing to generate spatial attention weights

### Multi-task Loss Balancing
```
ℒ_total = ℒ_det / detach(ℒ_det) + ℒ_cap / detach(ℒ_cap)
```
Normalizes each loss to prevent one task dominating training.

### LLM Integration
- ChatGPT or Llama2 as the cognitive agent
- Generates executable Python code to orchestrate vision tool calls
- Supports natural language interaction for analysis tasks

## Dataset: LEVIR-MCI

| Stat | Value |
|---|---|
| Image pairs | 10,077 bi-temporal pairs |
| Resolution | 0.5 m/pixel, 256×256 px |
| Annotations per pair | 1 change mask + 5 caption sentences |
| Changed objects | >40,000 (roads + buildings) |

## Results

| Metric | Improvement over SOTA |
|---|---|
| Change Detection MIoU | +0.75% |
| Change Captioning BLEU-4 | +1.56% |
| Change Captioning CIDEr-D | +3.68% |

## Capabilities Demonstrated
- Change mask prediction
- Change captioning and semantic description
- Change object counting
- Cause estimation and future change prediction
- Natural language interaction

## Why It Matters for AI4EO

Relevant to responsible AI because interpretability is a key pillar — Change-Agent makes model outputs explainable via natural language, addressing the black-box problem for mission-critical EO applications.

## Code & Data
- GitHub: [Chen-Yang-Liu/Change-Agent](https://github.com/Chen-Yang-Liu/Change-Agent)
