
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from ..config import FIG_DIR, VIDEO_ORDER, VIDEO_NAMES_SHORT, VIDEO_COLORS


# ---------------------------------------------------------------------------

def plot_video_effect(ht_df: pd.DataFrame, rm_res: dict) -> str:
    vm = (ht_df.groupby('video')['mean_rot_speed_total']
          .agg(['mean', 'sem'])
          .reindex(VIDEO_ORDER))
    vm['ci95'] = vm['sem'] * 1.96

    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(VIDEO_ORDER))
    ax.bar(x, vm['mean'], yerr=vm['ci95'],
           color=VIDEO_COLORS, capsize=5, edgecolor='white',
           linewidth=0.8, alpha=0.88, width=0.6)

    # Jittered individual points
    np.random.seed(42)
    for i, vid in enumerate(VIDEO_ORDER):
        y_vals = ht_df[ht_df['video'] == vid]['mean_rot_speed_total'].values
        jitter = np.random.normal(0, 0.12, size=len(y_vals))
        ax.scatter(x[i] + jitter, y_vals, s=18, color='black', alpha=0.3, zorder=5)

    ax.set_xticks(x)
    ax.set_xticklabels([VIDEO_NAMES_SHORT[v] for v in VIDEO_ORDER],
                        rotation=15, ha='right')
    ax.set_ylabel('Mean Rotation Speed (deg/s)')
    ax.set_xlabel('Video')
    ax.set_title(
        f'Mean Head-Rotation Speed by Video\n'
        f'RM-ANOVA: F={rm_res["F"]:.2f}, '
        f'p<.001, eta2g={rm_res["eta2g"]:.3f}'
    )
    ax.set_ylim(0, 55)

    path = os.path.join(FIG_DIR, 'figR2_1_video_effect.pdf')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    print(f'  Saved {os.path.basename(path)}')
    return path


# ---------------------------------------------------------------------------

def plot_posthoc_heatmap(posthoc_df: pd.DataFrame,
                         kw_H: float, kw_p: float, kw_eta2: float) -> str:
    vid_labels = [VIDEO_NAMES_SHORT[v] for v in VIDEO_ORDER]
    p_matrix   = np.ones((5, 5))
    for _, row in posthoc_df.iterrows():
        i = VIDEO_ORDER.index(row['A'])
        j = VIDEO_ORDER.index(row['B'])
        p_matrix[i, j] = row['p_bonf']
        p_matrix[j, i] = row['p_bonf']

    p_df  = pd.DataFrame(p_matrix, index=vid_labels, columns=vid_labels)
    mask  = np.eye(5, dtype=bool)
    annot = p_df.map(lambda x: f'{x:.3f}' if x != 1.0 else '--')

    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    sns.heatmap(p_df, annot=annot, fmt='', cmap='RdYlGn',
                vmin=0, vmax=0.5, mask=mask, linewidths=0.5, ax=ax,
                cbar_kws={'label': 'Bonferroni-corrected p-value'})
    ax.set_title(
        f'Mann-Whitney U Post-Hoc: Pairwise p-Values (Bonferroni)\n'
        f'KW: H={kw_H:.2f}, p<.001, eta2={kw_eta2:.3f}'
    )

    path = os.path.join(FIG_DIR, 'figR2_10_mw_posthoc.pdf')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    print(f'  Saved {os.path.basename(path)}')
    return path
