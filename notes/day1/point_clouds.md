# Deep Learning for Change Detection in 3D Point Clouds

**Event:** AI4EO Spring School 2026 — OBELIX / IRISA, Université Bretagne Sud, Vannes, April 8–10 2026
**Co-organised with:** Copernicus Master in Digital Earth, Cluster SequoIA (PANORAMIX chair), ESA Phi-lab

---

**Speaker:** Iris de Gélis (Estellus / Paris Observatory)
**Session:** Deep learning for change detection in 3D point clouds

## Speaker Background

Her PhD focused on this exact topic at Université Bretagne Sud; won Best PhD Thesis from CNRS geomatics group.

## Personal Notes

**Gap:** This is my weakest area coming in — prioritise understanding representations before the session.

## Zora Relevance

Lower direct relevance, but change detection logic maps onto peatland erosion feature tracking over time; LiDAR DEMs are already in our stack.

---

## Overview

- CO3D — global change detection dataset, launched last year
- Showed point cloud scenes from different years to illustrate land use change (LUC)

---

## 2.5D Change Detection

3D → 2.5D via rasterization.

**Evolution of methods:**
1. Difference methods (Murakami 1999): take difference of two elevations at some threshold
2. ML methods
3. DL methods

### Deep Learning on 2.5D

**2D convolution** for feature extraction.

**Fully Convolutional Siamese Network with difference** — Daudt 2018:
- Two images → encoder/decoder (Siamese = two encoders)
- Extract multi-scale feature differences
- Re-embed differences in the decoder at different scales to capture different types of change

### Limitation of 2.5D Rasterization

Going from 3D → 2.5D loses information. LiDAR gives deeper insight into vegetation structure, so processing point clouds directly is preferable.

---

## 3D Point Clouds for Change Detection

**Challenges:**
- Sparse and unordered; raw PCs ≠ matrices
- Different number of points and different spatial distribution between acquisitions (the plane doesn't fly the exact same path twice)
- No direct pixel-to-pixel comparison possible

**Levels of complexity:**
1. Binary change detection
2. Multiple change detection
3. Binary change segmentation
4. Multiple change segmentation

---

## SOTA: Distance-Based Methods

Even without direct point correspondence, distance between clouds is meaningful:
- **C2C:** Cloud-to-Cloud distance
- **M3C2:** Multiscale Model-to-Model Cloud Comparison

---

## SOTA: ML Methods (Tran 2018)

Hand-crafted features:
- **Point distribution** — point normals (N_x, N_y, N_z); three eigenvalues from PCA on 3D coordinates of neighbor points → linearity, planarity, omnivariance
- **Height information** — change stability signal

Features fed into a standard ML classifier.

---

## SOTA: Deep Learning Methods

Traditional convolution not applicable to unstructured point clouds. Since 2018, three main categories have emerged:

### 1. Projection-Based
- Project 3D onto 2D surfaces, then apply standard 2D DL
- Example: **SnapNet** — 3D point cloud semantic labeling with 2D deep segmentation networks

### 2. Discretization-Based (Voxels)
- 3D rasterization into voxels
- Example: **SEGCloud**
- Drawbacks: information loss during rasterization; empty voxels are computationally expensive

### 3. Point-Based

**PointNet** (Charles R. Qi 2017):
- Input points → MLPs → max pooling → classification
- Learns features directly from raw points
- Drawbacks: computationally demanding for large EO point clouds; poor generalization

**PointNet++:**
- Hierarchical point set feature learning
- Multi-scale features → segmentation/classification
- Many subsequent methods still build on PointNet (Lang 2019, Shi 2019)
- Main drawback: struggles with large scenes

---

## Point-Based Methods: Graph Representations

- Represent point cloud as a graph (e.g., k-NN neighborhood links)
- **Edge convolution:** MLP on edges
- **Graph attention convolution:** learned edge weighting (distance vs. other similarity measures)
- **Superpoint Graphs** (Landrieu & Simonovsky 2018): RGB point cloud → geometric partition → superpoint graph → semantic segmentation

---

## Point-Based Methods: Convolution on Points

Key question: how to define the kernel function *g*.

Options:
- **MLP:** fully connects all points — too expensive for large clouds
- **Geometric kernels:** constrain to local neighborhood — need to define that neighborhood

**KPConv: Kernel Point Convolution** (Thomas 2019):
- Kernel function *g* applies learned weights to different areas within a 3D "bowl"
- Only operates on existing 3D points — no wasted computation on empty space
- Deeper encoder layers → larger bowl radius → more spatial context

---

## DL for 3D Point Cloud Change Detection: Supervised

**Siamese KPConv:**
- Replace 2D conv with 3D KPConv in a Siamese architecture
- Difference features between the two date encodings
- Challenge: points aren't perfectly aligned → use nearest-point matching

**Siamese KPConv with Encoder Fusion:**
- Fuse feature differences and mono-date features directly in the encoder
- Differences are convolved within the encoder (earlier fusion → better change representation)

### Learning Strategy
- **Inputs:** cylindrical crops from large RS point clouds
- **Class imbalance:** sparse changes cause the model to default to "no change"; addressed with weighted random sampling of input cylinders
- **Loss:** SGD with momentum (0.98), point-wise weighted loss
- **Augmentation:** random rotation around vertical axis, Gaussian noise
- **Metrics:** accuracy, IoU, mean per-class accuracy

### Results
- Encoding change features in the encoder improves results
- Dropping hand-crafted features (letting the network extract them) gives best performance
- RF cannot cleanly separate objects at the same height but different positions

---

## Unsupervised Context

Without labeled change data, direct encoding is harder — encoding change features is even more critical here.

## Low-Supervised Context

**What if very few annotated examples are available?**

**DeepCluster** (Caron 2018):
- Originally for ImageNet image classification
- Input → ConvNet → cluster pseudo-labels → retrain (iterate)
- Network extracts meaningful pseudo-class features

**DeepCluster for 3D CD:**
- PC1 and PC2 → CD/Mono-date encoder → CD encoder
- Clustering → change pseudo-labels → segmentation
- Backprop through full pipeline, iterate

Learning setup:
- Backbone: Siamese KPConv and Encoder Fusion SiamKPConv
- Loss: negative log-likelihood
- ~1000 pseudo-clusters (beyond this, purity gains plateau)
- Fully unsupervised training; weakly supervised mapping to real classes
- A human labels whole clusters, not individual points — major annotation cost reduction

**Results:**
- Adding hand-crafted features improves unsupervised results
- Can approach supervised accuracy/IoU
- Contrastive loss boosts accuracy significantly, though semantic segmentation quality lags

---

## Takeaways

### Peatland Disturbance Applications

The core question: **are we detecting that change happened, or measuring how much?**

These are different products with different pipeline requirements:

| Goal | Output | Method fit |
|------|--------|-----------|
| Change presence / mask | Binary or multi-class change map | Siamese KPConv, DC3DCD, PBFormer |
| Volume loss / erosion depth | Δ elevation (m), m³ removed | M3C2 differencing + DEM of difference |
| Feature tracking over time | Erosion gully extent, hagg boundaries | Multi-class segmentation + temporal linking |
| Disturbance severity index | Continuous score per parcel | Regression head on change features |

**Concrete Zora use cases:**

- **Pre/post restoration:** repeat ALS before and after drain blocking or revegetation — supervised Siamese KPConv to classify stable/degraded/recovering zones
- **Erosion gully detection:** LiDAR DEMs already in stack → M3C2 or 2.5D differencing for rapid volume loss estimates; DL for gully delineation at scale
- **Hagg and bare peat tracking:** multi-class 3D change segmentation to distinguish intact moss vs exposed peat vs revegetated — maps directly onto Siamese KPConv multi-class outputs
- **Long-term time series:** if annual or biannual LiDAR is available, extend from two-epoch to multi-epoch tracking (open problem — most methods are pairwise only)

**Key gaps for peatland specifically:**
- No published work applying 3D DL change detection to peatlands — almost all benchmarks are urban (buildings, roads)
- Peatland point clouds have very different density characteristics than urban ALS: flatter terrain, low vegetation, subtle sub-cm elevation changes matter
- Class imbalance is even more severe: most of a peatland is stable at any given timestep
- Hand-crafted features from the session (normals, eigenvalues, height stability) should transfer well given the structured microtopography

**Starting point recommendation:** M3C2 differencing for a quick volumetric baseline, then fine-tune Siamese KPConv on a small labeled peatland dataset to get change segmentation. DC3DCD unsupervised approach is attractive if labeled data is scarce.

---

### Other Takeaways

- Unsupervised methods are still significantly improvable
- Change detection requires encoding change *information*, not just geometry
- Guiding the network with hand-crafted features is necessary for unsupervised learning to work well

---

## Paper References

### Papers Cited in Session

| Paper | Authors | Year | Venue | arXiv |
|-------|---------|------|-------|-------|
| Fully Convolutional Siamese Networks for Change Detection | Rodrigo Caye Daudt, Bertrand Le Saux, Alexandre Boulch | 2018 | ICIP 2018 | [1810.08462](https://arxiv.org/abs/1810.08462) |
| SnapNet: 3D point cloud semantic labeling with 2D deep segmentation networks | Alexandre Boulch, Joris Guerry, Bertrand Le Saux, Nicolas Audebert | 2017 | Computers & Graphics 71:189–198 | no arXiv (journal-first) |
| PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation | Charles R. Qi, Hao Su, Kaichun Mo, Leonidas J. Guibas | 2017 | CVPR 2017 | [1612.00593](https://arxiv.org/abs/1612.00593) |
| PointNet++: Deep Hierarchical Feature Learning on Point Sets in a Metric Space | Charles R. Qi, Li Yi, Hao Su, Leonidas J. Guibas | 2017 | NeurIPS 2017 | [1706.02413](https://arxiv.org/abs/1706.02413) |
| Large-scale Point Cloud Semantic Segmentation with Superpoint Graphs | Loic Landrieu, Martin Simonovsky | 2018 | CVPR 2018 | [1711.09869](https://arxiv.org/abs/1711.09869) |
| KPConv: Flexible and Deformable Convolution for Point Clouds | Hugues Thomas, Charles R. Qi, Jean-Emmanuel Deschaud, Beatriz Marcotegui, François Goulette, Leonidas J. Guibas | 2019 | ICCV 2019 | [1904.08889](https://arxiv.org/abs/1904.08889) |
| SEGCloud: Semantic Segmentation of 3D Point Clouds | Lyne P. Tchapmi, Christopher B. Choy, Iro Armeni, JunYoung Gwak, Silvio Savarese | 2017 | 3DV 2017 | [1710.07563](https://arxiv.org/abs/1710.07563) |
| Deep Clustering for Unsupervised Learning of Visual Features (DeepCluster) | Mathilde Caron, Piotr Bojanowski, Armand Joulin, Matthijs Douze | 2018 | ECCV 2018 | [1807.05520](https://arxiv.org/abs/1807.05520) |
| Siamese KPConv: 3D multiple change detection from raw point clouds using deep learning | Iris de Gélis, Sébastien Lefèvre, Thomas Corpetti | 2023 | ISPRS J. Photogramm. Remote Sens. 197:274–291 | — |
| Change detection needs change information: improving deep 3D point cloud change detection | Iris de Gélis, Thomas Corpetti, Sébastien Lefèvre | 2023 | arXiv preprint | [2304.12639](https://arxiv.org/abs/2304.12639) |

---

## Recent Research: Transformers for 3D Point Cloud Change Detection (2022–2025)

### Why Transformers for Point Clouds?

Standard ViTs operate on grid-structured image patches. Point clouds are unordered, irregular, and variable-density. Adaptation strategies vary across papers:
- **Serialization / space-filling curves** (Point Transformer V3): serialize points along a space-filling curve so standard window attention applies without radius search
- **k-NN grouping into local tokens** (PBFormer, ME-CPT): extract local point sequences via kNN, then apply transformer encoder on those sequences
- **Spherical/radial windows** (SphereFormer): partition space into non-overlapping elongated radial windows to handle LiDAR's range-dependent sparsity

---

### PBFormer (2023)

**Title:** PBFormer: Point and Bi-Spatiotemporal Transformer for Pointwise Change Detection of 3D Urban Point Clouds
**Authors:** (Ye et al.)
**Year:** 2023
**Venue:** Remote Sensing 15(9):2314
**arXiv:** no dedicated preprint found; published direct to MDPI Remote Sensing

**Architecture:** Custom "Point and Bi-Spatiotemporal Transformer" — Siamese encoder extracts point features per epoch; a spatiotemporal fusion module merges bi-temporal features for change detection. Point Transformer used as backbone encoder.

**Handling irregularity:** k-NN neighborhood grouping to extract point sequences from raw irregular clouds; no voxelization.

**Target domain:** Urban outdoor point clouds (Urb3DCD benchmark). Remote sensing / ALS / photogrammetric point clouds.

**Supervision:** Supervised.

**Notes:** Directly comparable to Siamese KPConv on Urb3DCD; claims to outperform it. One of the first papers to apply Point Transformer specifically to bitemporal 3D change detection.

---

### ME-CPT (2025)

**Title:** ME-CPT: Multi-Task Enhanced Cross-Temporal Point Transformer for Urban 3D Change Detection
**Authors:** Luqi Zhang, Haiping Wang, Chong Liu, Zhen Dong, Bisheng Yang
**Year:** 2025
**arXiv:** [2501.14004](https://arxiv.org/abs/2501.14004)

**Architecture:** "Cross-Temporal Point Transformer" — attention mechanisms establish spatiotemporal correspondences between point clouds from different epochs. Multi-task learning head for joint change detection and semantic segmentation.

**Handling irregularity:** Point Transformer-style attention on local point neighborhoods; kNN-based tokenization.

**Target domain:** Urban areas; Airborne Laser Scanning (ALS). Releases a 22.5 km² annotated ALS dataset.

**Supervision:** Supervised, but addresses class imbalance (sparse changes). Multi-task learning improves generalization.

**Notes:** Also contributes a new large ALS dataset for urban change detection. Addresses the annotation scarcity problem partly via multi-task learning rather than unsupervised approaches.

---

### DC3DCD (2023) — Unsupervised

**Title:** DC3DCD: unsupervised learning for multiclass 3D point cloud change detection
**Authors:** Iris de Gélis, Sébastien Lefèvre, Thomas Corpetti
**Year:** 2023
**arXiv:** [2305.05421](https://arxiv.org/abs/2305.05421)

**Architecture:** DeepCluster adapted for 3D point clouds. Backbone is Siamese KPConv (not a transformer). Iterative pseudo-label clustering → retraining loop.

**Handling irregularity:** KPConv backbone — kernel point convolution directly on raw irregular point clouds.

**Target domain:** Urban outdoor scenes; ALS / photogrammetric point clouds.

**Supervision:** Fully unsupervised clustering; weakly supervised class mapping (human labels entire clusters, not individual points).

**Notes:** This is the DC3DCD variant described in the session. Not transformer-based, but the leading unsupervised method for 3D point cloud change detection. Achieves 57–67% mean IoU on change classes without per-point labels.

---

### Deep Unsupervised Learning for 3D ALS Point Cloud Change Detection (2023)

**Title:** Deep Unsupervised Learning for 3D ALS Point Cloud Change Detection
**Authors:** Iris de Gélis, Sudipan Saha, Muhammad Shahzad, Thomas Corpetti, Sébastien Lefèvre, Xiao Xiang Zhu
**Year:** 2023
**arXiv:** [2305.03529](https://arxiv.org/abs/2305.03529)

**Architecture:** Self-supervised deep clustering + contrastive learning; adapted deep change vector analysis with nearest-point comparison. KPConv-based backbone (not transformer).

**Handling irregularity:** Nearest-point comparison between clouds; KPConv for feature extraction.

**Target domain:** Aerial LiDAR surveys; outdoor remote sensing.

**Supervision:** Fully unsupervised. Achieves >85% mean accuracy.

**Notes:** Companion paper to DC3DCD, focused on ALS data and contrastive learning. Joint work between Lefèvre/Corpetti (UBS/IRISA) and Zhu group (TU Munich / DLR).

---

### Point Transformer V3 (2024) — Backbone

**Title:** Point Transformer V3: Simpler, Faster, Stronger
**Authors:** Xiaoyang Wu, Li Jiang, et al.
**Year:** 2024
**arXiv:** [2312.10035](https://arxiv.org/abs/2312.10035)
**Venue:** CVPR 2024 (Oral)

**Architecture:** Replaces expensive radius-based neighbor search with serialized neighbor mapping (space-filling curves: Z-order, Hilbert). Standard window attention applies after serialization. PTv3 is 3× faster and uses 10–16× less memory than PTv2 at equal or better accuracy.

**Handling irregularity:** Serialization along space-filling curves maps irregular 3D points to 1D order; window attention then operates on contiguous segments.

**Target domain:** Both indoor (ScanNet) and outdoor (nuScenes, Waymo) point clouds. Designed as a general backbone — not change detection-specific but widely adopted downstream.

**Supervision:** Supervised (pretraining + fine-tuning).

**Notes:** PTv3 is the current standard backbone for point cloud perception tasks as of 2024. Change detection papers published in 2024–2025 may build on this. KPConvX (arXiv:2405.13194, 2024) is a parallel effort modernizing KPConv with kernel attention.

---

### Summary Table: Transformer Papers (2022–2025)

| Paper | Year | Transformer Type | Irregularity Handling | Remote Sensing / Outdoor | Supervision |
|-------|------|-----------------|----------------------|--------------------------|-------------|
| PBFormer | 2023 | Point Transformer (Siamese) | kNN grouping | Yes — urban ALS/photogrammetry | Supervised |
| ME-CPT | 2025 | Cross-Temporal Point Transformer | kNN + attention | Yes — ALS urban | Supervised |
| DC3DCD | 2023 | None (KPConv backbone) | KPConv on raw points | Yes — urban outdoor | Unsupervised |
| Deep Unsupervised ALS CD | 2023 | None (KPConv + contrastive) | Nearest-point matching | Yes — aerial LiDAR | Unsupervised |
| Point Transformer V3 | 2024 | Serialized window attention | Space-filling curve serialization | Both indoor + outdoor | Supervised (backbone) |

**Gap observations:**
- Very few papers combine transformers with *unsupervised* 3D point cloud change detection — this is an open research direction
- Most unsupervised 3D CD work still uses KPConv backbones (de Gélis group)
- Transformer-based change detection is more mature for 2D remote sensing images (SwinSUNet, ChangeViT, VcT) than for raw 3D point clouds
- PTv3 provides the efficiency backbone needed to scale transformer-based 3D CD to large outdoor ALS scenes
