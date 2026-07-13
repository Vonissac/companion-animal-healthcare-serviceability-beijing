import matplotlib.pyplot as plt
import pandas as pd

from common import DATA, clean_map, load_spatial, save_figure, setup_style


def main() -> None:
    setup_style()
    spatial = load_spatial()
    clinic = pd.read_parquet(DATA / "models/clinic_type_grid_exposure_1km.parquet")
    clinic = clinic.loc[clinic["year"].eq(2024)].drop(columns="year")
    spatial = spatial.merge(clinic, on="grid_id", how="left")
    spatial = spatial.loc[spatial["population"].gt(0)].copy()

    panels = [
        ("Morphology", "morphology_composite_index_exact", "GnBu", None),
        ("Nighttime light", "ntl_2024_mean_zonal", "YlOrBr", None),
        ("Demand signal", "household_pet_care_signal", "Purples", None),
        ("Serviceability", "serviceability_core_index", "Greens", None),
        ("Latent gap", "latent_high_demand_no_supply", "Reds", (0, 1)),
        (
            "Advanced/chain exposure",
            "type_advanced_or_chain_within_1000m",
            "Blues",
            None,
        ),
    ]
    fig, axes = plt.subplots(2, 3, figsize=(10.2, 6.0))
    for ax, (title, column, cmap, limits) in zip(axes.flat, panels):
        kwargs = {"column": column, "cmap": cmap, "ax": ax, "linewidth": 0}
        if limits:
            kwargs.update(vmin=limits[0], vmax=limits[1])
        spatial.plot(**kwargs)
        ax.set_title(title, loc="left", fontweight="bold")
        clean_map(ax)
    fig.tight_layout(pad=0.8, w_pad=0.4, h_pad=0.8)
    save_figure(fig, "Figure_2_reproduced_panels")


if __name__ == "__main__":
    main()
