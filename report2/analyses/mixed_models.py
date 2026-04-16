
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

from ..config import VIDEO_ORDER


# ---------------------------------------------------------------------------

def run_lmm(merged: pd.DataFrame) -> dict:
    lmm_data = (merged[['pid', 'video', 'mean_rot_speed_total',
                          'score_phq', 'score_gad', 'score_stai_t']]
                .copy().dropna())

    lmm_data['phq_z']  = stats.zscore(lmm_data['score_phq'])
    lmm_data['gad_z']  = stats.zscore(lmm_data['score_gad'])
    lmm_data['stai_z'] = stats.zscore(lmm_data['score_stai_t'])

    # -- REML fits (for parameter estimates) --------------------------------
    lmm2 = smf.mixedlm(
        'mean_rot_speed_total ~ phq_z + C(video)',
        lmm_data, groups=lmm_data['pid'],
    ).fit(reml=True)

    lmm3 = smf.mixedlm(
        'mean_rot_speed_total ~ phq_z + gad_z + C(video)',
        lmm_data, groups=lmm_data['pid'],
    ).fit(reml=True)

    # -- ML fits (for AIC comparison) ----------------------------------------
    lmm2_ml = smf.mixedlm(
        'mean_rot_speed_total ~ phq_z + C(video)',
        lmm_data, groups=lmm_data['pid'],
    ).fit(reml=False)

    lmm3_ml = smf.mixedlm(
        'mean_rot_speed_total ~ phq_z + gad_z + C(video)',
        lmm_data, groups=lmm_data['pid'],
    ).fit(reml=False)

    lmm4_ml = smf.mixedlm(
        'mean_rot_speed_total ~ phq_z * C(video)',
        lmm_data, groups=lmm_data['pid'],
    ).fit(reml=False)

    # -- ICC -----------------------------------------------------------------
    re_var  = float(lmm2.cov_re.values[0][0])
    res_var = float(lmm2.scale)
    icc     = re_var / (re_var + res_var)

    # -- Random effects distribution -----------------------------------------
    re_vals      = lmm2.random_effects
    re_intercepts = [v['Group'] for v in re_vals.values()]

    print(f"\n[LMM] ICC = {icc:.3f}  "
          f"(sigma2_between={re_var:.2f}, sigma2_within={res_var:.2f})")
    print(f"  Model 2  PHQ beta = {lmm2.params['phq_z']:.3f}  "
          f"SE={lmm2.bse['phq_z']:.3f}  p={lmm2.pvalues['phq_z']:.4f}  "
          f"AIC={lmm2_ml.aic:.1f}")
    print(f"  Model 3  PHQ beta = {lmm3.params['phq_z']:.3f}  "
          f"SE={lmm3.bse['phq_z']:.3f}  p={lmm3.pvalues['phq_z']:.4f}  "
          f"AIC={lmm3_ml.aic:.1f}")
    print(f"  Model 4  (PHQ x video interaction)  AIC={lmm4_ml.aic:.1f}")

    phq_ci2 = lmm2.conf_int().loc['phq_z'].values
    phq_ci3 = lmm3.conf_int().loc['phq_z'].values

    return {
        'model2_phq_beta': round(float(lmm2.params['phq_z']), 3),
        'model2_phq_se':   round(float(lmm2.bse['phq_z']), 3),
        'model2_phq_p':    round(float(lmm2.pvalues['phq_z']), 4),
        'model2_phq_ci':   [round(float(phq_ci2[0]), 3), round(float(phq_ci2[1]), 3)],
        'model2_aic':      round(float(lmm2_ml.aic), 2),
        'model2_bic':      round(float(lmm2_ml.bic), 2),

        'model3_phq_beta': round(float(lmm3.params['phq_z']), 3),
        'model3_phq_se':   round(float(lmm3.bse['phq_z']), 3),
        'model3_phq_p':    round(float(lmm3.pvalues['phq_z']), 4),
        'model3_phq_ci':   [round(float(phq_ci3[0]), 3), round(float(phq_ci3[1]), 3)],
        'model3_gad_beta': round(float(lmm3.params['gad_z']), 3),
        'model3_gad_p':    round(float(lmm3.pvalues['gad_z']), 4),
        'model3_aic':      round(float(lmm3_ml.aic), 2),
        'model3_bic':      round(float(lmm3_ml.bic), 2),

        'model4_aic':      round(float(lmm4_ml.aic), 2),

        'icc':             round(icc, 3),
        're_var':          round(re_var, 2),
        'res_var':         round(res_var, 2),
        're_sd':           round(float(np.sqrt(re_var)), 2),
        'res_sd':          round(float(np.sqrt(res_var)), 2),
        're_intercepts':   re_intercepts,

        # expose fitted objects for plotting
        'lmm2': lmm2,
        'lmm3': lmm3,
    }
