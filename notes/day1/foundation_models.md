# Foundation Models for EO

**Event:** AI4EO Spring School 2026 — OBELIX / IRISA, Université Bretagne Sud, Vannes, April 8–10 2026
**Co-organised with:** Copernicus Master in Digital Earth, Cluster SequoIA (PANORAMIX chair), ESA Phi-lab

---

**Speakers:** Stéphane May (CNES) and Pierre Adorni (PhD candidate, IRISA)
**Session:** Foundation Models for EO — lecture + two hands-on blocks

## Speaker Backgrounds

- **Stéphane May:** 20+ years in EO, led AI onboard the CO3D satellite (launched 2025)
- **Pierre Adorni:** PhD specifically on improving generalisation of ML models across diverse RS datasets and tasks

## Key Concepts

- ViT architecture
- MAE / contrastive pre-training
- Fine-tuning paradigms: full vs LoRA vs linear probe
- Geospatial foundation models: Prithvi, SatMAE, Scale-MAE, BioCLIP

## Personal Notes

**Strengths:** SAM fine-tuning with BNDVI on 4-band infrared, TorchGeo familiarity, geospatial embeddings thinking.

## Zora Relevance

**HIGH** — directly connects to surrogate model inputs for NbS impact assessment; embedding representations as inputs to GP surrogates over HEC-RAS outputs is an active area of thinking.

# Notes

## Context
- Tons of EO data
- High potential to exploit data in dev uses
- Could coudl be used more (only 20% of the acquired data is used)
- Someetimes, data is difficult to access

## FMs
Definition: any model that is trained on broad data (generally with self-supervision) that can be adapted aka fine tuned to a wide range of downstream tasks
Simplify labeling tasks

## Visual Language Model
Pre-training
- Use of image-text pairs
- Alignment of image and text features
Downstream task
- Description of an image
- Image retrieval
Advanced tasks
- Image retriveal with quantitative values 
- Instances count

## Architectures for foundation models
- Transformers let you mix different types of data into the transformer which is unique from convolutional networks or graph networks

### ViT - 2020
- Decompose an image into small parts -> project into patch embedding -> attention bits with transformer encoder -> head -> probability vector
Step 1: Patch + tokens -> vector
Step 2: Add embeddings
Step 3: Encoding into latent space
Step 4: Decoding

## Multi-satellites encoding into ViT
Question is always how can I embed information into the network
- CROMA (2023): Specific encoder for each satellite
- SatMAE (2022): Different patch embeddings for each spectral group (grouped by spatial resolution): [B2, B3, B4, B8], [B5, B6, B7, B8A], [B11, B12]
- SenPa-MAE (2024): Different patch embeddings for each spectral band. Explicit encoding of sensor info via wavelength and spatial resolution of each band
- SEnSel-v2 (2024): Encoding vector of wavelength info, type of input data, flexible optical/SAR
- EarthMAE (2025): Patch embedding for each satellite source (224x224 cells). Explicit encoding of the satellite source

## Foundation Models and Time Series
Same approaches as for position encoding or source/satellite encoding, but for the time encoding
- Relative time encoding of each image of the time series
- Encoding of the date (could be year, month, day, hour, season, whatever you like)
- Encoding the date with a language model
More complex vectors

## Pretraining with Masked Auto-Encoders
Principles:
- Some parts of the image are randomly masked
- Pretext task: reconstruct the og image
- Encoder learns a representation of the input data collection
- Self-supervised technique
Encoder learns the most probable patch that woudl be around known patches

## MAE 
- Train a ViT to reconstruct the masked parts of the image
- Fine tune the decoder on several specific tasks
- Encoder weights frozen or trainable*

Interests
- Embeddings = compact representation of the satellite images
- Faster convergence of fine tuning
- Less labeled data required for each specific task

MAESTRO 2025: studies the best waty to fuse different time steps and sensors
SMARTIES 2025: cross-sensor token mixup

## Self-supervised methods: contrastive learning
Priciples:
- Force the representations of similar things to be close in the latent space
- Force the representations of different things to be far away in the altent space

Student/teacher -> emerging properties in self-supervised vision transformers - Caton et al 2021

## Contrastive learning with satellite images
- Use of several iamges at the same location
  - One image with data augmentation
  - Through different sensors*
  - At different times*
  - Through different spectral bands*
  *: is available info identical inside each image? -> look into this more, and when you can be misrepresenting information 

## Contrastive learning based models
  - Joint-embedding architecture
  - Contrastive with temporal pairs

## I-JEPA: image joint embedding predictive architecture
Limits of MAE: reconstruction of pixel space
Some I-JEPA self-supervised methods: AnySAT, SAR-JEPA, X-JEPA

## Other training methods
ALl-in-one: Cross-Scale MAE (2023)
THOR: A Versatile Foundation Model for Earth Observation Climate and Society Applications (2026)
MMEarth: 2024

## How to Choose?
- More than 1- different RSFMs
- No clear winner -? sometimes better performance, balanced by downsides, complexity
- Differnet models for different uses
- Excellent databases fro S1/2
- Still reduced dataset for very high res images

## Conclusion
- New models using more diverse datasets
- Always the right benchmarks, not always the right tasks
- Less work on very high res imagery -> public VHR catalogs are limited
- Key issue: maintain a limited FLOPS at inference for environmental aspects