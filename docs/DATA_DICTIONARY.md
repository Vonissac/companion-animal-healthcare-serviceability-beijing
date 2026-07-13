# Data Dictionary

## Grid data

`data/derived/grids/beijing_grid_year_panel_2018_2024_enhanced.parquet` contains 16,992 grid cells for each year from 2018 to 2024. It includes population, district, centre distance, ring zone, service exposure at 500 m, 1 km and 2 km, housing, pet-service, comparison-service, road and mobility indicators.

`data/derived/grids/beijing_grid_2024_spatial_morphology_patterns.parquet` retains the full 16,992-cell spatial frame. Demand and morphology quintiles and the inferential analyses use the 12,236 cells with positive estimated population. The final grouping uses `morphology_composite_index_exact`.

## Main tables

`data/derived/tables/main_text/` contains exactly six manuscript tables:

1. service expansion and exposure benchmarks;
2. demand-signal validation and stability;
3. construct separation and reduced-predictor robustness;
4. exact-GIS high-demand morphology conversion;
5. mismatch typology and five Moran diagnostics;
6. predictive, service-ecology and mobility diagnostics.

`data/derived/tables/supplementary/` contains Table S1 on GIS construction robustness and Table S2 on morphology regime profiles.

## Figure inputs

`data/derived/tables/figure_inputs/` contains machine-readable inputs for Figures 2-7. Important mappings include:

- Figure 2: exact morphology, nighttime lights, demand, serviceability, latent-gap and clinic-type fields in the 2024 grid files;
- Figure 3: `table_post_fertility_service_exposure_contrast.csv` and related trajectory summaries;
- Figure 4: yearly metrics, ring summaries and `table_district_nonexposure_ranking_2024.csv`;
- Figure 5: construct variants, cut-off stability, specificity and radius benchmarks;
- Figure 6: morphology profiles, demand-by-morphology matrix, exact conversion, typology, Moran tests and GIS sensitivity;
- Figure 7: serviceability model terms, cross-service mismatch, serviceability quintiles, subway bands, spillovers and clinic-type supply.

## High-demand denominators

The radius-specific 1 km benchmark contains 17,650,625 residents and 6,151,302 latent residents, producing a 34.9% gap. The final exact-morphology typology contains 17,613,546 high-demand residents and 6,117,945 latent residents, producing a 34.7% gap. They are not interchangeable.

## Missing and displayed values

Zero denotes a defined absence of nearby service exposure. Missing values remain missing when a calculation is not applicable. Manuscript display rules are one decimal place for percentages, two decimals for population in millions, three decimals for Moran's I and two or three decimals for other indices as required by the evidence table.
