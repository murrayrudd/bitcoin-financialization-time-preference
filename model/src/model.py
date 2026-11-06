"""Endogenous holder engagement and financial monitoring, version 0.5.

Strictly convex stationary allocation; conditional effective-rate mapping.
One holder, common baseline patience. Provider support is an arrangement input,
not a solved provider strategy. All resources and rates are normalized.
"""
from dataclasses import dataclass, asdict, replace
import numpy as np
from scipy.optimize import brentq


@dataclass(frozen=True)
class Technology:
    budget: float = 1.0
    opportunity_value: float = 1.0
    engagement_cost: float = 0.5
    monitoring_cost: float = 0.5
    operational_loss: float = 0.7
    interpretation_loss: float = 0.2
    exit_readiness_value: float = 0.6
    engagement_response: float = 2.0
    interpretation_response: float = 2.0
    support_response: float = 1.0
    base_monitoring_reward: float = 0.9
    holder_capacity_productivity: float = 2.5
    support_capacity_productivity: float = 2.5
    anchor_productivity: float = 1.5
    anchor_decay: float = 0.2
    turnover_decay: float = 0.1
    ambient_turnover: float = 0.5
    monitoring_turnover: float = 1.5
    commitment_strength: float = 0.75
    pressure_strength: float = 1.0
    benefit_elasticity: float = 1.0
    benefit_reference_stake: float = 2.0
    benefit_scale: float = 1.0
    anchor_scale: float = 1.0
    salience_offset: float = 0.5
    salience_power: float = 2.0
    salience_cap: float = 4.0
    activity_complementarity: float = 0.0

    def validate(self):
        positive=('budget','opportunity_value','engagement_cost','monitoring_cost',
                  'engagement_response','interpretation_response','support_response',
                  'holder_capacity_productivity',
                  'anchor_productivity','anchor_decay','anchor_scale','salience_offset',
                  'salience_power','salience_cap','benefit_reference_stake')
        for key in positive: assert getattr(self,key)>0, key
        for key in ('operational_loss','interpretation_loss','exit_readiness_value',
                    'base_monitoring_reward','turnover_decay','ambient_turnover',
                    'monitoring_turnover','pressure_strength','benefit_elasticity',
                    'benefit_scale','support_capacity_productivity'): assert getattr(self,key)>=0, key
        assert 0 <= self.commitment_strength < 1
        assert 0 <= self.activity_complementarity < 1


@dataclass(frozen=True)
class Arrangement:
    name: str = 'Engaged independent holding'
    operational_support: float = 0.0
    independent_transfer: bool = True
    monitoring_incentive: float = 0.0
    engagement_friction: float = 1.0
    compulsory_turnover: float = 0.0
    education_complement: float = 0.0
    monitoring_elasticity: float = 1.0
    pressure_loading: float = 0.0

    def validate(self):
        for key in ('operational_support','monitoring_incentive',
                    'compulsory_turnover','education_complement'):
            assert getattr(self,key)>=0,key
        assert self.engagement_friction>0
        assert self.monitoring_elasticity>=0
        assert 0<=self.pressure_loading<=1
        assert isinstance(self.independent_transfer,bool)


def primitives(b, arrangement, tech):
    assert b>=0
    arrangement.validate();tech.validate()
    s=1+b
    benefit=tech.benefit_scale*tech.benefit_reference_stake*(s/tech.benefit_reference_stake)**tech.benefit_elasticity
    benefit_derivative=tech.benefit_elasticity*benefit/s
    h_cost=tech.engagement_cost*arrangement.engagement_friction
    synergy=tech.activity_complementarity*np.sqrt(h_cost*tech.monitoring_cost)
    return dict(stake=s, benefit_weight=benefit, benefit_derivative=benefit_derivative,
                op_loss=benefit*tech.operational_loss,
                interpretation_loss=benefit*(tech.interpretation_loss+
                    int(arrangement.independent_transfer)*tech.exit_readiness_value),
                reward=tech.base_monitoring_reward+arrangement.monitoring_incentive*s**arrangement.monitoring_elasticity,
                support=arrangement.operational_support,
                h_cost=h_cost, joint_effort_benefit=synergy)


def response(x,form):
    """Residual loss fraction and first two derivatives with respect to x."""
    if form=='exponential':
        v=np.exp(-x);return v,-v,v
    if form=='hyperbolic':return 1/(1+x),-1/(1+x)**2,2/(1+x)**3
    raise ValueError(form)


def derivatives(h,n,pr,t,form='exponential'):
    S=1+t.budget-h-n
    assert S>0
    r,r1,r2=response(t.engagement_response*h+t.support_response*pr['support'],form)
    g,g1,g2=response(t.interpretation_response*h,form)
    a=t.opportunity_value
    obj=(a*np.log((1+t.budget)/S)+.5*pr['h_cost']*h*h+
         .5*t.monitoring_cost*n*n+pr['op_loss']*r+pr['interpretation_loss']*g-
         pr['reward']*np.log1p(n)-pr['joint_effort_benefit']*h*n)
    fh=a/S+pr['h_cost']*h+pr['op_loss']*t.engagement_response*r1+pr['interpretation_loss']*t.interpretation_response*g1-pr['joint_effort_benefit']*n
    fn=a/S+t.monitoring_cost*n-pr['reward']/(1+n)-pr['joint_effort_benefit']*h
    opportunity_cross=a/S**2
    cross=opportunity_cross-pr['joint_effort_benefit']
    hh=opportunity_cross+pr['h_cost']+pr['op_loss']*t.engagement_response**2*r2+pr['interpretation_loss']*t.interpretation_response**2*g2
    nn=opportunity_cross+t.monitoring_cost+pr['reward']/(1+n)**2
    return float(obj),np.array([fh,fn]),np.array([[hh,cross],[cross,nn]])


def _bounded_root(grad,upper):
    if upper<=0 or grad(0)>=0:return 0.
    if grad(upper)<=0:return float(upper)
    return float(brentq(grad,0,upper,xtol=1e-13,rtol=1e-14))


def choose(pr,t,form='exponential'):
    """Global minimum via a one-dimensional convex profile on the triangle.

    For each h, solve n in [0,B-h]. At the upper n boundary the profile
    derivative is C_h-C_n, since n falls one-for-one with h.
    """
    def n_at(h):
        return _bounded_root(lambda n:derivatives(h,n,pr,t,form)[1][1],t.budget-h)
    def profile_grad(h):
        n=n_at(h); f=derivatives(h,n,pr,t,form)[1]
        if n>=t.budget-h-1e-11 and f[1]<0:return f[0]-f[1]
        return f[0]
    h=_bounded_root(profile_grad,t.budget);n=n_at(h)
    obj,f,H=derivatives(h,n,pr,t,form)
    binding=h+n>=t.budget-1e-10
    pos=np.array([h,n])>1e-10
    lam=max(0.,float(np.mean(-f[pos]))) if binding else 0.
    adjusted=f+lam
    residual=max(float(np.max(np.abs(adjusted[pos]))) if pos.any() else 0.,
                 float(np.max(np.maximum(-adjusted[~pos],0))) if (~pos).any() else 0.,
                 abs(lam*(t.budget-h-n)))
    return h,n,obj,lam,residual,H


def multipliers(A,D,v,t,anchor_form='rational',salience_form='power',
                commitment_strength=None,pressure_strength=None):
    k=t.commitment_strength if commitment_strength is None else commitment_strength
    beta=t.pressure_strength if pressure_strength is None else pressure_strength
    assert 0<=k<1 and beta>=0
    x=A/t.anchor_scale
    if anchor_form=='rational':gain=x/(1+x)
    elif anchor_form=='exponential':gain=1-np.exp(-x)
    else:raise ValueError(anchor_form)
    E=1-k*gain
    y=(v/(t.salience_offset+D))**t.salience_power
    if salience_form=='power':pressure=y
    elif salience_form=='bounded':pressure=y/(1+y/t.salience_cap)
    else:raise ValueError(salience_form)
    return float(E),float(1+beta*pressure)


def evaluate(b,arrangement=Arrangement(),tech=Technology(),loss_form='exponential',
             anchor_form='rational',salience_form='power',commitment_strength=None,pressure_strength=None):
    pr=primitives(b,arrangement,tech)
    h,n,obj,lam,kkt,H=choose(pr,tech,loss_form)
    v=tech.ambient_turnover+arrangement.compulsory_turnover+tech.monitoring_turnover*arrangement.pressure_loading*n
    D=tech.holder_capacity_productivity*h+tech.support_capacity_productivity*pr['support']
    q=tech.anchor_productivity*(1+arrangement.education_complement)
    A=q*h/(tech.anchor_decay+tech.turnover_decay*v)
    E,Z=multipliers(A,D,v,tech,anchor_form,salience_form,commitment_strength,pressure_strength)
    return dict(name=arrangement.name,b=float(b),h=h,n=n,unused_budget=tech.budget-h-n,
                D=D,A=A,v=v,normalized_rate=E*Z,anchor_multiplier=E,salience_multiplier=Z,
                objective=obj,budget_shadow=lam,kkt_residual=kkt,
                minimum_hessian_eigenvalue=float(np.linalg.eigvalsh(H).min()),
                net_cross_curvature=float(H[0,1]),
                independent_transfer=arrangement.independent_transfer,
                pressure_loading=arrangement.pressure_loading,**pr)


def _rate_chain(r, hp, np_, a, t):
    """Derivative of the rational commitment / power pressure specification."""
    vp=t.monitoring_turnover*a.pressure_loading*np_
    Dp=t.holder_capacity_productivity*hp
    den=t.anchor_decay+t.turnover_decay*r['v']
    q=t.anchor_productivity*(1+a.education_complement)
    Ap=q*(hp*den-r['h']*t.turnover_decay*vp)/den**2
    Ea=-t.commitment_strength*t.anchor_scale/(t.anchor_scale+r['A'])**2
    anchor_log=Ea*Ap/r['anchor_multiplier']
    y=(r['v']/(t.salience_offset+r['D']))**t.salience_power
    pressure_log=(t.pressure_strength*t.salience_power*y/r['salience_multiplier']*
        (vp/r['v']-Dp/(t.salience_offset+r['D']))) if r['v']>0 else 0.
    return dict(A_b=float(Ap),D_b=float(Dp),v_b=float(vp),
                anchor_log_b=float(anchor_log),pressure_log_b=float(pressure_log),
                rate_b=float(r['normalized_rate']*(anchor_log+pressure_log)))


def _exposure_gradient(r, a, t, loss_form):
    _,ro1,_=response(t.engagement_response*r['h']+t.support_response*a.operational_support,loss_form)
    _,rg1,_=response(t.interpretation_response*r['h'],loss_form)
    m=-(t.operational_loss*t.engagement_response*ro1+
        (t.interpretation_loss+int(a.independent_transfer)*t.exit_readiness_value)*t.interpretation_response*rg1)
    engagement_growth=r['benefit_derivative']*m
    reward_growth=a.monitoring_incentive*a.monitoring_elasticity*r['stake']**(a.monitoring_elasticity-1)
    return np.array([-engagement_growth,-reward_growth/(1+r['n'])]),m,reward_growth


def comparative_statics(b,a=Arrangement(),t=Technology(),loss_form='exponential'):
    """Interior derivatives. None at an activity or budget boundary."""
    r=evaluate(b,a,t,loss_form);h,n=r['h'],r['n'];pr=primitives(b,a,t)
    if min(h,n,t.budget-h-n)<1e-8:return None
    H=derivatives(h,n,pr,t,loss_form)[2]
    _,_,ro2=response(t.engagement_response*h+t.support_response*a.operational_support,loss_form)
    _,rg1,_=response(t.interpretation_response*h,loss_form)
    Fx=np.array([t.exit_readiness_value*pr['benefit_weight']*t.interpretation_response*rg1,0.])
    Fp=np.array([pr['op_loss']*t.engagement_response*t.support_response*ro2,0.])
    FW=np.array([0.,-1/(1+n)])
    Fb,_,_=_exposure_gradient(r,a,t,loss_form)
    dx,dp,dW,db=[-np.linalg.solve(H,F) for F in [Fx,Fp,FW,Fb]]
    return dict(h_x=dx[0],n_x=dx[1],h_support=dp[0],n_support=dp[1],
                h_reward=dW[0],n_reward=dW[1],h_b=db[0],n_b=db[1],
                **_rate_chain(r,*db,a,t))


def monitoring_statics(b,a=Arrangement(),t=Technology(),loss_form='exponential'):
    """Derivative with respect to the total instrumental reward Pi.

    Piecewise exact away from KKT regime switches. This varies the reward,
    not the pressure loading and not the baseline psychological discount rate.
    """
    r=evaluate(b,a,t,loss_form);h,n=r['h'],r['n']
    _,f,H=derivatives(h,n,primitives(b,a,t),t,loss_form)
    positive=np.array([h,n])>1e-9
    binding=h+n>=t.budget-1e-9
    kink=False
    if binding:
        kink=r['budget_shadow']<1e-7
        if positive.all():
            hp=-1/((1+n)*(H[0,0]+H[1,1]-2*H[0,1]));np_=-hp
        else:hp=np_=0.
        regime='binding budget'
    elif positive.all():
        hp,np_=-np.linalg.solve(H,np.array([0.,-1/(1+n)]))
        regime='interior'
    else:
        hp=0.;np_=1/((1+n)*H[1,1]) if positive[1] else 0.
        regime='activity corner'
    for i in np.flatnonzero(~positive):
        kink=kink or abs(f[i]+r['budget_shadow'])<1e-7
    return dict(monitoring_regime=regime,monitoring_at_kink=bool(kink),
                h_reward=float(hp),n_reward=float(np_))


def commitment_boundary(financialized,holding,t=Technology(),anchor_form='rational'):
    """Exact gap intercept/slope because choices and states do not depend on kappa."""
    def g(r):
        x=r['A']/t.anchor_scale
        if anchor_form=='rational':return x/(1+x)
        if anchor_form=='exponential':return 1-np.exp(-x)
        raise ValueError(anchor_form)
    f,h=financialized,holding
    a0=f['salience_multiplier']-h['salience_multiplier']
    a1=g(f)*f['salience_multiplier']-g(h)*h['salience_multiplier']
    root=float(a0/a1) if abs(a1)>1e-14 else None
    return dict(gap_intercept=float(a0),gap_coefficient=float(a1),
                commitment_root=root,
                root_in_domain=bool(root is not None and 0<=root<1),
                gap_slope=float(-a1))


def support_boundary(financialized,holding,t=Technology()):
    """Exact d_p crossing for p_F=1, p_H=0 and the power pressure mapping.

    The supplied states must be computed at the same kappa, and h/n must not
    depend on d_p. A negative root lies outside the admissible d_p >= 0 domain.
    """
    f,h=financialized,holding
    assert f['support']==1 and h['support']==0
    E=f['anchor_multiplier'];target=h['normalized_rate']/E-1
    limit_gap=E-h['normalized_rate']
    root=None
    if target>0 and t.pressure_strength>0 and f['v']>0:
        root=float(f['v']*(t.pressure_strength/target)**(1/t.salience_power)
                   -t.salience_offset-t.holder_capacity_productivity*f['h'])
    return dict(support_capacity_root=root,
                root_in_domain=bool(root is not None and root>=0),
                infinite_capacity_gap=float(limit_gap))


def exposure_statics(b,a=Arrangement(),t=Technology(),loss_form='exponential'):
    """Piecewise derivative in a stable KKT regime, with switching points flagged."""
    r=evaluate(b,a,t,loss_form);h,n=r['h'],r['n'];pr=primitives(b,a,t)
    _,f,H=derivatives(h,n,pr,t,loss_form)
    Fb,m,Wp=_exposure_gradient(r,a,t,loss_form)
    positive=np.array([h,n])>1e-9
    binding=h+n>=t.budget-1e-9
    kink=False
    if binding:
        kink=r['budget_shadow']<1e-7
        if positive.all():
            hp=-(Fb[0]-Fb[1])/(H[0,0]+H[1,1]-2*H[0,1]);np_=-hp
        else:hp=np_=0.
        regime='binding budget'
    elif positive.all():
        hp,np_=-np.linalg.solve(H,Fb);regime='interior'
    else:
        d=np.zeros(2)
        for i in np.flatnonzero(positive):d[i]=-Fb[i]/H[i,i]
        hp,np_=d;regime='activity corner'
    for i in np.flatnonzero(~positive):
        kink=kink or abs(f[i]+r['budget_shadow'])<1e-7
    return dict(regime=regime,at_kink=bool(kink),h_b=float(hp),n_b=float(np_),
                marginal_engagement_benefit_per_weight=float(m),
                engagement_benefit_growth=float(-Fb[0]),reward_derivative=float(Wp),
                **_rate_chain(r,hp,np_,a,t))


def named_arrangements():
    """Stylized activity and control bundles; labels never enter equations.

    Holding allows low financial review without pressure to adjust. Financialized
    bundles include both consequential and nonconsequential monitoring cases.
    No trades, leverage, portfolio fractions, or worldview conversions are chosen.
    """
    return [Arrangement(),
            Arrangement('Service with consequential monitoring',1.,False,.8,pressure_loading=1.),
            Arrangement('Delegation with routine review',1.,False,0.,pressure_loading=0.),
            Arrangement('Independent control with consequential monitoring',0.,True,.8,pressure_loading=1.),
            Arrangement('Independent holding with operational support',1.,True,0.,pressure_loading=0.),
            Arrangement('Service with monitoring but no added pressure',1.,False,.8,pressure_loading=0.)]
