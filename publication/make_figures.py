"""Reproduce the paper's four figures from saved model v0.5 outputs.

Only presentation changes: no model execution or parameter changes.
Run: python make_figures.py
Requires: matplotlib, numpy, pandas.
"""
from pathlib import Path
import hashlib
import json
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--figure', type=int, choices=[1, 2, 3, 4],
                    help='Regenerate only this figure; default is all four.')
args = parser.parse_args()

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FormatStrFormatter
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
for fmt in ('png', 'svg', 'pdf'):
    (ROOT / fmt).mkdir(exist_ok=True)

# Match the existing Word image footprints exactly to preserve pagination.
SIZES = [(6108192/914400, 4585498/914400),
         (5997575/914400, 2724150/914400),
         (6108192/914400, 3265256/914400),
         (6108192/914400, 2841258/914400)]
BLUE, ORANGE, BLACK = '#0072BD', '#D95319', '#202020'
STYLES = [(BLUE, '-'), (ORANGE, '--'), (BLACK, '-.')]
plt.rcdefaults()
plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 9,
    'axes.labelsize': 9, 'axes.titlesize': 9,
    'axes.titleweight': 'normal', 'axes.labelweight': 'normal',
    'xtick.labelsize': 8, 'ytick.labelsize': 8, 'legend.fontsize': 8,
    'axes.spines.top': True, 'axes.spines.right': True,
    'axes.edgecolor': 'black', 'axes.linewidth': .7,
    'axes.labelcolor': 'black', 'text.color': 'black',
    'axes.facecolor': 'white', 'figure.facecolor': 'white',
    'xtick.color': 'black', 'ytick.color': 'black',
    'xtick.direction': 'in', 'ytick.direction': 'in',
    'xtick.top': True, 'ytick.right': True,
    'lines.linewidth': 1.5, 'mathtext.fontset': 'dejavusans',
    'svg.fonttype': 'path', 'pdf.fonttype': 42, 'ps.fonttype': 42,
    'savefig.facecolor': 'white', 'savefig.transparent': False,
    'hatch.linewidth': .5,
})
files = []

def save(fig, stem):
    if args.figure is not None and int(stem.split('_')[1]) != args.figure:
        plt.close(fig)
        return
    for fmt in ('png', 'svg', 'pdf'):
        out = ROOT / fmt / f'{stem}.{fmt}'
        fig.savefig(out, dpi=600, bbox_inches=None)
        files.append({'file': out.relative_to(ROOT).as_posix(),
                      'sha256': hashlib.sha256(out.read_bytes()).hexdigest()})
    plt.close(fig)

def scientific_axes(ax, grid=False):
    ax.tick_params(which='major', length=3.5, width=.7, pad=4)
    ax.tick_params(which='minor', length=2, width=.5)
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.set_axisbelow(True)
    if grid:
        ax.grid(axis='y', which='major', color='.82', ls=':', lw=.55)

# Figure 1: an unshaded scientific process diagram.
fig, ax = plt.subplots(figsize=SIZES[0])
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax.set(xlim=(0, 1), ylim=(0, 1)); ax.axis('off')

def box(cx, cy, width, height, label, fontsize=8.5):
    ax.add_patch(Rectangle((cx-width/2, cy-height/2), width, height,
                          linewidth=.8, edgecolor='black', facecolor='white', zorder=3))
    ax.text(cx, cy, label, ha='center', va='center', fontsize=fontsize,
            linespacing=1.35, zorder=4)

def arrow(start, end, dashed=False):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle='-|>', mutation_scale=9,
                 linewidth=.85, linestyle=(0, (4, 3)) if dashed else '-',
                 color='black', shrinkA=2, shrinkB=2, zorder=2))

ax.text(.5, .965, r'Same holder   |   Matched exposure   |   Common baseline patience $\rho_0$',
        ha='center', va='center', fontsize=9)
box(.13, .835, .215, .115, 'Operational\nsupport $p$')
box(.375, .835, .215, .115, 'Independent\ncontrol $x$')
box(.62, .835, .215, .115, 'Monitoring\nreward $\\gamma$')
box(.865, .835, .215, .115, 'Consequences\nof review $\\lambda$')
box(.50, .635, .50, .135,
    'Joint attention choice\nEngagement $h$  ·  Monitoring $n$\nBudget $B$  ·  Complementarity $\\zeta$')
arrow((.13,.7775),(.30,.7025)); arrow((.375,.7775),(.41,.7025))
arrow((.62,.7775),(.60,.7025))

box(.155,.405,.275,.18,
    'Capacity $D$\n$D=d_hh+d_pp$\nPersonal + provider resources',fontsize=7.9)
box(.50,.405,.285,.18,
    'Maintained commitment $A^*$\n$A^*=qh/(\\delta+\\xi v)$\nCompetence and understanding',fontsize=7.8)
box(.845,.405,.275,.18,
    'Decision pressure $v$\n$v=\\bar{v}+\\tau\\lambda n$\nAmbient + review pressure',fontsize=7.9)
arrow((.35,.5675),(.18,.495)); arrow((.44,.5675),(.50,.495))
arrow((.66,.5675),(.80,.495)); arrow((.865,.7775),(.90,.495))
ax.text(.265,.55,'$h$',fontsize=9)
ax.text(.485,.545,'$h$',fontsize=9)
ax.text(.74,.535,'$n$',fontsize=9)
arrow((.07,.7775),(.07,.495),dashed=True)
ax.text(.042,.636,'Optional relief',rotation=90,fontsize=7.4,ha='center',va='center')
arrow((.7075,.405),(.6425,.405))
ax.text(.675,.435,'erodes',fontsize=6.9,ha='center')

box(.50,.15,.82,.155,
    'Effective discounting $R=\\rho_{\\mathrm{eff}}/\\rho_0$\n'
    'Commitment multiplier × pressure multiplier\n'
    'Lower with commitment; higher with pressure relative to capacity',fontsize=8.1)
arrow((.155,.315),(.28,.2275)); arrow((.50,.315),(.50,.2275))
arrow((.845,.315),(.72,.2275))
ax.text(.50,.025,'Temporal links are explicit hypotheses tested separately.',
        ha='center',fontsize=8)
save(fig,'Figure_01_Mechanisms')

# Figure 2: monochrome point-and-stem decomposition with a separate total.
d = pd.read_csv(DATA / 'four_factor_shapley.csv')
d = d[(d.complementarity == 0) & (d.commitment_strength == .75) &
      (d.support_capacity_productivity == 2.5)]
keys = ['control_loss','monitoring_incentive','pressure_loading','operational_support']
values = d.set_index('factor').loc[keys,'contribution'].to_numpy()
assert len(d) == 4 and np.isclose(values.sum(), d.total_gap.iloc[0], rtol=0, atol=1e-12)
fig, ax = plt.subplots(figsize=SIZES[1])
fig.subplots_adjust(left=.37, right=.865, bottom=.205, top=.865)
rows = np.array([4., 3., 2., 1.])
total_row = -.25
ax.set(xlim=(-.045, .41), ylim=(-.88, 4.65))
ax.set_yticks([])
ax.set_xticks([0, .1, .2, .3, .4])
ax.set_xticklabels(['0', '0.1', '0.2', '0.3', '0.4'])
ax.xaxis.set_minor_locator(MultipleLocator(.05))
ax.tick_params(axis='x', which='major', direction='out', top=False,
               length=3.5, width=.7, pad=5, labelsize=8)
ax.tick_params(axis='x', which='minor', direction='out', top=False,
               length=2, width=.55)
for side in ('left', 'right', 'top'):
    ax.spines[side].set_visible(False)
ax.spines['bottom'].set_linewidth(.7)
ax.axvline(0, color='black', lw=.7, ls=(0, (3, 3)), zorder=1)
ax.hlines(rows, np.minimum(0, values), np.maximum(0, values),
          color='black', lw=1.0, zorder=2)
ax.plot(values, rows, linestyle='none', marker='o', markersize=5.7,
        markerfacecolor='white', markeredgecolor='black',
        markeredgewidth=1.1, zorder=3)
total = float(values.sum())
ax.hlines(total_row, 0, total, color='black', lw=1.0, zorder=2)
ax.plot(total, total_row, marker='D', markersize=5.7, linestyle='none',
        markerfacecolor='black', markeredgecolor='black', zorder=3)
ax.set_xlabel('Contribution to normalized rate difference', labelpad=8, fontsize=8.7)

# Labels and values form aligned columns, independent of marker position.
def figure_y(y):
    return fig.transFigure.inverted().transform(ax.transData.transform((0, y)))[1]

labels = ['Loss of independent control', 'Stronger monitoring rewards',
          'More consequential review', 'Operational support']
for label, row, value in zip(labels, rows, values):
    fig.text(.025, figure_y(row), label, ha='left', va='center', fontsize=8.5)
    fig.text(.975, figure_y(row), f'{value:+.3f}'.replace('-', '\N{MINUS SIGN}'),
             ha='right', va='center', fontsize=8.5)
fig.text(.025, figure_y(total_row), 'Total rate difference',
         ha='left', va='center', fontsize=8.5, weight='bold')
fig.text(.975, figure_y(total_row), f'{total:+.3f}',
         ha='right', va='center', fontsize=8.5, weight='bold')
fig.text(.025, .94, 'Institutional feature', ha='left', va='center',
         fontsize=8.6, weight='bold')
fig.text(.975, .94, r'$\Delta R$', ha='right', va='center', fontsize=9.2)
for y in (.893, figure_y(.38)):
    fig.add_artist(matplotlib.lines.Line2D(
        [.025, .975], [y, y], transform=fig.transFigure,
        color='black', lw=.55, clip_on=False))
save(fig,'Figure_02_Contributions')

# Figure 3: full plotted ranges and near-zero inset use the same saved records.
s = pd.read_csv(DATA / 'support_capacity_sweep.csv')
names = sorted(s.name.unique(),key=lambda x: (0 if 'consequential' in x.lower() else
                                            1 if 'routine' in x.lower() else 2))
assert len(names) == 3
labels = ['Consequential service','Routine delegation','Review without added pressure']
fig, axs = plt.subplots(1,2,figsize=SIZES[2])
fig.subplots_adjust(left=.10,right=.975,bottom=.30,top=.87,wspace=.30)
handles=[]
for ax,kappa,title in zip(axs,[0,.75],['(A) No commitment effect','(B) Reference commitment effect']):
    scientific_axes(ax)
    for name,label,(color,ls) in zip(names,labels,STYLES):
        sub=s[(s.complementarity==0)&(s.commitment_strength==kappa)&(s.name==name)].sort_values('support_capacity_productivity')
        assert len(sub)==101
        line,=ax.plot(sub.support_capacity_productivity,sub.rate_difference,color=color,ls=ls,label=label)
        if kappa==0:handles.append(line)
    ax.axhline(0,color='black',lw=.7)
    ax.axvline(2.5,color='.35',lw=.8,ls=':')
    ax.set_xlim(0,10)
    ax.set_xticks([0,2.5,5,7.5,10],['0','2.5','5','7.5','10'])
    ax.set_title(title,loc='left',pad=9,fontsize=8.6)
    ax.set_xlabel('Provider pressure relief, $d_p$',labelpad=5)
    ax.set_ylim((-.12,2.4) if kappa==0 else (-.08,1.8))
axs[0].set_ylabel('Rate difference from independent holding',labelpad=5)
ia=axs[0].inset_axes([.395,.46,.565,.46])
for name,(color,ls) in zip(names,STYLES):
    sub=s[(s.complementarity==0)&(s.commitment_strength==0)&(s.name==name)].sort_values('support_capacity_productivity')
    ia.plot(sub.support_capacity_productivity,sub.rate_difference,color=color,ls=ls,lw=1.15)
ia.axhline(0,color='black',lw=.65)
ia.axvline(2.5,color='.35',lw=.7,ls=':')
ia.set(xlim=(0,10),ylim=(-.045,.105),xticks=[0,5,10],yticks=[0,.1])
ia.set_title('Near equal rates',fontsize=7,pad=4)
ia.tick_params(labelsize=6.5,length=2,pad=2,width=.5)
ia.set_facecolor('white')
fig.legend(handles,labels,loc='lower center',bbox_to_anchor=(.55,.012),
           frameon=False,ncol=1,fontsize=8,handlelength=3.0,labelspacing=.4)
save(fig,'Figure_03_Pressure_Relief')

# Figure 4: boxed, matched axes and distinguishable scientific line styles.
c=pd.read_csv(DATA/'complementarity_paths.csv')
fig,axs=plt.subplots(1,2,figsize=SIZES[3])
fig.subplots_adjust(left=.10,right=.975,bottom=.255,top=.86,wspace=.30)
for ax,budget,title in zip(axs,[1,3],['(A) Limited attention ($B=1$)',
                                    '(B) More available attention ($B=3$)']):
    scientific_axes(ax)
    for zeta,label,(color,ls) in zip([0,.5,.9],['None ($\\zeta=0$)',
                          'Moderate ($\\zeta=0.5$)','Strong ($\\zeta=0.9$)'],STYLES):
        sub=c[(c.budget==budget)&(c.complementarity==zeta)].sort_values('monitoring_incentive')
        assert len(sub)==81
        ax.plot(sub.monitoring_incentive,sub.h,color=color,ls=ls,label=label)
    ax.set_title(title,loc='left',pad=9,fontsize=8.6)
    ax.set(xlim=(0,.8),ylim=(.2,.9),xticks=[0,.2,.4,.6,.8])
    ax.yaxis.set_major_locator(MultipleLocator(.1))
    ax.set_xlabel('Additional monitoring incentive, $\\gamma$',labelpad=5)
axs[0].set_ylabel('Engagement, $h$',labelpad=5)
handles,labels=axs[0].get_legend_handles_labels()
fig.legend(handles,labels,loc='lower center',bbox_to_anchor=(.54,.025),
           ncol=3,frameon=False,fontsize=8,handlelength=3.0,columnspacing=1.5)
save(fig,'Figure_04_Complementarity')

files = [{'file': p.relative_to(ROOT).as_posix(),
          'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
         for fmt in ('png', 'svg', 'pdf') for p in sorted((ROOT/fmt).glob('*.'+fmt))]
manifest = {'figure_count':4,'png_dpi':600,'formats':['PNG','SVG','PDF'],
    'model_version':'0.5','model_executed':False,
    'source_data':[{ 'file':f'data/{p.name}','sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
                   for p in sorted(DATA.glob('*.csv'))],
    'reference_contributions':dict(zip(keys,values.tolist())),
    'reference_total_gap':float(values.sum()),'files':files}
(ROOT/'figure_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'figures':4,'files':len(files),'reference_total_gap':float(values.sum())},indent=2))
