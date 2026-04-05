"""
TorchGeo introductory tutorial scaffolded as Dagster assets.

Follows https://torchgeo.readthedocs.io/en/stable/tutorials/torchgeo.html

Pipeline:
  raw_data → geo_dataset → trained_model

Datasets: Landsat 7 + Landsat 8 (union) intersected with Cropland Data Layer (CDL).
Task: semantic segmentation of land cover from multi-spectral satellite imagery.

AI4EO Spring School 2026 — OBELIX / IRISA, Université Bretagne Sud, Vannes, April 8–10 2026.
Session: TorchGeo + MLOps — Adam Stewart (TU Munich).
Zora relevance: HIGH — patterns directly applicable to raster processing pipelines.
"""

from pathlib import Path

from dagster import AssetExecutionContext, Config, Output, asset


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


class DataConfig(Config):
    # Root directory for downloaded datasets
    data_root: str = "data/torchgeo_tutorial"


class TrainingConfig(Config):
    data_root: str = "data/torchgeo_tutorial"
    # Spatial size (pixels) of each sampled patch
    patch_size: int = 256
    # Number of random patches to sample per epoch
    length: int = 200
    batch_size: int = 8
    num_workers: int = 0
    max_epochs: int = 5
    learning_rate: float = 1e-3
    checkpoint_dir: str = "checkpoints"


# ---------------------------------------------------------------------------
# Asset 1: raw_data
# ---------------------------------------------------------------------------


_HF_BASE = (
    "https://hf.co/datasets/torchgeo/tutorials/resolve/"
    "ff30b729e3cbf906148d69a4441cc68023898924/"
)
_LANDSAT7_ARCHIVE = "LE07_L2SP_022032_20230725_20230820_02_T1.tar.gz"
_LANDSAT8_ARCHIVE = "LC08_L2SP_023032_20230831_20230911_02_T1.tar.gz"
_CDL_ARCHIVE = "2023_30m_cdls.zip"

LANDSAT7_BANDS = ["SR_B1", "SR_B2", "SR_B3", "SR_B4", "SR_B5", "SR_B7"]
LANDSAT8_BANDS = ["SR_B2", "SR_B3", "SR_B4", "SR_B5", "SR_B6", "SR_B7"]


@asset(
    group_name="torchgeo_tutorial",
    description=(
        "Download Landsat 7, Landsat 8, and Cropland Data Layer (CDL) sample tiles "
        "from the TorchGeo HuggingFace tutorial repository."
    ),
)
def raw_data(context: AssetExecutionContext, config: DataConfig) -> Output[dict]:
    """
    Download pre-packaged tutorial data from HuggingFace.

    Landsat 7/8 no longer support auto-download via TorchGeo; the tutorial
    instead ships small sample archives on HuggingFace. Both Landsat archives
    are extracted into the same directory so Landsat7/Landsat8 can share a
    single `paths` root. CDL is extracted separately.
    """
    from torchgeo.datasets.utils import download_and_extract_archive

    root = Path(config.data_root)
    landsat_root = root / "landsat"
    cdl_root = root / "cdl"
    landsat_root.mkdir(parents=True, exist_ok=True)
    cdl_root.mkdir(parents=True, exist_ok=True)

    context.log.info(f"Downloading Landsat 7 archive to {landsat_root}")
    download_and_extract_archive(_HF_BASE + _LANDSAT7_ARCHIVE, str(landsat_root))

    context.log.info(f"Downloading Landsat 8 archive to {landsat_root}")
    download_and_extract_archive(_HF_BASE + _LANDSAT8_ARCHIVE, str(landsat_root))

    context.log.info(f"Downloading CDL archive to {cdl_root}")
    download_and_extract_archive(_HF_BASE + _CDL_ARCHIVE, str(cdl_root))

    l7_files = list(landsat_root.rglob("LE07_*.TIF"))
    l8_files = list(landsat_root.rglob("LC08_*.TIF"))
    cdl_files = list(cdl_root.rglob("*.tif"))

    context.log.info(
        f"Landsat7: {len(l7_files)} TIF files | "
        f"Landsat8: {len(l8_files)} TIF files | "
        f"CDL: {len(cdl_files)} tif files"
    )

    return Output(
        value={
            "landsat_root": str(landsat_root),
            "cdl_root": str(cdl_root),
            "landsat7_bands": LANDSAT7_BANDS,
            "landsat8_bands": LANDSAT8_BANDS,
            "landsat7_files": len(l7_files),
            "landsat8_files": len(l8_files),
            "cdl_files": len(cdl_files),
        },
        metadata={
            "landsat7_files": len(l7_files),
            "landsat8_files": len(l8_files),
            "cdl_files": len(cdl_files),
        },
    )


# ---------------------------------------------------------------------------
# Asset 2: geo_dataset
# ---------------------------------------------------------------------------


@asset(
    group_name="torchgeo_tutorial",
    description=(
        "Compose Landsat 7 | Landsat 8 (union) and intersect with CDL labels. "
        "Returns dataset statistics: CRS, resolution, spatial extent, sample count."
    ),
)
def geo_dataset(
    context: AssetExecutionContext,
    raw_data: dict,  # noqa: A002
) -> Output[dict]:
    """
    Build the composed TorchGeo GeoDataset.

    TorchGeo's | operator unions two GeoDatasets so queries return whichever
    source covers a given location/time. The & operator intersects datasets so
    only regions covered by *both* are queryable — here that means pixels with
    both imagery and CDL labels.

    Returns dataset statistics for downstream assets and the Dagster UI.
    """
    from torchgeo.datasets import CDL, Landsat7, Landsat8
    from torchgeo.samplers import RandomGeoSampler

    landsat7 = Landsat7(paths=raw_data["landsat_root"], bands=raw_data["landsat7_bands"])
    landsat8 = Landsat8(paths=raw_data["landsat_root"], bands=raw_data["landsat8_bands"])
    cdl = CDL(paths=raw_data["cdl_root"])

    # Union of Landsat sources, then intersect with labels
    landsat = landsat7 | landsat8
    dataset = landsat & cdl

    context.log.info(f"Composed dataset CRS: {dataset.crs}")
    context.log.info(f"Composed dataset res: {dataset.res}")

    # Probe one sample to confirm shapes
    sampler = RandomGeoSampler(dataset, size=256, length=1)
    sample_query = next(iter(sampler))
    sample = dataset[sample_query]
    image_shape = list(sample["image"].shape)
    mask_shape = list(sample["mask"].shape)

    context.log.info(f"Sample image shape: {image_shape} | mask shape: {mask_shape}")

    b = dataset.bounds
    return Output(
        value={
            "crs": str(dataset.crs),
            "res": dataset.res,
            "bounds": {"minx": b.minx, "miny": b.miny, "maxx": b.maxx, "maxy": b.maxy},
            "image_shape": image_shape,
            "mask_shape": mask_shape,
            "image_channels": image_shape[0],
            "data_root": raw_data["landsat_root"],
            "cdl_root": raw_data["cdl_root"],
            "landsat7_bands": raw_data["landsat7_bands"],
            "landsat8_bands": raw_data["landsat8_bands"],
        },
        metadata={
            "crs": str(dataset.crs),
            "image_channels": image_shape[0],
            "patch_height": image_shape[1],
            "patch_width": image_shape[2],
        },
    )


# ---------------------------------------------------------------------------
# Asset 3: trained_model
# ---------------------------------------------------------------------------


@asset(
    group_name="torchgeo_tutorial",
    description=(
        "Train a semantic segmentation model on the Landsat+CDL dataset using "
        "TorchGeo's RandomGeoSampler and GridGeoSampler. Saves checkpoint to disk."
    ),
)
def trained_model(
    context: AssetExecutionContext,
    geo_dataset: dict,  # noqa: A002
    config: TrainingConfig,
) -> Output[dict]:
    """
    Train a U-Net style segmentation model on Landsat + CDL patches.

    Training uses RandomGeoSampler (random patch locations) and evaluation
    uses GridGeoSampler (non-overlapping grid, no double-counting).

    For a production-grade training loop with pretrained Landsat weights, swap
    the mini U-Net for torchgeo.trainers.SemanticSegmentationTask.

    Returns checkpoint path and final training loss.
    """
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader
    from torchgeo.datasets import CDL, Landsat7, Landsat8
    from torchgeo.datasets.utils import stack_samples
    from torchgeo.samplers import GridGeoSampler, RandomGeoSampler

    landsat7 = Landsat7(paths=geo_dataset["data_root"], bands=geo_dataset["landsat7_bands"])
    landsat8 = Landsat8(paths=geo_dataset["data_root"], bands=geo_dataset["landsat8_bands"])
    cdl = CDL(paths=geo_dataset["cdl_root"])

    landsat = landsat7 | landsat8
    dataset = landsat & cdl

    train_sampler = RandomGeoSampler(dataset, size=config.patch_size, length=config.length)
    val_sampler = GridGeoSampler(dataset, size=config.patch_size, stride=config.patch_size)

    train_loader = DataLoader(
        dataset,
        batch_size=config.batch_size,
        sampler=train_sampler,
        collate_fn=stack_samples,
        num_workers=config.num_workers,
    )
    DataLoader(  # val_loader — kept for evaluation loop extension
        dataset,
        batch_size=config.batch_size,
        sampler=val_sampler,
        collate_fn=stack_samples,
        num_workers=config.num_workers,
    )

    in_channels = geo_dataset["image_channels"]
    num_classes = 256  # CDL has up to 256 land cover classes

    model = _build_segmentation_model(in_channels=in_channels, num_classes=num_classes)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    criterion = nn.CrossEntropyLoss(ignore_index=0)

    context.log.info(
        f"Training on {device} | {config.max_epochs} epochs | "
        f"{len(train_sampler)} patches/epoch | batch_size={config.batch_size}"
    )

    train_losses = []
    for epoch in range(config.max_epochs):
        model.train()
        epoch_loss = 0.0
        for batch in train_loader:
            images = batch["image"].to(device)
            masks = batch["mask"].long().to(device)

            optimizer.zero_grad()
            logits = model(images)
            loss = criterion(logits, masks.squeeze(1))
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

        avg_loss = epoch_loss / len(train_loader)
        train_losses.append(avg_loss)
        context.log.info(f"Epoch {epoch + 1}/{config.max_epochs} — loss: {avg_loss:.4f}")

    ckpt_dir = Path(config.checkpoint_dir)
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    ckpt_path = ckpt_dir / "torchgeo_tutorial.pt"
    torch.save(
        {
            "epoch": config.max_epochs,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "train_losses": train_losses,
            "in_channels": in_channels,
            "num_classes": num_classes,
        },
        ckpt_path,
    )
    context.log.info(f"Checkpoint saved to {ckpt_path}")

    total_params = sum(p.numel() for p in model.parameters())

    return Output(
        value={
            "checkpoint": str(ckpt_path),
            "final_loss": train_losses[-1],
            "train_losses": train_losses,
            "in_channels": in_channels,
            "num_classes": num_classes,
            "patch_size": config.patch_size,
            "total_parameters": total_params,
            "hyperparameters": {
                "max_epochs": config.max_epochs,
                "learning_rate": config.learning_rate,
                "batch_size": config.batch_size,
                "patch_size": config.patch_size,
                "length": config.length,
            },
        },
        metadata={
            "checkpoint_path": str(ckpt_path),
            "final_train_loss": round(train_losses[-1], 4),
            "epochs": config.max_epochs,
        },
    )


# ---------------------------------------------------------------------------
# Internal helpers (no module-level torch import — loaded lazily above)
# ---------------------------------------------------------------------------


def _build_segmentation_model(in_channels: int, num_classes: int):
    """
    Minimal U-Net for semantic segmentation.

    For production use, replace with:
        from torchgeo.trainers import SemanticSegmentationTask
        task = SemanticSegmentationTask(
            model="unet", backbone="resnet18",
            weights="Landsat8_OLI_TIRS_LandCover",
            in_channels=in_channels, num_classes=num_classes,
        )
    """
    import torch
    import torch.nn as nn

    class _ConvBlock(nn.Module):
        """Two conv layers with BN + ReLU."""

        def __init__(self, in_ch: int, out_ch: int) -> None:
            super().__init__()
            self.block = nn.Sequential(
                nn.Conv2d(in_ch, out_ch, 3, padding=1, bias=False),
                nn.BatchNorm2d(out_ch),
                nn.ReLU(inplace=True),
                nn.Conv2d(out_ch, out_ch, 3, padding=1, bias=False),
                nn.BatchNorm2d(out_ch),
                nn.ReLU(inplace=True),
            )

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            return self.block(x)

    class MiniUNet(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.enc1 = _ConvBlock(in_channels, 32)
            self.enc2 = _ConvBlock(32, 64)
            self.pool = nn.MaxPool2d(2)
            self.bottleneck = _ConvBlock(64, 128)
            self.up1 = nn.ConvTranspose2d(128, 64, 2, stride=2)
            self.dec1 = _ConvBlock(128, 64)
            self.up2 = nn.ConvTranspose2d(64, 32, 2, stride=2)
            self.dec2 = _ConvBlock(64, 32)
            self.head = nn.Conv2d(32, num_classes, 1)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            e1 = self.enc1(x)
            e2 = self.enc2(self.pool(e1))
            b = self.bottleneck(self.pool(e2))
            d1 = self.dec1(torch.cat([self.up1(b), e2], dim=1))
            d2 = self.dec2(torch.cat([self.up2(d1), e1], dim=1))
            return self.head(d2)

    return MiniUNet()


# ---------------------------------------------------------------------------
# Asset 4: model_stac_item
# ---------------------------------------------------------------------------


@asset(
    group_name="torchgeo_tutorial",
    description=(
        "Write a STAC Item with MLM extension metadata describing the trained "
        "segmentation model. Saved as a JSON file alongside the checkpoint."
    ),
)
def model_stac_item(
    context: AssetExecutionContext,
    trained_model: dict,  # noqa: A002
    geo_dataset: dict,  # noqa: A002
) -> Output[dict]:
    """
    Produce a STAC Item conforming to the Machine Learning Model (MLM) extension.

    Spec: https://github.com/stac-extensions/mlm

    The item captures everything needed to reproduce or deploy the model:
    architecture, framework version, input/output tensor specs, training
    hyperparameters, spatial extent, and a link to the checkpoint artifact.
    """
    import datetime
    import json

    import torch
    from pyproj import CRS, Transformer

    MLM_SCHEMA = "https://stac-extensions.github.io/mlm/v1.4.0/schema.json"

    # ---- spatial extent (reproject to WGS-84 for STAC bbox/geometry) --------
    b = geo_dataset["bounds"]
    src_crs = CRS.from_user_input(geo_dataset["crs"])
    wgs84 = CRS.from_epsg(4326)
    if not src_crs.equals(wgs84):
        transformer = Transformer.from_crs(src_crs, wgs84, always_xy=True)
        west, south = transformer.transform(b["minx"], b["miny"])
        east, north = transformer.transform(b["maxx"], b["maxy"])
    else:
        west, south, east, north = b["minx"], b["miny"], b["maxx"], b["maxy"]

    bbox = [west, south, east, north]
    geometry = {
        "type": "Polygon",
        "coordinates": [[
            [west, south], [east, south], [east, north], [west, north], [west, south],
        ]],
    }

    # ---- tensor specs --------------------------------------------------------
    patch_size = trained_model["patch_size"]
    in_channels = trained_model["in_channels"]
    num_classes = trained_model["num_classes"]

    mlm_input = [{
        "name": "landsat_patch",
        "bands": geo_dataset["landsat7_bands"] + geo_dataset["landsat8_bands"],
        "input": {
            "shape": [-1, in_channels, patch_size, patch_size],
            "dim_order": ["batch", "channel", "height", "width"],
            "data_type": "float32",
        },
    }]

    mlm_output = [{
        "name": "land_cover_mask",
        "tasks": ["semantic-segmentation"],
        "result": {
            "shape": [-1, num_classes, patch_size, patch_size],
            "dim_order": ["batch", "class", "height", "width"],
            "data_type": "float32",
        },
    }]

    # ---- checkpoint artifact -------------------------------------------------
    ckpt_path = Path(trained_model["checkpoint"])
    ckpt_size = ckpt_path.stat().st_size if ckpt_path.exists() else None

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    item = {
        "type": "Feature",
        "stac_version": "1.0.0",
        "stac_extensions": [MLM_SCHEMA],
        "id": "torchgeo-tutorial-mini-unet",
        "geometry": geometry,
        "bbox": bbox,
        "properties": {
            "datetime": now,
            "mlm:name": "torchgeo-tutorial-mini-unet",
            "mlm:architecture": "U-Net",
            "mlm:tasks": ["semantic-segmentation"],
            "mlm:framework": "PyTorch",
            "mlm:framework_version": torch.__version__,
            "mlm:total_parameters": trained_model["total_parameters"],
            "mlm:pretrained": False,
            "mlm:pretrained_source": None,
            "mlm:input": mlm_input,
            "mlm:output": mlm_output,
            "mlm:hyperparameters": trained_model["hyperparameters"],
            "mlm:batch_size_suggestion": trained_model["hyperparameters"]["batch_size"],
        },
        "assets": {
            "model": {
                "href": str(ckpt_path.resolve()),
                "type": "application/octet-stream",
                "title": "PyTorch checkpoint (torch.save)",
                "roles": ["mlm:model"],
                "mlm:artifact_type": "torch.save",
                **({"file:size": ckpt_size} if ckpt_size else {}),
            }
        },
        "links": [],
    }

    stac_path = ckpt_path.with_suffix(".stac.json")
    stac_path.write_text(json.dumps(item, indent=2))
    context.log.info(f"STAC item written to {stac_path}")

    return Output(
        value={"stac_path": str(stac_path), "item_id": item["id"]},
        metadata={
            "stac_path": str(stac_path),
            "mlm_schema": MLM_SCHEMA,
            "total_parameters": trained_model["total_parameters"],
            "bbox": str(bbox),
        },
    )
