from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
MAIN_TABLES = ROOT / "data/derived/tables/main_text"
OUT = ROOT / "outputs/reproduced/tables"

FINAL_TABLES = [
    "Table_1_service_expansion_exposure_benchmark.csv",
    "Table_2_demand_signal_validation_ladder.csv",
    "Table_3_construct_separation_reduced_predictor_robustness.csv",
    "Table_4_high_demand_morphology_conversion_gradient.csv",
    "Table_5_serviceability_mismatch_typology_spatial_clustering.csv",
    "Table_6_model_diagnostics_service_ecology_spatial_dependence.csv",
]


def main() -> None:
    if len(FINAL_TABLES) != 6:
        raise ValueError("The manuscript must contain exactly six main tables.")

    actual = sorted(path.name for path in MAIN_TABLES.glob("Table_*.csv"))
    if actual != sorted(FINAL_TABLES):
        raise ValueError(f"Unexpected main-text table set: {actual}")

    OUT.mkdir(parents=True, exist_ok=True)
    summaries = []
    for filename in FINAL_TABLES:
        frame = pd.read_csv(MAIN_TABLES / filename)
        frame.to_csv(OUT / filename, index=False)
        summaries.append(
            {
                "table": filename,
                "rows": int(frame.shape[0]),
                "columns": int(frame.shape[1]),
                "column_names": "; ".join(frame.columns),
            }
        )

    pd.DataFrame(summaries).to_csv(OUT / "main_table_inventory.csv", index=False)
    print("Recreated 6 final manuscript tables.")


if __name__ == "__main__":
    main()
