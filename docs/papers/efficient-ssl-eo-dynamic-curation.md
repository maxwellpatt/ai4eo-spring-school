# Efficient Self-Supervised Learning for Earth Observation via Dynamic Dataset Curation

**arXiv:** [2504.06962](https://huggingface.co/papers/2504.06962)
**Session:** Day 2 — Foundation Models for EO

## Authors
Thomas Kerdreux, Alexandre Tuel, Quentin Febvre, Alexis Mouche, Bertrand Chapron
Galeio, Paris; Ifremer / CNRS LOPS, Brest

## Overview

Tackles an underexplored bottleneck in EO foundation model pretraining: dataset curation. Satellite imagery archives have strong redundancy and heavy-tailed geographic distributions, leading to biased representations and wasted compute. This paper proposes a **dynamic dataset pruning** strategy that iteratively refines the training set to maximize diversity — without needing a pre-existing feature extractor.

## Key Methods

- **Dynamic dataset pruning**: iteratively removes redundant/overrepresented samples during training
- No warm-start needed — well-suited for domains without large curated datasets
- Applied to **Sentinel-1 Wave Mode (WV) SAR** archive: 10 years of data, primarily ocean observations
- Models trained from scratch on the pruned dataset; evaluated on 3 downstream tasks

## Key Insight

EO satellite archives are dominated by:
- **Redundancy**: nearby or repeat acquisitions of similar scenes
- **Heavy-tailed distributions**: some regions/conditions vastly overrepresented

Standard random sampling → biased feature representations. Dynamic pruning → more balanced, transferable representations.

## Results

- Dynamic pruning improves both **computational efficiency** and **feature quality**
- Better downstream transferability across 3 validation tasks
- Scalable: designed for very large archives (billions of images)

## Why It Matters for AI4EO

Most EO FM papers focus on architecture or training objective. This paper focuses on *data* — often the biggest lever in practice. Directly applicable to any large-scale EO SSL pretraining pipeline.

## Datasets
- **Sentinel-1 Wave Mode SAR archive** (Ifremer): ocean surface observations over 10 years
- Released as **Nereus-SAR-1** and **Nereus family** datasets
