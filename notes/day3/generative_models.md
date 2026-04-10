# Generative Models for EO

**Event:** AI4EO Spring School 2026 — OBELIX / IRISA, Université Bretagne Sud, Vannes, April 8–10 2026
**Co-organised with:** Copernicus Master in Digital Earth, Cluster SequoIA (PANORAMIX chair), ESA Phi-lab

---

**Speaker:** Nicolas Audebert (IGN / LASTIG lab)
**Session:** Generative models — lecture + hands-on

## Speaker Background

Audebert's PhD (2018, Université Bretagne-Sud) on deep learning for RS; habilitation 2025; co-organises TerraBytes workshop and national workshops on generative AI and explainability.

## Key Concepts

- Diffusion models and GANs for EO (e.g. DiffusionSat)
- Conditional generation
- Super-resolution for satellite imagery
- Representation learning for image generation

## Zora Relevance

**MEDIUM-LOW** directly, but synthetic data generation for rare peatland erosion classes could be genuinely useful for SAM fine-tuning data augmentation.

---

## Generative vs Discriminative Models

- **Discriminative models** estimate P(Y|X) — given observation X, infer label Y. They cannot answer "what does a typical example of class Y look like?"
- **Generative models** estimate P(X|Y) — find what realizations of X lead to the observed target Y.
- Generative models do more than image synthesis:
  - *What is the likelihood of this image over Paris in June?* → anomaly detection
  - *What is the likelihood of this image representing a river?* → classification

## Why Generative Models?

- **Opportunity:** large-scale unlabelled data is abundant in RS
- **Pragmatism:** can be trained without labels — unsupervised learning is key in RS; metadata can still condition the model
- **Strategy:** generative models approximate the data distribution p(x), making it easier to quantify uncertainty and integrate prior assumptions

DiffusionSAT — Khanna 2024: https://www.samarkhanna.com/DiffusionSat/

## Applications

- **Image generation/editing:** simulating images under new conditions, image translation
- **Inverse problems:** inpainting (e.g. cloud gap-filling), denoising, super-resolution
- **Discriminative tasks:** anomaly detection via likelihood estimation, fine-tuning for classification/segmentation

---

## Flow Matching

The goal is to interpolate between two distributions p₀ and p₁. There are infinite solutions, so we restrict to those described by a **velocity field** v_t(x) — a field over data space and time where the flow (integral of the velocity field) describes a trajectory from p₀ to p₁.

### Defining the Velocity Field

Given X₀ ~ p₀ and X₁ ~ p₁, define the linear interpolation:

```
X_t = t·X₁ + (1-t)·X₀
```

The corresponding velocity field is the expected direction of all paths through x at time t:

```
v_t(x) = E[X₁ - X₀ | X_t = x]
```

This (p_t, v_t) pair satisfies the continuity equation.

**Optimal transport (OT) special case:** Let T* be the OT plan for Euclidean cost between p₀ and p₁. Then:

```
v_t( t·T*(x) + (1-t)·x ) = T*(x) - x
```

This gives straight-line, constant-velocity trajectories — but is intractable in high dimensions.

### Learning the Flow

Approximate v_t with a neural network v_θ(t, x_t). In practice, use a **conditional flow matching** objective — we don't need to know v_t directly, just the per-pair conditional velocities.

### Sampling

Numerical integration via Euler's method with K steps:

```
x_{k+1} = x_k + (1/K) · v_θ(t_k, x_k),   t_k = k/K
```

### Coupling

Flow matching trains on random independent pairs (x₀, x₁), but any coupling works. **Minibatch OT coupling** performs OT within minibatches to approximate straight-line trajectories at scale.

### Data-to-Data Flow Matching

Use natural paired samples from the dataset as the coupling — the model learns conditional generation from one real image to another (e.g. SAR → optical).

---

## Synthetic Data Augmentation

Synthetic data from conditional generative models is an effective augmentation strategy, especially for rare classes.

## Inverse Problems in RS

### Super-Resolution

Trains a model to recover a high-resolution image from a degraded low-resolution input. Key challenge: SR models tend to hallucinate detail that doesn't exist. Goal is improved spatial resolution without injecting false information.

### InSAR Denoising

InSAR encodes surface displacement via phase differences between SAR acquisitions. Preprocessing removes most external factors, but residual noise remains.

Deep InSAR denoising challenges:
- Few reliable ground truths of clean interferograms
- Standard MSE-trained models can produce values outside the valid [0, 2π] range

→ **Riemannian manifold of interferograms** — look into this further as a principled approach.

## SAR-to-Optical Translation (FlowEO)

SAR and multispectral sensors have complementary trade-offs (cloud penetration vs. interpretability). FlowEO uses flow matching with semantic preservation to translate between domains with less hallucination than GAN-based approaches.

## Out-of-Distribution Detection

Assign a likelihood score to each image to flag observations far from the training distribution. Uses ODE-based encoding/decoding to produce a per-image OOD score.

---

## Roadblocks

- How to harmonize heterogeneous data sources?
- How to improve trust in generative model outputs?

## Conclusion

- Generative models are versatile: super-resolution, denoising, image translation
- They can be turned into classifiers via likelihood estimation
- Synthetic data generation is practical when labelled data is scarce
