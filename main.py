from config import PHQ_CUTOFF
from data_loading import load_survey_data, load_headtracking_data, build_merged_dataset
from descriptive_stats import run_descriptive_stats
from visualizations import generate_all_figures
from inferential_stats import run_inferential_stats


def main():
    # ── Load data ──
    print("=" * 70)
    print("LOADING DATA")
    print("=" * 70)

    df = load_survey_data()
    n_dep = (df['dep_group'] == 'Depressed').sum()
    n_nondep = (df['dep_group'] == 'Non-Depressed').sum()
    print(f"Survey data: {len(df)} participants")
    print(f"Depression groups (PHQ >= {PHQ_CUTOFF}): "
          f"Depressed={n_dep}, Non-Depressed={n_nondep}")

    ht_df = load_headtracking_data(df)
    print(f"Headtracking summaries: {len(ht_df)} records "
          f"({len(ht_df) // 5} participants × 5 videos)")

    merged = build_merged_dataset(df, ht_df)
    print(f"Merged dataset: {merged.shape}")

    # ── Descriptive stats + outliers ──
    run_descriptive_stats(df, ht_df, merged)

    # ── Visualizations ───
    generate_all_figures(df, ht_df, merged)

    # ── Inferential stats ───
    run_inferential_stats(df, ht_df, merged)

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE — All figures saved to figures/")
    print("=" * 70)


if __name__ == '__main__':
    main()
