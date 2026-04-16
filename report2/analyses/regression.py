
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multitest import multipletests

from ..config import VIDEO_ORDER, VIDEO_NAMES_SHORT


# ---------------------------------------------------------------------------

def run_simple_regression(merged: pd.DataFrame) -> list:
    results = []
    for vid in VIDEO_ORDER:
        sub = (merged[merged['video'] == vid]
               [['score_phq', 'mean_rot_speed_total', 'dep_group']]
               .dropna())

        model = smf.ols('mean_rot_speed_total ~ score_phq', data=sub).fit()
        b     = model.params['score_phq']
        p     = model.pvalues['score_phq']
        r2    = model.rsquared
        ci    = model.conf_int().loc['score_phq'].values

        # non-parametric complement
        rho, p_rho = stats.spearmanr(sub['score_phq'], sub['mean_rot_speed_total'])

        results.append({
            'video':    vid,
            'beta':     round(b, 3),
            'p':        round(p, 4),
            'r2':       round(r2, 3),
            'ci_low':   round(ci[0], 3),
            'ci_high':  round(ci[1], 3),
            'spearman_rho': round(rho, 3),
            'spearman_p':   round(p_rho, 4),
        })

    # Multiple comparison corrections across the 5 p-values
    raw_ps = [r['p'] for r in results]
    _, p_fdr,  _, _ = multipletests(raw_ps, method='fdr_bh')
    _, p_holm, _, _ = multipletests(raw_ps, method='holm')
    for i, r in enumerate(results):
        r['p_fdr']  = round(p_fdr[i],  4)
        r['p_holm'] = round(p_holm[i], 4)
        r['sig_fdr'] = bool(p_fdr[i] < 0.05)

    print("\n[Simple Regression] PHQ-9 -> mean rotation speed per video")
    for r in results:
        print(f"  {VIDEO_NAMES_SHORT[r['video']]}: beta={r['beta']:.3f} "
              f"[{r['ci_low']}, {r['ci_high']}], p={r['p']:.4f}, "
              f"p_FDR={r['p_fdr']:.4f}, R2={r['r2']:.3f}")

    return results


# ---------------------------------------------------------------------------

def run_ancova(merged: pd.DataFrame) -> list:
    results = []
    for vid in VIDEO_ORDER:
        sub = (merged[merged['video'] == vid]
               [['score_phq', 'mean_rot_speed_total', 'score_gad', 'score_stai_t']]
               .dropna()
               .copy())

        sub['phq_z']  = stats.zscore(sub['score_phq'])
        sub['gad_z']  = stats.zscore(sub['score_gad'])
        sub['stai_z'] = stats.zscore(sub['score_stai_t'])

        model       = smf.ols('mean_rot_speed_total ~ phq_z + gad_z + stai_z', data=sub).fit()
        anova_table = anova_lm(model, typ=2)

        b_phq  = model.params['phq_z']
        p_phq  = model.pvalues['phq_z']
        ci_phq = model.conf_int().loc['phq_z'].values
        adj_r2 = model.rsquared_adj
        F_phq  = float(anova_table.loc['phq_z', 'F']) if 'F' in anova_table.columns else None

        results.append({
            'video':      vid,
            'beta_phq':   round(b_phq, 3),
            'p_phq':      round(p_phq, 4),
            'ci_low':     round(ci_phq[0], 3),
            'ci_high':    round(ci_phq[1], 3),
            'adj_r2':     round(adj_r2, 3),
            'F_phq':      round(F_phq, 3) if F_phq else None,
        })

    # FDR and Holm corrections
    raw_ps = [r['p_phq'] for r in results]
    _, p_fdr,  _, _ = multipletests(raw_ps, method='fdr_bh')
    _, p_holm, _, _ = multipletests(raw_ps, method='holm')
    for i, r in enumerate(results):
        r['p_fdr']  = round(p_fdr[i],  4)
        r['p_holm'] = round(p_holm[i], 4)

    print("\n[ANCOVA] PHQ-9 (controlling for GAD-7, STAI-T) -> speed per video")
    for r in results:
        print(f"  {VIDEO_NAMES_SHORT[r['video']]}: beta_PHQ={r['beta_phq']:.3f} "
              f"[{r['ci_low']}, {r['ci_high']}], p={r['p_phq']:.4f}, "
              f"p_FDR={r['p_fdr']:.4f}, adjR2={r['adj_r2']:.3f}")

    return results
