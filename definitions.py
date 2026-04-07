"""
Dagster Definitions entry point for the AI4EO Spring School 2026 project.

Run the UI:
    uv run --extra dagster dagster dev

AI4EO Spring School 2026 — OBELIX / IRISA, Université Bretagne Sud, Vannes, April 8–10 2026.
"""

from dagster import (
    AssetSelection,
    Definitions,
    define_asset_job,
    load_asset_checks_from_modules,
    load_assets_from_modules,
)

import assets.torchgeo_tutorial as torchgeo_tutorial_module
from assets.torchgeo_tutorial import geo_dataset, raw_data

all_assets = load_assets_from_modules([torchgeo_tutorial_module])
all_checks = load_asset_checks_from_modules([torchgeo_tutorial_module])

# Named jobs with Python-based selection (no antlr4 string parsing).
# Used by CI via `dagster job execute -j <name>` to avoid the
# antlr4-python3-runtime ord() bug triggered by --select string parsing.
data_assets_job = define_asset_job(
    name="data_assets_job",
    selection=AssetSelection.assets(raw_data, geo_dataset),
    description="Download and compose datasets. Runs on every PR in CI.",
)

full_pipeline_job = define_asset_job(
    name="full_pipeline_job",
    selection=AssetSelection.groups("torchgeo_tutorial"),
    description="Full TorchGeo tutorial pipeline. Runs on main pushes in CI.",
)

defs = Definitions(
    assets=all_assets,
    asset_checks=all_checks,
    jobs=[data_assets_job, full_pipeline_job],
)
