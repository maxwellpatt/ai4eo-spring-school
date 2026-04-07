# Fairness and Bias Mitigation in Computer Vision: A Survey

**arXiv:** [2408.02464](https://huggingface.co/papers/2408.02464)
**Session:** Day 2 — Responsible AI in EO

## Authors
Sepehr Dehdashtian, Ruozhen He, Yi Li, Guha Balakrishnan, Nuno Vasconcelos, Vicente Ordonez, Vishnu Naresh Boddeti
Michigan State University; Rice University; UC San Diego

## Overview

A comprehensive survey covering the full lifecycle of bias in computer vision systems: how biases originate, how they are discovered, how they can be mitigated, and how foundation/generative models inherit and propagate them. A useful foundation paper for understanding the EO-specific fairness challenges raised in the Responsible AI session.

## Key Concepts

### Fairness Definitions
- **Individual Fairness**: similar individuals should be treated similarly
- **Group Fairness**: demographic parity, equal opportunity, equality of odds
- **Counterfactual Fairness**: same decision under counterfactual demographic attributes
- **Bias Amplification**: model exacerbates biases present in training data

### Bias Origins
- **Social**: internet data collection → biased publication practices → geographic concentration
- **Intrinsic dependence**: target label Y and sensitive attribute S are genuinely correlated
- **Spurious correlations**: Y and S independent, but model learns the association

### Bias Mitigation Approaches
- **Fair Representation Learning**: adversarial or HSIC-based methods to decouple sensitive attributes
- **Counterfactual Data Rebalancing**: GAN-based augmentation, StyleGAN demographic transfer
- **Score Calibration / Loss Regularization**: adaptive margins, fairness-aware distillation

## Datasets Surveyed

Tasks covered: face recognition, image classification, action recognition, image captioning, VQA, text-to-image generation, object detection, person re-ID.

Most studied sensitive attributes: gender, race/ethnicity, age, skin tone. Underexamined: illumination, texture, geographic location.

## Key Findings

- Commercial face recognition systems show significant gender and skin-tone biases
- Geographic bias in ImageNet and Open Images (Amerocentric/Eurocentric)
- Pretrained models far from achieving best utility-fairness trade-offs
- HSIC-based approaches outperform neural network proxies for statistical independence
- FairerCLIP shows debiasing without ground-truth sensitive attribute labels
- Foundation model and generative model fairness largely underexplored

## Why It Matters for AI4EO

EO models trained on satellite imagery from densely monitored regions (Europe, USA) will systematically underperform on underrepresented geographies. This survey provides the conceptual toolkit to reason about and measure such biases.
