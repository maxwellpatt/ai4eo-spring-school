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

- Some relevant applications for pre/post peatland disturbance projects — key question: are we tracking change presence or deriving quantitative metrics?
- Unsupervised methods are still significantly improvable
- Change detection requires encoding change *information*, not just geometry
- Guiding the network with hand-crafted features is necessary for unsupervised learning to work well
