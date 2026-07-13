import matplotlib.pyplot as plt
import pandas as pd

from common import DATA, TABLES, save_figure, setup_style


def main() -> None:
    setup_style()
    profiles = pd.read_csv(TABLES / "table_spatial_morphology_cluster_profiles_2024.csv")
    matrix = pd.read_csv(TABLES / "table_spatial_morphology_demand_matrix_2024.csv")
    conversion = pd.read_csv(TABLES / "table_high_demand_mismatch_by_morphology_2024.csv")
    moran = pd.read_csv(TABLES / "table_spatial_morphology_moran_tests_2024.csv")

    fig, axes = plt.subplots(2, 2, figsize=(9.2, 7.0))
    profile_columns = ["mean_activity", "mean_built_form", "mean_functional_mix", "mean_urban_intensity", "mean_demand_signal", "mean_serviceability"]
    image = axes[0, 0].imshow(profiles[profile_columns], cmap="GnBu", aspect="auto")
    axes[0, 0].set_xticks(range(len(profile_columns)))
    axes[0, 0].set_xticklabels(
        ["activity", "built", "mix", "intensity", "demand", "service"],
        rotation=25,
        ha="right",
    )
    axes[0, 0].set_yticks(range(len(profiles)))
    axes[0, 0].set_yticklabels([f"C{i}" for i in range(1, len(profiles) + 1)])
    axes[0, 0].set_title("Morphology regime profiles", loc="left", fontweight="bold")

    demand_order = ["Q1_low", "Q2", "Q3", "Q4", "Q5_high"]
    morph_order = ["M1_low", "M2", "M3", "M4", "M5_high"]
    pivot = matrix.pivot(index="demand_quintile", columns="morphology_quintile", values="pw_matched_supply_rate").reindex(index=demand_order, columns=morph_order)
    axes[0, 1].imshow(pivot, cmap="GnBu", vmin=0, vmax=1, aspect="auto")
    axes[0, 1].set_xticks(range(5))
    axes[0, 1].set_xticklabels(morph_order, rotation=25, ha="right")
    axes[0, 1].set_yticks(range(5))
    axes[0, 1].set_yticklabels(demand_order)
    axes[0, 1].set_title("Demand x morphology conversion", loc="left", fontweight="bold")

    conversion = conversion.set_index("morphology_quintile").loc[["M2", "M3", "M4", "M5_high"]]
    x = range(len(conversion))
    axes[1, 0].bar(x, conversion["population_weighted_matched_supply_rate"], color="#56a17d", label="matched")
    axes[1, 0].bar(x, conversion["latent_share_within_quintile_population"], bottom=conversion["population_weighted_matched_supply_rate"], color="#c9766d", label="latent")
    axes[1, 0].set_xticks(list(x))
    axes[1, 0].set_xticklabels(conversion.index)
    axes[1, 0].set_ylim(0, 1)
    axes[1, 0].set_ylabel("Population share")
    axes[1, 0].set_title("High-demand conversion gradient", loc="left", fontweight="bold")
    axes[1, 0].legend(frameon=False)

    moran = moran.sort_values("moran_i")
    axes[1, 1].hlines(
        range(len(moran)), 0, moran["moran_i"].to_numpy(), color="#c9c7bf", lw=4
    )
    axes[1, 1].scatter(
        moran["moran_i"].to_numpy(), range(len(moran)), color="#4da4a4", s=36
    )
    axes[1, 1].set_yticks(range(len(moran)))
    axes[1, 1].set_yticklabels(["gap", "pet HC", "service", "demand", "morphology"])
    axes[1, 1].set_xlabel("Moran's I")
    axes[1, 1].set_title("Spatial clustering", loc="left", fontweight="bold")
    fig.tight_layout(h_pad=1.3, w_pad=1.2)
    save_figure(fig, "Figure_6_reproduced")


if __name__ == "__main__":
    main()
