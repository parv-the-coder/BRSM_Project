import os
import numpy as np
from scipy import stats
from config import FIG_DIR, VIDEO_NAMES, VIDEO_ORDER


def print_demographics(df):
    print("\n--- Demographics ---")
    print(f"N = {len(df)}")
    print(f"Age: M={df['age'].mean():.1f}, SD={df['age'].std():.1f}, "
          f"Range=[{df['age'].min()}, {df['age'].max()}]")
    print(f"Gender: Male={df['gender_label'].value_counts().get('Male', 0)}, "
          f"Female={df['gender_label'].value_counts().get('Female', 0)}")
    print(f"VR Experience: Yes={df['vr_exp_label'].value_counts().get('Yes', 0)}, "
          f"No={df['vr_exp_label'].value_counts().get('No', 0)}")


def print_clinical_scores(df):
    print("\n--- Clinical Scores ---")
    for var, label in [('score_phq', 'PHQ-9'), ('score_gad', 'GAD-7'),
                       ('score_stai_t', 'STAI-T')]:
        print(f"{label}: M={df[var].mean():.2f}, SD={df[var].std():.2f}, "
              f"Mdn={df[var].median():.1f}, Range=[{df[var].min()}, {df[var].max()}]")

    print(f"\nPHQ-9 Severity Distribution:")
    for cat in ['Minimal', 'Mild', 'Moderate', 'Moderately Severe', 'Severe']:
        n = (df['phq_severity'] == cat).sum()
        print(f"  {cat}: {n} ({n / len(df) * 100:.1f}%)")


def print_panas(df):
    print("\n--- PANAS Scores ---")
    for var, label in [('positive_affect_start', 'PA Pre'),
                       ('positive_affect_end', 'PA Post'),
                       ('negative_affect_start', 'NA Pre'),
                       ('negative_affect_end', 'NA Post')]:
        print(f"{label}: M={df[var].mean():.2f}, SD={df[var].std():.2f}")


def print_video_ratings(df):
    print("\n--- Valence & Arousal per Video ---")
    for vid in VIDEO_ORDER:
        val = df[f'valence_{vid}']
        aro = df[f'arousal_{vid}']
        imm = df[f'immersion_{vid}']
        print(f"{VIDEO_NAMES[vid]}:  Valence M={val.mean():.2f}(SD={val.std():.2f})  "
              f"Arousal M={aro.mean():.2f}(SD={aro.std():.2f})  "
              f"Presence M={imm.mean():.2f}(SD={imm.std():.2f})")


def print_headtracking_by_video(ht_df):
    print("\n--- Headtracking Mean Rotation Speed by Video ---")
    for vid in VIDEO_ORDER:
        sub = ht_df[ht_df['video'] == vid]
        print(f"{VIDEO_NAMES[vid]}:  MeanSpeed M={sub['mean_rot_speed_total'].mean():.2f}"
              f"(SD={sub['mean_rot_speed_total'].std():.2f})")


def print_headtracking_by_group(merged):
    print("\n--- Headtracking by Depression Group ---")
    for vid in VIDEO_ORDER:
        sub = merged[merged['video'] == vid]
        for grp in ['Non-Depressed', 'Depressed']:
            g = sub[sub['dep_group'] == grp]
            print(f"  {VIDEO_NAMES[vid]} | {grp}: MeanSpeed "
                  f"M={g['mean_rot_speed_total'].mean():.2f}"
                  f"(SD={g['mean_rot_speed_total'].std():.2f}), n={len(g)}")


def save_descriptive_table(df):
    desc = df[['age', 'score_phq', 'score_gad', 'score_stai_t', 'score_vrise',
               'positive_affect_start', 'negative_affect_start',
               'positive_affect_end', 'negative_affect_end']].describe().round(2)
    path = os.path.join(FIG_DIR, 'descriptive_stats.csv')
    desc.to_csv(path)
    print(f"\nDescriptive stats saved to {path}")


def print_outlier_analysis(df, ht_df):
    print("\n--- Outlier Detection ---")

    # IQR for clinical scores
    for var, label in [('score_phq', 'PHQ-9'), ('score_gad', 'GAD-7'),
                       ('score_stai_t', 'STAI-T')]:
        Q1 = df[var].quantile(0.25)
        Q3 = df[var].quantile(0.75)
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        outliers = df[(df[var] < lower) | (df[var] > upper)]
        print(f"  {label}: IQR=[{lower:.1f}, {upper:.1f}], "
              f"Outliers: {len(outliers)} participants")

    # z-score for headtracking
    print("\n  Headtracking speed outliers (|z| > 3):")
    for vid in VIDEO_ORDER:
        sub = ht_df[ht_df['video'] == vid]
        z_scores = np.abs(stats.zscore(sub['mean_rot_speed_total']))
        n_out = (z_scores > 3).sum()
        status = f"{n_out} outlier(s)" if n_out > 0 else "no outliers"
        print(f"    {VIDEO_NAMES[vid]}: {status}")

    # VRISE
    print(f"\n  VRISE Score: M={df['score_vrise'].mean():.1f}, "
          f"SD={df['score_vrise'].std():.1f}")
    print(f"  VRISE Range: [{df['score_vrise'].min()}, {df['score_vrise'].max()}]")
    low_vrise = df[df['score_vrise'] < 20]
    print(f"  Participants with VRISE < 20 (potential sickness): {len(low_vrise)}")


def run_descriptive_stats(df, ht_df, merged):
    print("=" * 70)
    print("DESCRIPTIVE STATISTICS")
    print("=" * 70)
    print_demographics(df)
    print_clinical_scores(df)
    print_panas(df)
    print_video_ratings(df)
    print_headtracking_by_video(ht_df)
    print_headtracking_by_group(merged)
    save_descriptive_table(df)

    print("\n" + "=" * 70)
    print("OUTLIER DETECTION")
    print("=" * 70)
    print_outlier_analysis(df, ht_df)
