
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests

from ..config import VIDEO_ORDER, VIDEO_NAMES_SHORT


# ---------------------------------------------------------------------------

def run_moderation(merged: pd.DataFrame) -> list:
    results = []
    for vid in VIDEO_ORDER:
        sub = (merged[merged['video'] == vid]
               [['score_phq', 'mean_rot_speed_total', 'immersion_vid', 'score_gad']]
               .dropna()
               .copy())

        sub['phq_z']  = stats.zscore(sub['score_phq'])
        sub['pres_z'] = stats.zscore(sub['immersion_vid'])
        sub['interaction'] = sub['phq_z'] * sub['pres_z']

        model  = smf.ols('mean_rot_speed_total ~ phq_z + pres_z + interaction',
                          data=sub).fit()
        b_int  = model.params['interaction']
        p_int  = model.pvalues['interaction']
        ci_int = model.conf_int().loc['interaction'].values

        results.append({
            'video':             vid,
            'beta_interaction':  round(float(b_int), 3),
            'p_interaction':     round(float(p_int), 4),
            'ci_low':            round(float(ci_int[0]), 3),
            'ci_high':           round(float(ci_int[1]), 3),
            'adj_r2':            round(float(model.rsquared_adj), 3),
        })
        print(f"  [Moderation] {VIDEO_NAMES_SHORT[vid]}: "
              f"interaction beta={b_int:.3f}  p={p_int:.4f}")

    # FDR correction on interaction p-values
    raw_ps = [r['p_interaction'] for r in results]
    _, p_fdr, _, _ = multipletests(raw_ps, method='fdr_bh')
    for i, r in enumerate(results):
        r['p_fdr'] = round(float(p_fdr[i]), 4)

    return results
