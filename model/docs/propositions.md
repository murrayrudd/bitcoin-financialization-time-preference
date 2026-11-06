# Analytical conditions for the Bitcoin institutional comparison

Version 0.5, October 30, 2026. These are conditional model results. The maintained mappings from commitment and pressure into effective temporal weighting are assumptions, not independently derived psychological laws.

## Notation

The objective and all variables are defined in model_specification.md. Let S=1+B-h-n, eta=zeta sqrt(c_h c_n), and let the objective Hessian have entries U=J_hh, V=J_nn, C=J_hn=a/S^2-eta. Write Delta=UV-C^2. Subscripts on choices denote derivatives. Pi denotes the total instrumental monitoring reward, not baseline patience. All statements compare the same holder and common primitives except the named intervention. In calculus arguments, x can be continuously interpolated between its binary endpoints; that mathematical device does not introduce fractional custody into the model.

## Proposition 1 Existence and uniqueness with activity complementarity

For 0<=zeta<1, strictly positive own activity costs, and the other admissible parameters, the allocation problem has one global optimum on h,n>=0, h+n<=B.

Proof. The feasible triangle is nonempty and compact. S>=1 there, so the objective is continuous. Its quadratic activity-cost matrix is [[c_h,-eta],[-eta,c_n]], whose leading principal minors are c_h>0 and c_h c_n-eta^2=c_h c_n(1-zeta^2)>0. It is positive definite. The opportunity-cost Hessian is (a/S^2) times the positive semidefinite all-ones matrix. Both exponential residual losses are convex in their affine arguments, and -Pi log(1+n) is convex for Pi>=0. Hyperbolic residual losses have the same convexity property. Summing these terms gives a strictly positive definite Hessian. Thus a minimizer exists and is unique. The bound excludes zeta=1; no claim about uniqueness at or beyond that boundary is needed.

The joint term lowers the cost of combining actual h and n, but total quadratic activity cost remains positive. It changes optimal choices, not just the rate formula. It neither counts the same attention unit twice nor allows n or provider support to replenish A directly.

## Proposition 2 Monitoring incentives can crowd out or support engagement

At an interior optimum:

h_Pi = -C / [(1+n) Delta],
n_Pi = U / [(1+n) Delta] > 0.

Consequently, monitoring rewards reduce engagement if C>0, leave it unchanged to first order if C=0, and raise it if C<0. Negative C is possible under complementarity when eta>a/S^2. More available attention alone is insufficient; complementarity must exceed the opportunity-cost cross-curvature.

Proof. Differentiate the two first-order conditions. Their direct derivative with respect to Pi is (0,-1/(1+n)). Multiplication by the negative inverse Hessian gives the stated formulas.

At a binding attention budget with both activities positive:

h_Pi = -1 / [(1+n)(U+V-2C)] < 0,
n_Pi = -h_Pi > 0.

Proof. Substitute n=B-h. The derivative of the tangential first-order condition J_h-J_n=0 yields the formula; the denominator is positive by strict convexity. At strict activity corners the corresponding derivatives can be zero. Derivatives need not exist at regime switches, which the code flags. Thus complementarity can reverse local crowding out with slack attention, but cannot eliminate the hard resource tradeoff on a binding budget.

## Proposition 3 Conditional institutional dominance without provider buffering

Consider the core zeta=0, common costs and practical-benefit function, d_p=0, equal education and compulsory-pressure inputs, and two arrangements such that x_F<=x_H, p_F>=p_H, Pi_F>=Pi_H, and lambda_F>=lambda_H. Then h_F<=h_H and n_F>=n_H. It follows that A_F<=A_H, D_F<=D_H, v_F>=v_H, and R_F>=R_H under the stated nonnegative temporal coefficients.

Proof. With zeta=0, C>0. Increasing Pi weakly reduces h and increases n, including by continuity through boundaries. At an interior solution, a reduction in x adds a nonnegative amount to J_h, and an increase in p does likewise because it reduces the marginal engagement benefit of addressing operational loss. Neither intervention enters J_n directly. Multiplication by the inverse Hessian therefore reduces h and increases n. On the binding budget the changes have the same signs; at activity corners they become weak. A sequence of these interventions establishes the finite comparison. Since lambda and n are nonnegative and weakly higher in F, v is weakly higher. With d_p=0, D tracks h. The stationary stock is increasing in h and nonincreasing in v. The commitment multiplier is nonincreasing in A, and the pressure multiplier is nondecreasing in v/(v_0+D). Hence both rate components weakly favor a higher F rate.

Strict rate inequality requires an actual state difference transmitted by an active temporal link. With kappa=beta=0 all rates are equal. The result does not depend on whether a particular arrangement is labeled financialized or on a different intrinsic discount rate. It depends on the specified control, payoff, activity, and temporal assumptions. Provider support still lowers operational loss at d_p=0; its practical benefit is separate from any effect on effective temporal weighting.

This proposition does not extend automatically to positive buffering, negative cross-curvature, different education/productivity, or altered common costs. The factorial and complementarity experiments identify these boundaries. It also does not claim a welfare ordering: omitted fixed costs and counterparty risks preclude cross-arrangement welfare comparisons.

## Proposition 4 General rate ordering

Let E_i=1-kappa g(A_i)>0 and Z_i=1+beta f(y_i)>0, where g and f are nondecreasing and y_i=v_i/(v_0+D_i). Then:

log(R_F/R_H) = log(E_F/E_H) + log(Z_F/Z_H).

If A_F<=A_H and y_F>=y_H, R_F>=R_H. Reverse both state inequalities to reverse the rate ordering. With opposing state effects, F has the higher rate precisely when the positive log component exceeds the absolute value of the negative component. Equality occurs when the components cancel. Strictness requires an active link and a strict state effect.

Proof. Substitute R_i=E_i Z_i and use positivity and monotonicity. This condition holds for both the rational and exponential commitment forms and for both the power and bounded pressure forms. It is a decomposition of the assumed temporal mapping; Proposition 3 adds conditions under which the choice problem generates the requisite state ordering.

## Proposition 5 Exact commitment-strength boundary

Holding arrangements and all other primitives fixed, choices, A, and Z do not depend on kappa because the temporal mapping is downstream of the allocation objective. Define:

a_0=Z_F-Z_H,
a_1=g(A_F)Z_F-g(A_H)Z_H.

Then R_F-R_H=a_0-kappa a_1. If a_1 is nonzero, equality occurs at kappa_star=a_0/a_1. For a_1>0, F is higher when kappa<kappa_star; for a_1<0, F is higher when kappa>kappa_star. Only roots in 0<=kappa<1 describe admissible reversals. If a_1=0, the sign is constant and equals the sign of a_0, including equality everywhere when both vanish.

Proof. Expand (1-kappa g_F)Z_F-(1-kappa g_H)Z_H. No numerical root finder is needed. Reported roots are nevertheless checked against evaluated rates. Their values are normalized sensitivity boundaries, not estimates of individual preferences.

## Proposition 6 Exact support-buffer boundary

Separate operational assistance k_p p from buffer productivity d_p. Because d_p does not enter the allocation objective or the commitment equation, varying d_p leaves h,n,A,v unchanged. For p_F=1,p_H=0 under power pressure weighting, write E_F=1-kappa g(A_F). The F rate falls monotonically with d_p when beta>0 and v_F>0 and converges to E_F as d_p tends to infinity.

If R_H>E_F, the algebraic equality point is:

d_p_star = v_F [beta/(R_H/E_F-1)]^(1/theta) - v_0 - d_h h_F.

A nonnegative root is an admissible crossing; F is higher below it and lower above it. A negative root means F is already lower for all admissible d_p. If R_H<E_F, no amount of buffering can reverse the rate comparison. If R_H=E_F, equality is approached only in the infinite-buffer limit when beta and v_F are positive. With beta=0 or v_F=0 there is no buffer effect on R_F and the rates must be compared directly.

At kappa=0 and positive beta, the ordering reduces to the pressure/capacity ratios. For general supports:

R_F>R_H iff v_F(v_0+d_h h_H+d_p p_H)>v_H(v_0+d_h h_F+d_p p_F).

For p_F=1,p_H=0 and v_H>0:

d_p_star = [v_F(v_0+d_h h_H)-v_H(v_0+d_h h_F)]/v_H.

These formulas do not validate a provider's capacity to buffer pressure. They make the unsupported magnitude assumption inspectable, including the zero-benefit boundary. Equal or lower rates never imply equal rights, equal exit options, or equal understanding.

## Proposition 7 Stake slopes depend on relative marginal incentives

Let m be the marginal practical engagement benefit per unit of G, with Pi_s the derivative of monitoring rewards. At an interior solution:

h_s=[V G'(s)m-C Pi_s/(1+n)]/Delta,
n_s=[U Pi_s/(1+n)-C G'(s)m]/Delta.

At a binding budget with both activities positive:

h_s=[G'(s)m-Pi_s/(1+n)]/(U+V-2C), n_s=-h_s.

Proof. Differentiate the first-order or tangential condition, using direct gradient changes (-G'm,-Pi_s/(1+n)). The complementarity parameter does not vary with stake in these experiments. When C<0 and both marginal rewards grow, both activities can increase at an interior solution. At a binding budget, relative marginal rewards determine the allocation direction. The observed rate slope also includes pressure and commitment effects and is computed by the chain rule.

These are within-arrangement comparative statics. They do not explain wealthy holders' selection into services, disclose total holdings, or identify a switch in worldview. All benefit-elasticity variants meet at s=2 by normalization; matching at that point is not an independent robustness finding.
