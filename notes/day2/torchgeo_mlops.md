# Introduction to Deep Learning with TorchGeo + MLOps

**Event:** AI4EO Spring School 2026 — OBELIX / IRISA, Université Bretagne Sud, Vannes, April 8–10 2026
**Co-organised with:** Copernicus Master in Digital Earth, Cluster SequoIA (PANORAMIX chair), ESA Phi-lab

---

**Speaker:** Adam Stewart (TU Munich, Chair of Data Science in EO under Prof. Xiaoxiang Zhu)
**Session:** Introduction to Deep Learning with TorchGeo + MLOps with TorchGeo (two afternoon blocks)

## Speaker Background

Adam is the creator and lead developer of TorchGeo.

## Key Concepts

- GeoDataset vs NonGeoDataset abstractions
- Samplers and transforms for geospatial data
- Multi-spectral raster handling
- End-to-end training loop
- Experiment tracking: MLflow / W&B
- Model registry

## Personal Notes

**Strengths:** TorchGeo familiarity, Dagster orchestration, STAC platform experience.

## Zora Relevance

**HIGH** — TorchGeo patterns directly applicable to our raster processing pipelines; MLOps concepts connect to the Dagster-based continuous learning pipeline architecture pitched at Kew/QMUL roundtable.

# Notes
Exact same API as pytorch

TorchGeo lets you slice data like you would in xarray etc
-> but the outputs are tensors in torchgeo that are pytorch compatible
so the library handles crs-like issues with preparing data for deep learning tasks

Samplers in torchgeo tell you where and when to sample data from
-> want as much and as diverse of a dataset as possible

GridGeoSampmler - to make sure we aren't amking multiple predictions from the same location

Has been re-writing torchgeo to handle time series data effectively
-> rewriting samplers from scratch

Weights of torchgeo models are enums
for models, torchgeo wraps around timm

Difference bw fine-tuning a FM vs fine-tuning an embeddings data product that was producted from a FM


So what if you have your own data you want to work with?
-> write a torchgeo-compatible dataset

___________

MLOps = data engineering + ML + dev ops

ML is stochastic by definition
This leads to randomess in data (cross validation split, data augmentations, data loader order, shuffling)
Also randomness in model (initial weights and dropout layers)


Covered things like licensing, best practices for versioning, cicd, etc

Tensorboard looks really useful 

Pytorch lightning 