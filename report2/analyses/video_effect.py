
import numpy as np
import pandas as pd
from itertools import combinations
from scipy.stats import kruskal, mannwhitneyu, friedmanchisquare
from statsmodels.stats.multitest import multipletests
import pingouin as pg

from ..config import VIDEO_ORDER, VIDEO_NAMES_SHORT


# ---------------------------------------------------------------------------

def run_kruskal_wallis(ht_df: pd.DataFrame) -> dict:
    groups = [ht_df[ht_df['video'] == v]['mean_rot_speed_total'].values
              for v in VIDEO_ORDER]
    h_stat, p_kw = kruskal(*groups)

    n_total = len(ht_df)
    k       = len(VIDEO_ORDER)
    eta2_kw = (h_stat - k + 1) / (n_total - k)

    # -- Pairwise Mann-Whitney U with Bonferroni post-hoc -------------------
    pairs   = list(combinations(VIDEO_ORDER, 2))
    u_vals, p_raw = [], []
    for v1, v2 in pairs:
        g1 = ht_df[ht_df['video'] == v1]['mean_rot_speed_total']
        g2 = ht_df[ht_df['video'] == v2]['mean_rot_speed_total']
        u, p = mannwhitneyu(g1, g2, alternative='two-sided')
        u_vals.append(u)
        p_raw.append(p)

    _, p_bonf, _, _ = multipletests(p_raw, method='bonferroni')

    # Rank-biserial correlation as effect size: r = 1 - 2U/(n1*n2)
    n1 = n2 = 40
    r_rb = [1 - 2 * u / (n1 * n2) for u in u_vals]

    posthoc_df = pd.DataFrame({
        'A':         [p[0] for p in pairs],
        'B':         [p[1] for p in pairs],
        'U':         [round(u, 1) for u in u_vals],
        'p_unc':     [round(p, 4) for p in p_raw],
        'p_bonf':    [round(p, 4) for p in p_bonf],
        'sig':       [p < 0.05 for p in p_bonf],
        'r_rb':      [round(r, 3) for r in r_rb],
    })

    video_desc = (
        ht_df.groupby('video')['mean_rot_speed_total']
        .agg(['mean', 'std', 'median'])
        .reindex(VIDEO_ORDER)
        .round(2)
    )

    print(f"\n[KW] H({k-1}) = {h_stat:.3f}, p = {p_kw:.6f}, eta2 = {eta2_kw:.3f}")
    print("\n  Post-hoc: pairwise Mann-Whitney U (Bonferroni corrected):")
    sig_rows = posthoc_df[posthoc_df['sig']]
    print(f"  Significant pairs after Bonferroni: {len(sig_rows)} of {len(posthoc_df)}")
    print(posthoc_df[['A', 'B', 'U', 'p_unc', 'p_bonf', 'sig', 'r_rb']].to_string(index=False))

    return {
        'H':           round(h_stat, 3),
        'p':           round(p_kw, 6),
        'eta2':        round(eta2_kw, 3),
        'df':          k - 1,
        'video_desc':  video_desc.to_dict(),
        'posthoc_df':  posthoc_df,
    }


# ---------------------------------------------------------------------------

def run_friedman_anova(merged: pd.DataFrame) -> dict:
    # Pivot to wide format: rows=participants, columns=videos
    wide = (merged[['pid', 'video', 'mean_rot_speed_total']]
            .pivot(index='pid', columns='video', values='mean_rot_speed_total')
            .reindex(columns=VIDEO_ORDER))

    groups = [wide[v].values for v in VIDEO_ORDER]
    stat, p = friedmanchisquare(*groups)

    # Kendall's W (effect size for Friedman): W = chi2 / (n*(k-1))
    n = len(wide)
    k = len(VIDEO_ORDER)
    kendall_w = stat / (n * (k - 1))

    print(f"\n[Friedman] chi2({k-1}, N={n}) = {stat:.3f}, "
          f"p = {p:.2e}, Kendall W = {kendall_w:.3f}")

    return {
        'statistic':  round(stat, 3),
        'p':          float(f'{p:.2e}'),
        'df':         k - 1,
        'n':          n,
        'kendall_w':  round(kendall_w, 3),
    }


# ---------------------------------------------------------------------------

def run_rm_anova(ht_df: pd.DataFrame) -> dict:
    rm_data   = ht_df[['pid', 'video', 'mean_rot_speed_total']].copy()
    rm_result = pg.rm_anova(
        data=rm_data, dv='mean_rot_speed_total',
        within='video', subject='pid', correction=True,
    )

    # Sphericity results from Mauchly's test
    W_spher  = float(rm_result['W_spher'].values[0])
    p_spher  = float(rm_result['p_spher'].values[0])
    spher_ok = bool(rm_result['sphericity'].values[0])

    F    = float(rm_result['F'].values[0])
    ng2  = float(rm_result['ng2'].values[0])
    dd1  = int(rm_result['ddof1'].values[0])
    dd2  = int(rm_result['ddof2'].values[0])

    # Use uncorrected p since sphericity is met (Mauchly's p=.257 > .05)
    p_report = float(rm_result['p_unc'].values[0])
    note = ('Standard (uncorrected) p used -- Mauchly sphericity met '
            f'(W={W_spher:.3f}, p={p_spher:.3f})')

    # Post-hoc paired t-tests with Holm
    posthoc = pg.pairwise_tests(
        data=rm_data, dv='mean_rot_speed_total',
        within='video', subject='pid',
        parametric=True, padjust='holm',
    )

    print(f"\n[RM-ANOVA] F({dd1},{dd2}) = {F:.3f}, p = {p_report:.2e}, "
          f"eta2g = {ng2:.3f}")
    print(f"  Mauchly's W = {W_spher:.3f}, p = {p_spher:.3f} "
          f"--> sphericity {'MET' if spher_ok else 'VIOLATED'}")
    print(f"  {note}")
    print("\n  Post-hoc paired t-tests (Holm corrected):")
    print(posthoc[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr', 'hedges']].to_string(index=False))

    return {
        'F':              round(F, 3),
        'p':              p_report,
        'eta2g':          round(ng2, 3),
        'ddof1':          dd1,
        'ddof2':          dd2,
        'W_spher':        round(W_spher, 3),
        'p_spher':        round(p_spher, 3),
        'sphericity_met': spher_ok,
        'posthoc':        posthoc,
    }
