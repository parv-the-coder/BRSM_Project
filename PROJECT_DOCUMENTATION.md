# PROJECT DOCUMENTATION
## Are Headtracking Measures an Indicator of Depressive Symptoms?
### BRSM Course — Report 1 (Complete Reference Guide)

**Author:** Parv Shah  
**Date:** February 2026  
**Course:** Behavioral Research & Statistical Methods (BRSM)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Background Theory & Why This Study](#2-background-theory--why-this-study)
3. [The Original Study We Are Replicating](#3-the-original-study-we-are-replicating)
4. [Experiment Setup & Procedure](#4-experiment-setup--procedure)
5. [Complete Dataset Description](#5-complete-dataset-description)
6. [Derived Variables We Created](#6-derived-variables-we-created)
7. [Code Architecture](#7-code-architecture)
8. [Step-by-Step: What We Did, Why, and How](#8-step-by-step-what-we-did-why-and-how)
9. [All Statistical Tests Explained](#9-all-statistical-tests-explained)
10. [All Results with Interpretation](#10-all-results-with-interpretation)
11. [All 12 Figures Explained](#11-all-12-figures-explained)
12. [Outlier Detection](#12-outlier-detection)
13. [Key Findings Summary](#13-key-findings-summary)
14. [Limitations](#14-limitations)
15. [Plans for Report 2](#15-plans-for-report-2)
16. [Glossary of Terms](#16-glossary-of-terms)
17. [References](#17-references)
18. [Viva Preparation: Likely Questions & Answers](#18-viva-preparation-likely-questions--answers)

---

## 1. Project Overview

### What is this project?
This is a **replication study** investigating whether **headtracking data** collected during 360° Virtual Reality (VR) video viewing can serve as an **objective behavioral marker for depression**. The core question is:

> **"Do depressed individuals move their heads less (lower rotation speed, smaller angular range) than non-depressed individuals when watching 360° VR videos?"**

### Why does this matter?
- Depression is currently diagnosed using **self-report questionnaires** (PHQ-9, BDI-II, etc.), which are **subjective** and can be biased
- If we could detect depression from **objective behavioral measures** (like how people move their heads in VR), it would be a breakthrough for **screening and early detection**
- This connects to the concept of **psychomotor retardation** — a well-documented symptom of depression where people physically slow down

### What data do we have?
- **40 participants** (college students in India)
- Each watched **5 different 360° VR videos** on a Meta Quest 3 headset
- We collected:
  - **Headtracking data** (how they moved their heads) — ~4000+ data points per participant per video at ~70 Hz
  - **Self-report questionnaires** — depression (PHQ-9), anxiety (GAD-7, STAI-T), mood (PANAS), presence/immersion, simulator sickness (VRISE), and emotional ratings per video

---

## 2. Background Theory & Why This Study

### Depression & Psychomotor Retardation
- **Psychomotor retardation** = slowing of physical movement AND cognitive processing in depression (Bennabi et al., 2013)
- This is not just "feeling slow" — it is a measurable reduction in motor activity
- It manifests as: slower speech, reduced gestures, less facial expression, and crucially for our study — **reduced physical exploration of environments**

### Anhedonia Connection
- **Anhedonia** = loss of interest/pleasure (a core symptom of depression, DSM-5 Criterion A2)
- In a stimulating VR environment, anhedonia might cause depressed individuals to **explore less** — moving their head less, looking at fewer things
- This reduced exploration would show up in headtracking data as **lower rotation speeds** and **smaller angular ranges**

### Why VR?
- VR provides a **controlled, immersive environment** where we can measure behavior precisely
- Unlike a lab setting, 360° videos require active head movement to explore the scene
- The headset's built-in sensors give us **high-frequency, objective motion data** (no relying on video coding or observer ratings)
- VR removes many confounds of real-world observation (different room sizes, furniture blocking movement, etc.)

### Depression-Anxiety Comorbidity
- Depression and anxiety are **highly correlated** (Kalin, 2020)
- ~60% of people with depression also have significant anxiety
- This means: if we find differences between depressed and non-depressed groups, we need to check whether it's **depression driving the effect** or **anxiety** (or their overlap)
- This is why we measured **both PHQ-9 (depression) AND GAD-7 + STAI-T (anxiety)**

---

## 3. The Original Study We Are Replicating

### Paper: Srivastava et al. (2025) — "What Do Head Scans Reveal About Depression?"

**Key findings of the original study:**
1. Using **ANCOVA** controlling for anxiety (GAD-7 and STAI-T as covariates), depression severity significantly affected **scanning speed** (p < .001, η² = .295)
2. The moderate-severe depression group had the **slowest scanning speed** (M = 3.88, SD = 0.88) vs mild (M = 4.94) and minimal (M = 5.29)
3. **Effect sizes were large** (Cohen's d = 1.64 between severe and none; d = −1.22 between severe and mild)
4. SDY (standard deviation of yaw) was **not significant** for depression after controlling for anxiety
5. Kruskal-Wallis showed depression affected scanning speed specifically in LVHA, Neutral, and HVLA videos

**What we are testing:**
- Can we replicate these findings with a different VR headset and sample size?
- Our hypothesis: Depressed group will show lower mean rotation speed and smaller angular exploration range

**Key differences in our replication:**
- Different VR headset (Meta Quest 3 vs. HTC Vive Pro at 90 Hz)
- Slightly different video selection (they used Stanford VR database + 1 YouTube horror)
- Smaller sample (N=40 vs. N=50)
- We use binary classification; they used 3 groups (minimal, mild, moderate-severe)

---

## 4. Experiment Setup & Procedure

### Participants
| Detail | Value |
|--------|-------|
| Total N | 40 |
| Gender | 36 Male (90%), 4 Female (10%) |
| Age M (SD) | 22.8 (1.8) years |
| Age Range | 19–27 years |
| VR Experience | 16 (40%) had prior VR experience |
| Recruitment | Convenience sampling, college students |

### Videos Used (5 total)
| Video | Content | Duration | Expected Emotion |
|-------|---------|----------|-----------------|
| V1: Abandoned Buildings | Eerie empty buildings | ~60s | Low valence, moderate arousal |
| V2: Beach | Pleasant evening beach | ~60s | High valence, low arousal |
| V3: Campus | Familiar campus walkthrough | ~60s | Neutral valence, low arousal |
| V4: Horror (The Nun) | Horror scene | ~3 min | Very low valence, high arousal |
| V5: Tahiti Surf | Surfing in Tahiti | ~3 min | High valence, high arousal |

**Why these specific videos?**
- To cover **different emotional quadrants** of the valence-arousal circumplex model
- This lets us test if the depression-headtracking relationship depends on **video emotionality**
- We expect exploration behavior might differ by emotional content (e.g., horror focuses attention, pleasant scenes invite exploration)

### Equipment
- **VR Headset:** Meta Quest 3
- **Data recording:** Built-in headtracking at ~70 Hz (≈ 70 data points per second)
- **Surveys:** PsyToolKit (online survey platform)

### Procedure (per participant)
1. Fill pre-VR surveys (demographics, PANAS pre, PHQ-9, GAD-7, STAI-T)
2. Put on VR headset
3. Watch all 5 videos (order may have been counterbalanced)
4. After each video: rate valence, arousal, emotion, immersion/presence
5. After all videos: PANAS post, VRISE (simulator sickness), feedback
6. Remove headset, debrief

---

## 5. Complete Dataset Description

### File 1: `data/data.xlsx` (Survey Data)
- **Rows:** 40 (one per participant)
- **Columns:** 64

#### Column-by-Column Breakdown:

| Column(s) | Type | Description | Values/Range |
|-----------|------|-------------|-------------|
| `participant` | ID | Participant number | 1–40 |
| `age` | Numeric | Age in years | 19–27 |
| `gender` | Categorical | 1=Male, 2=Female | 1 or 2 |
| `vr_experience` | Categorical | 1=No, 2=Yes | 1 or 2 |
| `v1` through `v5` | String | Filename of headtracking CSV for each video | e.g., `data_video1_20260125113153995.csv` |
| `valence_v1` to `valence_v5` | Numeric | Subjective pleasantness rating per video | 1 (unpleasant) – 9 (pleasant) |
| `arousal_v1` to `arousal_v5` | Numeric | Subjective excitement rating per video | 1 (calm) – 9 (excited) |
| `emotion_v1` to `emotion_v5` | Categorical | Dominant emotion felt per video | Text labels |
| `features_v1` to `features_v5` | Text | Features participant noticed | Free text |
| `immersion_v1` to `immersion_v5` | Numeric | Presence/immersion score per video | 5–35 (sum of 5 items, each 1–7) |
| `phq_1` to `phq_9` | Numeric | Individual PHQ-9 item responses | 0–3 each |
| `gad_1` to `gad_7` | Numeric | Individual GAD-7 item responses | 0–3 each |
| `score_phq` | Numeric | Total PHQ-9 score (sum of phq_1 to phq_9) | 0–27 |
| `score_gad` | Numeric | Total GAD-7 score (sum of gad_1 to gad_7) | 0–21 |
| `score_stai_t` | Numeric | STAI Trait Anxiety total score | 20–80 |
| `score_vrise` | Numeric | VRISE simulator sickness score | 5–35 |
| `positive_affect_start` | Numeric | PANAS Positive Affect before VR | 10–50 |
| `negative_affect_start` | Numeric | PANAS Negative Affect before VR | 10–50 |
| `positive_affect_end` | Numeric | PANAS Positive Affect after VR | 10–50 |
| `negative_affect_end` | Numeric | PANAS Negative Affect after VR | 10–50 |
| `feedback` | Text | Open-ended participant feedback | Free text |
| Various timestamp columns | DateTime | Start/end timestamps | Datetime strings |

### File 2: Headtracking CSVs (`data/headtracking-data/v1/` → `v5/`)
- **Organization:** 5 folders (one per video), each containing 40 CSV files (one per participant)
- **Total files:** 200 CSV files
- **Rows per file:** ~4000+ (depending on video duration and recording frequency)
- **Recording frequency:** ~70 Hz (70 rows per second)

#### Columns in Each Headtracking CSV:

| Column | Unit | Description |
|--------|------|-------------|
| `Time` | Seconds | Timestamp from start of video |
| `PositionChangeX` | Meters | Forward/backward head displacement |
| `PositionChangeY` | Meters | Up/down head displacement |
| `PositionChangeZ` | Meters | Left/right head displacement |
| `RotationChangeX` | Degrees | Pitch change (looking up/down) |
| `RotationChangeY` | Degrees | Yaw change (looking left/right) — **most important axis** |
| `RotationChangeZ` | Degrees | Roll change (tilting head sideways) |
| `RotationSpeedX` | °/s | Pitch rotation speed |
| `RotationSpeedY` | °/s | Yaw rotation speed — **primary measure** |
| `RotationSpeedZ` | °/s | Roll rotation speed |
| `RotationSpeedTotal` | °/s | Combined rotation speed (magnitude of all axes) |

**Important data quirk:** The last row of each CSV contains a summary line with extra columns (13 instead of 11). We handle this with `on_bad_lines='skip'` when loading.

#### Why is Yaw (Y-axis) the most important?
- **Yaw = horizontal head rotation** (looking left and right)
- In a 360° video, the main way to explore is to **turn your head horizontally** to look around
- The original study found the strongest depression effect on yaw speed
- Pitch (looking up/down) and roll (tilting) are secondary exploration movements

---

## 6. Derived Variables We Created

These are variables we **computed from the raw data** — they don't exist in the original files:

### From Survey Data (`data_loading.py`):

| Variable | Formula/Logic | Purpose |
|----------|--------------|---------|
| `pid` | `P01`, `P02`, ..., `P40` | Unique participant identifier for merging |
| `dep_group` | `"Depressed"` if PHQ-9 ≥ 10, else `"Non-Depressed"` | Binary depression classification |
| `phq_severity` | 0–4=Minimal, 5–9=Mild, 10–14=Moderate, 15–19=Mod.Severe, 20+=Severe | Clinical severity category |
| `gender_label` | 1→"Male", 2→"Female" | Human-readable gender |
| `vr_exp_label` | 1→"No", 2→"Yes" | Human-readable VR experience |
| `pa_change` | `positive_affect_end - positive_affect_start` | Change in positive affect due to VR |
| `na_change` | `negative_affect_end - negative_affect_start` | Change in negative affect due to VR |

### From Headtracking Data (computed per participant per video):

| Variable | Formula | What it measures |
|----------|---------|-----------------|
| `duration_s` | `Time.max() - Time.min()` | How long the recording lasted |
| `mean_rot_speed_total` | `mean(RotationSpeedTotal)` | Average overall head movement speed |
| `mean_rot_speed_x/y/z` | `mean(RotationSpeedX/Y/Z)` | Average speed per axis |
| `sd_rot_speed_total` | `std(RotationSpeedTotal)` | Variability of head movement (do they alternate fast/slow?) |
| `sd_rot_speed_x/y/z` | `std(RotationSpeedX/Y/Z)` | Variability per axis |
| `median_rot_speed_total` | `median(RotationSpeedTotal)` | Robust central tendency (less affected by outliers) |
| `mean_abs_rot_x/y/z` | `mean(abs(RotationChangeX/Y/Z))` | Average magnitude of rotation per frame |
| `sd_rot_change_x/y/z` | `std(RotationChangeX/Y/Z)` | Variability of rotation per frame |
| `range_rot_x/y/z` | `max - min` of `RotationChangeX/Y/Z` | Total angular space explored per axis |
| `max_rot_speed_total` | `max(RotationSpeedTotal)` | Peak head movement speed |
| `total_range` | `range_rot_x + range_rot_y + range_rot_z` | Combined angular exploration across all axes |

### Why so many headtracking measures?
We don't know in advance which measure best captures the depression effect, so we compute several:
- **Mean speed** = overall movement level (our primary hypothesis measure)
- **SD of speed** = variability of movement (depressed people might move more uniformly)
- **Range** = total space explored (depressed people might explore less of the scene)
- **Per-axis measures** = to check if the effect is axis-specific (the original paper found yaw was most informative)

---

## 7. Code Architecture

### File Structure
```
360 Videos VR project/
├── main.py                 ← Entry point: run this to execute everything
├── config.py               ← All settings, paths, constants
├── data_loading.py         ← Load Excel + CSVs, compute derived variables
├── descriptive_stats.py    ← Print stats + outlier detection
├── visualizations.py       ← Generate all 12 figures (saved as PDFs)
├── inferential_stats.py    ← Statistical tests
├── analysis.py             ← (Original single-file version, kept as backup)
├── report1.tex             ← LaTeX source for the report
├── report1.pdf             ← Compiled report (11 pages)
├── data/
│   ├── data.xlsx           ← Survey data (40 rows × 64 columns)
│   └── headtracking-data/
│       ├── v1/             ← 40 CSVs for Video 1
│       ├── v2/             ← 40 CSVs for Video 2
│       ├── v3/             ← 40 CSVs for Video 3
│       ├── v4/             ← 40 CSVs for Video 4
│       └── v5/             ← 40 CSVs for Video 5
├── figures/
│   ├── fig1_demographics.pdf → fig12_yaw_speed_by_group.pdf
│   ├── descriptive_stats.csv
│   └── ttest_results.csv
└── PROJECT_DOCUMENTATION.md  ← This file
```

### How to Run
```bash
python3 main.py
```
This executes the full pipeline: load data → descriptive stats → 12 figures → inferential tests → outlier detection.

### Module Descriptions

| Module | Lines | What it does |
|--------|-------|-------------|
| `config.py` | ~48 | Defines BASE_DIR, DATA_DIR, HEADTRACK_DIR, FIG_DIR, visual settings (seaborn theme, matplotlib rcParams), color palette, video names/order, PHQ cutoff |
| `data_loading.py` | ~113 | `load_survey_data()` reads data.xlsx & creates derived columns. `load_headtracking_data(df)` reads all 200 CSVs and computes 20+ summary measures per file. `build_merged_dataset()` joins survey + headtracking into one DataFrame. |
| `descriptive_stats.py` | ~139 | Prints demographics, clinical scores, PANAS, video ratings, headtracking by video/group. Saves descriptive_stats.csv. Runs outlier detection (IQR + z-score). |
| `visualizations.py` | ~210 | 12 functions (fig1 through fig12) each generating one PDF figure. `generate_all_figures()` calls them all. |
| `inferential_stats.py` | ~160 | Shapiro-Wilk normality, Pearson correlations, Welch's t-tests per video × 5 measures with Cohen's d and Bonferroni correction, paired t-test for PANAS, PHQ-headtracking Pearson correlations, one-way ANOVA across videos. |
| `main.py` | ~45 | Orchestrator: imports all modules, calls load → describe → visualize → test in sequence. |

### Libraries Used
| Library | Version | Why |
|---------|---------|-----|
| `pandas` | — | Data manipulation, reading Excel/CSV |
| `numpy` | — | Numerical operations, z-scores |
| `scipy.stats` | — | All statistical tests (Shapiro-Wilk, Welch's t-test, paired t-test, one-way ANOVA, Pearson) |
| `matplotlib` | — | Low-level plotting (bar charts, histograms) |
| `seaborn` | — | High-level statistical visualizations (violin plots, box plots, heatmaps) |
| `openpyxl` | — | Backend for reading .xlsx files via pandas |

---

## 8. Step-by-Step: What We Did, Why, and How

### Step 1: Load Survey Data

**What:** Read `data.xlsx` into a pandas DataFrame.

**Why:** This gives us all questionnaire responses, demographics, and the filenames of headtracking CSVs for each participant.

**How:** `pd.read_excel()` → then create derived columns (pid, dep_group, phq_severity, gender_label, vr_exp_label, pa_change, na_change).

**Key decision — PHQ-9 cutoff of ≥10:**
- The PHQ-9 manual (Kroenke et al., 2001) defines severity levels:
  - 0–4: Minimal depression
  - 5–9: Mild depression
  - 10–14: Moderate depression
  - 15–19: Moderately severe depression
  - 20–27: Severe depression
- We use ≥10 ("moderate") as the cutoff because:
  1. It's the standard clinical threshold for "probable clinical depression"
  2. The original study (Srivastava et al., 2025) used ≥10 as the moderate-severe threshold (they used 3 groups)
  3. It gives us a reasonable split (8 Depressed vs. 32 Non-Depressed)
- This is a **binary classification** — simple but loses information (treated as continuous in Report 2)

### Step 2: Load Headtracking Data

**What:** Read all 200 headtracking CSV files and compute summary statistics per participant per video.

**Why:** Raw data has ~4000+ rows per file × 200 files = ~800,000+ data points. We need to **summarize** this into one row per participant-video combination so we can link it to survey responses.

**How:**
- Loop through all 40 participants × 5 videos
- For each CSV: compute 20+ summary measures (mean speed, SD, range, etc.)
- Collect into a DataFrame with 200 rows (40 participants × 5 videos)

**Key decision — `on_bad_lines='skip'`:**
- The headtracking CSVs have a **malformed last row** that contains summary statistics with 13 columns instead of 11
- Rather than manually cleaning 200 files, we tell pandas to skip any line that doesn't match the expected column count
- This loses only 1 row of summary data per file (which we don't need; we compute our own summaries)

### Step 3: Merge Datasets

**What:** Join survey data with headtracking summaries on participant ID.

**Why:** So that each row has BOTH the headtracking measures AND the clinical/demographic information. This enables us to compare headtracking behavior between depression groups.

**How:** `df.merge(ht_df, on='pid', how='inner')` → creates a merged DataFrame with 200 rows (each participant appears 5 times, once per video).

### Step 4: Descriptive Statistics

**What:** Compute and print means, SDs, medians, ranges for all key variables.

**Why:** 
- Required before any inferential analysis — you must understand your data first
- Reveals potential issues (outliers, skewed distributions, missing data)
- Provides the numbers you report in the Methods and Results sections of the paper

**Key findings from descriptive stats:**
- Sample is mostly non-depressed (80%, n=32) with 20% meeting depression threshold (n=8)
- Unbalanced groups (8 vs 32) — this is important for choosing statistical tests
- PHQ-9 and GAD-7 are positively skewed (most people have low scores) — this is expected in a non-clinical sample

### Step 5: Generate 12 Visualizations

**What:** Create 12 publication-quality PDF figures covering demographics, clinical scores, video ratings, and headtracking measures.

**Why:**
- Visualizations reveal **patterns** that numbers alone miss
- Required for the report — each figure tells part of the story
- Help detect outliers, non-normality, group differences visually

### Step 6: Run Inferential Statistical Tests

**What:** Formal hypothesis tests to determine statistical significance.

**Why:** Descriptive stats and plots give us intuition, but we need **p-values** and **effect sizes** to make formal claims about differences.

**How:** See Section 9 below for detailed explanation of each test.

### Step 7: Outlier Detection

**What:** Identify unusual data points that might distort our analyses.

**Why:** Outliers can inflate or deflate group differences, distort means, and affect test results. We need to know they exist and decide how to handle them.

**How:** Two methods:
1. **IQR method** for clinical scores (robust to non-normality)
2. **Z-score method** for headtracking data (|z| > 3 = outlier)

---

## 9. All Statistical Tests Explained

### Why Parametric Tests?

**The fundamental question:** Should we use parametric tests (t-test, ANOVA, Pearson) or non-parametric tests (Mann-Whitney, Kruskal-Wallis, Spearman)?

**Our decision:** Primarily **parametric**, because:

1. **t-tests are robust to moderate non-normality:** Extensive simulation research shows that t-tests maintain correct Type I error rates even with non-normal data when N ≥ 20–30.

2. **Central Limit Theorem (Topic 4):** With N=40, the sampling distribution of the mean approaches normality regardless of the shape of the underlying distribution.

3. **Welch's correction:** We use Welch's t-test which does NOT assume equal variances, handling the 8 vs 32 group size imbalance appropriately.

4. **Syllabus alignment:** t-distributions, F-distributions, effect sizes (Cohen's d), and multiple comparison corrections (Bonferroni) are all covered in Topics 3–6 of the BRSM syllabus.

5. **Shapiro-Wilk results (for reference):**
   - PHQ-9: W=0.897, p=.002 → Non-normal
   - GAD-7: W=0.883, p<.001 → Non-normal
   - STAI-T: W=0.944, p=.045 → Marginally non-normal
   - Despite this, the parametric approach is justified by CLT and robustness arguments.

### Test 1: Shapiro-Wilk Test (Normality Assessment)

**What it tests:** Whether a variable follows a normal (Gaussian) distribution.

**Why we use it:** To assess distributional assumptions before applying parametric tests. Even though we use parametric tests (justified by CLT), Shapiro-Wilk results are reported for transparency.

**How it works:**
- H₀: The data is normally distributed
- H₁: The data is NOT normally distributed
- If p < 0.05 → reject H₀ → data is NOT normal → note as limitation but proceed with parametric tests (robust under CLT)

**Our results:**
| Variable | W | p | Verdict |
|----------|---|---|---------|
| PHQ-9 | 0.897 | .002 | Non-normal ✗ |
| GAD-7 | 0.883 | <.001 | Non-normal ✗ |
| STAI-T | 0.944 | .045 | Non-normal ✗ |

**Interpretation:** All three clinical measures are non-normal. However, we proceed with parametric tests because: (1) t-tests are robust to moderate non-normality, (2) CLT applies with N=40, (3) Welch's correction handles unequal variances.

### Test 2: Pearson Correlation (r)

**What it tests:** Linear association between two continuous variables.

**Assumptions:** Both variables approximately normal, linear relationship, no major outliers.

**Formula:** r = Σ[(xi - x̄)(yi - ȳ)] / √[Σ(xi - x̄)² × Σ(yi - ȳ)²]

**Range:** -1 (perfect negative) to +1 (perfect positive), 0 = no linear relationship.

**Why we use it:** To quantify the strength and direction of relationships (e.g., PHQ-9 vs GAD-7).

**Our results:**
| Pair | r | p | Interpretation |
|------|---|---|---------------|
| PHQ-9 vs GAD-7 | .579 | <.001 | Strong positive correlation |
| PHQ-9 vs STAI-T | .642 | <.001 | Strong positive correlation |

### Test 3: Welch's Independent-Samples t-test (Topic 5: Hypothesis Testing)

**What it tests:** Whether two independent groups have different means — using the t-distribution (Topic 3).

**Why Welch's (not Student's t-test):**
1. Does NOT assume equal variances between groups
2. Appropriate for unequal group sizes (8 vs 32)
3. Uses Welch-Satterthwaite degrees of freedom correction

**Formula:** t = (M₁ - M₂) / √(s₁²/n₁ + s₂²/n₂)

**Effect size (Cohen's d, Topic 5):** d = (M₁ - M₂) / pooled_SD. Interpretation:
- |d| < 0.2: negligible
- |d| ≈ 0.2–0.5: small
- |d| ≈ 0.5–0.8: medium
- |d| > 0.8: large

**We ran this test for:** 5 headtracking measures × 5 videos = **25 comparisons**

**Bonferroni correction (Topic 6):** α_corrected = 0.05 / 25 = 0.002

**Our results (abbreviated):**

| Video | Measure | t | p | Cohen's d | Sig (α=.05)? | Sig (Bonferroni)? |
|-------|---------|---|---|-----------|------|------|
| V1: Abandoned | Mean Speed Total | −0.24 | .816 | −0.08 | No | No |
| V2: Beach | Mean Speed Total | 1.22 | .239 | 0.38 | No | No |
| V3: Campus | Mean Speed Total | −0.64 | .532 | −0.24 | No | No |
| V4: Horror | Mean Speed Total | 1.07 | .303 | 0.37 | No | No |
| V4: Horror | Total Angular Range | 2.21 | .048 | 0.83 | *Yes* | No |
| V5: Tahiti | Mean Speed Total | −0.66 | .523 | −0.21 | No | No |

**Key findings:**
- 1/25 tests significant at α=.05 (uncorrected) — V4 angular range
- 0/25 tests significant after Bonferroni correction
- V4 angular range: depressed group showed **MORE** exploration (opposite to hypothesis) with a large effect size (d=0.83), but non-significant after multiple comparison correction

### Test 4: Paired t-test (Topic 5: Hypothesis Testing)

**What it tests:** Whether the mean difference between paired observations is zero — for within-subject comparisons.

**Why this test:** To compare PANAS scores before vs. after VR (same participants measured twice).

**How it works:**
1. Compute the difference for each participant (post - pre)
2. Compute the mean and SD of differences
3. t = mean_diff / (SD_diff / √n)
4. Compare against t-distribution with df = n-1

**Effect size (Cohen's d):** d = mean_diff / SD_diff

**Our results:**
| Pair | t(39) | p | Cohen's d | Interpretation |
|------|-------|---|-----------|---------------|
| Positive Affect: Pre vs Post | 2.09 | .043 | −0.33 | **Significant decrease** after VR |
| Negative Affect: Pre vs Post | −1.06 | .294 | 0.17 | No significant change |

**Interpretation:** VR exposure **reduced positive affect** (people felt less good after watching the videos), but did not significantly affect negative affect.

### Test 5: One-Way ANOVA / F-test (Topic 3+5: F-distributions)

**What it tests:** Whether 3+ independent group means are equal — based on the F-distribution (Topic 3).

**Why this test:** To check if headtracking speed differs across the 5 videos (5 groups).

**How it works:** Compares between-group variance to within-group variance. F = MS_between / MS_within. Large F → group means differ.

**Effect size (η²):** η² = SS_between / SS_total. Interpretation:
- η² ≈ 0.01: small
- η² ≈ 0.06: medium
- η² ≈ 0.14+: large

**Our results:**
- **F(4, 195) = 10.75, p < .0001, η² = .181** → Mean rotation speed **differs significantly** across videos (large effect)
- V1 (Abandoned Buildings) had highest speed (~39°/s), V4 (Horror) had lowest (~24°/s)

### Pearson Correlations: PHQ-9 vs Headtracking

**Purpose:** Test whether depression severity (continuous) is linearly associated with headtracking behavior.

**Our results:**
| Pair | r | p | Interpretation |
|------|---|---|---------------|
| PHQ-9 vs Mean Total Speed (avg across videos) | −.060 | .712 | No association |
| PHQ-9 vs Mean Yaw Speed (avg) | −.081 | .617 | No association |
| PHQ-9 vs SD Total Speed (avg) | −.158 | .329 | Weak, non-significant |

---

## 10. All Results with Interpretation

### Demographics
- 40 participants, 90% male, mean age 22.8 years
- **Limitation:** Heavily male-skewed sample limits generalizability to female populations
- 40% had prior VR experience — we should check if this affects headtracking behavior (potential confound)

### Clinical Scores
| Measure | M | SD | Median | Range |
|---------|---|-----|--------|-------|
| PHQ-9 | 6.03 | 4.63 | 4.5 | 0–18 |
| GAD-7 | 5.00 | 4.31 | 4.0 | 0–18 |
| STAI-T | 45.00 | 14.63 | — | 21–73 |

**Depression group split:** 8 Depressed (PHQ ≥ 10) vs. 32 Non-Depressed (PHQ < 10)

**PHQ-9 Severity:**
- 50% Minimal (0–4)
- 30% Mild (5–9)
- 12.5% Moderate (10–14)
- 7.5% Moderately Severe (15–19)
- 0% Severe (20+)

### Depression-Anxiety Relationship
- PHQ-9 & GAD-7: r=.579, ρ=.710 — **strong positive correlation**
- PHQ-9 & STAI-T: r=.642, ρ=.613 — **strong positive correlation**
- **Meaning:** People who are more depressed also tend to be more anxious. This is consistent with literature (Kalin, 2020). For Report 2, we need to control for anxiety when looking at depression effects.

### Video Emotional Profiles
| Video | Valence M(SD) | Arousal M(SD) | Presence M(SD) |
|-------|--------------|---------------|----------------|
| V1: Abandoned | 5.20 (1.67) | 4.60 (2.22) | 29.60 (4.41) |
| V2: Beach | 6.53 (1.75) | 4.65 (2.03) | 27.25 (5.31) |
| V3: Campus | 6.15 (1.61) | 4.33 (2.16) | 26.95 (4.52) |
| V4: Horror | 3.67 (1.85) | 5.95 (1.68) | 19.85 (5.44) |
| V5: Surf | 7.12 (1.68) | 6.50 (1.69) | 28.02 (4.79) |

**Key observations:**
- V5 (Surf): Highest valence AND arousal — most positive/exciting
- V4 (Horror): Lowest valence, high arousal, **lowest presence** — possibly poor video quality or discomfort reducing immersion
- V1 (Abandoned): **Highest presence** — the eerie environment may have been most immersive/engaging

### Depression vs Headtracking: THE MAIN FINDING
**Result: We did NOT replicate the original study's finding.**

- No significant differences in mean rotation speed between depressed and non-depressed groups for ANY video
- No significant correlations between PHQ-9 and headtracking measures averaged across videos
- The only significant result (V4 yaw/total range, p=.039) was in the **opposite direction** — depressed participants showed MORE exploration, not less

**Why might we not have replicated?**
1. **Small sample:** n=8 depressed is very small → low power to detect moderate effects
2. **Subclinical depression:** Most of our "depressed" participants are in the moderate range (PHQ 10–18), not severe
3. **Type II error:** The effect exists but our study couldn't detect it due to power issues

### PANAS Mood Changes
- Positive Affect decreased significantly (p=.031): VR made people feel **less positive**
- Negative Affect did not change significantly (p=.414)
- This suggests the VR experience had a mild mood-dampening effect, possibly driven by the horror video (V4)

### Headtracking Across Videos
- One-Way ANOVA: F(4,195)=10.75, p<.0001, η²=.181 → **Video content significantly affects head movement**
- Highest speed: V1 (Abandoned Buildings) ~39°/s — exploratory environment invites looking around
- Lowest speed: V4 (Horror) ~24°/s — horror scene may focus attention on specific threat cues

---

## 11. All 12 Figures Explained

### Fig 1: Demographics (`fig1_demographics.pdf`)
- **3 subplots:** Age histogram, Gender bar chart, VR Experience bar chart
- **Why:** Shows sample composition — need to report this for Methods section
- **What it reveals:** Right-skewed age (most 22–24), mostly male, about 60/40 split on VR experience

### Fig 2: Clinical Score Distributions (`fig2_clinical_distributions.pdf`)
- **3 histograms:** PHQ-9, GAD-7, STAI-T
- **Why:** Shows the shape of clinical score distributions → confirms positive skew → documents non-normality (parametric tests justified by CLT)
- **Red dashed line on PHQ-9:** The cutoff at 10 for moderate depression — shows 80% of sample falls below

### Fig 3: PHQ-9 Severity Pie Chart (`fig3_phq_severity.pdf`)
- **Why:** Visualizes the clinical severity breakdown of our sample
- **What it reveals:** Half the sample has minimal depression → this is a mostly healthy sample

### Fig 4: Correlation Heatmap (`fig4_correlation_heatmap.pdf`)
- **What:** Lower-triangle heatmap showing Pearson correlations among 8 variables (PHQ-9, GAD-7, STAI-T, VRISE, PA Pre, NA Pre, PA Post, NA Post)
- **Why:** Reveals inter-relationships among ALL measures at a glance
- **Key patterns:**
  - PHQ-9, GAD-7, STAI-T are all positively correlated (depression-anxiety cluster)
  - Negative affect correlated with depression/anxiety
  - VRISE shows weak correlations with everything

### Fig 5: Valence & Arousal Box Plots (`fig5_valence_arousal_by_video.pdf`)
- **What:** Box plots of participant ratings per video
- **Why:** Confirms that videos elicited the intended emotional responses
- **Key:** V4 (Horror) low valence/high arousal, V5 (Surf) high valence/high arousal — success in emotion induction

### Fig 6: Presence Violin Plots (`fig6_presence_by_video.pdf`)
- **What:** Violin plots showing distribution of immersion scores per video
- **Why:** Presence may moderate the headtracking-depression relationship — if you don't feel "present," you won't explore naturally
- **Key:** V4 (Horror) has notably lower and more variable presence scores

### Fig 7: PHQ-9 vs GAD-7 Scatter (`fig7_phq_vs_gad.pdf`)
- **What:** Scatter plot with color-coded dots (Depressed=orange, Non-Depressed=blue) and regression line
- **Why:** Visualizes the strong PHQ-GAD correlation and shows where depression groups fall
- **Key:** Strong positive linear relationship; all 8 depressed participants cluster in upper-right

### Fig 8: Headtrack Speed Violins (`fig8_headtrack_speed_by_group.pdf`)
- **What:** Split violin plots showing mean rotation speed distribution by video and depression group
- **Why:** THE KEY FIGURE — visually compares the headtracking behavior of depressed vs non-depressed
- **Key result:** The distributions **largely overlap** → no clear group separation → explains non-significant Welch's t-test results

### Fig 9: Headtrack SD Box Plots (`fig9_headtrack_sd_by_group.pdf`)
- **What:** Box plots of rotation speed variability (SD) by video and group
- **Why:** Tests whether depressed individuals show less variable movement (more monotone behavior)
- **Key result:** No clear group differences

### Fig 10: Angular Range Bar Plot (`fig10_angular_range_by_group.pdf`)
- **What:** Bar chart of total angular range explored by video and group, with 95% CI error bars
- **Why:** Tests whether depressed individuals explore less of the 360° scene
- **Key result:** Groups are similar except V4 (Horror) where depressed show MORE exploration

### Fig 11: PANAS Pre/Post (`fig11_panas_change.pdf`)
- **What:** Grouped bar chart (Positive Affect vs Negative Affect) × (Pre-VR vs Post-VR)
- **Why:** Shows mood changes induced by VR exposure
- **Key result:** Positive affect drops noticeably; negative affect stays roughly the same

### Fig 12: Yaw Speed Per Video (`fig12_yaw_speed_by_group.pdf`)
- **What:** 5 side-by-side box plots (one per video) showing mean yaw speed by depression group
- **Why:** Most fine-grained view of the primary measure (yaw = horizontal rotation)
- **Key result:** No consistent pattern of reduced yaw speed in the depressed group

---

## 12. Outlier Detection

### Clinical Score Outliers (IQR Method)

**How IQR works:**
- Q1 = 25th percentile, Q3 = 75th percentile
- IQR = Q3 - Q1
- Lower fence = Q1 - 1.5 × IQR
- Upper fence = Q3 + 1.5 × IQR
- Any value outside [lower, upper] = outlier

**Results:**
| Variable | Lower Fence | Upper Fence | N Outliers |
|----------|------------|------------|-----------|
| PHQ-9 | -7.1 | 14.2 | 3 (scores above 14.2) |
| GAD-7 | -6.5 | 14.5 | 2 (scores above 14.5) |
| STAI-T | (wide range) | (wide range) | 0 |

**Decision:** Retained all outliers because:
- These are genuine clinical variability (moderately severe depression/anxiety)
- Removing them would reduce our already-small depressed group further
- They represent the very participants we are most interested in

### Headtracking Outliers (Z-score Method)

**How z-score works:**
- z = (x - mean) / SD
- Values with |z| > 3 are considered outliers (more than 3 SDs from the mean)

**Result:** **No headtracking outliers detected** for any video (all |z| < 3)

### Simulator Sickness (VRISE)
- Mean VRISE = ~28, range [17, 35]
- 1 participant with VRISE < 20 (possible simulator sickness)
- **Flagged** for sensitivity analysis in Report 2 but retained for now

---

## 13. Key Findings Summary

1. **No replication of the original study's main finding:** Depressed and non-depressed groups did NOT differ significantly in headtracking speed for any video.

2. **Depression-anxiety comorbidity confirmed:** PHQ-9 and GAD-7 strongly correlated (ρ=.710), requiring covariate control in future analyses.

3. **Video content matters:** Headtracking speed differs significantly across videos (ANOVA F=10.75, p<.001, η²=.181), confirming that emotional content influences exploration behavior.

4. **One unexpected significant result (V4 Horror):** Depressed participants explored MORE in the horror video (p=.039, r=.33), opposite to our prediction. Likely a Type I error given 25 uncorrected comparisons.

5. **VR reduced positive affect:** Positive mood decreased significantly after VR exposure (paired t-test: t=2.09, p=.043, d=−0.33).

6. **PHQ-headtracking correlations near zero:** No meaningful correlation between depression severity and headtracking behavior (all ρ < .2, p > .05).

---

## 14. Limitations

| Limitation | Impact | Mitigation in Report 2 |
|-----------|--------|----------------------|
| Small sample (N=40, n_dep=8) | Very low statistical power | Use continuous PHQ-9 instead of binary split |
| Unbalanced groups (8 vs 32) | Standard t-test may be affected | Welch's t-test used (no equal-variance assumption); consider bootstrapping |
| Mostly male sample (90%) | Hard to generalize to women | Acknowledge in discussion; no fix possible |
| 25 comparisons without correction | Inflated Type I error | Apply Bonferroni or Benjamini-Hochberg correction |
| Binary depression classification | Wastes information from PHQ-9 | Use regression with continuous PHQ-9 |
| Does not control for anxiety | Can't separate depression from anxiety effects | Include GAD-7/STAI-T as covariates (ANCOVA) |
| VR experience variability | 40% had prior VR → might explore differently | Test VR experience as a covariate |
| Different videos have different durations | V4/V5 are ~3x longer than V1-V3 | Normalize or account for duration |

---

## 15. Plans for Report 2

### Statistical Methods to Apply:

1. **Multiple Comparison Correction:**
   - Bonferroni: α_adjusted = 0.05 / 25 = 0.002
   - Benjamini-Hochberg (FDR): less conservative, controls false discovery rate
   - Will likely make the V4 finding non-significant

2. **Regression with Continuous PHQ-9:**
   - Instead of binary grouping, use PHQ-9 score as a continuous IV
   - Linear regression: headtracking_speed ~ PHQ-9
   - Multiple regression: headtracking_speed ~ PHQ-9 + GAD-7 + STAI-T + age + gender

3. **ANCOVA (Analysis of Covariance):**
   - Compare depression groups while controlling for anxiety
   - DV: headtracking measure, IV: dep_group, Covariates: GAD-7, STAI-T, VR_experience

4. **Repeated-Measures / Mixed-Effects Models:**
   - Account for within-subject structure (each participant has 5 video measurements)
   - Random intercept for participant
   - Fixed effects: dep_group, video, dep_group × video interaction

5. **Video × Depression Interaction:**
   - Does the depression effect depend on video type?
   - Two-way interaction in ANOVA or regression

6. **Mediation Analysis:**
   - Does presence mediate the depression → headtracking relationship?
   - Path: Depression → Presence → Less exploration

7. **Power Analysis:**
   - Calculate the minimum effect size we could detect with N=40
   - Calculate the N needed to detect the original study's effect size

---

## 16. Glossary of Terms

| Term | Definition |
|------|-----------|
| **PHQ-9** | Patient Health Questionnaire-9: 9-item depression screener (0–27), scores ≥10 indicate moderate depression |
| **GAD-7** | Generalized Anxiety Disorder-7: 7-item anxiety measure (0–21) |
| **STAI-T** | State-Trait Anxiety Inventory, Trait subscale: measures chronic anxiety tendency (20–80) |
| **PANAS** | Positive and Negative Affect Schedule: measures current mood (PA and NA subscales, each 10–50) |
| **VRISE** | Virtual Reality Induced Symptoms and Effects: measures simulator sickness (5–35) |
| **Psychomotor retardation** | Slowing of physical movement and cognitive processing in depression |
| **Anhedonia** | Loss of interest or pleasure — a core depression symptom |
| **Yaw** | Horizontal head rotation (left/right) — maps to Y-axis in headtracking |
| **Pitch** | Vertical head rotation (up/down) — maps to X-axis |
| **Roll** | Lateral head tilt (ear to shoulder) — maps to Z-axis |
| **360° video** | Video captured in all directions; viewer can look anywhere by turning their head |
| **Valence** | How pleasant/unpleasant an emotional stimulus is (1=unpleasant, 9=pleasant) |
| **Arousal** | How calm/exciting an emotional stimulus is (1=calm, 9=excited) |
| **Presence/Immersion** | Feeling of "being there" in the virtual environment |
| **Welch's t-test** | Independent-samples t-test without equal-variance assumption (Topic 5) |
| **Paired t-test** | Within-subject comparison of means (Topic 5) |
| **One-way ANOVA** | F-test comparing 3+ group means (Topic 3+5, F-distribution) |
| **Cohen's d** | Standardized effect size for mean differences (Topic 5) |
| **Bonferroni correction** | Multiple comparison correction: α/m (Topic 6) |
| **Shapiro-Wilk** | Test for normality of a distribution |
| **η² (eta-squared)** | Effect size for ANOVA (proportion of variance explained) |
| **Pearson r** | Parametric correlation (linear association) |
| **Effect size (r)** | Standardized measure of the magnitude of an effect (r = z / √N) |
| **p-value** | Probability of observing the data (or more extreme) IF the null hypothesis is true |
| **Type I error** | False positive — rejecting H₀ when it's actually true |
| **Type II error** | False negative — failing to reject H₀ when it's actually false |
| **IQR** | Interquartile Range = Q3 - Q1 (middle 50% of data) |
| **Bonferroni correction** | Adjusts α by dividing by number of tests to control family-wise error rate |
| **ANCOVA** | Analysis of Covariance — ANOVA with continuous covariates controlled |

---

## 17. References

1. **Srivastava, P., Lahane, R., Vivek, R., & Pulapa, P. (2025).** What Do Head Scans Reveal About Depression? Insights from 360° Psychomotor Assessment. *Proceedings of the Annual Meeting of the Cognitive Science Society, 47*(0).

2. **Bennabi, D., et al. (2013).** Psychomotor retardation in depression: A systematic review. *BioMed Research International.*

3. **Kalin, N. H. (2020).** The Critical Relationship Between Anxiety and Depression. *American Journal of Psychiatry, 177*(5), 365–367.

4. **Kourtesis, P., et al. (2019).** Validation of the Virtual Reality Neuroscience Questionnaire. *Frontiers in Human Neuroscience, 13*, 417.

5. **Kroenke, K., Spitzer, R. L., & Williams, J. B. (2001).** The PHQ-9: Validity of a brief depression severity measure. *Journal of General Internal Medicine, 16*(9), 606–613.

6. **Spitzer, R. L., et al. (2006).** A brief measure for assessing generalized anxiety disorder: The GAD-7. *Archives of Internal Medicine, 166*(10), 1092–1097.

7. **Spielberger, C. D. (1983).** Manual for the State-Trait Anxiety Inventory (STAI). Consulting Psychologists Press.

8. **Watson, D., Clark, L. A., & Tellegen, A. (1988).** Development and validation of brief measures of positive and negative affect: the PANAS scales. *JPSP, 54*(6), 1063–1070.

---

## 18. Viva Preparation: Likely Questions & Answers

### Q1: Why did you use PHQ-9 ≥ 10 as the cutoff?
**A:** This is the clinically validated cutoff for **moderate depression** from the PHQ-9 manual (Kroenke et al., 2001). It has a sensitivity of 88% and specificity of 88% for major depressive disorder. The original study (Srivastava et al., 2025) used the same threshold for their moderate-severe group, making our results comparable.

### Q2: Why parametric tests despite non-normal data?
**A:** Three reasons: (1) t-tests are robust to moderate non-normality — extensive simulation research confirms this, (2) the Central Limit Theorem (CLT, Topic 4) ensures that with N=40, sampling distributions of means approach normality, and (3) Welch's t-test doesn't assume equal variances, handling our 8 vs 32 group imbalance. We also applied Bonferroni correction (Topic 6) for the 25 simultaneous t-tests (α_corrected = .002).

### Q3: What is Welch's t-test and why use it instead of Student's t-test?
**A:** Welch's t-test is an independent-samples t-test that does NOT assume equal variances between groups. It uses the Welch-Satterthwaite formula to adjust degrees of freedom. We use it because our groups (8 vs 32) likely have different variances, and Welch's is more robust in this situation. The test statistic is computed as t = (M₁ - M₂) / √(s₁²/n₁ + s₂²/n₂).

### Q4: You ran 25 t-tests. Isn't that a problem?
**A:** Yes — this is the **multiple comparisons problem** (Topic 6). At α=.05, we'd expect ~1.25 false positives by chance alone. We applied **Bonferroni correction** (α_corrected = 0.05/25 = 0.002). After correction, NONE of the 25 comparisons are significant. The single uncorrected result (V4 angular range, p=.048) does not survive correction — confirming it is likely a Type I error.

### Q5: Why didn't you replicate the original study's finding?
**A:** Most likely **insufficient statistical power**. With only n=8 in the depressed group, we need a very large effect size to detect it. The original study had a larger sample. Other possibilities: subclinical severity levels, different VR equipment.

### Q6: What is the difference between Pearson and Spearman correlation?
**A:** Pearson (r) measures **linear** association assuming roughly normal data. Spearman (ρ) measures **monotonic** association using ranks (non-parametric). We use Pearson because it aligns with the syllabus (Topic 7) and our parametric framework. With N=40, Pearson is reasonably robust to non-normality.

### Q7: Why did positive affect decrease after VR?
**A:** The paired t-test result (t=2.09, p=.043, Cohen's d=−0.33) shows a significant drop in positive affect—a small-to-medium effect. This could be due to: (1) the horror video (V4) having a lingering negative mood effect, (2) general fatigue from watching 5 videos in a row, or (3) VR-induced discomfort/motion sickness.

### Q8: What does "psychomotor retardation" mean and how does it relate to headtracking?
**A:** Psychomotor retardation is the **clinically observed slowing of movement and thinking** in depressed individuals. The theoretical link is: if depressed people's physical movements are slower, this should show up as **lower head rotation speed** and **less exploration** in VR. Srivastava et al. (2025) found significantly reduced scanning speed in the moderate-severe depression group (p < .001, η² = .295), but we did not replicate this, likely due to lower statistical power.

### Q9: Why did you compute so many headtracking summary measures?
**A:** Because we don't know a priori which measure best captures the depression-headtracking relationship. Speed captures how fast they move, SD captures variability, range captures how much of the scene they explored. The original study reported effects on multiple measures, so we compute all of them for comparison.

### Q10: What is the Kruskal-Wallis test?
**A:** It's the non-parametric equivalent of one-way ANOVA — it tests whether 3 or more independent groups differ in their distributions. We used it to test whether mean head rotation speed differed across the 5 videos. It did (H=33.51, p<.001), confirming that video content influences exploration behavior.

### Q11: What is Wilcoxon signed-rank test?
**A:** It's the non-parametric equivalent of the paired t-test. It tests whether paired measurements (same person, two time points) differ. We used it for pre-vs-post PANAS scores because the same participants were measured before AND after VR. It works by computing differences, ranking their absolute values, and testing if positive vs negative differences are balanced.

### Q12: How did you handle the data issues in the headtracking CSVs?
**A:** Each CSV had a **malformed last row** containing summary statistics with 13 columns instead of the 11 expected columns. Rather than manually editing 200 files, we used pandas' `on_bad_lines='skip'` parameter, which silently skips any row that doesn't match the expected format. We only lose one row per file (the summary row), which we don't need since we compute our own summaries.

### Q13: What is the IQR method for outlier detection?
**A:** IQR = Q3 - Q1 (interquartile range, the middle 50% of data). We define outlier fences at Q1 - 1.5×IQR (lower) and Q3 + 1.5×IQR (upper). Any point outside these fences is an outlier. It's robust because it uses the median and quartiles, which are not affected by extreme values themselves.

### Q14: Why did you keep the outliers?
**A:** The clinical score "outliers" (PHQ-9 > 14.2, GAD-7 > 14.5) are actually the **most clinically relevant participants** — they represent moderately severe depression/anxiety. Removing them would (1) reduce our already small depressed group, (2) remove exactly the participants we are most interested in, and (3) have no statistical justification since they represent genuine clinical variability.

### Q15: What is the effect size r and how is it computed from Mann-Whitney U?
**A:** Effect size r standardizes the magnitude of the difference so it's independent of sample size. For Mann-Whitney U, we compute it as r = z / √N, where z is the standardized test statistic. Interpretation: r < 0.1 negligible, 0.1–0.3 small, 0.3–0.5 medium, > 0.5 large. Our V4 finding had r=0.33 (medium), but the p-value barely reached significance.

### Q16: What is the difference between a parametric and non-parametric test?
**A:** **Parametric** tests (t-test, ANOVA, Pearson) assume the data follows a specific distribution (usually normal) and use sample statistics (mean, variance) directly. **Non-parametric** tests (Mann-Whitney, Kruskal-Wallis, Spearman) make no distributional assumptions and work on ranked data instead of raw values. Non-parametric tests have slightly less power when data IS normal but are more robust when it isn't.

### Q17: What will you do differently in Report 2?
**A:** Key improvements: (1) correct for multiple comparisons, (2) use PHQ-9 as continuous (not binary) in regression models, (3) include GAD-7/STAI-T as covariates to separate depression from anxiety, (4) use mixed-effects models for the within-subject repeated structure (5 videos per person), (5) test video × depression interactions, (6) conduct power analysis, (7) potentially test mediation by presence.

### Q18: What is a Type I vs Type II error in this context?
**A:** **Type I error (false positive):** Concluding headtracking differs between groups when it actually doesn't. Risk: our V4 finding might be this — 1 out of 25 tests being significant at p=.039 could easily be chance. **Type II error (false negative):** Concluding no difference exists when there actually is one. Risk: our non-significant main results might be this — we may have missed a real effect because N=8 gives very low power.

### Q19: Why use seaborn's violin plots instead of just box plots?
**A:** Violin plots show the **full distribution shape** (density estimation), not just summary statistics. This is important because: (1) with small samples, distributions can be multimodal or skewed, and box plots hide this; (2) the split violin (by group) lets us visually compare distribution shapes between depressed and non-depressed; (3) the inner quartile lines still show median and IQR.

### Q20: What is the VRISE score and why does it matter?
**A:** VRISE (VR-Induced Symptoms and Effects) measures **simulator sickness** — nausea, dizziness, disorientation from VR. Range is 5–35 (higher = less sickness). It matters because: if someone feels sick, their head movements might be **artificially restricted** (they stay still to avoid increasing nausea), which would confound our depression-headtracking analysis. One participant had VRISE=17 (potential sickness), flagged for sensitivity analysis.

---

*Last updated: March 2026*
