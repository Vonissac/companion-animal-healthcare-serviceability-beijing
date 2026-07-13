from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "data/derived/tables/figure_inputs"
OUT = ROOT / "outputs/reproduced/figures"


def savefig(name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(OUT / f"{name}.png", dpi=220)
    plt.close()


def figure_service_trajectories() -> None:
    path = TABLES / "table_post_fertility_service_exposure_contrast.csv"
    frame = pd.read_csv(path)
    keep = frame[frame["service"].isin(["pet_healthcare", "human_medical", "childcare_core", "child_oriented"])]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    for service, group in keep.groupby("service"):
        group = group.sort_values("year")
        ax.plot(
            group["year"].to_numpy(),
            group["pw_exposure_1km"].to_numpy(),
            marker="o",
            linewidth=1.8,
            label=service,
        )
    ax.set_xlabel("Year")
    ax.set_ylabel("Population-weighted 1 km exposure")
    ax.grid(axis="y", color="#dddddd", linewidth=0.6)
    ax.legend(frameon=False, fontsize=8)
    savefig("verification_service_trajectories")


def figure_morphology_conversion() -> None:
    path = TABLES / "table_high_demand_mismatch_by_morphology_2024.csv"
    frame = pd.read_csv(path)
    x = frame["morphology_quintile"].astype(str)
    y_col = (
        "pw_matched_supply_rate"
        if "pw_matched_supply_rate" in frame.columns
        else "population_weighted_matched_supply_rate"
    )
    y = frame[y_col]
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    ax.bar(x.to_numpy(), y.to_numpy(), color="#2a807d")
    ax.set_xlabel("Morphology quintile")
    ax.set_ylabel("Matched supply rate")
    ax.grid(axis="y", color="#dddddd", linewidth=0.6)
    savefig("verification_morphology_conversion")


def figure_mismatch_benchmark() -> None:
    path = TABLES / "table_cross_service_mismatch_benchmark_v2.csv"
    frame = pd.read_csv(path)
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    ax.bar(
        frame["service_outcome"].to_numpy(),
        frame["latent_share_within_high_demand_population"].to_numpy(),
        color="#c86f67",
    )
    ax.set_ylabel("Latent share within high-demand population")
    ax.tick_params(axis="x", rotation=25)
    ax.grid(axis="y", color="#dddddd", linewidth=0.6)
    savefig("verification_mismatch_benchmark")


def main() -> None:
    figure_service_trajectories()
    figure_morphology_conversion()
    figure_mismatch_benchmark()
    print(f"Verification figures written to {OUT}.")


if __name__ == "__main__":
    main()
