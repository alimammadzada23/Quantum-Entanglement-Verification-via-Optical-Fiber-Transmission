# ================================================================
# MULTI-METHOD ENTANGLEMENT COMPARISON
# Methods compared:
#   M1 — Bell Fidelity F(|Ψ⁻⟩) & Witness W = 0.5 - F
#   M3 — CHSH S_max via Horodecki (1995)
#   M4 — Concurrence C (Wootters 1998)
# ================================================================

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# ────────────────────────────────────────────────────────────────
# 1. LOAD CSVs
# ────────────────────────────────────────────────────────────────
df_chsh = pd.read_csv('chsh_horodecki_results.csv')
df_conc = pd.read_csv('concurrence_results.csv')
df_fid  = pd.read_csv('fidelity_witness_results.csv')

for df in [df_chsh, df_conc, df_fid]:
    df['fiber'] = df['fiber'].str.upper().str.strip()
    df['fiber'] = df['fiber'].replace({'NANF': 'HCF'})
    df['dt_ps'] = df['dt_ps'].round(2)

print("Loaded:")
print(f"  CHSH       : {len(df_chsh)} rows  cols={list(df_chsh.columns)}")
print(f"  Concurrence: {len(df_conc)} rows  cols={list(df_conc.columns)}")
print(f"  Fidelity   : {len(df_fid)}  rows  cols={list(df_fid.columns)}")

# ────────────────────────────────────────────────────────────────
# 2. MERGE ALL THREE ON (dt_ps, fiber)
# ────────────────────────────────────────────────────────────────
# Detect CHSH entangled column
for _col in ['entangled_2sigma', 'entangled_2sig', 'entangled']:
    if _col in df_chsh.columns:
        chsh_ent_col = _col
        break
chsh_sel = df_chsh[['dt_ps','fiber','S_mean','S_std','significance_sigma',
                     chsh_ent_col,'purity']].copy()
chsh_sel.columns = ['dt_ps','fiber','S','S_std','S_sig','nonlocal_M3','purity_M3']

# Detect correct column name: Concurrence CSV uses 'entangled_2sigma'
for _col in ['entangled_2sigma', 'entangled_2sig', 'entangled']:
    if _col in df_conc.columns:
        conc_ent_col = _col
        break
conc_sel = df_conc[['dt_ps','fiber','C_mean','C_std', conc_ent_col]].copy()
conc_sel.columns = ['dt_ps','fiber','C','C_std','ent_M4']

# Detect correct column name: Fidelity CSV uses 'entangled_2sig'
for _col in ['entangled_2sig', 'entangled_2sigma', 'entangled']:
    if _col in df_fid.columns:
        fid_ent_col = _col
        break

print(f"  Column mapping detected:")
print(f"    CHSH   entangled col : {chsh_ent_col}")
print(f"    Conc   entangled col : {conc_ent_col}")
print(f"    Fidelity entangled col: {fid_ent_col}")
fid_sel = df_fid[['dt_ps','fiber','F_mean','F_std','W','W_std', fid_ent_col]].copy()
fid_sel.columns = ['dt_ps','fiber','F','F_std','W','W_std','ent_M1']

df = chsh_sel.merge(conc_sel, on=['dt_ps','fiber'], how='outer')
df = df.merge(fid_sel, on=['dt_ps','fiber'], how='outer')
df = df.sort_values(['fiber','dt_ps']).reset_index(drop=True)

# Only compare on rows where ALL three methods have data
df_common = df[df[['ent_M1','nonlocal_M3','ent_M4']].notna().all(axis=1)].copy()
print(f'\n  Common rows (all 3 methods have data): {len(df_common)} / {len(df)} total')

# all_agree defined on common rows only
df['all_agree'] = False
df.loc[df_common.index, 'all_agree'] = (
    (df.loc[df_common.index,'ent_M1'] == df.loc[df_common.index,'nonlocal_M3']) &
    (df.loc[df_common.index,'nonlocal_M3'] == df.loc[df_common.index,'ent_M4'])
)
# Rebuild df_common FROM df so it inherits the all_agree column
df_common = df[df[['ent_M1','nonlocal_M3','ent_M4']].notna().all(axis=1)].copy()

# ────────────────────────────────────────────────────────────────
# 3. PRINT SUMMARY TABLE
# ────────────────────────────────────────────────────────────────
print("\n" + "="*90)
print("MULTI-METHOD ENTANGLEMENT COMPARISON TABLE")
print("  M1: Bell Fidelity F>0.5 (2sig)  |  M3: CHSH S>2.0 → NONLOCAL  |  M4: Concurrence C>0 (2sig)")
print("="*90)

for fiber in ['HCF', 'SMF28']:
    sub = df[df['fiber'] == fiber].copy()
    print(f"\n{'─'*90}")
    print(f"  {fiber} FIBER")
    print(f"{'─'*90}")
    print(f"  {'dt(ps)':>8}  {'F':>7}  {'S':>7}  {'C':>7}  "
          f"  {'M1':>12}  {'M3(NONLOC)':>12}  {'M4':>12}  {'agree':>6}")
    print(f"  {'-'*83}")
    for _, r in sub.iterrows():
        F_str = f"{r['F']:.4f}" if pd.notna(r.get('F')) else "   n/a "
        S_str = f"{r['S']:.4f}" if pd.notna(r.get('S')) else "   n/a "
        C_str = f"{r['C']:.4f}" if pd.notna(r.get('C')) else "   n/a "
        m1 = "ENTANGLED" if r.get('ent_M1') else "not conf."
        m3 = "NONLOCAL" if r.get('nonlocal_M3') else "not conf."
        m4 = "ENTANGLED" if r.get('ent_M4') else "not conf."
        ag = "YES" if r.get('all_agree') else "NO"
        print(f"  {r['dt_ps']:>8.2f}  {F_str}  {S_str}  {C_str}  "
              f"  {m1:>12}  {m3:>12}  {m4:>12}  {ag:>6}")

# ────────────────────────────────────────────────────────────────
# 4. THRESHOLD ANALYSIS
# ────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("THRESHOLD DT — first confirmed entanglement by each method (ps)")
print("  Lower threshold = more sensitive method")
print("  Expected order: M1 (F) <= M4 (C) <= M3 (CHSH) — each stricter")
print("="*70)
print(f"  {'Fiber':<8}  {'M1 F>0.5':>10}  {'M4 C>0':>10}  {'M3 S>2.0':>10}  "
      f"  {'M3/M1':>8}  {'M3/M4':>8}")
print(f"  {'-'*60}")
for fiber in ['HCF', 'SMF28']:
    sub = df[df['fiber'] == fiber].sort_values('dt_ps')
    def first_ent(col):
        rows = sub[sub[col] == True]
        return rows['dt_ps'].min() if len(rows) > 0 else np.nan
    t1 = first_ent('ent_M1')
    t3 = first_ent('nonlocal_M3')
    t4 = first_ent('ent_M4')
    r31 = t3/t1 if not np.isnan(t1) else np.nan
    r34 = t3/t4 if not np.isnan(t4) else np.nan
    print(f"  {fiber:<8}  {t1:>10.2f}  {t4:>10.2f}  {t3:>10.2f}  "
          f"  {r31:>8.2f}  {r34:>8.2f}")

# ────────────────────────────────────────────────────────────────
# 5. PLATEAU STATISTICS
# ────────────────────────────────────────────────────────────────
TSIRELSON = 2 * np.sqrt(2)
SRC = {'F': 0.9759, 'S': 2.6921, 'C': 0.9183}
# Plateau: data-driven — points within 95% of the method's maximum value
# More defensible than a hardcoded dt cutoff
def get_plateau(sub, col):
    vals = sub[col].dropna()
    if len(vals) == 0:
        return sub.iloc[0:0]
    threshold_95 = 0.95 * vals.max()
    return sub[sub[col] >= threshold_95]
PLAT = {'HCF': 177.5, 'SMF28': 295.0}  # kept as fallback reference only

print("\n" + "="*70)
print("PLATEAU VALUES — saturated regime (large dt)")
print("="*70)
print(f"  {'Fiber':<8}  {'metric':>6}  {'mean':>9}  {'std':>8}  {'max':>8}  "
      f"{'source':>8}  {'recovery%':>10}")
print(f"  {'-'*65}")
for fiber in ['HCF', 'SMF28']:
    sub_all = df[df['fiber'] == fiber].sort_values('dt_ps')
    for col, src_val in [('S', SRC['S']), ('C', SRC['C']), ('F', SRC['F'])]:
        plat_sub = get_plateau(sub_all.dropna(subset=[col]), col)
        vals = plat_sub[col].dropna()
        if len(vals) == 0:
            continue
        mn, sd, mx = vals.mean(), vals.std(), vals.max()
        plat_min_dt = plat_sub['dt_ps'].min()
        if col == 'S':
            rec = (mn - 2.0) / (src_val - 2.0) * 100
        else:
            rec = mn / src_val * 100
        print(f"  {fiber:<8}  {col:>6}  {mn:>9.4f}  {sd:>8.4f}  {mx:>8.4f}  "
              f"{src_val:>8.4f}  {rec:>9.1f}%  [plateau from {plat_min_dt:.1f}ps]")

# ────────────────────────────────────────────────────────────────
# 6. DISAGREEMENT ANALYSIS
# ────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("METHOD DISAGREEMENTS (where M1 / M3 / M4 give different verdicts)")
print("="*70)
any_disagreement = False
for fiber in ['HCF', 'SMF28']:
    sub = df[(df['fiber'] == fiber)].copy()
    sub = df_common[df_common['fiber'] == fiber].copy()
    disagree = sub[~sub['all_agree']]
    if len(disagree) == 0:
        print(f"  {fiber}: all shared points agree across M1/M3/M4 ✓")
    else:
        any_disagreement = True
        print(f"\n  {fiber} disagreements:")
        for _, r in disagree.iterrows():
            print(f"    dt={r['dt_ps']:>7.2f}  M1={'ENT' if r['ent_M1'] else 'no ':>4}  "
                  f"M3={'NLC' if r['nonlocal_M3'] else 'no ':>4}  "
                  f"M4={'ENT' if r['ent_M4'] else 'no ':>4}  "
                  f"F={r['F']:.4f}  S={r['S']:.4f}  C={r['C']:.4f}")
        print()
        print("  Physical interpretation:")
        print("  Disagreements at low dt expected: M1 (Bell witness) is most sensitive,")
        print("  M4 (Concurrence) intermediate, M3 (CHSH) most conservative.")
        print("  Disagreements at high dt would flag an inconsistency — check those carefully.")

# ────────────────────────────────────────────────────────────────
# 7. SAVE MERGED CSV
# ────────────────────────────────────────────────────────────────
df.to_csv('merged_comparison.csv', index=False)
print("\nMerged CSV saved: merged_comparison.csv")

# ────────────────────────────────────────────────────────────────
# 8. FIGURE 1: 6-PANEL COMPARISON
# ────────────────────────────────────────────────────────────────
HCF_C  = '#1a78c2'
SMF_C  = '#e05c2a'
ALPHA_F = 0.10
fibers     = ['HCF', 'SMF28']
colors     = [HCF_C, SMF_C]
markers    = ['o', 's']
lstyles    = ['-', '--']
fib_labels = ['NANF (HCF)', 'SMF28']

fig, axes = plt.subplots(3, 2, figsize=(15, 14))
axes = axes.flatten()

# Panel 0: CHSH
ax = axes[0]
for fib, col, mk, ls, lab in zip(fibers, colors, markers, lstyles, fib_labels):
    sub = df[df['fiber']==fib].sort_values('dt_ps').dropna(subset=['S'])
    ax.errorbar(sub['dt_ps'], sub['S'], yerr=sub['S_std'],
                fmt=mk+ls, color=col, lw=2, ms=5, capsize=3, label=lab)
ax.axhline(2.0,        color='red',    ls='--', lw=1.5, label='Classical bound S=2')
ax.axhline(TSIRELSON,  color='purple', ls=':',  lw=1.5, label=f'Tsirelson={TSIRELSON:.4f}')
ax.axhline(SRC['S'],   color='green',  ls=':',  lw=1.5, label=f"Source S={SRC['S']}")
ax.fill_between([30,540],[0,0],[2,2], color='red', alpha=ALPHA_F)
ax.set_title('M3: CHSH S_max (Horodecki 1995)', fontweight='bold')
ax.set_ylabel('S_max'); ax.set_xlabel('dt (ps)')
ax.set_xlim(30,540); ax.set_ylim(0.9, 2.95)
ax.legend(fontsize=7); ax.grid(alpha=0.3)

# Panel 1: Concurrence
ax = axes[1]
for fib, col, mk, ls, lab in zip(fibers, colors, markers, lstyles, fib_labels):
    sub = df[df['fiber']==fib].sort_values('dt_ps').dropna(subset=['C'])
    ax.errorbar(sub['dt_ps'], sub['C'], yerr=sub['C_std'],
                fmt=mk+ls, color=col, lw=2, ms=5, capsize=3, label=lab)
ax.axhline(0,          color='red',    ls='--', lw=1.5, label='C=0 separable')
ax.axhline(SRC['C'],   color='green',  ls=':',  lw=1.5, label=f"Source C={SRC['C']}")
ax.axhline(1.0,        color='purple', ls=':',  lw=1.5, label='C=1 perfect Bell')
ax.fill_between([30,540],[-0.05,-0.05],[0,0], color='red', alpha=ALPHA_F)
ax.set_title('M4: Concurrence C (Wootters 1998)', fontweight='bold')
ax.set_ylabel('Concurrence C'); ax.set_xlabel('dt (ps)')
ax.set_xlim(30,540); ax.set_ylim(-0.05, 1.05)
ax.legend(fontsize=7); ax.grid(alpha=0.3)

# Panel 2: Bell Fidelity
ax = axes[2]
for fib, col, mk, ls, lab in zip(fibers, colors, markers, lstyles, fib_labels):
    sub = df[df['fiber']==fib].sort_values('dt_ps').dropna(subset=['F'])
    ax.errorbar(sub['dt_ps'], sub['F'], yerr=sub['F_std'],
                fmt=mk+ls, color=col, lw=2, ms=5, capsize=3, label=lab)
ax.axhline(0.5,        color='red',    ls='--', lw=1.5, label='Threshold F=0.5')
ax.axhline(SRC['F'],   color='green',  ls=':',  lw=1.5, label=f"Source F={SRC['F']}")
ax.axhline(1.0,        color='purple', ls=':',  lw=1.5, label='F=1 perfect Bell')
ax.fill_between([30,540],[0,0],[0.5,0.5], color='red', alpha=ALPHA_F)
ax.set_title('M1: Bell Fidelity F(|Psi-⟩)', fontweight='bold')
ax.set_ylabel('Bell Fidelity F'); ax.set_xlabel('dt (ps)')
ax.set_xlim(30,540); ax.set_ylim(0.3, 1.05)
ax.legend(fontsize=7); ax.grid(alpha=0.3)

# Panel 3: Witness
ax = axes[3]
for fib, col, mk, ls, lab in zip(fibers, colors, markers, lstyles, fib_labels):
    sub = df[df['fiber']==fib].sort_values('dt_ps').dropna(subset=['W'])
    ax.errorbar(sub['dt_ps'], sub['W'], yerr=sub['W_std'],
                fmt=mk+ls, color=col, lw=2, ms=5, capsize=3, label=lab)
ax.axhline(0,               color='red',   ls='--', lw=1.5, label='W=0 threshold')
ax.axhline(0.5-SRC['F'],    color='green', ls=':',  lw=1.5, label=f"Source W={0.5-SRC['F']:.3f}")
ax.fill_between([30,540],[-0.6,-0.6],[0,0], color='blue', alpha=ALPHA_F, label='W<0: entangled')
ax.set_title('M1: Entanglement Witness W = 0.5 - F', fontweight='bold')
ax.set_ylabel('Witness W'); ax.set_xlabel('dt (ps)')
ax.set_xlim(30,540)
ax.legend(fontsize=7); ax.grid(alpha=0.3)

# Panel 4: Normalised overlay
ax = axes[4]
for fib, col, mk, ls, lab in zip(fibers, colors, markers, lstyles, fib_labels):
    sub = df[df['fiber']==fib].sort_values('dt_ps')
    s_sub = sub.dropna(subset=['S'])
    c_sub = sub.dropna(subset=['C'])
    f_sub = sub.dropna(subset=['F'])
    S_n = (s_sub['S'] - 2.0) / (TSIRELSON - 2.0)
    C_n = c_sub['C']
    F_n = (f_sub['F'] - 0.5) / 0.5
    ax.plot(s_sub['dt_ps'], S_n, mk+ls,   color=col, lw=2, ms=4, alpha=0.9, label=f'{lab} M3(S)')
    ax.plot(c_sub['dt_ps'], C_n, mk+':',  color=col, lw=1.5, ms=4, alpha=0.7, label=f'{lab} M4(C)')
    ax.plot(f_sub['dt_ps'], F_n, mk+'-.', color=col, lw=1.5, ms=4, alpha=0.7, label=f'{lab} M1(F)')
ax.axhline(0, color='red',    ls='--', lw=1.5, label='Threshold = 0')
ax.axhline(1, color='purple', ls=':',  lw=1.2, label='Perfect Bell = 1')
ax.set_title('Normalised M1/M3/M4 — visual diagnostic only\n'
             '[S: nonlocality  |  C: entanglement monotone  |  F: Bell-state fidelity]\n'
             'Scales are NOT physically equivalent — threshold crossing only',
             fontweight='bold', fontsize=8)
ax.set_ylabel('Normalised value [0=threshold, 1=perfect]\n(visual only — not physically equivalent)')
ax.set_xlabel('dt (ps)')
ax.set_xlim(30,540); ax.set_ylim(-0.2, 1.15)
ax.legend(fontsize=6, ncol=2); ax.grid(alpha=0.3)

# Panel 5: Threshold bar chart
ax = axes[5]
ent_cols   = ['ent_M1', 'ent_M4', 'nonlocal_M3']
meth_names = ['M1\nF>0.5', 'M4\nC>0', 'M3\nS>2.0']
x = np.arange(len(meth_names))
width = 0.3
for i, (fib, col, lab) in enumerate(zip(fibers, colors, fib_labels)):
    sub = df[df['fiber']==fib].sort_values('dt_ps')
    thresholds = []
    for ec in ent_cols:
        rows = sub[sub[ec]==True]
        t = rows['dt_ps'].min() if len(rows) > 0 else 0
        thresholds.append(t)
    bars = ax.bar(x + (i-0.5)*width, thresholds, width,
                  color=col, alpha=0.8, label=lab, edgecolor='white', linewidth=0.5)
    for bar, val in zip(bars, thresholds):
        if val > 0:
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+3,
                    f'{val:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(meth_names, fontsize=10)
ax.set_ylabel('First confirmed entanglement dt (ps)')
ax.set_title('Sensitivity Comparison\n(lower bar = more sensitive entanglement detector)',
             fontweight='bold')
ax.legend(); ax.grid(alpha=0.3, axis='y')

plt.suptitle(
    'Multi-Method Entanglement Comparison — NANF (HCF) vs SMF28\n'
    'M1: Bell Fidelity & Witness  |  M3: CHSH/Horodecki  |  M4: Concurrence/Wootters',
    fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('comparison_6panel.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nFigure saved: comparison_6panel.png")

# ────────────────────────────────────────────────────────────────
# 9. FIGURE 2: PER-METHOD with threshold crossings annotated
# ────────────────────────────────────────────────────────────────
fig2, axes2 = plt.subplots(1, 3, figsize=(16, 5))
configs = [
    ('S', 'S_std', 'nonlocal_M3', 2.0, TSIRELSON, SRC['S'],
     'M3: CHSH S_max (Horodecki 1995)', 'S_max', 'Classical S=2', 'Source S=2.692'),
    ('C', 'C_std', 'ent_M4', 0.0, 1.0, SRC['C'],
     'M4: Concurrence C (Wootters 1998)', 'Concurrence C', 'C=0 separable', 'Source C=0.918'),
    ('F', 'F_std', 'ent_M1', 0.5, 1.0, SRC['F'],
     'M1: Bell Fidelity F(|Psi-⟩)', 'Bell Fidelity F', 'Threshold F=0.5', 'Source F=0.976'),
]
for ax2, (col, ecol, ent_col, thr, ceiling, src, title, ylabel, thr_lbl, src_lbl) in zip(axes2, configs):
    for fib, c, mk, ls, lab in zip(fibers, colors, markers, lstyles, fib_labels):
        sub = df[df['fiber']==fib].sort_values('dt_ps').dropna(subset=[col])
        ax2.errorbar(sub['dt_ps'], sub[col], yerr=sub[ecol],
                     fmt=mk+ls, color=c, lw=2, ms=5, capsize=3, label=lab)
        rows_ent = sub[sub[ent_col]==True]
        if len(rows_ent):
            first = rows_ent.iloc[0]
            ax2.axvline(first['dt_ps'], color=c, ls=':', lw=1.5, alpha=0.7)
            ax2.annotate(f"{first['dt_ps']:.0f} ps",
                         xy=(first['dt_ps'], thr+(ceiling-thr)*0.05),
                         xytext=(first['dt_ps']+10, thr+(ceiling-thr)*0.12),
                         fontsize=8.5, color=c, fontweight='bold',
                         arrowprops=dict(arrowstyle='->', color=c, lw=1.2))
    ax2.axhline(thr, color='red',   ls='--', lw=1.5, label=thr_lbl)
    ax2.axhline(src, color='green', ls=':',  lw=1.5, label=src_lbl)
    ax2.fill_between([30,540],[thr-(ceiling-thr)*0.3]*2,[thr,thr],
                     color='red', alpha=0.07)
    ax2.set_title(title, fontweight='bold', fontsize=10)
    ax2.set_ylabel(ylabel); ax2.set_xlabel('dt (ps)')
    ax2.set_xlim(30,540); ax2.legend(fontsize=8); ax2.grid(alpha=0.3)

plt.suptitle(
    'Per-Method Comparison: NANF (HCF) vs SMF28\n'
    'Vertical dashed lines = first confirmed entanglement (2-sigma)',
    fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('comparison_per_method.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure saved: comparison_per_method.png")

print("\n" + "="*70)
print("DONE — files written:")
print("  merged_comparison.csv")
print("  comparison_6panel.png")
print("  comparison_per_method.png")
print("="*70)
