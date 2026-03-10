import os
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import pearsonr, shapiro, ttest_ind, ttest_rel, f_oneway

from config import FIG_DIR, VIDEO_NAMES, VIDEO_ORDER


def cohens_d(g1, g2):
    n1, n2 = len(g1), len(g2)
    var1, var2 = g1.var(ddof=1), g2.var(ddof=1)
    pooled_sd = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_sd == 0:
        return 0.0
    return (g1.mean() - g2.mean()) / pooled_sd


def cohens_d_paired(pre, post):
    diff = post - pre
    if diff.std(ddof=1) == 0:
        return 0.0
    return diff.mean() / diff.std(ddof=1)


def bonferroni_correct(p_values, alpha=0.05):
    m = len(p_values)
    adjusted_alpha = alpha / m
    return adjusted_alpha, [p < adjusted_alpha for p in p_values]


def test_normality(df):
    print("\n--- Shapiro-Wilk Normality Tests ---")
    for var, label in [('score_phq', 'PHQ-9'), ('score_gad', 'GAD-7'),
                       ('score_stai_t', 'STAI-T')]:
        w, p = shapiro(df[var])
        verdict = '(Non-normal)' if p < 0.05 else '(Normal)'
        print(f"  {label}: W={w:.3f}, p={p:.4f} {verdict}")
    print("  Note: t-tests are robust to moderate non-normality (CLT, Topic 4).")


def test_clinical_correlations(df):
    print("\n--- Pearson Correlation: PHQ-9 vs GAD-7 ---")
    r, p = pearsonr(df['score_phq'], df['score_gad'])
    print(f"  Pearson r = {r:.3f}, p = {p:.4f}")

    print("\n--- Pearson Correlation: PHQ-9 vs STAI-T ---")
    r, p = pearsonr(df['score_phq'], df['score_stai_t'])
    print(f"  Pearson r = {r:.3f}, p = {p:.4f}")


def test_headtracking_group_differences(merged):
    print("\n--- Welch's t-tests: Headtracking by Depression Group ---")

    measures = ['mean_rot_speed_total', 'mean_rot_speed_y', 'sd_rot_speed_total',
                'range_rot_y', 'total_range']
    labels = ['Mean Speed (Total)', 'Mean Yaw Speed', 'SD Speed (Total)',
              'Yaw Range', 'Total Angular Range']

    results = []
    all_pvalues = []

    for vid in VIDEO_ORDER:
        sub = merged[merged['video'] == vid]
        dep = sub[sub['dep_group'] == 'Depressed']
        nondep = sub[sub['dep_group'] == 'Non-Depressed']
        print(f"\n  {VIDEO_NAMES[vid]}:")

        for measure, mlabel in zip(measures, labels):
            t_stat, p = ttest_ind(dep[measure], nondep[measure],
                                  equal_var=False)  # Welch's
            d = cohens_d(dep[measure], nondep[measure])
            all_pvalues.append(p)
            print(f"    {mlabel}: t={t_stat:.3f}, p={p:.4f}, Cohen's d={d:.3f}")
            results.append({
                'Video': VIDEO_NAMES[vid], 'Measure': mlabel,
                't': t_stat, 'p': p, 'Cohens_d': d,
                'Dep_Mean': dep[measure].mean(),
                'Dep_SD': dep[measure].std(),
                'NonDep_Mean': nondep[measure].mean(),
                'NonDep_SD': nondep[measure].std(),
            })

    # Bonferroni correction (Topic 6)
    adj_alpha, sig_flags = bonferroni_correct(all_pvalues)
    print(f"\n  Bonferroni-corrected α = 0.05 / {len(all_pvalues)} = {adj_alpha:.4f}")
    for i, row in enumerate(results):
        row['Bonferroni_sig'] = '*' if sig_flags[i] else ''
        row['Significant_uncorrected'] = '*' if row['p'] < 0.05 else ''
    n_sig_raw = sum(1 for r in results if r['Significant_uncorrected'] == '*')
    n_sig_bonf = sum(1 for r in results if r['Bonferroni_sig'] == '*')
    print(f"  Significant at α=.05 (uncorrected): {n_sig_raw}/{len(results)}")
    print(f"  Significant after Bonferroni: {n_sig_bonf}/{len(results)}")

    results_df = pd.DataFrame(results)
    path = os.path.join(FIG_DIR, 'ttest_results.csv')
    results_df.to_csv(path, index=False)
    print(f"\n  Results saved to {path}")


def test_panas_change(df):
    print("\n--- PANAS Pre-Post Change (Paired t-test) ---")
    t, p = ttest_rel(df['positive_affect_start'], df['positive_affect_end'])
    d = cohens_d_paired(df['positive_affect_start'], df['positive_affect_end'])
    print(f"  Positive Affect: t={t:.3f}, p={p:.4f}, Cohen's d={d:.3f}")

    t, p = ttest_rel(df['negative_affect_start'], df['negative_affect_end'])
    d = cohens_d_paired(df['negative_affect_start'], df['negative_affect_end'])
    print(f"  Negative Affect: t={t:.3f}, p={p:.4f}, Cohen's d={d:.3f}")


def test_phq_headtracking_correlation(df, ht_df):
    print("\n--- Pearson Correlation: PHQ-9 vs Headtracking (averaged across videos) ---")
    ht_avg = ht_df.groupby('pid').agg({
        'mean_rot_speed_total': 'mean',
        'mean_rot_speed_y': 'mean',
        'sd_rot_speed_total': 'mean',
    }).reset_index()
    ht_avg = ht_avg.merge(df[['pid', 'score_phq', 'score_gad', 'score_stai_t']],
                          on='pid')

    for measure, mlabel in [('mean_rot_speed_total', 'Mean Total Speed'),
                            ('mean_rot_speed_y', 'Mean Yaw Speed'),
                            ('sd_rot_speed_total', 'SD Total Speed')]:
        r, p = pearsonr(ht_avg['score_phq'], ht_avg[measure])
        print(f"  PHQ-9 vs {mlabel}: Pearson r = {r:.3f}, p = {p:.4f}")


def test_video_speed_differences(ht_df):
    print("\n--- One-Way ANOVA: Does mean speed differ across videos? ---")
    groups = [ht_df[ht_df['video'] == v]['mean_rot_speed_total']
              for v in VIDEO_ORDER]
    f_stat, p = f_oneway(*groups)
    print(f"  F = {f_stat:.2f}, p = {p:.4f}")

    # Eta-squared effect size
    grand_mean = ht_df['mean_rot_speed_total'].mean()
    ss_between = sum(len(g) * (g.mean() - grand_mean)**2 for g in groups)
    ss_total = sum((ht_df['mean_rot_speed_total'] - grand_mean)**2)
    eta_sq = ss_between / ss_total if ss_total != 0 else 0
    print(f"  η² = {eta_sq:.3f}")


def run_inferential_stats(df, ht_df, merged):
    print("\n" + "=" * 70)
    print("PRELIMINARY INFERENTIAL STATISTICS")
    print("=" * 70)
    test_normality(df)
    test_clinical_correlations(df)
    test_headtracking_group_differences(merged)
    test_panas_change(df)
    test_phq_headtracking_correlation(df, ht_df)