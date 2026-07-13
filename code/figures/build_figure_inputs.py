from pathlib import Path

import pandas as pd

from common import DATA, DISTRICT_NAMES, TABLES


def main() -> None:
    spatial = pd.read_parquet(
        DATA / "grids/beijing_grid_2024_spatial_morphology_patterns.parquet"
    )
    spatial = spatial.loc[spatial["population"].gt(0)].copy()
    spatial["nonexposed_population"] = spatial["population"].where(
        spatial["pet_medical_within_1000m"].eq(0), 0
    )
    district = (
        spatial.loc[spatial["district"].isin(DISTRICT_NAMES)]
        .groupby("district", as_index=False)
        .agg(
            population=("population", "sum"),
            nonexposed_population=("nonexposed_population", "sum"),
        )
        .assign(
            nonexposed_population_share=lambda frame: (
                frame["nonexposed_population"] / frame["population"]
            ),
            district_english=lambda frame: frame["district"].map(DISTRICT_NAMES),
        )
        .sort_values("nonexposed_population_share", ascending=False)
    )
    path = TABLES / "table_district_nonexposure_ranking_2024.csv"
    district.to_csv(path, index=False)
    print(path.relative_to(Path(__file__).resolve().parents[2]))


if __name__ == "__main__":
    main()
