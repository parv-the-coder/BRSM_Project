
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests

from ..config import VIDEO_ORDER, VIDEO_NAMES_SHORT


# ---------------------------------------------------------------------------

_MEASURES = [
    ('mean_rot_speed_total', 'Mean Speed (Total)'),
    ('mean_rot_speed_y',     'Mean Yaw Speed'),
    ('sd_rot_speed_total',   'SD Speed'),
    ('range_rot_y',          'Yaw Range'),
    ('total_range',          'Total Range'),
    ('sdy',                  'SDY (Yaw Position SD)'),
]


def run_mcc_comparison(merged: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for vid in VIDEO_ORDER:
        sub  = merged[merged['video'] == vid]
        dep    = sub[sub['dep_group'] == 'Depressed']
        nondep = sub[sub['dep_group'] == 'Non-Depressed']
        for col, label in _MEASURES:
            _, p = mannwhitneyu(dep[col], nondep[col], alternative='two-sided')
            rows.append({'Video': vid, 'Measure': label, 'p_uncorrected': p})

    df = pd.DataFrame(rows)
    raw = df['p_uncorrected'].values

    _, p_bonf, _, _ = multipletests(raw, method='bonferroni')
    _, p_holm, _, _ = multipletests(raw, method='holm')
    _, p_fdr,  _, _ = multipletests(raw, method='fdr_bh')

    df['p_bonferroni'] = p_bonf.round(4)
    df['p_holm']       = p_holm.round(4)
    df['p_fdr_bh']     = p_fdr.round(4)
    df['sig_uncorrected'] = (raw < 0.05)
    df['sig_bonferroni']  = (p_bonf < 0.05)
    df['sig_holm']        = (p_holm < 0.05)
    df['sig_fdr']         = (p_fdr  < 0.05)

    print(f"\n[MCC] k = {len(df)} tests")
    print(f"  Significant (p < 0.05):"
          f"  Uncorrected={df['sig_uncorrected'].sum()}  "
          f"  Bonferroni={df['sig_bonferroni'].sum()}  "
          f"  Holm={df['sig_holm'].sum()}  "
          f"  BH-FDR={df['sig_fdr'].sum()}")

    return df
