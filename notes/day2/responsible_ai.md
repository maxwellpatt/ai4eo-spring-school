# Responsible AI in EO

**Event:** AI4EO Spring School 2026 — OBELIX / IRISA, Université Bretagne Sud, Vannes, April 8–10 2026
**Co-organised with:** Copernicus Master in Digital Earth, Cluster SequoIA (PANORAMIX chair), ESA Phi-lab

---

**Speaker:** Pedram Ghamisi (Helmholtz-Zentrum Dresden-Rossendorf / Lancaster University)
**Hands-on:** Weikang Yu (HZDR / TUM)
**Session:** Responsible AI in EO — lecture + hands-on

## Speaker Background

Ghamisi heads the Responsible AI Group at HZDR; co-chairs GEO-AI4EO policy briefs; established the Responsible AI Working Group in IEEE GRSS.

## Key Concepts

- Distributional shift and domain adaptation in RS
- Explainability: GradCAM, SHAP for image models
- Open science practices
- AI security in EO contexts
- Fairness across geographies / sensor types

## Zora Relevance

**MEDIUM** — explainability methods relevant to communicating NbS model outputs to water company stakeholders; domain shift relevant to cross-catchment model transfer.

# Notes

Roles for data and models to addresss challenges in responsible AI
Since training foundation models is expensive, one cannot afford to guess what the specific job will be for the model
Reserachs applied massive experiments/calculus to derive the defined mathematical blueprint for optimal AI scaling
- Training compute budget (text & vision): C = 6ND (D = tokens, N = paramers, C = compute resources in flops)
- Compute-optimal data ratio (Chinchilla Law): D = 30N

"How can you evaluate the performance of different foudnation models?"
-> To do so, need benchmarks that cover a wide variety of tasks
  -> SustainFM: grounding foundation models in global sustainability to drive real-world impact
- Chose benchmarks from all over the world, esp global south 

FMs deliver strong performance, butare not always superior to task-specific approaches
Transferability offers a step toward energy-efficent AI across domains
High generalization and fast convergence make FMs a scalable alternative to traditional models



______

Change Detection Approaches: Early Fusion
Can apply early fusion on bitemporal images:
Or can do late fusion
But applying middle fusion is the best.
- Enable feature interaction with less noise
- End to end
- Faster computation
- Disadvantages: domain shift? (temporal)

https://arxiv.org/abs/2505.24528


Hands-on: https://github.com/EricYu97/CDTutorial?tab=readme-ov-file

