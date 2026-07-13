# Companion-Animal Healthcare Serviceability in Beijing

This repository provides the data and code supporting the manuscript:

**When Companion-Animal Healthcare Becomes Locally Serviceable: Urban Morphology and Supply-Exposure Mismatch in Beijing**

The package begins from the shared derived analytical layer. It reproduces the article's reported values, six main tables, two supplementary evidence tables, map layers and data-driven figure panels. Restricted raw point-of-interest, housing transaction, building footprint and platform data are not redistributed.

## Repository structure

```text
code/                         Package checks and table reproduction
code/figures/                 Figure-input and data-panel reproduction
data/derived/grids/           Grid-year and 2024 analytical indicators
data/derived/maps/            Derived spatial layers
data/derived/models/          Reported model summaries
data/derived/tables/          Main, supplementary and figure-input tables
outputs/publication_figures/  Submitted Figure 1-7 PDFs
outputs/reproduced/           Outputs created by the public scripts
docs/                         Data dictionary and source boundaries
MANIFEST.csv                  File-level sizes and SHA-256 checksums
```

## Reproducibility boundary

The public package reproduces the analysis from derived, de-identified grid and table data. Figure 1 is a manually composed schematic based on validated analytical outputs. Figures 2 and 4 use publication-layout cropping or manual panel composition after reproducible map and chart panels are generated. Manual layout changes presentation only; it does not alter the underlying values.

The two high-demand summaries have distinct scopes:

- the cross-radius benchmark uses 17.65 million residents and reports a 34.9% 1 km pet-medical gap;
- the exact-morphology typology uses 17.61 million residents and reports 6.12 million latent residents, or 34.7%.

The checks keep these denominators separate.

## Quick start

Use Python 3.10 or newer:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Validate files, checksums, analytical denominators and reported values:

```bash
python code/check_reproducibility.py
```

Reproduce the six main tables:

```bash
python code/reproduce_tables.py
```

Build the district-level figure input and reproduce the data-driven panels:

```bash
python code/figures/build_figure_inputs.py
python code/figures/reproduce_figure_2.py
python code/figures/reproduce_figure_3.py
python code/figures/reproduce_figure_4_panels.py
python code/figures/reproduce_figure_5.py
python code/figures/reproduce_figure_6.py
python code/figures/reproduce_figure_7.py
```

Simplified diagnostic figures remain available as a lightweight check:

```bash
python code/reproduce_verification_figures.py
```

## Tables and figures

`data/derived/tables/main_text/` contains exactly Table 1-6. Earlier morphology-construction and regime-profile evidence is retained as Table S1-S2 in `data/derived/tables/supplementary/`. The submitted PDFs are stored in `outputs/publication_figures/`; reconstructed data panels are written to `outputs/reproduced/figures/`.

## Citation

Please cite the associated article once bibliographic details are available.

## License

Code is released under the MIT License. Derived data are provided under `LICENSE-DATA.md`, subject to the source restrictions described in `docs/DATA_SOURCES_AND_BOUNDARIES.md`.
