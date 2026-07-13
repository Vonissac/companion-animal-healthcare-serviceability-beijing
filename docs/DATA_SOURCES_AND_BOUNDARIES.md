# Data Sources and Boundaries

## Shared derived data

The repository provides derived analytical data used in the manuscript:

- 1 km grid-year indicators for Beijing, 2018-2024;
- population-weighted service-exposure indicators;
- child-oriented, human medical, companion-animal healthcare and other service exposure measures;
- 2024 morphology and serviceability indicators;
- model summaries and table-level evidence files;
- figure-input tables used to support visual verification.
- submitted Figure 1-7 PDFs and reproducible data-panel scripts.

## Restricted source data

The raw data layer is not redistributed. It includes commercial or platform-derived point-of-interest data, housing transaction records, raw building footprint data and other source files with redistribution limits.

The analytical files in `data/derived/` were created from those sources after aggregation, transformation and removal of source-file paths or local processing fields. The package is therefore intended to reproduce and verify the article from the derived research layer, not to rebuild the complete raw-data pipeline.

## Spatial unit

The spatial frame contains 16,992 projected 1 km cells covering Beijing. Population-weighted, morphology-quintile and model analyses use the 12,236 cells with positive estimated population in 2024. Empty-population cells remain in the shared spatial files so that maps preserve the full city frame; they are not silently treated as populated observations.

## High-demand denominators

Two related high-demand summaries have distinct scopes. The cross-radius 1 km benchmark is calculated from the radius-specific demand construct and contains 17,650,625 residents; its latent share is 34.9%. The final exact-morphology typology contains 17,613,546 residents; its matched and latent shares are 65.3% and 34.7%. These values should not be interchanged because the classification stages and denominators differ.

## Figure production boundary

Figure 1 is a manually composed conceptual schematic. Figures 2 and 4 combine reproducible map and chart panels using publication-layout cropping or manual composition. Figures 3 and 5-7 are data-driven. Public scripts reproduce the analytical values and panel data; exact typography and final panel placement are publication-design operations.

## Missing values

Absence of nearby service exposure is encoded as zero where a count or exposure measure is defined. Missing values are preserved where a variable is not applicable or where a calculation cannot be made from the derived layer.
