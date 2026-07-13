import matplotlib.pyplot as plt
import pandas as pd

from common import DATA, TABLES, save_figure, setup_style


def main() -> None:
    setup_style()
    typology = pd.read_csv(TABLES / "table_spatial_morphology_serviceability_typology_2024.csv")
    cross = pd.read_csv(TABLES / "table_cross_service_mismatch_benchmark_v2.csv")
    terms = pd.read_csv(DATA / "models/high_demand_serviceability_split_model_terms.csv")
    subway = pd.read_csv(TABLES / "table_subway_band_by_clinic_type.csv")

    high = typology["serviceability_mismatch_type"].str.startswith(("A_", "B_", "C_", "D_"))
    latent = typology["serviceability_mismatch_type"].str.startswith(("B_", "C_"))
    high_population = typology.loc[high, "population"].sum()
    latent_population = typology.loc[latent, "population"].sum()
    matched_population = high_population - latent_population

    fig, axes = plt.subplots(2, 2, figsize=(9.2, 6.3))
    axes[0, 0].barh(["High demand"], [matched_population], color="#58a17e", label="matched")
    axes[0, 0].barh(["High demand"], [latent_population], left=[matched_population], color="#ca756d", label="latent")
    axes[0, 0].set_xlabel("Population")
    axes[0, 0].set_title(f"Morphology typology: latent {latent_population/high_population:.1%}", loc="left", fontweight="bold")
    axes[0, 0].legend(frameon=False)

    cross = cross.sort_values("latent_share_within_high_demand_population")
    axes[0, 1].barh(cross["service_outcome"], 100 * cross["latent_share_within_high_demand_population"], color="#4a9492")
    axes[0, 1].set_xlabel("No local supply within high demand (%)")
    axes[0, 1].set_title("Cross-service 1 km benchmark", loc="left", fontweight="bold")

    focal = terms.loc[terms["model"].eq("base_serviceability_lpm")].copy()
    focal = focal.loc[focal["term"].isin(["z_human_medical", "z_parking", "z_nonmedical_pet"])]
    axes[1, 0].barh(focal["term"].str.replace("z_", "").str.replace("_", " "), focal["coef"], color="#6a9daa")
    axes[1, 0].set_xlabel("LPM coefficient")
    axes[1, 0].set_title("Serviceability filters", loc="left", fontweight="bold")

    bands = subway.loc[subway["year"].eq(2024)].copy()
    subway_band = bands["subway_band"].to_numpy()
    axes[1, 1].plot(
        subway_band,
        bands["pw_pet_medical_within_1000m"].to_numpy(),
        marker="o",
        label="all",
    )
    axes[1, 1].plot(
        subway_band,
        bands["pw_type_general_within_1000m"].to_numpy(),
        marker="o",
        label="general",
    )
    axes[1, 1].plot(
        subway_band,
        bands["pw_type_advanced_or_chain_within_1000m"].to_numpy(),
        marker="o",
        label="advanced/chain",
    )
    axes[1, 1].tick_params(axis="x", rotation=25)
    axes[1, 1].set_ylabel("Population-weighted 1 km exposure")
    axes[1, 1].set_title("Metro-distance bands", loc="left", fontweight="bold")
    axes[1, 1].legend(frameon=False)
    fig.tight_layout(h_pad=1.5, w_pad=1.4)
    save_figure(fig, "Figure_7_reproduced")


if __name__ == "__main__":
    main()
