
import os
import numpy as np
import pandas as pd
from scipy import stats

from .config import (
    DATA_DIR, HEADTRACK_DIR,
    VIDEO_ORDER, PHQ_CUTOFF,
)


# ---------------------------------------------------------------------------
# Survey data
# ---------------------------------------------------------------------------

def load_survey() -> pd.DataFrame:
    df = pd.read_excel(os.path.join(DATA_DIR, 'data.xlsx'))
    df['pid'] = [f'P{i+1:02d}' for i in range(len(df))]

    # Depression classification
    df['dep_group']  = df['score_phq'].apply(
        lambda x: 'Depressed' if x >= PHQ_CUTOFF else 'Non-Depressed'
    )
    df['dep_binary'] = (df['score_phq'] >= PHQ_CUTOFF).astype(int)

    # PHQ-9 severity bands (Kroenke et al., 2001)
    def _severity(score):
        if score <= 4:   return 'Minimal'
        if score <= 9:   return 'Mild'
        if score <= 14:  return 'Moderate'
        if score <= 19:  return 'Moderately Severe'
        return 'Severe'
    df['phq_severity'] = df['score_phq'].apply(_severity)

    # Labels
    df['gender_label'] = df['gender'].map({1: 'Male', 2: 'Female'})
    df['vr_exp_label'] = df['vr_experience'].map({1: 'No', 2: 'Yes'})

    # PANAS change scores
    df['pa_change'] = df['positive_affect_end'] - df['positive_affect_start']
    df['na_change'] = df['negative_affect_end'] - df['negative_affect_start']

    return df


# ---------------------------------------------------------------------------
# Head-tracking data
# ---------------------------------------------------------------------------

def load_headtracking(df: pd.DataFrame) -> pd.DataFrame:
    records = []
    for _, row in df.iterrows():
        pid = row['pid']
        for vid in VIDEO_ORDER:
            fpath = os.path.join(HEADTRACK_DIR, vid, row[vid])
            if not os.path.exists(fpath):
                print(f'  WARNING: missing {fpath}')
                continue
            ht = pd.read_csv(fpath, on_bad_lines='skip')

            records.append({
                'pid':    pid,
                'video':  vid,
                'duration_s': ht['Time'].max() - ht['Time'].min(),

                # rotation speed (degrees/s)
                'mean_rot_speed_total':   ht['RotationSpeedTotal'].mean(),
                'sd_rot_speed_total':     ht['RotationSpeedTotal'].std(),
                'median_rot_speed_total': ht['RotationSpeedTotal'].median(),
                'mean_rot_speed_x':       ht['RotationSpeedX'].mean(),
                'mean_rot_speed_y':       ht['RotationSpeedY'].mean(),
                'mean_rot_speed_z':       ht['RotationSpeedZ'].mean(),
                'sd_rot_speed_x':         ht['RotationSpeedX'].std(),
                'sd_rot_speed_y':         ht['RotationSpeedY'].std(),
                'sd_rot_speed_z':         ht['RotationSpeedZ'].std(),

                # absolute rotation change
                'mean_abs_rot_y': ht['RotationChangeY'].abs().mean(),

                # angular range explored
                'range_rot_x': ht['RotationChangeX'].max() - ht['RotationChangeX'].min(),
                'range_rot_y': ht['RotationChangeY'].max() - ht['RotationChangeY'].min(),
                'range_rot_z': ht['RotationChangeZ'].max() - ht['RotationChangeZ'].min(),

                # SD of yaw position (SDY) -- key measure in Srivastava et al.
                'sdy': ht['RotationChangeY'].std(),

                # peak speed burst
                'max_rot_speed_total': ht['RotationSpeedTotal'].max(),
            })

    ht_df = pd.DataFrame(records)
    ht_df['total_range'] = (
        ht_df['range_rot_x'] + ht_df['range_rot_y'] + ht_df['range_rot_z']
    )
    return ht_df


# ---------------------------------------------------------------------------
# Merged dataset  (participant survey + per-video headtracking)
# ---------------------------------------------------------------------------

def build_merged(df: pd.DataFrame, ht_df: pd.DataFrame) -> pd.DataFrame:
    merged = df.merge(ht_df, on='pid', how='inner')

    # Attach the correct video-level ratings to each row
    valence_col  = []
    arousal_col  = []
    immersion_col = []
    for _, row in merged.iterrows():
        vid = row['video']
        valence_col.append(row[f'valence_{vid}'])
        arousal_col.append(row[f'arousal_{vid}'])
        immersion_col.append(row[f'immersion_{vid}'])

    merged['valence_vid']   = valence_col
    merged['arousal_vid']   = arousal_col
    merged['immersion_vid'] = immersion_col

    # Standardised predictors (computed on full merged set)
    for col in ['score_phq', 'score_gad', 'score_stai_t']:
        merged[f'{col.replace("score_", "")}_z'] = stats.zscore(merged[col])

    return merged


# ---------------------------------------------------------------------------
# Long-format subjective-ratings table
# ---------------------------------------------------------------------------

def build_subjective(df: pd.DataFrame) -> pd.DataFrame:
    records = []
    for _, row in df.iterrows():
        for vid in VIDEO_ORDER:
            records.append({
                'pid':          row['pid'],
                'video':        vid,
                'score_phq':    row['score_phq'],
                'score_gad':    row['score_gad'],
                'score_stai_t': row['score_stai_t'],
                'dep_group':    row['dep_group'],
                'valence':      row[f'valence_{vid}'],
                'arousal':      row[f'arousal_{vid}'],
                'presence':     row[f'immersion_{vid}'],
            })
    subj = pd.DataFrame(records)
    subj['phq_z'] = stats.zscore(subj['score_phq'])
    return subj
