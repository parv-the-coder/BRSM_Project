
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy.stats import spearmanr, mannwhitneyu

from ..config import FIG_DIR, VIDEO_ORDER, VIDEO_NAMES_SHORT, PALETTE_DEP


# ---------------------------------------------------------------------------

def plot_panas_by_group(df: pd.DataFrame) -> str:
    panas_long = []
    for _, row in df.iterrows():
        for affect, pre_col, post_col in [
            ('Positive Affect', 'positive_affect_start', 'positive_affect_end'),
            ('Negative Affect', 'negative_affect_start', 'negative_affect_end'),
        ]:
            panas_long.append({
                'pid':       row['pid'],
                'dep_group': row['dep_group'],
                'affect':    affect,
                'Change':    row[post_col] - row[pre_col],
            })
    panas_df = pd.DataFrame(panas_long)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    np.random.seed(0)
    for i, affect_type in enumerate(['Positive Affect', 'Negative Affect']):
        ax  = axes[i]
        sub = panas_df[panas_df['affect'] == affect_type]

        sns.boxplot(data=sub, x='dep_group', y='Change', palette=PALETTE_DEP,
                    ax=ax, order=['Non-Depressed', 'Depressed'])
        ax.axhline(y=0, color='red', linestyle='--', linewidth=1.2, alpha=0.7)
        ax.set_xlabel('')
        ax.set_ylabel(f'Delta {affect_type} (Post - Pre)')
        ax.set_title(f'{affect_type} Change\nby Depression Group')
        ax.set_xticklabels(['Non-Dep.', 'Depressed'], rotation=10)

        # Jittered individual points
        for j, grp in enumerate(['Non-Depressed', 'Depressed']):
            vals   = sub[sub['dep_group'] == grp]['Change']
            jitter = np.random.normal(0, 0.08, size=len(vals))
            ax.scatter(np.repeat(j, len(vals)) + jitter, vals,
                       s=20, color='black', alpha=0.4, zorder=5)

        dep_c    = sub[sub['dep_group'] == 'Depressed']['Change']
        nondep_c = sub[sub['dep_group'] == 'Non-Depressed']['Change']
        u, p_val = mannwhitneyu(dep_c, nondep_c, alternative='two-sided')
        ax.set_xlabel(f'U={u:.0f}, p={p_val:.3f}', fontsize=9)

    fig.suptitle('PANAS Affect Change (Post - Pre VR) by Depression Group',
                 fontsize=12, y=1.02)
    path = os.path.join(FIG_DIR, 'figR2_7_panas_by_group.pdf')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    print(f'  Saved {os.path.basename(path)}')
    return path


# ---------------------------------------------------------------------------

def plot_phq_subj_ratings(subj_df: pd.DataFrame) -> str:
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    vid_colors = ['#4C72B0', '#55A868', '#C44E52', '#8172B2', '#CCB974']

    for i, (dv, label) in enumerate([
        ('valence',  'Valence'),
        ('arousal',  'Arousal'),
        ('presence', 'Presence'),
    ]):
        ax = axes[i]
        for j, vid in enumerate(VIDEO_ORDER):
            sub_v = subj_df[subj_df['video'] == vid]
            r, p  = spearmanr(sub_v['score_phq'], sub_v[dv])
            ax.scatter(sub_v['score_phq'], sub_v[dv],
                       alpha=0.5, s=20, color=vid_colors[j],
                       label=f'{VIDEO_NAMES_SHORT[vid]} (rho={r:.2f})')

        # Overall regression line
        r_all, p_all = spearmanr(subj_df['score_phq'], subj_df[dv])
        m, b = np.polyfit(subj_df['score_phq'], subj_df[dv], 1)
        x_line = np.linspace(0, 18, 50)
        ax.plot(x_line, m * x_line + b, color='black', linestyle='--',
                linewidth=2, label=f'Overall (rho={r_all:.2f}, p={p_all:.3f})')
        ax.set_xlabel('PHQ-9 Score')
        ax.set_ylabel(label)
        ax.set_title(f'PHQ-9 vs {label}')
        ax.legend(fontsize=7)

    fig.suptitle('PHQ-9 vs Subjective VR Experience Ratings', fontsize=11, y=1.02)
    path = os.path.join(FIG_DIR, 'figR2_8_phq_subj_ratings.pdf')
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f'  Saved {os.path.basename(path)}')
    return path
