from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "data/derived/tables"

FINAL_TABLES = [
    "Table_1_service_expansion_exposure_benchmark.csv",
    "Table_2_demand_signal_validation_ladder.csv",
    "Table_3_construct_separation_reduced_predictor_robustness.csv",
    "Table_4_high_demand_morphology_conversion_gradient.csv",
    "Table_5_serviceability_mismatch_typology_spatial_clustering.csv",
    "Table_6_model_diagnostics_service_ecology_spatial_dependence.csv",
]

REQUIRED_FILES = [
    "data/derived/grids/beijing_grid_year_panel_2018_2024_enhanced.parquet",
    "data/derived/grids/beijing_grid_2024_spatial_morphology_patterns.parquet",
    "data/derived/maps/beijing_grid_1km_metric.parquet",
    *[f"data/derived/tables/main_text/{name}" for name in FINAL_TABLES],
    "data/derived/tables/supplementary/Table_S1_urban_morphology_construction_gis_robustness.csv",
    "data/derived/tables/supplementary/Table_S2_morphology_regimes_serviceability.csv",
    "data/derived/models/morphology_model_comparison_2024.csv",
    "docs/DATA_DICTIONARY.md",
    "docs/DATA_SOURCES_AND_BOUNDARIES.md",
    *[f"outputs/publication_figures/Figure_{number}.pdf" for number in range(1, 8)],
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_manifest() -> None:
    manifest = pd.read_csv(ROOT / "MANIFEST.csv")
    if manifest["path"].duplicated().any():
        raise ValueError("MANIFEST.csv contains duplicate paths.")

    expected = set(manifest["path"])
    actual = set()
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        generated = relative.parts[:2] == ("outputs", "reproduced")
        if (
            path.is_file()
            and ".git" not in relative.parts
            and not generated
            and "__pycache__" not in relative.parts
            and path.name != "MANIFEST.csv"
            and path.suffix != ".pyc"
        ):
            actual.add(str(relative))
    if expected != actual:
        raise ValueError(
            f"Manifest mismatch; missing={sorted(expected - actual)}, "
            f"unlisted={sorted(actual - expected)}"
        )

    for row in manifest.itertuples(index=False):
        path = ROOT / row.path
        if path.stat().st_size != int(row.bytes) or sha256(path) != row.sha256:
            raise ValueError(f"Manifest value mismatch: {row.path}")


def weighted_mean(frame: pd.DataFrame, value: str) -> float:
    return float(np.average(frame[value], weights=frame["population"]))


def exact_conversion_rows(spatial: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for group, frame in spatial.loc[spatial["high_demand"].eq(1)].groupby(
        "morphology_quintile", observed=True
    ):
        population = float(frame["population"].sum())
        latent = float(
            frame.loc[frame["pet_supply_positive_1km"].eq(0), "population"].sum()
        )
        rows.append(
            {
                "morphology_quintile": str(group),
                "cells": int(len(frame)),
                "population": population,
                "population_weighted_matched_supply_rate": weighted_mean(
                    frame, "pet_supply_positive_1km"
                ),
                "latent_high_demand_no_supply_population": latent,
                "latent_share_within_quintile_population": latent / population,
                "pw_pet_medical_1km": weighted_mean(frame, "pet_medical_within_1000m"),
                "mean_morphology_composite": float(
                    frame["morphology_composite_index_exact"].mean()
                ),
                "mean_serviceability": float(frame["serviceability_core_index"].mean()),
            }
        )
    return pd.DataFrame(rows)


def verify_table_structure() -> None:
    main = sorted(path.name for path in (TABLES / "main_text").glob("Table_*.csv"))
    if main != sorted(FINAL_TABLES):
        raise ValueError(f"The main-text folder must contain the final six tables: {main}")
    supplementary = sorted(
        path.name for path in (TABLES / "supplementary").glob("Table_*.csv")
    )
    if supplementary != [
        "Table_S1_urban_morphology_construction_gis_robustness.csv",
        "Table_S2_morphology_regimes_serviceability.csv",
    ]:
        raise ValueError(f"Unexpected supplementary table set: {supplementary}")


def verify_core_values() -> None:
    panel = pd.read_parquet(
        ROOT / "data/derived/grids/beijing_grid_year_panel_2018_2024_enhanced.parquet"
    )
    spatial = pd.read_parquet(
        ROOT / "data/derived/grids/beijing_grid_2024_spatial_morphology_patterns.parquet"
    )
    if len(panel) != 16_992 * 7 or panel["year"].nunique() != 7:
        raise ValueError("The 2018-2024 grid-year panel has drifted.")
    populated = spatial.loc[spatial["population"].gt(0)].copy()
    if len(spatial) != 16_992 or len(populated) != 12_236:
        raise ValueError("The full-grid or populated-grid denominator has drifted.")

    rho = populated[
        ["morphology_composite_index_exact", "serviceability_core_index"]
    ].corr(method="spearman").iloc[0, 1]
    if not np.isclose(rho, 0.865, atol=0.0005):
        raise ValueError("Morphology-serviceability correlation has drifted.")
    table3 = pd.read_csv(TABLES / "main_text/Table_3_construct_separation_reduced_predictor_robustness.csv")
    reported_rho = float(
        table3.loc[
            table3["Check"].eq("Morphology-serviceability correlation"), "Result"
        ].iloc[0]
    )
    if not np.isclose(reported_rho, rho, atol=0.0005):
        raise ValueError("Table 3 does not report the grid-derived correlation.")

    calculated = exact_conversion_rows(spatial).sort_values("morphology_quintile")
    published = pd.read_csv(
        TABLES / "figure_inputs/table_high_demand_mismatch_by_morphology_2024.csv"
    ).sort_values("morphology_quintile")
    numeric = [
        "cells",
        "population",
        "population_weighted_matched_supply_rate",
        "latent_high_demand_no_supply_population",
        "latent_share_within_quintile_population",
        "pw_pet_medical_1km",
        "mean_morphology_composite",
        "mean_serviceability",
    ]
    if not np.allclose(calculated[numeric], published[numeric], rtol=1e-10, atol=1e-8):
        raise ValueError("Exact morphology conversion values have drifted.")

    table4 = pd.read_csv(TABLES / "main_text/Table_4_high_demand_morphology_conversion_gradient.csv")
    table4 = table4.set_index("Morphology group within high demand")
    for row in published.itertuples(index=False):
        shown = table4.loc[row.morphology_quintile]
        checks = [
            int(str(shown["Cells"]).replace(",", "")) == row.cells,
            str(shown["Population"]) == f"{row.population / 1_000_000:.2f}m",
            str(shown["PW matched"]) == f"{row.population_weighted_matched_supply_rate:.1%}",
            str(shown["Latent share"]) == f"{row.latent_share_within_quintile_population:.1%}",
            np.isclose(float(shown["PW pet HC 1 km"]), row.pw_pet_medical_1km, atol=0.0005),
            np.isclose(float(shown["Morphology"]), row.mean_morphology_composite, atol=0.005),
            np.isclose(float(shown["Serviceability"]), row.mean_serviceability, atol=0.005),
        ]
        if not all(checks):
            raise ValueError(f"Table 4 differs from exact data for {row.morphology_quintile}.")

    moran = pd.read_csv(TABLES / "figure_inputs/table_spatial_morphology_moran_tests_2024.csv")
    expected_moran = {
        "morphology_composite_index_exact": 0.883,
        "household_pet_care_signal": 0.873,
        "serviceability_core_index": 0.843,
        "pet_medical_within_1000m": 0.605,
        "latent_high_demand_no_supply": 0.363,
    }
    for variable, expected in expected_moran.items():
        value = moran.loc[moran["variable"].eq(variable), "moran_i"].iloc[0]
        if not np.isclose(value, expected, atol=0.0005):
            raise ValueError(f"Moran's I has drifted for {variable}.")
    table5 = pd.read_csv(TABLES / "main_text/Table_5_serviceability_mismatch_typology_spatial_clustering.csv")
    if int(table5["Type or test"].str.startswith("Spatial clustering:").sum()) != 5:
        raise ValueError("Table 5 must contain all five Moran diagnostics.")

    radius = pd.read_csv(TABLES / "figure_inputs/table_cross_radius_service_mismatch_benchmark_v3.csv")
    expected_radius = {
        500: (0.6850621015570323, 142.44425331101132, 97.58315952796367),
        1000: (0.3485033732742985, 56.94207347396403, 19.84450468690942),
        2000: (0.1098367930840821, 19.05619106075457, 2.0930709145108364),
    }
    pet = radius.loc[radius["service_outcome"].eq("pet_medical")].set_index("radius_m")
    for distance, expected in expected_radius.items():
        values = pet.loc[distance, [
            "latent_share_within_high_demand_population",
            "high_vs_nonhigh_supply_ratio",
            "selective_but_incomplete_index",
        ]].to_numpy(dtype=float)
        if not np.allclose(values, expected, rtol=1e-10, atol=1e-10):
            raise ValueError(f"Radius benchmark has drifted at {distance} m.")

    typology = pd.read_csv(
        TABLES / "figure_inputs/table_spatial_morphology_serviceability_typology_2024.csv"
    )
    high = typology["serviceability_mismatch_type"].str.startswith(("A_", "B_", "C_", "D_"))
    latent = typology["serviceability_mismatch_type"].str.startswith(("B_", "C_"))
    high_population = float(typology.loc[high, "population"].sum())
    latent_population = float(typology.loc[latent, "population"].sum())
    if not np.allclose(
        [high_population, latent_population, latent_population / high_population],
        [17_613_545.763750374, 6_117_945.4572582245, 0.3473432061504212],
    ):
        raise ValueError("The morphology-typology denominator has drifted.")

    for number in range(1, 8):
        path = ROOT / f"outputs/publication_figures/Figure_{number}.pdf"
        if path.stat().st_size < 20_000 or path.read_bytes()[:4] != b"%PDF":
            raise ValueError(f"Invalid publication figure: {path.name}")


def describe(path: Path) -> dict:
    if path.suffix == ".parquet":
        frame = pd.read_parquet(path)
    elif path.suffix == ".csv":
        frame = pd.read_csv(path)
    else:
        return {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size}
    return {
        "path": str(path.relative_to(ROOT)),
        "rows": int(frame.shape[0]),
        "columns": int(frame.shape[1]),
    }


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        raise FileNotFoundError("Missing required files: " + ", ".join(missing))
    verify_manifest()
    verify_table_structure()
    verify_core_values()

    out = ROOT / "outputs/reproduced"
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(describe(ROOT / path) for path in REQUIRED_FILES).to_json(
        out / "reproducibility_check.json", orient="records", indent=2
    )
    print("Reproducibility check passed: package, six tables, figures and key values agree.")


if __name__ == "__main__":
    main()
