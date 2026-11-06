"""Final targeted institutional comparisons, version 0.5. No calibration."""
from pathlib import Path
from dataclasses import asdict, replace
from itertools import product, permutations
import importlib.util, sys, json, csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.model import *

ROOT=Path(__file__).resolve().parent
RESULTS=ROOT/'results';FIGS=ROOT/'figures'
RESULTS.mkdir(exist_ok=True);FIGS.mkdir(exist_ok=True)

def csvout(name,rows):
    with (RESULTS/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def count(rows):
    return dict(cases=len(rows),higher=sum(r['rate_difference']>1e-10 for r in rows),
        lower=sum(r['rate_difference']< -1e-10 for r in rows),equal=sum(abs(r['rate_difference'])<=1e-10 for r in rows))

def tag(t):
    return dict(complementarity=t.activity_complementarity,commitment_strength=t.commitment_strength,
                support_capacity_productivity=t.support_capacity_productivity)

def factorial_arr(bits):
    loss,support,incentive,loading=bits
    return Arrangement('Factorial arrangement',float(support),not bool(loss),.8*incentive,pressure_loading=float(loading))

def legacy_module():
    spec=importlib.util.spec_from_file_location('legacy_v04',ROOT/'previous'/'model_v04.py')
    mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
    return mod

def run():
    t=Technology();arr=named_arrangements();old=legacy_module();ot=old.Technology()
    cfg=dict(version='0.5',review_date='2026-10-30',technology=asdict(t),arrangements=[asdict(a) for a in arr],
        commitment_strengths=[0,.25,.5,.75],complementarities=[0,.5,.9],support_capacity_values=[0,2.5,10],
        factorial_factors={'control_loss':[0,1],'operational_support':[0,1],'monitoring_incentive':[0,.8],'pressure_loading':[0,1]},
        support_sweep=[0,10,.1],reference_stake=2.,
        interpretation='Uncalibrated normalized scenarios. Stress ranges are not empirically plausible bounds; counts are not probabilities.')
    (RESULTS/'configuration.json').write_text(json.dumps(cfg,indent=2))
    legacy=[]
    for oa,na in zip(old.named_arrangements(),arr):
        for b in np.linspace(0,2,21):
            before=old.evaluate(float(b),oa,ot);after=evaluate(float(b),na,t)
            err=max(abs(before[k]-after[k]) for k in ['h','n','A','D','v','normalized_rate','objective'])
            legacy.append(dict(name=oa.name,b=float(b),maximum_error=err))
    csvout('legacy_reproduction.csv',legacy)
    named=[]
    for z,k,dp in product([0.,.5,.9],[0.,.25,.5,.75],[0.,2.5,10.]):
        tt=replace(t,activity_complementarity=z,commitment_strength=k,support_capacity_productivity=dp)
        ref=evaluate(1.,arr[0],tt)
        for a in arr:
            r=evaluate(1.,a,tt)
            named.append(dict(**tag(tt),**r,reference_rate=ref['normalized_rate'],rate_difference=r['normalized_rate']-ref['normalized_rate']))
    csvout('named_endpoints.csv',named)
    factors=['control_loss','operational_support','monitoring_incentive','pressure_loading']
    factorial=[];marginal=[];attribution=[];factor_summaries=[]
    for z,k,dp in product([0.,.5,.9],[0.,.25,.75],[0.,2.5,10.]):
        tt=replace(t,activity_complementarity=z,commitment_strength=k,support_capacity_productivity=dp)
        states={bits:evaluate(1.,factorial_arr(bits),tt) for bits in product([0,1],repeat=4)}
        base=states[(0,0,0,0)];end=states[(1,1,1,1)]
        for bits,r in states.items():
            factorial.append(dict(**tag(tt),**dict(zip(['loss_bit','support_bit','incentive_bit','loading_bit'],bits)),
                **r,reference_rate=base['normalized_rate'],rate_difference=r['normalized_rate']-base['normalized_rate']))
        for j,factor in enumerate(factors):
            mm=[]
            for bits in states:
                if bits[j]:continue
                switched=list(bits);switched[j]=1;switched=tuple(switched)
                before,after=states[bits],states[switched]
                row=dict(**tag(tt),factor=factor,background=''.join(map(str,bits)),
                    h_difference=after['h']-before['h'],n_difference=after['n']-before['n'],
                    A_difference=after['A']-before['A'],rate_difference=after['normalized_rate']-before['normalized_rate'])
                mm.append(row);marginal.append(row)
            factor_summaries.append(dict(**tag(tt),factor=factor,mean_rate_difference=float(np.mean([r['rate_difference'] for r in mm])),
                minimum_rate_difference=min(r['rate_difference'] for r in mm),maximum_rate_difference=max(r['rate_difference'] for r in mm),**count(mm)))
        contrib=np.zeros(4)
        for order in permutations(range(4)):
            bits=[0]*4
            for j in order:
                before=states[tuple(bits)]['normalized_rate'];bits[j]=1
                contrib[j]+=states[tuple(bits)]['normalized_rate']-before
        contrib/=24
        for factor,value in zip(factors,contrib):
            attribution.append(dict(**tag(tt),factor=factor,contribution=float(value),
                total_gap=end['normalized_rate']-base['normalized_rate']))
    csvout('institutional_factorial.csv',factorial);csvout('paired_factor_effects.csv',marginal)
    csvout('factor_effect_summary.csv',factor_summaries);csvout('four_factor_shapley.csv',attribution)
    capacity=[];boundaries=[];kboundaries=[]
    for z,k,idx in product([0.,.9],[0.,.25,.75],[1,2,5]):
        tt=replace(t,activity_complementarity=z,commitment_strength=k)
        ref=evaluate(1.,arr[0],tt);r=evaluate(1.,arr[idx],tt)
        boundaries.append(dict(**tag(tt),name=arr[idx].name,**support_boundary(r,ref,tt)))
        for dp in np.linspace(0,10,101):
            ts=replace(tt,support_capacity_productivity=float(dp));rr=evaluate(1.,arr[idx],ts)
            capacity.append(dict(**tag(ts),name=arr[idx].name,rate=rr['normalized_rate'],reference_rate=ref['normalized_rate'],
                rate_difference=rr['normalized_rate']-ref['normalized_rate']))
    for z,dp,idx in product([0.,.9],[0.,2.5,10.],[1,2,4,5]):
        tt=replace(t,activity_complementarity=z,support_capacity_productivity=dp)
        ref=evaluate(1.,arr[0],tt);r=evaluate(1.,arr[idx],tt)
        kboundaries.append(dict(**tag(tt),name=arr[idx].name,**commitment_boundary(r,ref,tt)))
    csvout('support_capacity_sweep.csv',capacity);csvout('support_capacity_boundaries.csv',boundaries)
    csvout('commitment_boundaries.csv',kboundaries)
    loading=[]
    for z,k,dp,lam in product([0.,.9],[0.,.25,.75],[0.,2.5,10.],np.linspace(0,1,51)):
        tt=replace(t,activity_complementarity=z,commitment_strength=k,support_capacity_productivity=dp)
        ref=evaluate(1.,arr[0],tt);r=evaluate(1.,replace(arr[1],pressure_loading=float(lam)),tt)
        loading.append(dict(**tag(tt),pressure_loading=float(lam),rate=r['normalized_rate'],
                           rate_difference=r['normalized_rate']-ref['normalized_rate']))
    csvout('pressure_loading_sweep.csv',loading)
    complement=[];examples=[]
    for B,z,gamma in product([1.,3.],[0.,.5,.9],np.linspace(0,.8,81)):
        tt=replace(t,budget=B,activity_complementarity=z)
        a=replace(arr[2],monitoring_incentive=float(gamma))
        r=evaluate(1.,a,tt)
        complement.append(dict(budget=B,complementarity=z,monitoring_incentive=float(gamma),**r,**monitoring_statics(1.,a,tt)))
    for B,z in product([1.,3.],[0.,.5,.9]):
        tt=replace(t,budget=B,activity_complementarity=z)
        r=evaluate(1.,arr[2],tt)
        examples.append(dict(budget=B,complementarity=z,**r,**monitoring_statics(1.,arr[2],tt)))
    csvout('complementarity_paths.csv',complement);csvout('complementarity_examples.csv',examples)
    variants=[]
    for loss,xi,anchor,pressure,z,k,dp in product(['exponential','hyperbolic'],[0.,.1],['rational','exponential'],
            ['power','bounded'],[0.,.9],[0.,.75],[0.,2.5]):
        tt=replace(t,turnover_decay=xi,activity_complementarity=z,commitment_strength=k,support_capacity_productivity=dp)
        ref=evaluate(1.,arr[0],tt,loss,anchor,pressure)
        for idx in [1,2,5]:
            r=evaluate(1.,arr[idx],tt,loss,anchor,pressure)
            variants.append(dict(loss_form=loss,turnover_decay=xi,anchor_form=anchor,pressure_form=pressure,**tag(tt),
                name=arr[idx].name,rate=r['normalized_rate'],reference_rate=ref['normalized_rate'],
                rate_difference=r['normalized_rate']-ref['normalized_rate']))
    csvout('structural_variants.csv',variants)
    grid=[]
    for B,z,k,dp,lam,alpha,b in product([.5,1.,2.],[0.,.9],[0.,.75],[0.,2.5,10.],[0.,.5,1.],[.5,1.],[0.,1.,2.]):
        tt=replace(t,budget=B,activity_complementarity=z,commitment_strength=k,
                   support_capacity_productivity=dp,benefit_elasticity=alpha)
        a=replace(arr[1],name='Service arrangement',pressure_loading=lam);r=evaluate(b,a,tt);ref=evaluate(b,arr[0],tt)
        grid.append(dict(budget=B,benefit_elasticity=alpha,**tag(tt),**r,
            reference_rate=ref['normalized_rate'],rate_difference=r['normalized_rate']-ref['normalized_rate']))
    csvout('joint_stress_grid.csv',grid)
    paths=[]
    for z,alpha,idx,b in product([0.,.9],[0.,.5,1.],[0,1],np.linspace(0,2,101)):
        tt=replace(t,activity_complementarity=z,benefit_elasticity=alpha)
        paths.append(dict(complementarity=z,benefit_elasticity=alpha,**evaluate(float(b),arr[idx],tt),**exposure_statics(float(b),arr[idx],tt)))
    csvout('stake_scaling_paths.csv',paths)
    removals=[]
    for z,label,k,beta,xi in [(z,label,k,beta,xi) for z in [0.,.9] for label,k,beta,xi in [
        ('Both links at reference strengths',.75,1.,.1),('No commitment weighting',0.,1.,.1),
        ('No direct pressure weighting',.75,0.,.1),('No pressure weighting or pressure erosion',.75,0.,0.),
        ('Neither temporal link',0.,0.,0.)]]:
        tt=replace(t,activity_complementarity=z,commitment_strength=k,pressure_strength=beta,turnover_decay=xi)
        for a in arr:removals.append(dict(scenario=label,complementarity=z,commitment_strength=k,pressure_strength=beta,
            turnover_decay=xi,**evaluate(1.,a,tt)))
    csvout('temporal_link_removals.csv',removals)
    summary=dict(version='0.5',legacy_reproduction_cases=len(legacy),legacy_maximum_error=max(r['maximum_error'] for r in legacy),
        factorial_records=len(factorial),paired_factor_effects=len(marginal),shapley_decompositions=len(attribution)//4,
        named_comparisons=[r for r in named if r['name'] in [arr[0].name,arr[1].name,arr[2].name] and r['commitment_strength'] in [0,.75]],
        reference_shapley=[r for r in attribution if r['complementarity']==0 and r['commitment_strength']==.75 and r['support_capacity_productivity']==2.5],
        support_boundaries=boundaries,commitment_boundaries=kboundaries,complementarity_examples=examples,
        joint_grid=count(grid),joint_grid_by_commitment=[dict(commitment_strength=k,**count([r for r in grid if r['commitment_strength']==k])) for k in [0.,.75]],
        joint_grid_with_zero_buffer=count([r for r in grid if r['support_capacity_productivity']==0]),
        structural_counts=[dict(name=arr[idx].name,complementarity=z,commitment_strength=k,support_capacity_productivity=dp,
            **count([r for r in variants if r['name']==arr[idx].name and r['complementarity']==z and r['commitment_strength']==k and r['support_capacity_productivity']==dp]))
            for idx,z,k,dp in product([1,2,5],[0.,.9],[0.,.75],[0.,2.5])],
        maximum_grid_kkt=max(r['kkt_residual'] for r in grid),
        stake_slopes=[dict(complementarity=z,benefit_elasticity=alpha,**exposure_statics(1.,arr[1],replace(t,activity_complementarity=z,benefit_elasticity=alpha)))
            for z,alpha in product([0.,.9],[0.,.5,1.])])
    (RESULTS/'summary.json').write_text(json.dumps(summary,indent=2))
    figures(named,capacity,complement,attribution,paths,arr)
    print(json.dumps({k:summary[k] for k in ['version','legacy_reproduction_cases','legacy_maximum_error','factorial_records',
        'paired_factor_effects','shapley_decompositions','reference_shapley','joint_grid','joint_grid_by_commitment','joint_grid_with_zero_buffer','maximum_grid_kkt']},indent=2))

def figures(named,capacity,complement,attribution,paths,arr):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':190})
    colors=['#244e6b','#b05c31','#666666'];styles=['-','--',':']
    fig,axs=plt.subplots(1,2,figsize=(9.3,3.8),sharey=False)
    for ax,k in zip(axs,[0,.75]):
        for idx,c,ls in zip([1,2,5],colors,styles):
            rows=[r for r in capacity if r['commitment_strength']==k and r['complementarity']==0 and r['name']==arr[idx].name]
            ax.plot([r['support_capacity_productivity'] for r in rows],[r['rate_difference'] for r in rows],color=c,ls=ls,lw=2,
                label={1:'Consequential monitoring',2:'Routine review',5:'Monitoring without pressure'}[idx])
        ax.axhline(0,color='black',lw=.7);ax.axvline(2.5,color='#aaaaaa',lw=1,ls=':')
        ax.set(title=f'Commitment strength κ = {k:g}',xlabel='Support buffering productivity dₚ',ylabel='Rate difference\nrelative to independent holding')
    hs,ls=axs[0].get_legend_handles_labels();fig.legend(hs,ls,loc='lower center',ncol=3,frameon=False,fontsize=8)
    fig.tight_layout(rect=[0,.1,1,1]);fig.savefig(FIGS/'01_support_capacity.png',bbox_inches='tight');plt.close(fig)
    fig,axs=plt.subplots(1,2,figsize=(9.3,3.7),sharey=False)
    for ax,B in zip(axs,[1.,3.]):
        for z,c,ls in zip([0.,.5,.9],colors,styles):
            rows=[r for r in complement if r['budget']==B and r['complementarity']==z]
            ax.plot([r['monitoring_incentive'] for r in rows],[r['h'] for r in rows],color=c,ls=ls,lw=2,label=f'Complementarity ζ = {z:g}')
        ax.set(title=f'Attention budget B = {B:g}',xlabel='Additional monitoring incentive γ',ylabel='Chosen substantive engagement h')
    hs,ls=axs[0].get_legend_handles_labels();fig.legend(hs,ls,loc='lower center',ncol=3,frameon=False,fontsize=8)
    fig.tight_layout(rect=[0,.1,1,1]);fig.savefig(FIGS/'02_complementarity.png',bbox_inches='tight');plt.close(fig)
    fig,ax=plt.subplots(figsize=(9.1,3.5));rows=[r for r in attribution if r['complementarity']==0 and r['commitment_strength']==.75 and r['support_capacity_productivity']==2.5]
    names=['Loss of independent\ntransfer authority','Operational\nsupport','Monitoring\nincentive','Pressure\nloading']
    vv=[r['contribution'] for r in rows]
    ax.bar(np.arange(4),vv,color=['#244e6b' if v>=0 else '#9b7250' for v in vv]);ax.axhline(0,color='black',lw=.7)
    ax.set(xticks=np.arange(4),xticklabels=names,ylabel='Contribution to normalized\nrate difference',ylim=(-.05,.18))
    for i,v in enumerate(vv):ax.text(i,v+(.006 if v>=0 else -.006),f'{v:+.3f}',ha='center',va='bottom' if v>=0 else 'top',fontsize=9)
    fig.tight_layout();fig.savefig(FIGS/'03_factor_attribution.png',bbox_inches='tight');plt.close(fig)
    fig,axs=plt.subplots(1,2,figsize=(9.3,3.7))
    for ax,z in zip(axs,[0.,.9]):
        for alpha,c,ls in zip([0.,.5,1.],colors,styles):
            rows=[r for r in paths if r['complementarity']==z and r['benefit_elasticity']==alpha and r['name']==arr[1].name]
            ax.plot([r['stake'] for r in rows],[r['normalized_rate'] for r in rows],color=c,ls=ls,lw=2,label=f'Benefit elasticity α = {alpha:g}')
        ax.axvline(2,color='#aaaaaa',lw=.7);ax.set(title=f'Complementarity ζ = {z:g}',xlabel='Normalized position value s',ylabel='Effective rate / common baseline')
    hs,ls=axs[0].get_legend_handles_labels();fig.legend(hs,ls,loc='lower center',ncol=3,frameon=False,fontsize=8)
    fig.tight_layout(rect=[0,.1,1,1]);fig.savefig(FIGS/'04_stake_scaling.png',bbox_inches='tight');plt.close(fig)

if __name__=='__main__':run()
