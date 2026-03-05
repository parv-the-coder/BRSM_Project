"""
data_loading.py — Load and preprocess survey + headtracking data.
"""

import os
import pandas as pd
from config import DATA_DIR, HEADTRACK_DIR, VIDEO_ORDER, PHQ_CUTOFF


def phq_severity(score):
    """Classify PHQ-9 score into clinical severity categories."""
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


def load_survey_data():
    """Load and preprocess the survey Excel data. Returns a DataFrame."""
    df = pd.read_excel(os.path.join(DATA_DIR, 'data.xlsx'))

    # Participant IDs
    df['pid'] = [f'P{i+1:02d}' for i in range(len(df))]

    # Depression group
    df['dep_group'] = df['score_phq'].apply(
        lambda x: 'Depressed' if x >= PHQ_CUTOFF else 'Non-Depressed'
    )

    # PHQ-9 severity
    df['phq_severity'] = df['score_phq'].apply(phq_severity)

    # Label mappings
    df['gender_label'] = df['gender'].map({1: 'Male', 2: 'Female'})
    df['vr_exp_label'] = df['vr_experience'].map({1: 'No', 2: 'Yes'})

    # PANAS change scores
    df['pa_change'] = df['positive_affect_end'] - df['positive_affect_start']
    df['na_change'] = df['negative_affect_end'] - df['negative_affect_start']

    return df


def load_headtracking_data(df):
    """
    Load all headtracking CSVs and compute summary measures per participant
    per video. Returns a DataFrame of summary records.
    """
    records = []

    for _, row in df.iterrows():
        pid = row['pid']
        for vid in VIDEO_ORDER:
            fname = row[vid]
            fpath = os.path.join(HEADTRACK_DIR, vid, fname)
            if not os.path.exists(fpath):
                print(f"  WARNING: Missing file {fpath}")
                continue

            ht = pd.read_csv(fpath, on_bad_lines='skip')
            duration = ht['Time'].max() - ht['Time'].min()

            record = {
                'pid': pid,
                'video': vid,
                'duration_s': duration,
                # Mean rotation speed
                'mean_rot_speed_total': ht['RotationSpeedTotal'].mean(),
                'mean_rot_speed_x': ht['RotationSpeedX'].mean(),
                'mean_rot_speed_y': ht['RotationSpeedY'].mean(),
                'mean_rot_speed_z': ht['RotationSpeedZ'].mean(),
                # SD of rotation speed
                'sd_rot_speed_total': ht['RotationSpeedTotal'].std(),
                'sd_rot_speed_x': ht['RotationSpeedX'].std(),
                'sd_rot_speed_y': ht['RotationSpeedY'].std(),
                'sd_rot_speed_z': ht['RotationSpeedZ'].std(),
                # Median rotation speed
                'median_rot_speed_total': ht['RotationSpeedTotal'].median(),
                # Mean absolute rotation change
                'mean_abs_rot_x': ht['RotationChangeX'].abs().mean(),
                'mean_abs_rot_y': ht['RotationChangeY'].abs().mean(),
                'mean_abs_rot_z': ht['RotationChangeZ'].abs().mean(),
                # SD of rotation change
                'sd_rot_change_x': ht['RotationChangeX'].std(),
                'sd_rot_change_y': ht['RotationChangeY'].std(),
                'sd_rot_change_z': ht['RotationChangeZ'].std(),
                # Range of rotation change
                'range_rot_x': ht['RotationChangeX'].max() - ht['RotationChangeX'].min(),
                'range_rot_y': ht['RotationChangeY'].max() - ht['RotationChangeY'].min(),
                'range_rot_z': ht['RotationChangeZ'].max() - ht['RotationChangeZ'].min(),
                # Max speed
                'max_rot_speed_total': ht['RotationSpeedTotal'].max(),
            }
            records.append(record)

    ht_df = pd.DataFrame(records)
    return ht_df


def build_merged_dataset(df, ht_df):
    """Merge survey data with headtracking summaries. Returns merged DataFrame."""
    merged = df.merge(ht_df, on='pid', how='inner')
    merged['total_range'] = (merged['range_rot_x'] +
                             merged['range_rot_y'] +
                             merged['range_rot_z'])
    return merged
