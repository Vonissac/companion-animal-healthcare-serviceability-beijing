import matplotlib.pyplot as plt
import pandas as pd

from common import TABLES, save_figure, setup_style


LABELS = {
    "pet_healthcare": "Pet healthcare",
    "human_medical": "Human medical",
    "childcare_core": "Childcare core",
    "child_oriented": "Child oriented",
}
COLORS = {
    "pet_healthcare": "#278887",
    "human_medical": "#8d7bb2",
    "childcare_core": "#cf7468",
    "child_oriented": "#b7953e",
}


def main() -> None:
    setup_style()
    data = pd.read_csv(TABLES / "table_post_fertility_service_exposure_contrast.csv")
    data = data.loc[data["service"].isin(LABELS)].copy()
    base = data.loc[data["year"].eq(2018), ["service", "pw_exposure_1km"]].set_index("service")
    data["index"] = data.apply(
        lambda row: 100 * row["pw_exposure_1km"] / base.loc[row["service"], "pw_exposure_1km"],
        axis=1,
    )
    changes = (
        data.sort_values("year")
        .groupby("service")["pw_exposure_1km"]
        .agg(first="first", last="last")
    )
    changes["change"] = changes["last"] / changes["first"] - 1

    fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.8), gridspec_kw={"width_ratios": [2.4, 1]})
    for service, group in data.groupby("service"):
        axes[0].plot(
            group["year"].to_numpy(), group["index"].to_numpy(), marker="o", lw=1.8,
            color=COLORS[service], label=LABELS[service]
        )
    axes[0].axhline(100, color="#999999", lw=0.7, ls="--")
    axes[0].set(xlabel="Year", ylabel="Indexed 1 km exposure (2018=100)")
    axes[0].legend(frameon=False, ncol=2)
    axes[0].grid(axis="y", color="#e5e5e5", lw=0.6)

    ordered = list(LABELS)
    axes[1].barh(
        [LABELS[key] for key in ordered],
        [100 * changes.loc[key, "change"] for key in ordered],
        color=[COLORS[key] for key in ordered],
    )
    axes[1].axvline(0, color="#555555", lw=0.7)
    axes[1].set_xlabel("Exposure change, 2018-2024 (%)")
    axes[1].invert_yaxis()
    fig.tight_layout()
    save_figure(fig, "Figure_3_reproduced")


if __name__ == "__main__":
    main()
