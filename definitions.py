"""
Dagster Definitions entry point for the AI4EO Spring School 2026 project.

Run the UI:
    uv run --extra dagster dagster dev

AI4EO Spring School 2026 — OBELIX / IRISA, Université Bretagne Sud, Vannes, April 8–10 2026.
"""

from dagster import Definitions, load_assets_from_modules

import assets.torchgeo_tutorial as torchgeo_tutorial_module

all_assets = load_assets_from_modules([torchgeo_tutorial_module])

defs = Definitions(assets=all_assets)
