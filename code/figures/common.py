from pathlib import Path

import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/derived"
TABLES = DATA / "tables/figure_inputs"
OUT = ROOT / "outputs/reproduced/figures"

DISTRICT_NAMES = {
    "东城区": "Dongcheng",
    "西城区": "Xicheng",
    "朝阳区": "Chaoyang",
    "丰台区": "Fengtai",
    "石景山区": "Shijingshan",
    "海淀区": "Haidian",
    "门头沟区": "Mentougou",
    "房山区": "Fangshan",
    "通州区": "Tongzhou",
    "顺义区": "Shunyi",
    "昌平区": "Changping",
    "大兴区": "Daxing",
    "怀柔区": "Huairou",
    "平谷区": "Pinggu",
    "密云区": "Miyun",
    "延庆区": "Yanqing",
}


def setup_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8,
            "axes.titlesize": 9,
            "axes.labelsize": 8,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "pdf.fonttype": 42,
        }
    )


def load_spatial() -> gpd.GeoDataFrame:
    grid_frame = pd.read_parquet(DATA / "maps/beijing_grid_1km_metric.parquet")
    geometry = gpd.GeoSeries.from_wkb(grid_frame.pop("geometry"), crs="EPSG:32650")
    grid = gpd.GeoDataFrame(grid_frame, geometry=geometry, crs=geometry.crs)
    values = pd.read_parquet(
        DATA / "grids/beijing_grid_2024_spatial_morphology_patterns.parquet"
    )
    overlap = [column for column in grid.columns if column != "grid_id"]
    return grid.merge(values.drop(columns=overlap, errors="ignore"), on="grid_id")


def save_figure(fig: mpl.figure.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", dpi=240, bbox_inches="tight")
    plt.close(fig)


def clean_map(ax: mpl.axes.Axes) -> None:
    ax.set_axis_off()
    ax.set_aspect("equal")
