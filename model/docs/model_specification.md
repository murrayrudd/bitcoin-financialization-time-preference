# Bitcoin financialization and effective time preference version 0.5

## Scope and interpretation

The core question is whether, and under which stated mechanisms, financialized Bitcoin arrangements produce a higher effective discount rate than engaged independent holding at matched exposure. Baseline psychological patience is common. The model compares stylized arrangements; it does not infer a worldview from holding duration, wallet size, or a visible transfer.

The sovereignty-first benchmark combines accumulation/holding, independent transfer authority, and engagement with monetary commitments and practical control. DCA and information gathering need not imply trading. Low leverage and diffuse strategic/custodial control are ideal-type commitments from the book; this model represents holder transfer authority but does not add an aggregate concentration index, debt market, or endogenous admissibility choice.

Mixed portfolios, entry into financialization, changes of worldview, wealth thresholds, and endogenous switching remain outside the core. A person may combine arrangements. Continued self-custody engagement could preserve understanding while that person also owns financial products. Pure-case comparisons do not identify whole-person or population effects.

## Activities and resource allocation

The holder chooses h >= 0 and n >= 0 subject to h+n <= B.

- h is substantive engagement that maintains practical competence and understanding of Bitcoin's monetary commitments. Technical, institutional, monetary, and relevant macroeconomic learning or discussion can contribute. Platform, reading frequency, ideological affirmation, and simple exposure to commentary are not sufficient classification rules.
- n is instrumental financial performance monitoring. It can be routine review without trading or pressure to adjust. The model chooses neither trades nor a trading propensity. Activities serving both purposes require content-based attribution; the same unit of time cannot be counted twice.
- Unused attention has outside value. The joint production of competence and understanding through h remains a simplifying assumption. A bounded joint-effort efficiency variant tests activity complementarity without counting time twice or allowing monitoring to directly replenish commitment.

Let s = 1+b >= 1 be normalized position value at risk. It is not a count of people adopting Bitcoin. It does not distinguish Bitcoin purchases from appreciation, nor measure the position's share of total wealth.

Practical payoff weight:
G(s) = m_G s_ref (s/s_ref)^alpha,
where s_ref = 2, m_G = 1 in the reference, and alpha is tested at 0, 0.5, and 1.

G(s_ref)=m_G s_ref for every alpha. This holds the practical payoff level constant at the matched comparison while changing its growth. Equality of alpha variants at that point is therefore normalization, not independent robustness evidence. Separate magnitude checks vary m_G at 0.5, 1, and 2. Proportional scaling alpha=1 reproduces version 0.3; alpha=0 is a zero-growth boundary. All are uncalibrated hypotheses about effective payoffs, not alternative arithmetic definitions of dollar loss.

Monitoring payoff:
Pi(s)=Pi_0+gamma s^epsilon.

The recurring net cost is:
J(h,n) = a log[(1+B)/(1+B-h-n)] + c_h h^2/2 + c_n n^2/2
       + G(s)L_o exp[-k_h h-k_p p]
       + G(s)(L_c+xL_x) exp[-k_c h]
       - Pi(s) log(1+n) - eta h n.

Here eta = zeta sqrt(c_h c_n), with 0 <= zeta < 1 and c_h including arrangement friction. The reference zeta=0 exactly nests version 0.4; zeta=0.5 and 0.9 test cost complementarity. The negative cross term reduces the cost of combining actual activities. It neither adds n directly to the commitment stock nor creates independent transfer rights. The total quadratic activity cost remains positive definite.

Here p is operational support, x is binary independent transfer authority, and an arrangement may multiply c_h by a positive friction factor. L_o concerns access/recovery/arrangement mistakes; L_c concerns interpretation mistakes; xL_x values readiness to exercise available rights. An early sale is not itself a mistake. Rate reduction is not in J. Fixed provider costs are conditioned on. Cross-arrangement objective values are not welfare comparisons because omitted constants and fixed costs differ.

Provider support may reduce operational burdens, but it does not reproduce independent transfer authority or add directly to the holder's commitment stock. Optional participatory education is zero in all reference cases.

## Optimality and comparative statics

The objective is strictly convex on the compact feasible triangle. Write S=1+B-h-n and C=a/S^2-eta. The quadratic cost Hessian [[c_h,-eta],[-eta,c_n]] is positive definite because eta^2<c_h c_n; all other objective curvature is positive semidefinite. Hence U>0, V>0, and Delta=UV-C^2>0, even when C<0. A unique solution can include zero activities or a binding resource budget. The solver profiles over n for each h and checks KKT conditions. Hyperbolic residual losses remain convex. Complete propositions and proofs are in propositions.md.

Let m be the marginal engagement benefit per unit of G, and let Pi_s denote dPi/ds. At an interior solution:
h_s = [V G'(s)m - C Pi_s/(1+n)]/Delta,
n_s = [U Pi_s/(1+n) - C G'(s)m]/Delta.

When h+n=B and both activities are positive:
h_s = [G'(s)m - Pi_s/(1+n)]/(U+V-2C),
n_s = -h_s.

Thus relative marginal incentives determine the sign. Faster-than-proportional monitoring growth is not necessary when practical engagement benefits grow subproportionally. With gamma=0 and G'(s)>=0, greater s weakly raises engagement; at alpha=0 the reference holding choices are flat. This is a within-arrangement comparative static, not a prediction about actual switching by wealthy holders.

At an interior solution, h_Pi=-C/[(1+n)Delta] and n_Pi=U/[(1+n)Delta]>0. Monitoring incentives displace h when C>0 but increase h when C<0. With a binding budget and both activities positive, h_Pi=-1/[(1+n)(U+V-2C)]<0. Usable authority raises h; operational support reduces its residual operational benefit. Their effects on n depend on the cross-curvature away from the budget boundary. Support adds pressure-buffer capacity only if d_p>0. None of these comparative statics establishes a change in psychological patience.

## Explicit temporal hypotheses

v = v_bar + nu + tau lambda n
D = d_h h + d_p p, with d_p >= 0
dot(A) = q(1+chi)h - (delta_A + xi v)A
A_star = q(1+chi)h/(delta_A + xi v)

lambda in [0,1] is the loading from financial monitoring into consequential updating/adjustment pressure. It is an arrangement input, not a trading frequency or a measured fraction of people. lambda=0 permits extensive financial review without added decision pressure. It does not eliminate ambient pressure v_bar or external obligations nu. Public macro discussion contributes to h only when substantive; it is not automatically mapped into v.

The conditional normalized effective rate is:
R = rho_effective/rho_0 = E(A_star) Z(v,D)
E(A) = 1 - kappa A/(K+A)
Z(v,D) = 1 + beta [v/(v_0+D)]^theta.

kappa in [0,1) is the assumed maximum commitment effect. Tested values are 0, 0.25, 0.5, and 0.75. The old 25%-of-baseline asymptote corresponds to kappa=0.75 and has no special empirical status. At kappa=0, A has no direct temporal-weighting effect. beta>=0 is the direct pressure-weighting strength.

Operational assistance enters the loss term through k_p p. Pressure buffering enters only through d_p p. Setting d_p=0 removes the latter while preserving the former; the choices h,n and maintained A are unchanged. Values from 0 to 10 are illustrative stress settings, not estimated or empirically plausible bounds.

These are hypotheses about effective temporal weighting, not derived consequences of the effort optimum. They do not estimate annual rates, required returns, liquidation hazards, or deep preferences. The model's benchmark capacity effect is favorable by construction; counterparties' operational failures, fees, and malfeasance are not represented.

Pressure has two paths: direct weighting through beta, and erosion of A through xi. Setting beta=0 removes only direct weighting. Removing both pressure paths requires beta=0 and xi=0. Setting kappa=beta=0 makes R=1 for all arrangements, while all activity choices remain unchanged.

At h=0, stationary A=0 regardless of p. An existing stock decays gradually. The analysis compares stationary arrangements and does not model portfolio switching or irreversible lock-in.

## Arrangement inputs

All cases have friction=1, epsilon=1, nu=0, chi=0. The following bundles are illustrative, not measured descriptions of products or people.

| Case | p | x | gamma | lambda |
|---|---:|---:|---:|---:|
| Engaged independent holding | 0 | 1 | 0 | 0 |
| Service with consequential monitoring | 1 | 0 | 0.8 | 1 |
| Delegation with routine review | 1 | 0 | 0 | 0 |
| Independent control with consequential monitoring | 0 | 1 | 0.8 | 1 |
| Independent holding with operational support | 1 | 1 | 0 | 0 |
| Service with monitoring but no added pressure | 1 | 0 | 0.8 | 0 |

Labels have no effect on the equations. The fourth case is a diagnostic of financial practices under independent control; it is not classified as the sovereignty-first ideal type and does not imply actual trading. A routine holder can have small positive n without frequent account checking or tactical decisions.

The matched reference retains version 0.4 values, including d_p=2.5, and sets zeta=0. These values provide continuity, not preferred calibration. The complete configuration is in results/configuration.json. There is no newly estimated parameter.

## Comparisons and limits

For financialized F and independent holding H:
R_F/R_H = (E_F/E_H)(Z_F/Z_H).

A lower A_F favors a higher R_F when kappa>0. A lower pressure/capacity ratio can offset that difference. The comparison is conditional on the temporal hypotheses; equal rates never imply equal exit rights.

The reference at s=2 retains kappa=0.75 and alpha=1 solely for an exact prior/current comparison. Matched level effects are primary. Stake slopes are secondary sensitivity results. The tested power scalings intersect at s=2 by construction. Changing kappa or lambda leaves chosen h and n unchanged because there is no rate feedback in J.

The experiment script exactly reproduces version 0.4 at zeta=0 and the previous support-buffer productivity. All six named arrangements are checked across 21 position values. The prior source module, delivered CSV and summary, and complete v0.4 package are preserved in previous/; that package retains the v0.3 checkpoint.

The factorial design crosses independent transfer authority, operational support, monitoring incentives, and monitoring-pressure loading. It compares all 16 combinations at three complementarity values, three commitment strengths, and three support-buffer productivities. Paired effects condition on the remaining factor values. Four-factor Shapley decompositions average each contribution over all 24 orders, allocating model interactions by convention. These are model attributions, not causal estimates from data.

The support and pressure sweeps locate ranking reversals. Complementarity paths vary instrumental monitoring incentives at budgets 1 and 3. The joint stress grid changes attention, complementarity, commitment strength, support buffering, pressure loading, benefit growth, and position value. Sixteen structural specifications cross residual-loss forms, pressure erosion, commitment functions, and bounded/unbounded pressure weighting. Counts describe the chosen grid only.

The retained 36-record Fieldguide ledger supplies theoretical analogies and measurement cautions. Version 0.5 adds no literature estimates or new empirical findings. Demonstrating a modeled rate difference does not identify a causal population effect of financialization. Transfers do not reveal total wealth, remaining self-custody, worldview, or a before/after change in patience.
