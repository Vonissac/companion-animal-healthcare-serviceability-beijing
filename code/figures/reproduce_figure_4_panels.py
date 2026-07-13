import matplotlib.pyplot as plt
import pandas as pd

from common import TABLES, save_figure, setup_style


RING_ORDER = ["inner_2nd", "2nd_3rd", "3rd_4th", "4th_5th", "5th_6th", "outer_6th"]
RING_LABELS = ["<2nd", "2nd-3rd", "3rd-4th", "4th-5th", "5th-6th", ">6th"]


def main() -> None:
    setup_style()
    yearly = pd.read_csv(TABLES / "table_main_yearly_metrics.csv")
    rings = pd.read_csv(TABLES / "table_ring_exposure_summary.csv")
    district = pd.read_csv(TABLES / "table_district_nonexposure_ranking_2024.csv")

    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.6))
    axes[0].plot(
        yearly["year"].to_numpy(),
        yearly["medical_points"].to_numpy(),
        marker="o",
        color="#278887",
    )
    axes[0].set(xlabel="Year", ylabel="Sites", title="Service expansion")
    axes[0].grid(axis="y", color="#e5e5e5", lw=0.6)

    ring = rings.loc[rings["year"].eq(2024)].set_index("ring_zone").loc[RING_ORDER]
    axes[1].barh(RING_LABELS, ring["pw_pet_medical_1km"], color="#42918e")
    axes[1].invert_yaxis()
    axes[1].set(xlabel="Population-weighted 1 km exposure", title="Ring-zone gradient")

    ranked = district.head(10).sort_values("nonexposed_population_share")
    axes[2].barh(
        ranked["district_english"], 100 * ranked["nonexposed_population_share"], color="#ce7d73"
    )
    axes[2].set(xlabel="Non-exposed population (%)", title="District ranking")
    fig.tight_layout()
    save_figure(fig, "Figure_4_reproduced_summary_panels")


if __name__ == "__main__":
    main()
