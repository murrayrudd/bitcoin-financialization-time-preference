"""Independent numerical checks of the targeted version 0.5 changes."""
from pathlib import Path
from dataclasses import replace
import sys,json,csv
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.model import *
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def record(name,passed,**details):
    checks.append(dict(name=name,passed=bool(passed),**details))
    if not passed:raise AssertionError(checks[-1])
def rows(name):
    with (ROOT/'results'/name).open() as f:return list(csv.DictReader(f))

def main():
    rng=np.random.default_rng(314159);t=Technology();arr=named_arrangements()
    max_obj=max_alloc=max_kkt=max_stake=max_reward=max_grad=max_hess=0.;mineig=1e9;regimes=set();count_s=count_r=negative_cross=0
    for j in range(160):
        a=Arrangement('Unlabeled',float(rng.uniform(0,3)),bool(j%2),float(rng.uniform(0,2)),
            float(rng.uniform(.3,3)),monitoring_elasticity=float(rng.uniform(0,3)),
            pressure_loading=0. if j%5==0 else float(rng.uniform(0,1)))
        tt=replace(t,budget=float(rng.uniform(.3,3)),opportunity_value=float(rng.uniform(.1,2)),
            activity_complementarity=[0.,.5,.9,.98][j%4],support_capacity_productivity=0. if j%3==0 else float(rng.uniform(0,10)),
            base_monitoring_reward=float(rng.uniform(.1,2)),exit_readiness_value=float(rng.uniform(0,1)),
            ambient_turnover=float(rng.uniform(.1,3)),benefit_elasticity=0. if j%4==0 else float(rng.uniform(0,1.5)),
            benefit_scale=float(rng.uniform(.3,2)),commitment_strength=float(rng.uniform(0,.95)),
            pressure_strength=0. if j%5==0 else float(rng.uniform(.2,2)))
        b=float(rng.uniform(.02,2));form=['exponential','hyperbolic'][j%2];pr=primitives(b,a,tt);r=evaluate(b,a,tt,form)
        opt=minimize(lambda x:derivatives(*x,pr,tt,form)[0],np.array([tt.budget*.25]*2),
            jac=lambda x:derivatives(*x,pr,tt,form)[1],method='SLSQP',bounds=[(0,tt.budget)]*2,
            constraints=[{'type':'ineq','fun':lambda x:tt.budget-x.sum(),'jac':lambda x:np.array([-1.,-1.])}],
            options={'ftol':1e-12,'maxiter':500})
        assert opt.success,opt.message
        max_obj=max(max_obj,abs(opt.fun-r['objective']));max_alloc=max(max_alloc,float(np.max(np.abs(opt.x-[r['h'],r['n']]))))
        max_kkt=max(max_kkt,r['kkt_residual']);mineig=min(mineig,r['minimum_hessian_eigenvalue'])
        negative_cross+=r['net_cross_curvature']<0
        assert min(r['h'],r['n'],r['unused_budget'])>=-1e-10
        ep=1e-5
        x=np.array([tt.budget*.22,tt.budget*.27]);obj,grad,H=derivatives(*x,pr,tt,form)
        for i in range(2):
            dx=np.eye(2)[i]*ep
            lo=derivatives(*(x-dx),pr,tt,form);hi=derivatives(*(x+dx),pr,tt,form)
            max_grad=max(max_grad,abs((hi[0]-lo[0])/(2*ep)-grad[i]))
            max_hess=max(max_hess,float(np.max(np.abs((hi[1]-lo[1])/(2*ep)-H[:,i]))))
        d=exposure_statics(b,a,tt,form);lo=evaluate(b-ep,a,tt,form);hi=evaluate(b+ep,a,tt,form)
        dlo=exposure_statics(b-ep,a,tt,form);dhi=exposure_statics(b+ep,a,tt,form);regimes.add(d['regime'])
        if not d['at_kink'] and dlo['regime']==dhi['regime']:
            for var,key in [('h','h_b'),('n','n_b'),('normalized_rate','rate_b')]:
                max_stake=max(max_stake,abs((hi[var]-lo[var])/(2*ep)-d[key]))
            count_s+=1
        tl=replace(tt,base_monitoring_reward=tt.base_monitoring_reward-ep)
        th=replace(tt,base_monitoring_reward=tt.base_monitoring_reward+ep)
        d=monitoring_statics(b,a,tt,form);lo=evaluate(b,a,tl,form);hi=evaluate(b,a,th,form)
        dl=monitoring_statics(b,a,tl,form);dh=monitoring_statics(b,a,th,form)
        if not d['monitoring_at_kink'] and dl['monitoring_regime']==dh['monitoring_regime']:
            for var,key in [('h','h_reward'),('n','n_reward')]:
                max_reward=max(max_reward,abs((hi[var]-lo[var])/(2*ep)-d[key]))
            count_r+=1
    record('Independent constrained optimizer including complementarity',max_obj<1e-8 and max_alloc<2e-5,
        scenarios=160,maximum_objective_error=max_obj,maximum_allocation_error=max_alloc)
    record('Feasibility and global optimality',max_kkt<1e-8 and mineig>0,
        maximum_kkt=max_kkt,minimum_hessian_eigenvalue=mineig,negative_cross_curvature_cases=int(negative_cross))
    record('Objective gradient and Hessian finite differences',max_grad<1e-6 and max_hess<1e-5,
        locations=160,maximum_gradient_error=max_grad,maximum_hessian_error=max_hess)
    record('Stake derivative agreement',max_stake<3e-6,comparisons=count_s,maximum_error=max_stake,regimes=sorted(regimes))
    record('Monitoring incentive derivative agreement',max_reward<3e-6,comparisons=count_r,maximum_error=max_reward)
    summary=json.loads((ROOT/'results/summary.json').read_text())
    record('Exact version 0.4 nesting',summary['legacy_maximum_error']<1e-12,
        scenarios=summary['legacy_reproduction_cases'],maximum_error=summary['legacy_maximum_error'])
    with (ROOT/'previous/named_endpoints_v04.csv').open() as f:prev=list(csv.DictReader(f))
    errs=[abs(float(r['normalized_rate'])-evaluate(float(r['b']),next(a for a in arr if a.name==r['name']),t)['normalized_rate']) for r in prev]
    record('Previously delivered CSV reproduced',max(errs)<1e-12,comparisons=len(errs),maximum_error=max(errs))
    # Inspect a genuine positive engagement response, not an ex post multiplier.
    ts=replace(t,budget=3.,activity_complementarity=.9);d=monitoring_statics(1.,arr[2],ts);r=evaluate(1.,arr[2],ts)
    record('Complementarity can raise engagement when attention is slack',d['h_reward']>0 and d['n_reward']>0 and r['unused_budget']>0 and r['net_cross_curvature']<0,
        h_reward=d['h_reward'],n_reward=d['n_reward'],unused_budget=r['unused_budget'])
    ts=replace(t,activity_complementarity=.9);d=monitoring_statics(1.,arr[1],ts)
    record('A binding budget retains the activity tradeoff',d['h_reward']<0 and abs(d['h_reward']+d['n_reward'])<1e-12,
        h_reward=d['h_reward'])
    tt=replace(t,support_capacity_productivity=0.);r=evaluate(1.,arr[1],tt);base=evaluate(1.,arr[1],t)
    pr=primitives(1.,arr[1],tt);no_support=replace(arr[1],operational_support=0.)
    op_with=pr['op_loss']*np.exp(-tt.engagement_response*r['h']-tt.support_response)
    op_without=pr['op_loss']*np.exp(-tt.engagement_response*r['h'])
    record('Zero buffering retains operational assistance',r['h']==base['h'] and r['n']==base['n'] and r['A']==base['A'] and op_with<op_without and r['D']==tt.holder_capacity_productivity*r['h'])
    max_kroot=max_dproot=max_affine=0.;nk=ndp=0
    for row in rows('commitment_boundaries.csv'):
        tt=replace(t,activity_complementarity=float(row['complementarity']),support_capacity_productivity=float(row['support_capacity_productivity']))
        a=next(a for a in arr if a.name==row['name'])
        for k in [0.,.2,.75,.98]:
            tk=replace(tt,commitment_strength=k)
            gap=evaluate(1.,a,tk)['normalized_rate']-evaluate(1.,arr[0],tk)['normalized_rate']
            max_affine=max(max_affine,abs(gap-(float(row['gap_intercept'])-k*float(row['gap_coefficient']))))
        if row['root_in_domain']=='True':
            tk=replace(tt,commitment_strength=float(row['commitment_root']))
            max_kroot=max(max_kroot,abs(evaluate(1.,a,tk)['normalized_rate']-evaluate(1.,arr[0],tk)['normalized_rate']));nk+=1
    record('Exact commitment ordering and crossing',max_affine<1e-12 and max_kroot<1e-10,
        affine_comparisons=4*len(rows('commitment_boundaries.csv')),roots=nk,maximum_affine_error=max_affine,maximum_root_error=max_kroot)
    for row in rows('support_capacity_boundaries.csv'):
        if row['root_in_domain']!='True':continue
        tt=replace(t,activity_complementarity=float(row['complementarity']),commitment_strength=float(row['commitment_strength']),
            support_capacity_productivity=float(row['support_capacity_root']))
        a=next(a for a in arr if a.name==row['name'])
        max_dproot=max(max_dproot,abs(evaluate(1.,a,tt)['normalized_rate']-evaluate(1.,arr[0],tt)['normalized_rate']));ndp+=1
    record('Exact support capacity crossing',max_dproot<1e-10,roots=ndp,maximum_error=max_dproot)
    shap=rows('four_factor_shapley.csv');errors=[]
    for z,k,dp in {(r['complementarity'],r['commitment_strength'],r['support_capacity_productivity']) for r in shap}:
        rr=[r for r in shap if (r['complementarity'],r['commitment_strength'],r['support_capacity_productivity'])==(z,k,dp)]
        errors.append(abs(sum(float(r['contribution']) for r in rr)-float(rr[0]['total_gap'])))
    record('Four factor attribution sums to the total gap',max(errors)<1e-12,decompositions=len(errors),maximum_error=max(errors))
    for z in [0.,.9]:
        tt=replace(t,activity_complementarity=z)
        x=evaluate(1.,arr[1],tt);y=evaluate(1.,replace(arr[1],pressure_loading=0.),tt)
        assert x['h']==y['h'] and x['n']==y['n'] and y['v']==t.ambient_turnover
        r=evaluate(1.,replace(arr[1],monitoring_incentive=10.,education_complement=100.),tt)
        assert r['h']==0 and r['A']==0 and r['D']>0
        for a in arr:
            r=evaluate(1.,a,replace(tt,commitment_strength=0.,pressure_strength=0.));original=evaluate(1.,a,tt)
            assert r['normalized_rate']==1. and r['h']==original['h'] and r['n']==original['n']
        tp=replace(tt,pressure_strength=0.,turnover_decay=0.)
        assert evaluate(1.,arr[1],tp)['normalized_rate']==evaluate(1.,replace(arr[1],pressure_loading=0.),tp)['normalized_rate']
    record('Pressure loading leaves choice unchanged',True)
    record('Support and joint efficiency do not create commitment without engagement',True)
    record('No temporal links gives the common baseline',True)
    record('Removing both pressure paths removes pressure effects',True)
    x=evaluate(1.,arr[1],t);y=evaluate(1.,replace(arr[1],name='Different worldview'),t)
    record('Arrangement names have no causal role',all(x[k]==y[k] for k in ['h','n','A','v','normalized_rate']))
    record('Stress grid satisfies optimality',summary['maximum_grid_kkt']<1e-8,maximum_kkt=summary['maximum_grid_kkt'],cases=summary['joint_grid']['cases'])
    out=dict(all_passed=all(r['passed'] for r in checks),check_count=len(checks),checks=checks)
    (ROOT/'results/verification.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
