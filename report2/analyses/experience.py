
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, wilcoxon
import statsmodels.formula.api as smf

from ..config import VIDEO_ORDER


# ---------------------------------------------------------------------------

def run_subjective_ratings(subj_df: pd.DataFrame) -> list:
    results = []
    for dv in ['valence', 'arousal', 'presence']:
        model = smf.mixedlm(
            f'{dv} ~ phq_z + C(video)', subj_df,
            groups=subj_df['pid'],
        ).fit(reml=True)

        b  = model.params['phq_z']
        p  = model.pvalues['phq_z']
        ci = model.conf_int().loc['phq_z'].values

        results.append({
            'dv':      dv,
            'beta':    round(float(b), 3),
            'p':       round(float(p), 4),
            'ci_low':  round(float(ci[0]), 3),
            'ci_high': round(float(ci[1]), 3),
        })
        print(f"  [Subj LMM] {dv:10s}: beta={b:.3f}  "
              f"[{ci[0]:.3f}, {ci[1]:.3f}]  p={p:.4f}")

    return results


# ---------------------------------------------------------------------------

def run_panas_analysis(df: pd.DataFrame) -> dict:
    groups_out = {}
    for grp in ['Non-Depressed', 'Depressed']:
        sub = df[df['dep_group'] == grp]
        n   = len(sub)

        pa_pre  = sub['positive_affect_start']
        pa_post = sub['positive_affect_end']
        na_pre  = sub['negative_affect_start']
        na_post = sub['negative_affect_end']

        stat_pa, p_pa = wilcoxon(pa_pre, pa_post)
        stat_na, p_na = wilcoxon(na_pre, na_post)

        pa_diff = pa_post - pa_pre
        na_diff = na_post - na_pre
        d_pa = float(pa_diff.mean() / pa_diff.std()) if pa_diff.std() > 0 else 0.0
        d_na = float(na_diff.mean() / na_diff.std()) if na_diff.std() > 0 else 0.0

        groups_out[grp] = {
            'n': n,
            'pa_pre':   round(float(pa_pre.mean()),  2),
            'pa_post':  round(float(pa_post.mean()), 2),
            'pa_delta': round(float(pa_diff.mean()), 2),
            'pa_W':     round(float(stat_pa), 1),
            'pa_p':     round(float(p_pa), 4),
            'pa_d':     round(d_pa, 2),
            'na_pre':   round(float(na_pre.mean()),  2),
            'na_post':  round(float(na_post.mean()), 2),
            'na_delta': round(float(na_diff.mean()), 2),
            'na_W':     round(float(stat_na), 1),
            'na_p':     round(float(p_na), 4),
            'na_d':     round(d_na, 2),
        }
        print(f"\n  [PANAS] {grp} (n={n}):")
        print(f"    PA: pre={pa_pre.mean():.2f} post={pa_post.mean():.2f} "
              f"delta={pa_diff.mean():.2f}  W={stat_pa:.1f}  p={p_pa:.4f}  d={d_pa:.2f}")
        print(f"    NA: pre={na_pre.mean():.2f} post={na_post.mean():.2f} "
              f"delta={na_diff.mean():.2f}  W={stat_na:.1f}  p={p_na:.4f}  d={d_na:.2f}")

    # Between-group comparison of change scores
    dep_sub    = df[df['dep_group'] == 'Depressed']
    nondep_sub = df[df['dep_group'] == 'Non-Depressed']
    u_pa, p_pa_bg = mannwhitneyu(dep_sub['pa_change'], nondep_sub['pa_change'],
                                  alternative='two-sided')
    u_na, p_na_bg = mannwhitneyu(dep_sub['na_change'], nondep_sub['na_change'],
                                  alternative='two-sided')

    print(f"\n  Between-group PA change: U={u_pa:.1f}  p={p_pa_bg:.4f}")
    print(f"  Between-group NA change: U={u_na:.1f}  p={p_na_bg:.4f}")

    return {
        'by_group':            groups_out,
        'pa_between_U':        round(float(u_pa), 1),
        'pa_between_p':        round(float(p_pa_bg), 4),
        'na_between_U':        round(float(u_na), 1),
        'na_between_p':        round(float(p_na_bg), 4),
    }
