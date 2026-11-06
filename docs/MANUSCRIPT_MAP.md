# Manuscript to output map

This map refers to manuscript draft v04, November 5, 2026. Numerical paths below are relative to model/results/.

| Manuscript item | Source |
| --- | --- |
| Figure 1: institutional mechanisms | model/docs/model_specification.md; diagram in publication/make_figures.py |
| Figure 2: four contributions and total | four_factor_shapley.csv; complementarity 0, commitment strength 0.75, support productivity 2.5 |
| Figure 3: pressure relief | support_capacity_sweep.csv; complementarity 0, commitment strengths 0 and 0.75 |
| Figure 4: complementarity | complementarity_paths.csv; budgets 1 and 3, complementarities 0, 0.5, 0.9 |
| Six reference arrangements | named_endpoints.csv; complementarity 0, commitment strength 0.75, support productivity 2.5 |
| Factorial and paired features | institutional_factorial.csv; paired_factor_effects.csv; factor_effect_summary.csv |
| Exact reversals | commitment_boundaries.csv; support_capacity_boundaries.csv |
| Structural and joint stress comparisons | structural_variants.csv; joint_stress_grid.csv |
| Position sensitivity | stake_scaling_paths.csv |
| Temporal-link removals | temporal_link_removals.csv |
| Appendix A: analytical results | model/docs/propositions.md; model/src/model.py |
| Appendix B: parameters and experiments | configuration.json; model/run_experiments.py |

The three publication/data/ CSVs are exact copies of their model/results/ counterparts.
