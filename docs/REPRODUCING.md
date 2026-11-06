# Reproduction

Run commands from the repository root using Python 3.12.14 and requirements.txt.

| Command | Purpose |
| --- | --- |
| python scripts/verify_package.py | Check every distributed research file against SHA-256 digests |
| python scripts/reproduce.py | Run 19 substantive numerical checks in a temporary copy |
| python scripts/reproduce.py --full | Regenerate experiments, compare every result CSV, and run numerical checks |
| python scripts/reproduce.py --full --figures | Also rebuild publication graphics using regenerated results |
| python publication/make_figures.py | Save all publication figures in place from supplied plotting CSVs |
| python publication/make_figures.py --figure 2 | Save only the monochrome Figure 2 in place |

The wrapper leaves distributed files unchanged, removes its temporary copy, prints a JSON report, and exits unsuccessfully if a check fails. Numerical comparisons use relative tolerance 1e-9 and absolute tolerance 1e-11. Text columns and row/column identities must match. Figure metadata and rendering can vary across environments; graphics are checked for successful reconstruction, not pixel identity.

The original model/run_experiments.py writes results and development figures within model/. Its graphics precede the manuscript's final figure design; use publication/ for manuscript figures.

The implementation uses position increment b; the manuscript uses normalized position s = 1 + b. Reference b = 1 therefore means s = 2.
