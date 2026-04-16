
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy.stats import spearmanr

from ..config import (
    FIG_DIR, VIDEO_ORDER, VIDEO_NAMES_SHORT,
    PALETTE_DEP, PHQ_CUTOFF,
)


# ---------------------------------------------------------------------------

def plot_phq_scatter(merged: pd.DataFrame, reg_results: list) -> str:
    fig, axes = plt.subplots(1, 5, figsize=(16, 3.8), sharey=False)

    for i, vid in enumerate(VIDEO_ORDER):
        sub = (merged[merged['video'] == vid]
               [['score_phq', 'mean_rot_speed_total', 'dep_group']]
               .dropna())
        dep_colors = sub['dep_group'].map(PALETTE_DEP)
        axes[i].scatter(sub['score_phq'], sub['mean_rot_speed_total'],
                        c=dep_colors, s=35, alpha=0.7,
                        edgecolors='white', linewidth=0.4)

        # Regression line
        m, b = np.polyfit(sub['score_phq'], sub['mean_rot_speed_total'], 1)
        x_line = np.linspace(sub['score_phq'].min(), sub['score_phq'].max(), 50)
        axes[i].plot(x_line, m * x_line + b,
                     color='gray', linestyle='--', linewidth=1.5)

        rho, p = spearmanr(sub['score_phq'], sub['mean_rot_speed_total'])
        sig = '*' if p < 0.05 else ''
        axes[i].set_title(f'{VIDEO_NAMES_SHORT[vid]}\nrho={rho:.2f}{sig}',
                           fontsize=9)
        axes[i].set_xlabel('PHQ-9', fontsize=9)
        if i == 0:
            axes[i].set_ylabel('Mean Rotation Speed (deg/s)', fontsize=9)
        axes[i].axvline(x=PHQ_CUTOFF, color='red', linestyle=':',
                         linewidth=1, alpha=0.5)

    legend_handles = [
        mpatches.Patch(facecolor='#4C72B0', label='Non-Depressed'),
        mpatches.Patch(facecolor='#DD8452', label='Depressed'),
    ]
    fig.legend(handles=legend_handles, loc='lower right', ncol=2,
               bbox_to_anchor=(0.98, -0.02), fontsize=9)
    fig.suptitle('PHQ-9 vs Mean Head-Rotation Speed per Video (Spearman rho)',
                 fontsize=11, y=1.01)

    path = os.path.join(FIG_DIR, 'figR2_2_phq_scatter.pdf')
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f'  Saved {os.path.basename(path)}')
    return path


# ---------------------------------------------------------------------------

def plot_ancova_forest(ancova_results: list) -> str:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    y_pos     = np.arange(len(ancova_results))
    betas     = [r['beta_phq']  for r in ancova_results]
    ci_lo     = [r['ci_low']    for r in ancova_results]
    ci_hi     = [r['ci_high']   for r in ancova_results]
    ps        = [r['p_phq']     for r in ancova_results]
    vid_labs  = [VIDEO_NAMES_SHORT[r['video']] for r in ancova_results]
    colors    = ['#C44E52' if p < 0.05 else '#4C72B0' for p in ps]

    for i in range(len(ancova_results)):
        ax.plot([ci_lo[i], ci_hi[i]], [y_pos[i], y_pos[i]],
                color=colors[i], linewidth=2)
        ax.scatter(betas[i], y_pos[i], s=80, color=colors[i], zorder=5)
        ax.text(max(ci_hi) + 0.3, y_pos[i],
                f'p={ps[i]:.3f}', va='center', fontsize=9)

    ax.axvline(x=0, color='black', linestyle='--', linewidth=1, alpha=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(vid_labs)
    ax.set_xlabel('Standardised beta (PHQ-9 effect on mean rotation speed)')
    ax.set_title('ANCOVA: PHQ-9 Effect on Head-Rotation Speed\n'
                 '(Controlling for GAD-7 and STAI-T)')
    ax.set_xlim(min(ci_lo) - 1, max(ci_hi) + 2)

    path = os.path.join(FIG_DIR, 'figR2_3_ancova_forest.pdf')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    print(f'  Saved {os.path.basename(path)}')
    return path


# ---------------------------------------------------------------------------

def plot_phq_continuous(df, ht_df: pd.DataFrame) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    # Left: PHQ-9 histogram with cutoff
    axes[0].hist(df['score_phq'], bins=range(0, 20),
                 color='#4C72B0', edgecolor='white', alpha=0.85)
    axes[0].axvline(x=PHQ_CUTOFF, color='red', linestyle='--',
                    linewidth=2, label=f'Binary cutoff ({PHQ_CUTOFF})')
    axes[0].set_xlabel('PHQ-9 Score')
    axes[0].set_ylabel('Count')
    axes[0].set_title('PHQ-9 Distribution\n(Continuous vs Binary)')
    axes[0].legend()

    # Right: avg speed vs PHQ-9
    ht_avg = (ht_df.groupby('pid')['mean_rot_speed_total']
              .mean().reset_index())
    ht_avg = ht_avg.merge(df[['pid', 'score_phq', 'dep_group']], on='pid')
    dep_colors = ht_avg['dep_group'].map(PALETTE_DEP)

    axes[1].scatter(ht_avg['score_phq'], ht_avg['mean_rot_speed_total'],
                    c=dep_colors, s=55, alpha=0.8,
                    edgecolors='white', linewidth=0.5)
    m, b = np.polyfit(ht_avg['score_phq'], ht_avg['mean_rot_speed_total'], 1)
    x_line = np.linspace(0, 18, 50)
    axes[1].plot(x_line, m * x_line + b,
                 color='gray', linestyle='--', linewidth=1.8)
    from scipy.stats import spearmanr
    rho, p = spearmanr(ht_avg['score_phq'], ht_avg['mean_rot_speed_total'])
    axes[1].set_xlabel('PHQ-9 Score')
    axes[1].set_ylabel('Mean Speed (avg across videos, deg/s)')
    axes[1].set_title(f'PHQ-9 vs Average Head-Rotation Speed\n'
                      f'(rho={rho:.2f}, p={p:.3f})')
    axes[1].axvline(x=PHQ_CUTOFF, color='red', linestyle=':', linewidth=1, alpha=0.5)
    legend_handles = [
        mpatches.Patch(facecolor='#4C72B0', label='Non-Depressed'),
        mpatches.Patch(facecolor='#DD8452', label='Depressed'),
    ]
    axes[1].legend(handles=legend_handles, fontsize=9)

    path = os.path.join(FIG_DIR, 'figR2_9_phq_continuous.pdf')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    print(f'  Saved {os.path.basename(path)}')
    return path
