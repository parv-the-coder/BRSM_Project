#!/usr/bin/env python3
"""
Report 1 Analysis: Are Headtracking Measures an Indicator of Depressive Symptoms?
==================================================================================
This script performs data loading, preprocessing, descriptive statistics,
visualization, and preliminary inferential analysis for the 360° VR experiment.
"""

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats
from scipy.stats import pearsonr, spearmanr, mannwhitneyu, shapiro, ttest_ind, wilcoxon

warnings.filterwarnings('ignore')

# ── Configuration ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
HEADTRACK_DIR = os.path.join(DATA_DIR, 'headtracking-data')
FIG_DIR = os.path.join(BASE_DIR, 'figures')
os.makedirs(FIG_DIR, exist_ok=True)

# Visual settings
sns.set_theme(style='whitegrid', context='paper', font_scale=1.2)
plt.rcParams.update({
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'font.family': 'serif',
})
PALETTE_DEP = {'Non-Depressed': '#4C72B0', 'Depressed': '#DD8452'}
VIDEO_NAMES = {
    'v1': 'V1: Abandoned Buildings',
    'v2': 'V2: Beach',
    'v3': 'V3: Campus',
    'v4': 'V4: Horror (Nun)',
    'v5': 'V5: Tahiti Surf',
}
VIDEO_ORDER = ['v1', 'v2', 'v3', 'v4', 'v5']

# PHQ-9 clinical cutoffs (Kroenke et al., 2001)
PHQ_CUTOFF = 10  # ≥10 is moderate depression

# ══════════════════════════════════════════════════════════════════════════════
# PART 1: LOAD AND PREPROCESS SURVEY DATA
# ══════════════════════════════════════════════════════════════════════════════
print("=" * 70)
print("PART 1: Loading survey data")
print("=" * 70)

df = pd.read_excel(os.path.join(DATA_DIR, 'data.xlsx'))
print(f"Loaded survey data: {df.shape[0]} participants, {df.shape[1]} columns")

# Assign participant IDs (P01 .. P40)
df['pid'] = [f'P{i+1:02d}' for i in range(len(df))]

# Depression group (PHQ-9 >= 10 → Depressed)
df['dep_group'] = df['score_phq'].apply(
    lambda x: 'Depressed' if x >= PHQ_CUTOFF else 'Non-Depressed'
)

# PHQ-9 severity categories
def phq_severity(score):
    if score <= 4:
        return 'Minimal'
    elif score <= 9:
        return 'Mild'
    elif score <= 14:
        return 'Moderate'
    elif score <= 19:
        return 'Moderately Severe'
    else:
        return 'Severe'

df['phq_severity'] = df['score_phq'].apply(phq_severity)

# Gender labels
df['gender_label'] = df['gender'].map({1: 'Male', 2: 'Female'})

# VR experience labels
df['vr_exp_label'] = df['vr_experience'].map({1: 'No', 2: 'Yes'})

# PANAS change scores
df['pa_change'] = df['positive_affect_end'] - df['positive_affect_start']
df['na_change'] = df['negative_affect_end'] - df['negative_affect_start']

n_dep = (df['dep_group'] == 'Depressed').sum()
n_nondep = (df['dep_group'] == 'Non-Depressed').sum()
print(f"Depression groups (PHQ >= {PHQ_CUTOFF}): Depressed={n_dep}, Non-Depressed={n_nondep}")

# ══════════════════════════════════════════════════════════════════════════════
# PART 2: LOAD AND SUMMARIZE HEADTRACKING DATA
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PART 2: Processing headtracking data")
print("=" * 70)

headtrack_records = []

for idx, row in df.iterrows():
    pid = row['pid']
    for vid in VIDEO_ORDER:
        fname = row[vid]
        fpath = os.path.join(HEADTRACK_DIR, vid, fname)
        if not os.path.exists(fpath):
            print(f"  WARNING: Missing file {fpath}")
            continue
        ht = pd.read_csv(fpath, on_bad_lines='skip')

        # Duration
        duration = ht['Time'].max() - ht['Time'].min()

        # Compute summary measures
        record = {
            'pid': pid,
            'video': vid,
            'duration_s': duration,
            # Mean rotation speed (degrees/sec)
            'mean_rot_speed_total': ht['RotationSpeedTotal'].mean(),
            'mean_rot_speed_x': ht['RotationSpeedX'].mean(),
            'mean_rot_speed_y': ht['RotationSpeedY'].mean(),
            'mean_rot_speed_z': ht['RotationSpeedZ'].mean(),
            # SD of rotation speed
            'sd_rot_speed_total': ht['RotationSpeedTotal'].std(),
            'sd_rot_speed_x': ht['RotationSpeedX'].std(),
            'sd_rot_speed_y': ht['RotationSpeedY'].std(),
            'sd_rot_speed_z': ht['RotationSpeedZ'].std(),
            # Median rotation speed (robust to outliers)
            'median_rot_speed_total': ht['RotationSpeedTotal'].median(),
            # Mean absolute rotation change (position change)
            'mean_abs_rot_x': ht['RotationChangeX'].abs().mean(),
            'mean_abs_rot_y': ht['RotationChangeY'].abs().mean(),
            'mean_abs_rot_z': ht['RotationChangeZ'].abs().mean(),
            # SD of rotation change
            'sd_rot_change_x': ht['RotationChangeX'].std(),
            'sd_rot_change_y': ht['RotationChangeY'].std(),
            'sd_rot_change_z': ht['RotationChangeZ'].std(),
            # Range of rotation change (total angular range explored)
            'range_rot_x': ht['RotationChangeX'].max() - ht['RotationChangeX'].min(),
            'range_rot_y': ht['RotationChangeY'].max() - ht['RotationChangeY'].min(),
            'range_rot_z': ht['RotationChangeZ'].max() - ht['RotationChangeZ'].min(),
            # Max speed (peak exploration burst)
            'max_rot_speed_total': ht['RotationSpeedTotal'].max(),
        }
        headtrack_records.append(record)

ht_df = pd.DataFrame(headtrack_records)
print(f"Headtracking summaries computed: {len(ht_df)} records ({len(ht_df)//5} participants × 5 videos)")

# Merge with survey data
merged = df.merge(ht_df, on='pid', how='inner')
print(f"Merged dataset shape: {merged.shape}")

# ══════════════════════════════════════════════════════════════════════════════
# PART 3: DESCRIPTIVE STATISTICS
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PART 3: Descriptive statistics")
print("=" * 70)

# --- 3a. Demographics ---
print("\n--- Demographics ---")
print(f"N = {len(df)}")
print(f"Age: M={df['age'].mean():.1f}, SD={df['age'].std():.1f}, Range=[{df['age'].min()}, {df['age'].max()}]")
print(f"Gender: Male={df['gender_label'].value_counts().get('Male',0)}, Female={df['gender_label'].value_counts().get('Female',0)}")
print(f"VR Experience: Yes={df['vr_exp_label'].value_counts().get('Yes',0)}, No={df['vr_exp_label'].value_counts().get('No',0)}")

# --- 3b. Clinical scores ---
print("\n--- Clinical Scores ---")
for var, label in [('score_phq', 'PHQ-9'), ('score_gad', 'GAD-7'), ('score_stai_t', 'STAI-T')]:
    print(f"{label}: M={df[var].mean():.2f}, SD={df[var].std():.2f}, Mdn={df[var].median():.1f}, Range=[{df[var].min()}, {df[var].max()}]")
    
print(f"\nPHQ-9 Severity Distribution:")
for cat in ['Minimal', 'Mild', 'Moderate', 'Moderately Severe', 'Severe']:
    n = (df['phq_severity'] == cat).sum()
    print(f"  {cat}: {n} ({n/len(df)*100:.1f}%)")

# --- 3c. PANAS ---
print("\n--- PANAS Scores ---")
for var, label in [('positive_affect_start', 'PA Pre'), ('positive_affect_end', 'PA Post'),
                   ('negative_affect_start', 'NA Pre'), ('negative_affect_end', 'NA Post')]:
    print(f"{label}: M={df[var].mean():.2f}, SD={df[var].std():.2f}")

# --- 3d. Video-wise valence and arousal ---
print("\n--- Valence & Arousal per Video ---")
for vid in VIDEO_ORDER:
    val = df[f'valence_{vid}']
    aro = df[f'arousal_{vid}']
    imm = df[f'immersion_{vid}']
    print(f"{VIDEO_NAMES[vid]}:  Valence M={val.mean():.2f}(SD={val.std():.2f})  "
          f"Arousal M={aro.mean():.2f}(SD={aro.std():.2f})  "
          f"Presence M={imm.mean():.2f}(SD={imm.std():.2f})")

# --- 3e. Headtracking by video ---
print("\n--- Headtracking Mean Rotation Speed by Video ---")
for vid in VIDEO_ORDER:
    sub = ht_df[ht_df['video'] == vid]
    print(f"{VIDEO_NAMES[vid]}:  MeanSpeed M={sub['mean_rot_speed_total'].mean():.2f}(SD={sub['mean_rot_speed_total'].std():.2f})")

# --- 3f. Headtracking by depression group ---
print("\n--- Headtracking by Depression Group ---")
for vid in VIDEO_ORDER:
    sub = merged[merged['video'] == vid]
    for grp in ['Non-Depressed', 'Depressed']:
        g = sub[sub['dep_group'] == grp]
        print(f"  {VIDEO_NAMES[vid]} | {grp}: MeanSpeed M={g['mean_rot_speed_total'].mean():.2f}(SD={g['mean_rot_speed_total'].std():.2f}), n={len(g)}")

# Save descriptive stats table
desc_stats = df[['age', 'score_phq', 'score_gad', 'score_stai_t', 'score_vrise',
                 'positive_affect_start', 'negative_affect_start',
                 'positive_affect_end', 'negative_affect_end']].describe().round(2)
desc_stats.to_csv(os.path.join(FIG_DIR, 'descriptive_stats.csv'))
print("\nDescriptive stats saved to figures/descriptive_stats.csv")

# ══════════════════════════════════════════════════════════════════════════════
# PART 4: VISUALIZATIONS
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PART 4: Generating visualizations")
print("=" * 70)

# --- Fig 1: Demographics Overview ---
fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
# Age distribution
axes[0].hist(df['age'], bins=range(18, 30), color='#4C72B0', edgecolor='white', alpha=0.85)
axes[0].set_xlabel('Age')
axes[0].set_ylabel('Count')
axes[0].set_title('Age Distribution')
# Gender
df['gender_label'].value_counts().plot.bar(ax=axes[1], color=['#4C72B0', '#DD8452'], edgecolor='white')
axes[1].set_title('Gender Distribution')
axes[1].set_xlabel('Gender')
axes[1].set_ylabel('Count')
axes[1].tick_params(axis='x', rotation=0)
# VR Experience
df['vr_exp_label'].value_counts().plot.bar(ax=axes[2], color=['#4C72B0', '#DD8452'], edgecolor='white')
axes[2].set_title('Prior VR Experience')
axes[2].set_xlabel('Experience')
axes[2].set_ylabel('Count')
axes[2].tick_params(axis='x', rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig1_demographics.pdf'))
plt.close()
print("  Saved fig1_demographics.pdf")

# --- Fig 2: PHQ-9, GAD-7, STAI-T Distributions ---
fig, axes = plt.subplots(1, 3, figsize=(13, 4))
# PHQ-9
axes[0].hist(df['score_phq'], bins=range(0, 29), color='#4C72B0', edgecolor='white', alpha=0.85)
axes[0].axvline(x=PHQ_CUTOFF, color='red', linestyle='--', linewidth=1.5, label=f'Cutoff = {PHQ_CUTOFF}')
axes[0].set_xlabel('PHQ-9 Score')
axes[0].set_ylabel('Count')
axes[0].set_title('PHQ-9 Distribution')
axes[0].legend()
# GAD-7
axes[1].hist(df['score_gad'], bins=range(0, 22), color='#55A868', edgecolor='white', alpha=0.85)
axes[1].set_xlabel('GAD-7 Score')
axes[1].set_ylabel('Count')
axes[1].set_title('GAD-7 Distribution')
# STAI-T
axes[2].hist(df['score_stai_t'], bins=12, color='#C44E52', edgecolor='white', alpha=0.85)
axes[2].set_xlabel('STAI-T Score')
axes[2].set_ylabel('Count')
axes[2].set_title('STAI-T Distribution')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig2_clinical_distributions.pdf'))
plt.close()
print("  Saved fig2_clinical_distributions.pdf")

# --- Fig 3: PHQ-9 Severity Pie Chart ---
severity_counts = df['phq_severity'].value_counts()
severity_order = ['Minimal', 'Mild', 'Moderate', 'Moderately Severe', 'Severe']
severity_counts = severity_counts.reindex(severity_order).dropna()
colors_sev = ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c', '#8e44ad']
fig, ax = plt.subplots(figsize=(5, 5))
wedges, texts, autotexts = ax.pie(
    severity_counts, labels=severity_counts.index, autopct='%1.0f%%',
    colors=colors_sev[:len(severity_counts)], startangle=90, pctdistance=0.75
)
ax.set_title('PHQ-9 Depression Severity')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig3_phq_severity.pdf'))
plt.close()
print("  Saved fig3_phq_severity.pdf")

# --- Fig 4: Correlation Heatmap (PHQ, GAD, STAI-T, PANAS, VRISE) ---
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

# --- Fig 5: Valence and Arousal by Video (Box plots) ---
val_data = []
for vid in VIDEO_ORDER:
    for _, row in df.iterrows():
        val_data.append({'Video': VIDEO_NAMES[vid], 'Valence': row[f'valence_{vid}'],
                         'Arousal': row[f'arousal_{vid}']})
val_df = pd.DataFrame(val_data)

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

# --- Fig 6: Presence (Immersion) by Video ---
imm_data = []
for vid in VIDEO_ORDER:
    for _, row in df.iterrows():
        imm_data.append({'Video': VIDEO_NAMES[vid], 'Presence Score': row[f'immersion_{vid}']})
imm_df = pd.DataFrame(imm_data)

fig, ax = plt.subplots(figsize=(7, 4))
sns.violinplot(data=imm_df, x='Video', y='Presence Score', palette='Set2', ax=ax, inner='box')
ax.set_title('Presence (Immersion) Score by Video')
ax.set_xticklabels(ax.get_xticklabels(), rotation=25, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig6_presence_by_video.pdf'))
plt.close()
print("  Saved fig6_presence_by_video.pdf")

# --- Fig 7: PHQ-9 vs GAD-7 Scatter (showing covariance) ---
fig, ax = plt.subplots(figsize=(5.5, 5))
r_val, p_val = pearsonr(df['score_phq'], df['score_gad'])
sns.scatterplot(data=df, x='score_phq', y='score_gad', hue='dep_group',
                palette=PALETTE_DEP, s=60, ax=ax, edgecolor='white', linewidth=0.5)
# Regression line
m, b = np.polyfit(df['score_phq'], df['score_gad'], 1)
x_line = np.linspace(0, df['score_phq'].max(), 50)
ax.plot(x_line, m * x_line + b, color='gray', linestyle='--', alpha=0.7)
ax.set_xlabel('PHQ-9 Score')
ax.set_ylabel('GAD-7 Score')
ax.set_title(f'PHQ-9 vs GAD-7 (r = {r_val:.2f}, p = {p_val:.3f})')
ax.legend(title='Group')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig7_phq_vs_gad.pdf'))
plt.close()
print("  Saved fig7_phq_vs_gad.pdf")

# --- Fig 8: Headtracking Mean Speed by Video and Depression Group (Violin) ---
fig, ax = plt.subplots(figsize=(10, 5))
sns.violinplot(data=merged, x='video', y='mean_rot_speed_total',
               hue='dep_group', split=True, palette=PALETTE_DEP,
               inner='quartile', ax=ax, order=VIDEO_ORDER)
ax.set_xticklabels([VIDEO_NAMES[v] for v in VIDEO_ORDER], rotation=20, ha='right')
ax.set_xlabel('Video')
ax.set_ylabel('Mean Rotation Speed (°/s)')
ax.set_title('Mean Rotation Speed by Video and Depression Group')
ax.legend(title='Group')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig8_headtrack_speed_by_group.pdf'))
plt.close()
print("  Saved fig8_headtrack_speed_by_group.pdf")

# --- Fig 9: Headtracking SD of Speed by Video and Depression Group ---
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=merged, x='video', y='sd_rot_speed_total',
            hue='dep_group', palette=PALETTE_DEP, ax=ax, order=VIDEO_ORDER)
ax.set_xticklabels([VIDEO_NAMES[v] for v in VIDEO_ORDER], rotation=20, ha='right')
ax.set_xlabel('Video')
ax.set_ylabel('SD of Rotation Speed (°/s)')
ax.set_title('Variability of Rotation Speed by Video and Depression Group')
ax.legend(title='Group')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig9_headtrack_sd_by_group.pdf'))
plt.close()
print("  Saved fig9_headtrack_sd_by_group.pdf")

# --- Fig 10: Angular Range Explored by Video and Group ---
merged['total_range'] = merged['range_rot_x'] + merged['range_rot_y'] + merged['range_rot_z']
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=merged, x='video', y='total_range', hue='dep_group',
            palette=PALETTE_DEP, ci=95, ax=ax, order=VIDEO_ORDER)
ax.set_xticklabels([VIDEO_NAMES[v] for v in VIDEO_ORDER], rotation=20, ha='right')
ax.set_xlabel('Video')
ax.set_ylabel('Total Angular Range Explored (°)')
ax.set_title('Total Angular Range Explored by Video and Depression Group')
ax.legend(title='Group')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig10_angular_range_by_group.pdf'))
plt.close()
print("  Saved fig10_angular_range_by_group.pdf")

# --- Fig 11: PANAS Before and After VR (Grouped Bar) ---
panas_summary = pd.DataFrame({
    'Measure': ['Positive Affect', 'Positive Affect', 'Negative Affect', 'Negative Affect'],
    'Time': ['Pre-VR', 'Post-VR', 'Pre-VR', 'Post-VR'],
    'Mean': [df['positive_affect_start'].mean(), df['positive_affect_end'].mean(),
             df['negative_affect_start'].mean(), df['negative_affect_end'].mean()],
    'SE': [df['positive_affect_start'].sem(), df['positive_affect_end'].sem(),
           df['negative_affect_start'].sem(), df['negative_affect_end'].sem()]
})

fig, ax = plt.subplots(figsize=(6, 4.5))
x = np.arange(2)
width = 0.35
pa_means = [df['positive_affect_start'].mean(), df['positive_affect_end'].mean()]
pa_ses = [df['positive_affect_start'].sem(), df['positive_affect_end'].sem()]
na_means = [df['negative_affect_start'].mean(), df['negative_affect_end'].mean()]
na_ses = [df['negative_affect_start'].sem(), df['negative_affect_end'].sem()]
ax.bar(x - width/2, pa_means, width, yerr=pa_ses, label='Positive Affect',
       color='#4C72B0', capsize=4, edgecolor='white')
ax.bar(x + width/2, na_means, width, yerr=na_ses, label='Negative Affect',
       color='#DD8452', capsize=4, edgecolor='white')
ax.set_xticks(x)
ax.set_xticklabels(['Pre-VR', 'Post-VR'])
ax.set_ylabel('Score')
ax.set_title('PANAS Scores Pre- and Post-VR')
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig11_panas_change.pdf'))
plt.close()
print("  Saved fig11_panas_change.pdf")

# --- Fig 12: Headtracking Yaw Speed (key axis) by Depression Group per Video ---
fig, axes = plt.subplots(1, 5, figsize=(16, 4), sharey=True)
for i, vid in enumerate(VIDEO_ORDER):
    sub = merged[merged['video'] == vid]
    sns.boxplot(data=sub, x='dep_group', y='mean_rot_speed_y', palette=PALETTE_DEP,
                ax=axes[i], order=['Non-Depressed', 'Depressed'])
    axes[i].set_title(VIDEO_NAMES[vid].split(': ')[1], fontsize=10)
    axes[i].set_xlabel('')
    if i == 0:
        axes[i].set_ylabel('Mean Yaw Speed (°/s)')
    else:
        axes[i].set_ylabel('')
fig.suptitle('Mean Yaw (Horizontal) Rotation Speed by Depression Group', fontsize=12, y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig12_yaw_speed_by_group.pdf'))
plt.close()
print("  Saved fig12_yaw_speed_by_group.pdf")

# ══════════════════════════════════════════════════════════════════════════════
# PART 5: PRELIMINARY INFERENTIAL STATISTICS
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PART 5: Preliminary inferential statistics")
print("=" * 70)

# --- 5a. Normality tests for key variables ---
print("\n--- Shapiro-Wilk Normality Tests ---")
for var, label in [('score_phq', 'PHQ-9'), ('score_gad', 'GAD-7'),
                   ('score_stai_t', 'STAI-T')]:
    w, p = shapiro(df[var])
    print(f"  {label}: W={w:.3f}, p={p:.4f} {'(Non-normal)' if p < 0.05 else '(Normal)'}")

# --- 5b. Correlation: PHQ-9 vs GAD-7 ---
print("\n--- Correlation: PHQ-9 vs GAD-7 ---")
r, p = pearsonr(df['score_phq'], df['score_gad'])
rho, p_s = spearmanr(df['score_phq'], df['score_gad'])
print(f"  Pearson r = {r:.3f}, p = {p:.4f}")
print(f"  Spearman ρ = {rho:.3f}, p = {p_s:.4f}")

# --- 5c. Correlation: PHQ-9 vs STAI-T ---
print("\n--- Correlation: PHQ-9 vs STAI-T ---")
r, p = pearsonr(df['score_phq'], df['score_stai_t'])
rho, p_s = spearmanr(df['score_phq'], df['score_stai_t'])
print(f"  Pearson r = {r:.3f}, p = {p:.4f}")
print(f"  Spearman ρ = {rho:.3f}, p = {p_s:.4f}")

# --- 5d. Mann-Whitney U: Headtracking by Depression Group (per video) ---
print("\n--- Mann-Whitney U Tests: Mean Rotation Speed by Depression Group ---")
headtrack_measures = ['mean_rot_speed_total', 'mean_rot_speed_y', 'sd_rot_speed_total',
                      'range_rot_y', 'total_range']
measure_labels = ['Mean Speed (Total)', 'Mean Yaw Speed', 'SD Speed (Total)',
                  'Yaw Range', 'Total Angular Range']

results_table = []
for vid in VIDEO_ORDER:
    sub = merged[merged['video'] == vid]
    dep = sub[sub['dep_group'] == 'Depressed']
    nondep = sub[sub['dep_group'] == 'Non-Depressed']
    print(f"\n  {VIDEO_NAMES[vid]}:")
    for measure, mlabel in zip(headtrack_measures, measure_labels):
        u_stat, p_val = mannwhitneyu(dep[measure], nondep[measure], alternative='two-sided')
        # Effect size: r = Z / sqrt(N)
        z = stats.norm.ppf(1 - p_val / 2) if p_val < 1 else 0
        r_eff = z / np.sqrt(len(dep) + len(nondep))
        sig = '*' if p_val < 0.05 else ''
        print(f"    {mlabel}: U={u_stat:.1f}, p={p_val:.4f}, r={r_eff:.3f} {sig}")
        results_table.append({
            'Video': VIDEO_NAMES[vid],
            'Measure': mlabel,
            'U': u_stat,
            'p': p_val,
            'effect_r': r_eff,
            'Dep_Mean': dep[measure].mean(),
            'Dep_SD': dep[measure].std(),
            'NonDep_Mean': nondep[measure].mean(),
            'NonDep_SD': nondep[measure].std(),
            'Significant': sig,
        })

results_df = pd.DataFrame(results_table)
results_df.to_csv(os.path.join(FIG_DIR, 'mann_whitney_results.csv'), index=False)
print("\n  Results saved to figures/mann_whitney_results.csv")

# --- 5e. PANAS Change: Paired tests ---
print("\n--- PANAS Pre-Post Change (Wilcoxon Signed-Rank) ---")
stat, p = wilcoxon(df['positive_affect_start'], df['positive_affect_end'])
print(f"  Positive Affect: W={stat:.1f}, p={p:.4f}")
stat, p = wilcoxon(df['negative_affect_start'], df['negative_affect_end'])
print(f"  Negative Affect: W={stat:.1f}, p={p:.4f}")

# --- 5f. Correlation: PHQ-9 vs Headtracking (aggregated across videos) ---
print("\n--- Correlation: PHQ-9 vs Headtracking (averaged across videos) ---")
# Average headtracking measures across videos per participant
ht_avg = ht_df.groupby('pid').agg({
    'mean_rot_speed_total': 'mean',
    'mean_rot_speed_y': 'mean',
    'sd_rot_speed_total': 'mean',
}).reset_index()
ht_avg = ht_avg.merge(df[['pid', 'score_phq', 'score_gad', 'score_stai_t']], on='pid')

for measure, mlabel in [('mean_rot_speed_total', 'Mean Total Speed'),
                        ('mean_rot_speed_y', 'Mean Yaw Speed'),
                        ('sd_rot_speed_total', 'SD Total Speed')]:
    r, p = spearmanr(ht_avg['score_phq'], ht_avg[measure])
    print(f"  PHQ-9 vs {mlabel}: Spearman ρ = {r:.3f}, p = {p:.4f}")

# --- 5g. Kruskal-Wallis: Headtracking speed differs across videos? ---
print("\n--- Kruskal-Wallis: Does mean speed differ across videos? ---")
groups = [ht_df[ht_df['video'] == v]['mean_rot_speed_total'] for v in VIDEO_ORDER]
h_stat, p_val = stats.kruskal(*groups)
print(f"  H = {h_stat:.2f}, p = {p_val:.4f}")

# ══════════════════════════════════════════════════════════════════════════════
# PART 6: OUTLIER DETECTION
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PART 6: Outlier detection")
print("=" * 70)

# IQR method for key variables
for var, label in [('score_phq', 'PHQ-9'), ('score_gad', 'GAD-7'), ('score_stai_t', 'STAI-T')]:
    Q1 = df[var].quantile(0.25)
    Q3 = df[var].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[var] < lower) | (df[var] > upper)]
    print(f"  {label}: IQR=[{lower:.1f}, {upper:.1f}], Outliers: {len(outliers)} participants")

# Headtracking outliers (per video)
print("\n  Headtracking speed outliers (|z| > 3):")
for vid in VIDEO_ORDER:
    sub = ht_df[ht_df['video'] == vid]
    z_scores = np.abs(stats.zscore(sub['mean_rot_speed_total']))
    n_out = (z_scores > 3).sum()
    if n_out > 0:
        print(f"    {VIDEO_NAMES[vid]}: {n_out} outlier(s)")
    else:
        print(f"    {VIDEO_NAMES[vid]}: no outliers")

# VRISE outlier check
print(f"\n  VRISE Score: M={df['score_vrise'].mean():.1f}, SD={df['score_vrise'].std():.1f}")
print(f"  VRISE Range: [{df['score_vrise'].min()}, {df['score_vrise'].max()}]")
# Low VRISE may indicate severe sickness → potential exclusion
low_vrise = df[df['score_vrise'] < 20]
print(f"  Participants with VRISE < 20 (potential sickness issues): {len(low_vrise)}")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE - All figures saved to figures/ directory")
print("=" * 70)
