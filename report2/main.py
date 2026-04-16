
import json
import warnings
warnings.filterwarnings('ignore')

from .config import STATS_OUT, FIG_DIR

# -- data --------------------------------------------------------------------
from .data_loader import load_survey, load_headtracking, build_merged, build_subjective

# -- analyses ----------------------------------------------------------------
from .analyses.video_effect  import run_kruskal_wallis, run_friedman_anova, run_rm_anova
from .analyses.regression    import run_simple_regression, run_ancova
from .analyses.mixed_models  import run_lmm
from .analyses.power         import run_power_analysis
from .analyses.corrections   import run_mcc_comparison
from .analyses.experience    import run_subjective_ratings, run_panas_analysis
from .analyses.moderation    import run_moderation

# -- plots -------------------------------------------------------------------
from .plots.video_plots      import plot_video_effect, plot_posthoc_heatmap
from .plots.regression_plots import plot_phq_scatter, plot_ancova_forest, plot_phq_continuous
from .plots.model_plots      import plot_power_curve, plot_mcc_comparison, plot_lmm_effects
from .plots.experience_plots import plot_panas_by_group, plot_phq_subj_ratings


# ===========================================================================

def main():
    print('=' * 70)
    print('REPORT 2 ANALYSIS')
    print('=' * 70)

    # ── 1. Load data ─────────────────────────────────────────────────────────
    print('\n[1/3] Loading data ...')
    df      = load_survey()
    ht_df   = load_headtracking(df)
    merged  = build_merged(df, ht_df)
    subj_df = build_subjective(df)
    print(f'  survey: {df.shape}  |  headtracking: {ht_df.shape}  |  '
          f'merged: {merged.shape}  |  subjective: {subj_df.shape}')

    # ── 2. Analyses ──────────────────────────────────────────────────────────
    print('\n[2/3] Running analyses ...')

    print('\n--- Analysis 1+2: Video effect ---')
    kw_res      = run_kruskal_wallis(ht_df)
    friedman_res = run_friedman_anova(merged)
    rm_res      = run_rm_anova(ht_df)

    print('\n--- Analysis 3+4: PHQ-9 as continuous predictor ---')
    reg_res  = run_simple_regression(merged)
    anc_res  = run_ancova(merged)

    print('\n--- Analysis 5: Linear Mixed Model ---')
    lmm_res = run_lmm(merged)

    print('\n--- Analysis 6: Power analysis ---')
    n_dep    = int((df['dep_group'] == 'Depressed').sum())
    n_nondep = int((df['dep_group'] == 'Non-Depressed').sum())
    pow_res  = run_power_analysis(n_dep, n_nondep)

    print('\n--- Analysis 7: Multiple comparison corrections ---')
    mcc_df  = run_mcc_comparison(merged)

    print('\n--- Analysis 8: PHQ-9 and subjective ratings ---')
    subj_res = run_subjective_ratings(subj_df)

    print('\n--- Analysis 9: PANAS by depression group ---')
    panas_res = run_panas_analysis(df)

    print('\n--- Analysis 10: Presence moderation ---')
    mod_res = run_moderation(merged)

    # ── 3. Figures ───────────────────────────────────────────────────────────
    print('\n[3/3] Generating figures ...')

    plot_video_effect(ht_df, rm_res)
    plot_posthoc_heatmap(kw_res['posthoc_df'], kw_res['H'], kw_res['p'], kw_res['eta2'])
    plot_phq_scatter(merged, reg_res)
    plot_ancova_forest(anc_res)
    plot_phq_continuous(df, ht_df)
    plot_power_curve(pow_res)
    plot_mcc_comparison(mcc_df)
    plot_lmm_effects(lmm_res)
    plot_panas_by_group(df)
    plot_phq_subj_ratings(subj_df)

    # ── 4. Save stats summary to JSON ────────────────────────────────────────
    # Strip non-serialisable objects (DataFrames, fitted models) from lmm_res
    lmm_serial = {k: v for k, v in lmm_res.items()
                  if k not in ('lmm2', 'lmm3', 're_intercepts')}

    summary = {
        'kw_video':          {k: v for k, v in kw_res.items()
                               if k not in ('posthoc_df',)},
        'friedman':          friedman_res,
        'rm_anova':          {k: v for k, v in rm_res.items()
                               if k not in ('posthoc',)},
        'simple_regression': reg_res,
        'ancova':            anc_res,
        'lmm':               lmm_serial,
        'power':             {k: v for k, v in pow_res.items()
                               if k not in ('d_range', 'power_current',
                                            'power_doubled', 'power_needed')},
        'mcc':               {
            'n_tests':          len(mcc_df),
            'sig_uncorrected':  int(mcc_df['sig_uncorrected'].sum()),
            'sig_bonferroni':   int(mcc_df['sig_bonferroni'].sum()),
            'sig_holm':         int(mcc_df['sig_holm'].sum()),
            'sig_fdr':          int(mcc_df['sig_fdr'].sum()),
        },
        'subj_ratings':      subj_res,
        'panas_by_group':    panas_res,
        'moderation':        mod_res,
    }

    with open(STATS_OUT, 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    print(f'\n  Stats saved to {STATS_OUT}')

    # Save CSVs
    import os
    kw_res['posthoc_df'].to_csv(os.path.join(FIG_DIR, 'mw_bonf_posthoc.csv'),  index=False)
    rm_res['posthoc'].to_csv(     os.path.join(FIG_DIR, 'rm_anova_posthoc.csv'), index=False)
    mcc_df.to_csv(                os.path.join(FIG_DIR, 'mcc_comparison.csv'),  index=False)

    print('\n' + '=' * 70)
    print(f'REPORT 2 ANALYSIS COMPLETE  |  Figures -> {FIG_DIR}')
    print('=' * 70)


if __name__ == '__main__':
    main()
