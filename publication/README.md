# Bitcoin financialization figure originals

These four figures accompany draft v04 of *Bitcoin financialization and effective time preference* by Murray A. Rudd.

## Formats

- **PNG:** 600 dpi, white background, approximately 4,000 pixels wide. These are the files embedded in the updated Word manuscript.
- **SVG:** vector graphics with fonts converted to outlines, so lettering remains consistent when resized or opened on another computer.
- **PDF:** vector graphics with embedded fonts, suitable for publication and printing.

Use these originals directly when inserting figures into another document. The SVG and PDF files retain vector detail at larger sizes; the PNG files provide a high resolution raster alternative.

| Figure | Subject | Saved data source |
| --- | --- | --- |
| 1 | Institutional pathways and model sequence | Model equations and manuscript definitions |
| 2 | Contributions of four institutional features | four_factor_shapley.csv |
| 3 | Provider pressure relief and the rate comparison | support_capacity_sweep.csv |
| 4 | Complementarity and attention availability | complementarity_paths.csv |

The plots use conventional scientific axes, inward ticks, thinner lines, mathematical notation, and distinct line patterns. Figure 1 uses plain unshaded boxes and arrows. Figure 2 uses a monochrome point-and-stem plot with signed values and a separate total row. Open circles show the four contributions and a solid diamond shows their sum. Horizontal lines connect each value to zero; they are not uncertainty intervals. The negative operational-support contribution lies to the left of the zero line. No color or hatching is needed to interpret the figure.

## Reproduction

The `data` folder contains unchanged saved outputs from model version 0.5. The script `make_figures.py` reads those files and produces all twelve graphics files. It does not execute or modify the model.

Install the packages in `requirements.txt`, then run:

```bash
python make_figures.py

# Regenerate Figure 2 alone:
python make_figures.py --figure 2
```

The `figure_manifest.json` file records source and output hashes. The effective rates, decomposition values, parameter settings, and plotted data are unchanged.
