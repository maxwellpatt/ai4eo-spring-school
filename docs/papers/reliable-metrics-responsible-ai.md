# The Quest for Reliable Metrics of Responsible AI

**arXiv:** [2510.26007](https://huggingface.co/papers/2510.26007)
**Session:** Day 2 — Responsible AI in EO

## Authors
Theresia Veronika Rampisela, Maria Maistro, Tuukka Ruotsalo, Christina Lioma
University of Copenhagen; LUT University

## Overview

A reflective, methods-focused paper asking: *are the metrics we use to evaluate responsible AI actually reliable?* Draws on the authors' prior work auditing fairness metrics in recommender systems and distils findings into practical guidelines applicable to any AI application — including AI in science (AIS) and EO.

## Key Arguments

### Problems with Existing Fairness Metrics
1. **Invalid mathematical operations**: some metrics crash (divide-by-zero) on valid inputs
2. **Unknown score ranges**: the theoretical min/max is unreachable in practice, making scores uninterpretable
3. **Compressed sensitivity**: some metrics score near 0 regardless of actual fairness level
4. **Redundancy**: many metrics yield near-identical conclusions — no need to compute all of them
5. **Group ≠ Individual**: group fairness metrics cannot serve as proxies for individual fairness, and vice versa

### Guidelines for Reliable Responsible AI Metrics

1. Are there inputs that cause invalid mathematical operations?
2. What is the metric's range and how should it be interpreted?
3. What input produces the minimum and maximum score?
4. How sensitive is the metric to input changes?
5. Does the metric yield conclusions similar to an existing one?

## Contributions

- Corrected formulations of existing fairness metrics with proper min-max normalization
- New joint effectiveness-fairness metric (Pareto frontier approach)
- Open-source implementations of corrected metrics

## Code
- Corrected individual item fairness: [github.com/theresiavr/individual-item-fairness-measures-recsys](https://github.com/theresiavr/individual-item-fairness-measures-recsys)
- Joint evaluation: [github.com/theresiavr/DPFR-recsys-evaluation](https://github.com/theresiavr/DPFR-recsys-evaluation)

## Why It Matters for AI4EO

Before claiming that an EO model is "fair" or "responsible," you need metrics that actually measure what you claim. This paper is a useful antidote to naive metric adoption, especially as EU AI Act compliance becomes a real consideration.
