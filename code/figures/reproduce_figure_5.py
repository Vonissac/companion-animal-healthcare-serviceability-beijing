import matplotlib.pyplot as plt
import pandas as pd

from common import DATA, TABLES, save_figure, setup_style


def heatmap(ax, frame, title, row_labels, columns, formats):
    values = frame[columns].to_numpy(dtype=float)
    image = ax.imshow(values, cmap="GnBu", aspect="auto")
    for row in range(values.shape[0]):
        for col in range(values.shape[1]):
            ax.text(col, row, formats[col](values[row, col]), ha="center", va="center", fontsize=6)
    ax.set_xticks(range(len(columns)))
    ax.set_xticklabels(
        [name.replace("_", " ") for name in columns], rotation=25, ha="right"
    )
    ax.set_yticks(range(len(row_labels)))
    ax.set_yticklabels(row_labels)
    ax.set_title(title, loc="left", fontweight="bold")
    for spine in ax.spines.values():
        spine.set_visible(False)
    return image


def main() -> None:
    setup_style()
    variants = pd.read_csv(TABLES / "table_demand_construct_variant_stability.csv")
    thresholds = pd.read_csv(TABLES / "table_demand_construct_threshold_stability.csv")
    radius = pd.read_csv(TABLES / "table_cross_radius_service_mismatch_benchmark_v3.csv")
    radius = radius.loc[radius["service_outcome"].eq("pet_medical")]

    fig, axes = plt.subplots(3, 1, figsize=(8.4, 8.2))
    heatmap(
        axes[0], variants, "Construct ablation",
        variants["variant"].str.replace("_", " "),
        ["population_overlap_with_main_top20", "latent_gap_share_within_high_demand", "matched_share_within_high_demand", "entry_top_minus_bottom_cell_rate", "platform_top_minus_bottom_cell_rate"],
        [lambda x: f"{x:.0%}"] * 5,
    )
    heatmap(
        axes[1], thresholds, "Demand cut-off stability",
        thresholds["threshold"].str.replace("_", " "),
        ["latent_gap_population", "matched_share_within_high_demand", "entry_top_minus_bottom_cell_rate", "platform_top_minus_bottom_cell_rate"],
        [lambda x: f"{x/1e6:.1f}m", lambda x: f"{x:.0%}", lambda x: f"{x:.1%}", lambda x: f"{x:.0%}"],
    )
    heatmap(
        axes[2], radius, "Radius sensitivity",
        radius["radius_m"].map(lambda value: f"{value} m"),
        ["latent_share_within_high_demand_population", "high_vs_nonhigh_supply_ratio", "selective_but_incomplete_index"],
        [lambda x: f"{x:.1%}", lambda x: f"{x:.0f}x", lambda x: f"{x:.1f}"],
    )
    fig.tight_layout(h_pad=1.3)
    save_figure(fig, "Figure_5_reproduced")


if __name__ == "__main__":
    main()
