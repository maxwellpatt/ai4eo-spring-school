# Generate Your Own Scotland: Satellite Image Generation Conditioned on Maps

**arXiv:** [2308.16648](https://huggingface.co/papers/2308.16648)
**Session:** Day 3 — Generative Models for EO

## Authors
Miguel Espinosa, Elliot J. Crowley
School of Engineering, University of Edinburgh

## Overview

Demonstrates that state-of-the-art pretrained diffusion models can be conditioned on cartographic data (OpenStreetMap) to generate realistic satellite images. Trains a **ControlNet** model on paired OSM+satellite image datasets covering Mainland Scotland and the Central Belt. A clear, accessible entry point into conditioned generative models for EO.

## Key Methods

- **ControlNet** conditioned on OpenStreetMap tiles → generates corresponding satellite imagery
- **Stable Diffusion** (v1.5) as the frozen backbone — only ControlNet adapters are trained
- Fixed text prompt: *"Convert this OpenStreetMap into its satellite view"*
- Training: 8×A100 40GB GPUs, ~8 hours, 250 epochs

## Datasets Created

| Dataset | Size | Region | Zoom level |
|---|---|---|---|
| Mainland Scotland | 78,414 training pairs | All of Scotland (mostly rural) | 17 |
| Central Belt | 68,195 training pairs | Edinburgh/Glasgow area (urban) | 17 |

Image size: 256×256 px. Sources: OSM tiles + World Imagery / Clarity (ArcGIS).

## Key Results (Qualitative)

- Generated images are realistic and diverse for the same map input (seasonal variation, lighting changes)
- Handles agricultural land, forests, water bodies, and urban areas
- **Failure cases**: fine road structures, highway intersections, railways (underrepresented in dataset)

## Key Takeaways

**Opportunities:**
- Data augmentation for low-data EO tasks
- Dataset expansion without additional satellite collection
- Cloud/haze removal as image-to-image translation

**Challenges:**
- Fake satellite image generation risks — adversarial use in geopolitical/emergency contexts
- Concurrent need for deepfake detection in the EO domain

## Why It Matters for AI4EO

Clean, reproducible example of conditioned generation in EO. Importantly, the Day 3 presenter (Nicolas Audebert) is cited in this paper's references — his work on joint EO + OSM learning directly motivated this approach.

## Code & Models
- GitHub: [miquel-espinosa/map-sat](https://github.com/miquel-espinosa/map-sat)
- HuggingFace model: [mespinosami/controlearth](https://huggingface.co/mespinosami/controlearth)
