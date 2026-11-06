# Version 0.5 output map

All results are deterministic, normalized, and uncalibrated. The configuration describes the exact settings. A positive rate_difference means a higher service or changed-arrangement rate than the stated independent-holding reference or paired baseline. R=1 is the common baseline psychological rate, not one percent or one annual unit.

| File | Content |
|---|---|
| legacy_reproduction.csv | 126 exact comparisons with v0.4 over six arrangements and 21 position values |
| named_endpoints.csv | Six named arrangements at s=2, crossed with three complementarities, four commitment strengths, and three support-buffer productivities |
| institutional_factorial.csv | All 16 binary factor combinations at 27 common technology settings, 432 rows |
| paired_factor_effects.csv | 864 one-factor changes conditioning on the other factors |
| factor_effect_summary.csv | Mean, range, and sign counts of the eight paired effects per factor and technology setting |
| four_factor_shapley.csv | 27 four-factor decompositions; each contribution averages all 24 intervention orders |
| support_capacity_sweep.csv | Service, routine-delegation, and service-without-pressure comparisons as buffer productivity varies from 0 to 10 |
| support_capacity_boundaries.csv | Exact d_p roots under the power pressure function; a blank root means the formula has no finite crossing under the stated conditions |
| commitment_boundaries.csv | Exact affine gap coefficients and kappa roots; roots outside the admissible domain are retained and explicitly flagged |
| pressure_loading_sweep.csv | Monitoring pressure loading from 0 to 1 at the matched exposure |
| complementarity_paths.csv | Actual allocation responses to monitoring incentives at budgets 1 and 3 and three complementarities |
| complementarity_examples.csv | Local reward derivatives and states at zero additional monitoring incentive |
| structural_variants.csv | Sixteen functional specifications at eight common parameter settings and three service arrangements, 384 rows |
| joint_stress_grid.csv | 648 combinations of budget, complementarity, commitment strength, buffer productivity, loading, benefit growth, and exposure |
| stake_scaling_paths.csv | Within-arrangement stake paths, KKT regimes, and analytical rate/choice derivatives |
| temporal_link_removals.csv | Separate removals of commitment weighting, direct pressure weighting, and pressure-induced commitment erosion |
| summary.json | Computed report summaries and comparison boundaries |
| verification.json | All numerical verification results and tolerances |

The four factorial bits specify loss of transfer authority, operational support, added monitoring incentive, and pressure loading. The reference endpoint has bits 0000; the consequential service endpoint has 1111. Incentive bit 1 means gamma=0.8, not a rate or an observed frequency. Labels do not affect calculations.

Complementarity zeta measures joint effort efficiency, bounded below one. It is not a measured fraction of activities performed jointly. Provider d_p measures buffer productivity; it does not control operational assistance, which remains in the loss function through a separate coefficient. The reference d_p column in a boundary table identifies the comparison setup; support_capacity_root is the derived threshold, not an estimated value.

The joint stress grid tests kappa=0 and 0.75. Its lack of reversals at 0.75 must not be read as a theorem about every positive kappa. The separate capacity analysis includes a routine-delegation reversal at kappa=0.25 with strong complementarity.
