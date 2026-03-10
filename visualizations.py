import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

from config import FIG_DIR, PALETTE_DEP, VIDEO_NAMES, VIDEO_ORDER, PHQ_CUTOFF


def fig1_demographics(df):
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
    axes[0].hist(df['age'], bins=range(18, 30), color='#4C72B0',
                 edgecolor='white', alpha=0.85)
    axes[0].set_xlabel('Age'); axes[0].set_ylabel('Count')
    axes[0].set_title('Age Distribution')

    df['gender_label'].value_counts().plot.bar(
        ax=axes[1], color=['#4C72B0', '#DD8452'], edgecolor='white')
    axes[1].set_title('Gender Distribution')
    axes[1].set_xlabel('Gender'); axes[1].set_ylabel('Count')
    axes[1].tick_params(axis='x', rotation=0)

    df['vr_exp_label'].value_counts().plot.bar(
        ax=axes[2], color=['#4C72B0', '#DD8452'], edgecolor='white')
    axes[2].set_title('Prior VR Experience')
    axes[2].set_xlabel('Experience'); axes[2].set_ylabel('Count')
    axes[2].tick_params(axis='x', rotation=0)

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig1_demographics.pdf'))
    plt.close()
    print("  Saved fig1_demographics.pdf")


def fig2_clinical_distributions(df):
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    axes[0].hist(df['score_phq'], bins=range(0, 29), color='#4C72B0',
                 edgecolor='white', alpha=0.85)
    axes[0].axvline(x=PHQ_CUTOFF, color='red', linestyle='--', linewidth=1.5,
                    label=f'Cutoff = {PHQ_CUTOFF}')
    axes[0].set_xlabel('PHQ-9 Score'); axes[0].set_ylabel('Count')
    axes[0].set_title('PHQ-9 Distribution'); axes[0].legend()

    axes[1].hist(df['score_gad'], bins=range(0, 22), color='#55A868',
                 edgecolor='white', alpha=0.85)
    axes[1].set_xlabel('GAD-7 Score'); axes[1].set_ylabel('Count')
    axes[1].set_title('GAD-7 Distribution')

    axes[2].hist(df['score_stai_t'], bins=12, color='#C44E52',
                 edgecolor='white', alpha=0.85)
    axes[2].set_xlabel('STAI-T Score'); axes[2].set_ylabel('Count')
    axes[2].set_title('STAI-T Distribution')

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig2_clinical_distributions.pdf'))
    plt.close()
    print("  Saved fig2_clinical_distributions.pdf")


def fig3_phq_severity(df):
    severity_order = ['Minimal', 'Mild', 'Moderate', 'Moderately Severe', 'Severe']
    counts = df['phq_severity'].value_counts().reindex(severity_order).dropna()
    colors = ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c', '#8e44ad']

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(counts, labels=counts.index, autopct='%1.0f%%',
           colors=colors[:len(counts)], startangle=90, pctdistance=0.75)
    ax.set_title('PHQ-9 Depression Severity')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig3_phq_severity.pdf'))
    plt.close()
    print("  Saved fig3_phq_severity.pdf")


def fig4_correlation_heatmap(df):
    corr_vars = ['score_phq', 'score_gad', 'score_stai_t', 'score_vrise',
                 'positive_affect_start', 'negative_affect_start',
                 'positive_affect_end', 'negative_affect_end']
    corr_labels = ['PHQ-9', 'GAD-7', 'STAI-T', 'VRISE',
                   'PA (Pre)', 'NA (Pre)', 'PA (Post)', 'NA (Post)']
    corr_matrix = df[corr_vars].corr()
    corr_matrix.index = corr_labels
    corr_matrix.columns = corr_labels

    fig, ax = plt.subplots(figsize=(8, 6.5))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
                mask=mask, square=True, linewidths=0.5, ax=ax,
                vmin=-1, vmax=1, cbar_kws={'shrink': 0.8})
    ax.set_title('Correlation Matrix: Clinical & Affect Measures')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig4_correlation_heatmap.pdf'))
    plt.close()
    print("  Saved fig4_correlation_heatmap.pdf")


def fig5_valence_arousal(df):
    rows = []
    for vid in VIDEO_ORDER:
        for _, row in df.iterrows():
            rows.append({'Video': VIDEO_NAMES[vid],
                         'Valence': row[f'valence_{vid}'],
                         'Arousal': row[f'arousal_{vid}']})
    val_df = pd.DataFrame(rows)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    sns.boxplot(data=val_df, x='Video', y='Valence', ax=axes[0], palette='Set2')
    axes[0].set_title('Valence by Video')
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=25, ha='right')
    axes[0].set_ylim(0, 10)

    sns.boxplot(data=val_df, x='Video', y='Arousal', ax=axes[1], palette='Set2')
    axes[1].set_title('Arousal by Video')
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=25, ha='right')
    axes[1].set_ylim(0, 10)

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig5_valence_arousal_by_video.pdf'))
    plt.close()
    print("  Saved fig5_valence_arousal_by_video.pdf")


def fig6_presence(df):
    rows = []
    for vid in VIDEO_ORDER:
        for _, row in df.iterrows():
            rows.append({'Video': VIDEO_NAMES[vid],
                         'Presence Score': row[f'immersion_{vid}']})
    imm_df = pd.DataFrame(rows)

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.violinplot(data=imm_df, x='Video', y='Presence Score',
                   palette='Set2', ax=ax, inner='box')
    ax.set_title('Presence (Immersion) Score by Video')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=25, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig6_presence_by_video.pdf'))
    plt.close()
    print("  Saved fig6_presence_by_video.pdf")


def fig7_phq_vs_gad(df):
    fig, ax = plt.subplots(figsize=(5.5, 5))
    r_val, p_val = pearsonr(df['score_phq'], df['score_gad'])
    sns.scatterplot(data=df, x='score_phq', y='score_gad', hue='dep_group',
                    palette=PALETTE_DEP, s=60, ax=ax,
                    edgecolor='white', linewidth=0.5)
    m, b = np.polyfit(df['score_phq'], df['score_gad'], 1)
    x_line = np.linspace(0, df['score_phq'].max(), 50)
    ax.plot(x_line, m * x_line + b, color='gray', linestyle='--', alpha=0.7)
    ax.set_xlabel('PHQ-9 Score'); ax.set_ylabel('GAD-7 Score')
    ax.set_title(f'PHQ-9 vs GAD-7 (r = {r_val:.2f}, p = {p_val:.3f})')
    ax.legend(title='Group')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig7_phq_vs_gad.pdf'))
    plt.close()
    print("  Saved fig7_phq_vs_gad.pdf")


def fig8_headtrack_speed_violin(merged):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.violinplot(data=merged, x='video', y='mean_rot_speed_total',
                   hue='dep_group', split=True, palette=PALETTE_DEP,
                   inner='quartile', ax=ax, order=VIDEO_ORDER)
    ax.set_xticklabels([VIDEO_NAMES[v] for v in VIDEO_ORDER], rotation=20, ha='right')
    ax.set_xlabel('Video'); ax.set_ylabel('Mean Rotation Speed (°/s)')
    ax.set_title('Mean Rotation Speed by Video and Depression Group')
    ax.legend(title='Group')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig8_headtrack_speed_by_group.pdf'))
    plt.close()
    print("  Saved fig8_headtrack_speed_by_group.pdf")


def fig9_headtrack_sd_box(merged):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=merged, x='video', y='sd_rot_speed_total',
                hue='dep_group', palette=PALETTE_DEP, ax=ax, order=VIDEO_ORDER)
    ax.set_xticklabels([VIDEO_NAMES[v] for v in VIDEO_ORDER], rotation=20, ha='right')
    ax.set_xlabel('Video'); ax.set_ylabel('SD of Rotation Speed (°/s)')
    ax.set_title('Variability of Rotation Speed by Video and Depression Group')
    ax.legend(title='Group')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig9_headtrack_sd_by_group.pdf'))
    plt.close()
    print("  Saved fig9_headtrack_sd_by_group.pdf")


def fig10_angular_range(merged):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=merged, x='video', y='total_range', hue='dep_group',
                palette=PALETTE_DEP, ci=95, ax=ax, order=VIDEO_ORDER)
    ax.set_xticklabels([VIDEO_NAMES[v] for v in VIDEO_ORDER], rotation=20, ha='right')
    ax.set_xlabel('Video'); ax.set_ylabel('Total Angular Range Explored (°)')
    ax.set_title('Total Angular Range Explored by Video and Depression Group')
    ax.legend(title='Group')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig10_angular_range_by_group.pdf'))
    plt.close()
    print("  Saved fig10_angular_range_by_group.pdf")


def fig11_panas_change(df):
    fig, ax = plt.subplots(figsize=(6, 4.5))
    x = np.arange(2)
    width = 0.35
    pa_means = [df['positive_affect_start'].mean(), df['positive_affect_end'].mean()]
    pa_ses = [df['positive_affect_start'].sem(), df['positive_affect_end'].sem()]
    na_means = [df['negative_affect_start'].mean(), df['negative_affect_end'].mean()]
    na_ses = [df['negative_affect_start'].sem(), df['negative_affect_end'].sem()]

    ax.bar(x - width / 2, pa_means, width, yerr=pa_ses, label='Positive Affect',
           color='#4C72B0', capsize=4, edgecolor='white')
    ax.bar(x + width / 2, na_means, width, yerr=na_ses, label='Negative Affect',
           color='#DD8452', capsize=4, edgecolor='white')
    ax.set_xticks(x); ax.set_xticklabels(['Pre-VR', 'Post-VR'])
    ax.set_ylabel('Score')
    ax.set_title('PANAS Scores Pre- and Post-VR')
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig11_panas_change.pdf'))
    plt.close()
    print("  Saved fig11_panas_change.pdf")


def fig12_yaw_speed_by_group(merged):
    fig, axes = plt.subplots(1, 5, figsize=(16, 4), sharey=True)
    for i, vid in enumerate(VIDEO_ORDER):
        sub = merged[merged['video'] == vid]
        sns.boxplot(data=sub, x='dep_group', y='mean_rot_speed_y',
                    palette=PALETTE_DEP, ax=axes[i],
                    order=['Non-Depressed', 'Depressed'])
        axes[i].set_title(VIDEO_NAMES[vid].split(': ')[1], fontsize=10)
        axes[i].set_xlabel('')
        axes[i].set_ylabel('Mean Yaw Speed (°/s)' if i == 0 else '')
    fig.suptitle('Mean Yaw (Horizontal) Rotation Speed by Depression Group',
                 fontsize=12, y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig12_yaw_speed_by_group.pdf'))
    plt.close()
    print("  Saved fig12_yaw_speed_by_group.pdf")


def generate_all_figures(df, ht_df, merged):
    print("=" * 70)
    print("GENERATING VISUALIZATIONS")
    print("=" * 70)
    fig1_demographics(df)
    fig2_clinical_distributions(df)
    fig3_phq_severity(df)
    fig4_correlation_heatmap(df)
    fig5_valence_arousal(df)
    fig6_presence(df)
    fig7_phq_vs_gad(df)
    fig8_headtrack_speed_violin(merged)
    fig9_headtrack_sd_box(merged)
    fig10_angular_range(merged)
    fig11_panas_change(df)
    fig12_yaw_speed_by_group(merged)
