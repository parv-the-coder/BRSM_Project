
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from ..config import FIG_DIR, VIDEO_ORDER, VIDEO_NAMES_SHORT


# ---------------------------------------------------------------------------

def plot_power_curve(power_res: dict) -> str:
    d_range  = power_res['d_range']
    orig_d   = power_res['original_d']
    mde      = power_res['mde_80pct']
    n_dep    = power_res['n_dep_current']
    n_needed = power_res['n_dep_needed_80pct']

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(d_range, power_res['power_current'],
            color='#C44E52', linewidth=2.5,
            label=f'Current n_dep={n_dep}')
    ax.plot(d_range, power_res['power_doubled'],
            color='#4C72B0', linewidth=2.5,
            label=f'Doubled n_dep={n_dep * 2}')
    ax.plot(d_range, power_res['power_needed'],
            color='#55A868', linewidth=2.5,
            label=f'n_dep={n_needed} (needed for 80%)')

    ax.axhline(y=0.80, color='black', linestyle='--', linewidth=1,
               alpha=0.7, label='80% threshold')
    ax.axvline(x=orig_d, color='purple', linestyle=':', linewidth=1.5,
               label=f'Original d={orig_d:.2f}')
    ax.axvline(x=mde, color='#C44E52', linestyle=':', linewidth=1.5,
               label=f'MDE current (d={mde:.2f})')

    ax.set_xlabel("Cohen's d (Effect Size)")
    ax.set_ylabel('Statistical Power (1 - beta)')
    ax.set_title('Power Analysis for Two-Sample t-Test\n(alpha=0.05, two-tailed)')
    ax.legend(fontsize=8, loc='lower right')
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 1.05)

    path = os.path.join(FIG_DIR, 'figR2_4_power_analysis.pdf')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    print(f'  Saved {os.path.basename(path)}')
    return path


# ---------------------------------------------------------------------------

def plot_mcc_comparison(mcc_df: pd.DataFrame) -> str:
    mean_speed = mcc_df[mcc_df['Measure'] == 'Mean Speed (Total)'].copy()

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))

    # Left: bar chart
    ax = axes[0]
    x_pos = np.arange(len(VIDEO_ORDER))
    w     = 0.22
    for j, (col, label, color) in enumerate([
        ('p_uncorrected', 'Uncorrected', '#4C72B0'),
        ('p_bonferroni',  'Bonferroni',  '#C44E52'),
        ('p_holm',        'Holm',        '#55A868'),
        ('p_fdr_bh',      'BH-FDR',      '#8172B2'),
    ]):
        vals = mean_speed.set_index('Video').reindex(VIDEO_ORDER)[col].values
        ax.bar(x_pos + (j - 1.5) * w, -np.log10(vals),
               width=w, label=label, color=color, alpha=0.85, edgecolor='white')
    ax.axhline(y=-np.log10(0.05), color='black', linestyle='--',
               linewidth=1.5, label='p=0.05 threshold')
    ax.set_xticks(x_pos)
    ax.set_xticklabels([VIDEO_NAMES_SHORT[v] for v in VIDEO_ORDER],
                        rotation=15, ha='right')
    ax.set_ylabel('-log10(p)')
    ax.set_title('Mean Speed: p-Values Under\nDifferent Correction Methods')
    ax.legend(fontsize=8)

    # Right: BH-FDR heatmap for all measures
    pivot = mcc_df.pivot(index='Measure', columns='Video', values='p_fdr_bh')
    ax2 = axes[1]
    sns.heatmap(pivot, annot=True, fmt='.3f', cmap='RdYlGn_r',
                vmin=0, vmax=0.5, linewidths=0.5, ax=ax2,
                cbar_kws={'label': 'BH-FDR p-value'})
    ax2.set_title('All Measures: BH-FDR Corrected p-Values\n'
                  '(green = significant, red = not)')
    ax2.set_xticklabels([VIDEO_NAMES_SHORT[v] for v in VIDEO_ORDER],
                         rotation=20, ha='right')

    path = os.path.join(FIG_DIR, 'figR2_5_mcc_comparison.pdf')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    print(f'  Saved {os.path.basename(path)}')
    return path


# ---------------------------------------------------------------------------

def plot_lmm_effects(lmm_res: dict) -> str:
    lmm3   = lmm_res['lmm3']
    re_var = lmm_res['re_var']
    icc    = lmm_res['icc']

    fe_coef  = lmm3.params
    fe_se    = lmm3.bse
    fe_pval  = lmm3.pvalues

    vid_keys  = [k for k in fe_coef.index if 'C(video)' in k]
    all_keys  = ['Intercept', 'phq_z', 'gad_z'] + vid_keys
    all_labels = [
        'Intercept\n(V1 reference)',
        'PHQ-9 (z)',
        'GAD-7 (z)',
    ] + ['vs V1: ' + k.replace('C(video)[T.', '').replace(']', '') for k in vid_keys]

    ci_lo = fe_coef[all_keys] - 1.96 * fe_se[all_keys]
    ci_hi = fe_coef[all_keys] + 1.96 * fe_se[all_keys]
    colors = ['#C44E52' if fe_pval[k] < 0.05 else '#4C72B0' for k in all_keys]

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))

    ax = axes[0]
    y_pos = np.arange(len(all_keys))
    for i, k in enumerate(all_keys):
        ax.plot([ci_lo[k], ci_hi[k]], [y_pos[i], y_pos[i]],
                color=colors[i], linewidth=2)
        ax.scatter(fe_coef[k], y_pos[i], s=70, color=colors[i], zorder=5)
    ax.axvline(x=0, color='black', linestyle='--', linewidth=1, alpha=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(all_labels, fontsize=9)
    ax.set_xlabel('Coefficient estimate (95% CI)')
    ax.set_title('LMM Fixed Effects\n(Model 3: PHQ + GAD + video)')

    ax2 = axes[1]
    re_intercepts = lmm_res['re_intercepts']
    ax2.hist(re_intercepts, bins=12, color='#4C72B0', edgecolor='white', alpha=0.85)
    ax2.axvline(x=0, color='red', linestyle='--', linewidth=1.5)
    ax2.set_xlabel('Random Intercept Deviation (deg/s)')
    ax2.set_ylabel('Count')
    ax2.set_title(
        f'LMM Random Intercepts by Participant\n'
        f'(sigma_between={lmm_res["re_sd"]:.1f} deg/s, ICC={icc:.2f})'
    )

    path = os.path.join(FIG_DIR, 'figR2_6_lmm_effects.pdf')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    print(f'  Saved {os.path.basename(path)}')
    return path
