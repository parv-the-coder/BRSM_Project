# Presentation Explainer — Slide-by-Slide Guide

> **Purpose:** This document explains every slide in `presentation.html` in detail so that any group member (Parv / Hardik / Gaurav) can present confidently and answer viva questions.

---

## Slide 1: Title Slide

**What's on screen:** Project title, subtitle, group member names with roll numbers, date.

**What to say:**

"This project investigates whether headtracking data collected during 360° VR video viewing can serve as a behavioral marker of depressive symptoms. This is Report 1, which covers preliminary descriptive statistics, data visualization, and initial inferential tests. The study is a replication of Srivastava et al. (2025) conducted at IIIT Hyderabad."

**Key points if asked:**
- It's a **replication study** — we're testing whether findings from an earlier paper hold with our sample.
- Report 1 is preliminary (10 marks). Report 2 will have advanced analyses (20 marks).

---

## Slide 2: Background & Motivation

**What's on screen:** Four bullet points about depression, psychomotor retardation, VR headtracking, and the original study.

**What to say:**

"Depression is one of the top global causes of disability, but most screening tools like the PHQ-9 are self-report questionnaires — subjective and prone to bias. There's a clinical concept called **psychomotor retardation**, which is the observable slowing of physical movements in depressed individuals. The PHQ-9 even has an item for this (Item 8: 'Moving or speaking so slowly that other people noticed'). The idea is: if depressed people move more slowly, this should show up as **reduced head movement** when they're placed in an immersive 360° VR environment where there's lots to explore. Srivastava et al. (2025) from IIIT Hyderabad tested this and found that scanning speed was significantly lower in the moderate-severe depression group, with a large effect (p < .001, η² = .295, Cohen's d = 1.64). We're trying to replicate their finding."

**Viva questions to expect:**
- *"What is psychomotor retardation?"* → Clinically observed slowing of movements and thinking; a DSM-5 symptom of Major Depressive Disorder.
- *"What did the original study find?"* → Scanning speed (how fast you move your head around) was significantly lower in moderate-severe depression. Effect size η² = .295 means depression group explained ~30% of variance in scanning speed.
- *"What is anhedonia and how does it relate?"* → Anhedonia = loss of interest/pleasure. In VR, this could manifest as less curiosity → less head movement.

---

## Slide 3: Research Question

**What's on screen:** The core research question in large text.

**What to say:**

"Our central question is straightforward: can we distinguish people with depressive symptoms from those without based purely on how they move their heads in VR? Specifically, do depressed individuals rotate their heads more slowly or explore a smaller angular range during 360° video viewing?"

**Why it matters:**
- If yes → potential for an **objective, passive screening tool** for depression (no questionnaires needed).
- Could be embedded in consumer VR devices for passive mental health monitoring.

---

## Slide 4: Methods Overview

**What's on screen:** Four stat cards (40 participants, 5 videos, 200 headtracking files, ~70 Hz), list of measures, list of videos.

**What to say:**

"We recruited 40 college students. Each participant watched 5 different 360° videos on a Meta Quest 3 headset. This gives us 200 headtracking files (40 participants × 5 videos). The headset records head rotation at approximately 70 frames per second — so for each participant per video, we have thousands of data points recording their pitch (up-down), yaw (left-right), and roll (tilt) angles over time.

Alongside headtracking, we collected several self-report measures:
- **PHQ-9** — the main depression measure (9 items, scored 0–27)
- **GAD-7** — generalized anxiety (7 items, 0–21)
- **STAI-T** — trait anxiety (20 items, 20–80)
- **PANAS** — mood measured before AND after VR viewing
- **VRNQ-VRISE** — simulator sickness subscale
- Plus valence (pleasant-unpleasant), arousal (calm-excited), and presence ratings per video.

The five videos were chosen to span different emotional contexts: eerie (abandoned buildings), pleasant (beach), neutral (campus), high-arousal negative (horror movie), and high-arousal positive (surfing)."

**Viva questions:**
- *"Why 5 different videos?"* → To test whether the depression-headtracking relationship depends on the emotional content of the video. Srivastava et al. found effects were strongest in specific video types.
- *"What is PANAS?"* → Positive and Negative Affect Schedule — Short Form. 20 items: 10 for positive affect (enthusiastic, active, alert...) and 10 for negative affect (distressed, upset, hostile...). We measured it before and after VR to see if VR viewing changes mood.
- *"Why Meta Quest 3?"* → It's a standalone headset (no PC needed), widely available. The original study used HTC Vive Pro (tethered, 90 Hz). Our device is different, which is one reason results might differ.
- *"What does ~70 Hz mean?"* → About 70 measurements per second. So for a 60-second video, we get ~4,200 data points per participant per video.

---

## Slide 5: Depression Classification

**What's on screen:** PHQ-9 cutoff explanation, group sizes (8 depressed, 32 non-depressed), severity pie chart.

**What to say:**

"We used a PHQ-9 score of 10 or above as the cutoff for moderate depression. This is the standard clinical cutoff established by Kroenke et al. (2001) with sensitivity and specificity of 88% each for Major Depressive Disorder. The same cutoff was used by Srivastava et al.

In our sample, only 8 out of 40 participants scored ≥ 10 (the 'Depressed' group), while 32 scored below 10 (the 'Non-Depressed' group). This 20%/80% split is a major limitation because it gives us very low statistical power to detect group differences. Looking at the severity breakdown: 50% of our sample is in the minimal range (0–4), 30% mild (5–9), 12.5% moderate (10–14), and 7.5% moderately severe (15–19). Nobody scored in the severe range (20+)."

**Viva questions:**
- *"Why ≥ 10 specifically?"* → It identifies moderate depression. Kroenke et al. (2001) validated this threshold against structured clinical interviews (SCID). Sens = 88%, Spec = 88%.
- *"Why not use 3 groups like the original?"* → With only 8 depressed participants, further splitting would create groups too small for any meaningful analysis.
- *"What's the power issue?"* → With n₁=8, n₂=32, we'd need a very large effect size (d > 1.0) to detect a significant difference at α=.05 with 80% power. The original study's effect was d=1.64, but their sample was also bigger.

---

## Slide 6: Statistical Approach

**What's on screen:** Table of all statistical tests with their purpose and syllabus topic mappings. Highlight box explaining why parametric tests are appropriate.

**What to say:**

"Here's a summary of all tests we used and why. Everything is drawn from our BRSM syllabus:

1. **Shapiro-Wilk** (Topic 3) — tests whether data follows a normal distribution
2. **Pearson r** (Topic 7) — measures linear correlation between two variables
3. **Welch's t-test** (Topic 5) — compares means of two independent groups without assuming equal variances
4. **Paired t-test** (Topic 5) — compares means of the same group measured twice (pre vs post)
5. **Cohen's d** (Topic 5) — effect size measure for mean differences
6. **Bonferroni correction** (Topic 6) — adjusts significance threshold when making multiple comparisons
7. **IQR and z-score methods** — outlier detection

**Important:** You might be asked 'Why parametric tests when your data is non-normal?' The answer is:
- T-tests are **robust to moderate non-normality** — decades of simulation studies confirm this.
- With N=40, the **Central Limit Theorem** (Topic 4) ensures sampling distributions of means are approximately normal.
- **Welch's correction** handles the unequal variance issue (8 vs 32 group sizes).
- All these methods align directly with the BRSM syllabus topics."

**Viva questions:**
- *"What is Welch's t-test vs Student's t-test?"* → Student's assumes equal variances in both groups. Welch's does NOT — it adjusts degrees of freedom using the Welch-Satterthwaite formula. With 8 vs 32, variances likely differ, so Welch's is safer.
- *"What is the Central Limit Theorem?"* → As sample size increases, the sampling distribution of the mean approaches normality regardless of the population distribution. With N=40 it's generally considered sufficient.
- *"Why Bonferroni?"* → We ran 25 simultaneous t-tests. At α=.05, we'd expect 1.25 false positives by chance. Bonferroni divides α by the number of tests: .05/25 = .002. Only results below .002 are considered significant.

---

## Slide 7: Section Divider — Results

**What's on screen:** Large "Results" text.

**What to say:** "Now let's go through our results."

---

## Slide 8: Demographics

**What's on screen:** Demographics table (N, gender, age, VR experience) + demographics figure.

**What to say:**

"Our sample consists of 40 college students — 36 males and 4 females (90% male), which is a significant limitation for generalizability. Mean age is 22.8 years (SD = 1.8) with a range of 19–27. Sixteen participants (40%) had some prior VR experience.

The demographic figure shows three panels: age distribution (roughly normal around 23), the gender imbalance, and VR experience split."

**Viva questions:**
- *"Why is gender imbalance a problem?"* → Depression prevalence is roughly 2× higher in women. With only 4 females, any gender-specific depression patterns would be undetectable.
- *"Does VR experience matter?"* → Possibly — first-time VR users might explore more out of novelty, or less due to discomfort. This is a potential confound we should check in Report 2.

---

## Slide 9: Clinical Measure Distributions

**What's on screen:** PHQ-9 mean 6.03, GAD-7 mean 5.00, STAI-T mean 45.00. Distribution plots for all three.

**What to say:**

"The average PHQ-9 score was 6.03 — that's in the 'mild' range. Average GAD-7 was 5.00 (also mild) and STAI-T was 45.00 (moderate trait anxiety). The distributions are all positively skewed — most people score low, with a long right tail. The dashed red line in the PHQ-9 plot shows our cutoff at ≥ 10.

Shapiro-Wilk tests confirmed all three are significantly non-normal: PHQ-9 (W=0.897, p=.002), GAD-7 (W=0.883, p<.001), STAI-T (W=0.944, p=.045). This is expected in a predominantly non-clinical college sample — most people are healthy, creating a floor effect."

**Viva questions:**
- *"What does W=0.897 mean?"* → The Shapiro-Wilk W statistic ranges from 0 to 1. Values close to 1 mean data is close to normal. 0.897 is moderately below 1, indicating departure from normality.
- *"What is positive skew?"* → Most values clustered at the low end, with a tail stretching toward higher values. This is typical for clinical measures in non-clinical populations.

---

## Slide 10: Depression–Anxiety Covariance

**What's on screen:** Two figures side-by-side — PHQ-9 vs GAD-7 scatter plot and correlation heatmap. Pearson correlations reported.

**What to say:**

"This is clinically very important. PHQ-9 and GAD-7 are correlated at r = .579 (p < .001), and PHQ-9 and STAI-T at r = .642 (p < .001). This means depression and anxiety strongly overlap in our sample.

Why does this matter? If we just compare headtracking between depressed and non-depressed groups, any difference could be driven by **anxiety**, not depression — because the depressed group also tends to be more anxious. This is called **confounding**. In Report 2, we need to use ANCOVA or multiple regression to control for GAD-7 and STAI-T when testing the depression effect. The original study by Srivastava et al. did exactly this — they used ANCOVA with GAD-7 and STAI-T as covariates."

**Viva questions:**
- *"What is a confound?"* → A variable that is correlated with both the independent variable (depression) and dependent variable (headtracking), making it unclear which one is driving the effect.
- *"What is Pearson r?"* → A measure of linear association ranging from -1 to +1. r=.579 means a moderate-to-strong positive linear relationship.
- *"Why is the heatmap useful?"* → Shows the full correlation matrix of ALL variables at once — lets you spot patterns quickly. E.g., you can see that PANAS Negative Affect also correlates with PHQ-9.

---

## Slide 11: Video Emotional Profiles

**What's on screen:** Table of valence/arousal/presence per video + box plots.

**What to say:**

"The five videos elicited clearly different emotional profiles, confirming they span the intended emotional space:

- **V5 (Tahiti Surf)** had the highest valence (7.12 — very pleasant) and highest arousal (6.50 — exciting). 
- **V4 (Horror)** had the lowest valence (3.67 — unpleasant) but high arousal (5.95 — exciting in a scary way). 
- **V3 (Campus)** was the most neutral (moderate valence 6.15, lowest arousal 4.33).
- **V1 (Abandoned Buildings)** had low-moderate valence (5.20) and medium arousal.
- **V2 (Beach)** was pleasant (6.53) and calm (4.65).

For **presence** (how immersed you feel), V1 (Abandoned Buildings) scored highest (29.60) and V4 (Horror) scored lowest (19.85). The low presence for Horror might be because the video quality was lower or the horror content disrupted the feeling of 'being there'.

This matters because effects of depression on headtracking might depend on the emotional context of the video."

**Viva questions:**
- *"What is the circumplex model of emotion?"* → Russell (1980): emotions can be mapped on two dimensions — valence (pleasant/unpleasant) and arousal (calm/excited). Our 5 videos span different quadrants.
- *"What is presence?"* → The subjective feeling of 'being there' in the virtual environment. Measured via the VRNQ.

---

## Slide 12: Headtracking Speed Across Videos

**What's on screen:** Split violin plots of mean rotation speed by video and depression group. Descriptive speed pattern noted in green highlight.

**What to say:**

"This is one of the most important figures. It shows how fast people moved their heads (mean rotation speed in degrees per second) for each video, split by depression group (blue = non-depressed, orange = depressed).

Descriptively, we can see speed varies across videos. V1 (Abandoned Buildings) has the highest speed (~39°/s) because it's an exploratory, open environment. V4 (Horror) has the lowest (~24°/s) probably because the horror narrative forces you to look at specific focal points rather than freely explore.

Formal testing of whether these video-level differences are statistically significant (one-way ANOVA) is **deferred to Report 2**, where we'll also do repeated-measures analyses.

Visually, the blue and orange violins overlap substantially for every video — there's no obvious separation between depression groups."

**Viva questions:**
- *"What's a violin plot?"* → Combines a box plot with a density curve. Shows the full distribution shape, not just the quartiles. Wider parts = more data points at that value.
- *"Why does V4 have lower speed?"* → The Horror video has a narrative focus point (the nun) that draws attention. There's less incentive to freely explore.
- *"Why didn't you run ANOVA in Report 1?"* → We're saving ANOVA for Report 2 where we'll combine it with repeated-measures analysis and post-hoc comparisons for a more complete picture.

---

## Slide 13: Headtracking by Depression Group (Welch's t-test Results)

**What's on screen:** Table of t-statistics, p-values, and Cohen's d for Mean Speed and Total Angular Range across 5 videos. Red highlight about Bonferroni correction.

**What to say:**

"This is the key analysis. We ran Welch's t-tests comparing the depressed vs. non-depressed group on 5 headtracking measures across 5 videos = 25 tests.

For **mean speed**, no video shows a significant difference. All p-values are well above .05 (the smallest is V2 Beach at p=.239). Effect sizes (Cohen's d) are tiny: mostly |d| < 0.4.

The only result that reaches p < .05 (uncorrected) is **V4 Horror total angular range**: t = 2.21, p = .048, d = 0.83. But notice two problems:
1. The effect is in the **wrong direction** — depressed participants explored a LARGER angular range, opposite to the psychomotor retardation hypothesis.
2. After **Bonferroni correction** (α_corrected = .05/25 = .002), this result is NOT significant.

So the bottom line: **no reliable group differences** in headtracking between depressed and non-depressed participants."

**Viva questions:**
- *"What is Cohen's d and how do you interpret it?"* → Standardized mean difference: d = (M₁ - M₂) / pooled_SD. d=0.2 is small, 0.5 medium, 0.8 large. The V4 angular range d=0.83 is large, but the p-value doesn't survive correction.
- *"What is Bonferroni correction?"* → Divide α by number of tests: .05/25 = .002. Only p < .002 counts as significant. This controls the **family-wise error rate** (the probability of making ANY false positive across all 25 tests).
- *"Isn't Bonferroni too conservative?"* → Yes, it's the most conservative correction. Alternatives like Holm or Benjamini-Hochberg are less conservative. We'll explore these in Report 2.

---

## Slide 14: PHQ-9 vs Headtracking Correlations

**What's on screen:** Table of Pearson correlations between PHQ-9 and 3 headtracking measures. Yaw speed by group figure.

**What to say:**

"Instead of just grouping people as depressed vs. not, we also checked whether depression severity as a continuous score (PHQ-9 0–27) correlates with headtracking measures. We averaged each person's headtracking across all 5 videos to get one number per participant, then computed Pearson correlations.

The results are uniformly null:
- PHQ-9 vs Mean Total Speed: r = -.060, p = .712
- PHQ-9 vs Mean Yaw Speed: r = -.081, p = .617
- PHQ-9 vs SD Total Speed: r = -.158, p = .329

All correlations are near zero and nowhere close to significant. This confirms: in our sample, depression severity is **not linearly related** to any headtracking summary measure."

**Viva questions:**
- *"Why average across videos?"* → Gives one robust, summary measure per person. Video-specific effects cancel out and we get the person's typical head movement behavior.
- *"Could the relationship be non-linear?"* → Possible — maybe only severe depression affects headtracking, while mild-moderate doesn't. But with only 8 people above the cutoff (max score 18), we can't test this well.

---

## Slide 15: Angular Range by Group

**What's on screen:** Bar chart of total angular range by video and depression group with 95% CI error bars.

**What to say:**

"This figure shows the total angular range — how many degrees of rotation each participant covered — for each video, split by group. Error bars are 95% confidence intervals.

The key observation: in most videos, the confidence intervals completely overlap between groups, meaning no significant difference. V4 (Horror) shows a noticeable gap where the depressed group has a LARGER range, but this is the result we already flagged as opposite-to-hypothesis and non-significant after Bonferroni."

**Viva questions:**
- *"What do overlapping confidence intervals mean?"* → If 95% CIs overlap substantially, the group means are likely not significantly different. (Though technically, CIs can overlap slightly and still be significant — this is a visual heuristic.)
- *"What is angular range?"* → The total span of head rotation from the minimum angle to maximum angle during the video. Larger range = participant looked around more.

---

## Slide 16: PANAS Pre- & Post-VR Mood

**What's on screen:** Paired t-test table for Positive and Negative Affect + PANAS bar chart.

**What to say:**

"We measured mood using the PANAS before and after VR. Paired t-tests compare each person's pre vs. post score.

**Positive Affect** decreased from 34.52 to 32.15 — a significant drop (t(39) = 2.09, p = .043, Cohen's d = −0.33). This is a **small-to-medium effect**.

**Negative Affect** increased slightly from 12.70 to 13.95, but this was NOT significant (t = −1.06, p = .294, d = 0.17).

The decrease in positive affect could be because: (1) the horror video (V4) left a lingering negative mood, (2) general fatigue from watching 5 videos back-to-back, or (3) VR-induced discomfort."

**Viva questions:**
- *"What is a paired t-test?"* → Tests whether the mean DIFFERENCE between two measurements on the SAME participants is zero. df = n−1 = 39.
- *"What does Cohen's d = −0.33 mean?"* → A small-to-medium effect. The negative sign means post was lower than pre. The PA dropped by about 1/3 of a standard deviation.
- *"Why is this relevant to the study?"* → Watson et al. (1988) showed that low Positive Affect is characteristic of depression specifically (not just distress). If VR reduces PA → it could interact with depression effects on headtracking.

---

## Slide 17: Outlier Analysis

**What's on screen:** Table of outlier detection methods at results.

**What to say:**

"We checked for outliers using two methods:
- **IQR method** for clinical scores: values beyond Q1 − 1.5×IQR or Q3 + 1.5×IQR. Found 3 PHQ-9 outliers (scores above 14.2 — these are the moderately severe participants) and 2 GAD-7 outliers.
- **Z-score method** for headtracking: flagging any |z| > 3. Found zero outliers.

We also inspected the VRISE scores and found 1 participant with a low score (17), which could indicate simulator sickness.

**Important decision:** We retained ALL outliers because:
1. The clinical 'outliers' are just people with genuine moderately-severe depression — removing them would eliminate the exact people we're studying.
2. No headtracking values were extreme enough to suggest recording errors.
3. The low-VRISE participant is flagged for sensitivity analysis in Report 2 (re-run analyses without them to check if they affect results)."

**Viva questions:**
- *"What is the IQR method?"* → IQR = Q3 − Q1. Outlier if value < Q1 − 1.5×IQR or > Q3 + 1.5×IQR. It's robust to skewed distributions.
- *"When should you remove vs retain outliers?"* → Remove if they're data errors (typos, sensor malfunction). Retain if they represent real variability. Our clinical outliers are genuine.

---

## Slide 18: Summary of Findings

**What's on screen:** Six numbered findings with red highlight about non-replication.

**What to say:**

"Let me summarize our six main findings:

1. The sample is **predominantly non-clinical** — 80% below the moderate depression threshold.
2. Depression and anxiety are **strongly correlated** (r = .58) — MUST control for anxiety in Report 2.
3. Videos produced **distinct emotional profiles** and headtracking speed varies descriptively across videos (V1 highest at 39°/s, V4 lowest at 24°/s; formal ANOVA deferred to Report 2).
4. **No significant group differences** in mean headtracking speed between depressed and non-depressed groups for any video, even before Bonferroni correction.
5. The one uncorrected-significant result (V4 angular range, p = .048, d = 0.83) is in the **opposite direction** and doesn't survive Bonferroni.
6. **Positive affect decreased** significantly after VR (p = .043, d = −0.33).

**Bottom line:** The original study's finding of reduced scanning speed in depression was **not replicated** in this preliminary analysis."

---

## Slide 19: Why Didn't We Replicate?

**What's on screen:** Five bullet points explaining possible reasons for non-replication.

**What to say:**

"There are several plausible reasons:

1. **Insufficient statistical power** — the biggest issue. Only n=8 depressed vs n=32. The original had N=50 with 40% moderate-severe. With our small group, we'd need a massive effect to detect it.

2. **Binary vs 3-group classification** — the original used minimal/mild/moderate-severe groups. They found the effect primarily comparing moderate-severe to minimal. We collapsed into just 2 groups, diluting the effect.

3. **No anxiety covariate** — this is crucial. The original used ANCOVA to control for GAD-7 and STAI-T. Since depression and anxiety overlap (r = .58 in our data), the raw group comparison conflates both. In Report 2, we'll run ANCOVA.

4. **Different equipment** — Meta Quest 3 (our headset) vs HTC Vive Pro (original). Different tracking precision, field of view, and comfort could affect movement patterns.

5. **Different severity distribution** — our sample is mostly minimal-mild. The original had 40% moderate-severe. The strongest effects were in the severe group."

**Viva questions:**
- *"Is non-replication a failure?"* → No! It's valuable information. It suggests the effect may be smaller than originally reported, or dependent on specific conditions (severe depression, controlled anxiety, specific equipment).
- *"What would you need for adequate power?"* → To detect d=0.8 with α=.05 and 80% power in a two-sample t-test, you need ~26 per group. We only have 8 in one group.

---

## Slide 20: Plans for Report 2

**What's on screen:** Seven numbered plans for advanced analyses.

**What to say:**

"For Report 2, we plan these advanced analyses:

1. Compare **multiple comparison corrections** — Bonferroni, Holm step-down, and Benjamini-Hochberg FDR (Topic 6).
2. Use PHQ-9 as a **continuous predictor** in linear regression, exploiting the full range of scores instead of dichotomizing.
3. Run **ANCOVA** with GAD-7 and STAI-T as covariates — matching the original study's approach to isolate depression from anxiety.
4. Use **repeated-measures / mixed-effects models** — each person contributed 5 video observations; we need to account for this within-subject structure.
5. Test **video-type interactions** — maybe depression only affects headtracking in certain emotional contexts (neutral vs horror vs positive).
6. Conduct **mediation/moderation analysis** — does presence or simulator sickness mediate the depression-headtracking link?
7. Perform **power analysis** — calculate exactly what effect sizes we can detect, and plan sample size for future studies."

**Viva questions:**
- *"What is ANCOVA?"* → Analysis of Covariance. Like ANOVA but includes continuous covariates. Tests group differences in the DV while statistically controlling for the covariates. We'd test: does depression group predict headtracking speed after controlling for GAD-7 and STAI-T?
- *"What are mixed-effects models?"* → Models that include both fixed effects (e.g., depression group, video type) and random effects (e.g., individual participant intercepts). They handle the repeated-measures structure (5 videos per person).
- *"What is Benjamini-Hochberg?"* → Controls the False Discovery Rate (FDR) instead of FWER. Less conservative than Bonferroni — instead of controlling the chance of ANY false positive, it controls the PROPORTION of positives that are false. Typically has more power.

---

## Slide 21: References

**What's on screen:** Full list of 8 references.

**What to say:**

"These are our key references. The most important ones to know:
- **Srivastava et al. (2025)** — the original study we're replicating
- **Kroenke et al. (2001)** — validation of PHQ-9 and the ≥10 cutoff
- **Watson et al. (1988)** — PANAS development; key insight: low PA ↔ depression, high NA ↔ general distress
- **Spitzer et al. (2006)** — GAD-7 validation
- **Bennabi et al. (2013)** — systematic review of psychomotor retardation in depression"

---

## Slide 22: Thank You

**What's on screen:** "Thank You" + "Questions?"

**What to say:** "Thank you. Any questions?"

---

## Quick Reference: Numbers to Remember for Viva

| Statistic | Value | Source |
|-----------|-------|--------|
| N total | 40 | Our study |
| Depressed / Non-Depressed | 8 / 32 | PHQ-9 ≥ 10 |
| PHQ-9 Mean (SD) | 6.03 (4.63) | Our data |
| GAD-7 Mean | 5.00 | Our data |
| PHQ-9 & GAD-7 correlation | r = .579 | Our data |
| PHQ-9 & STAI-T correlation | r = .642 | Our data |
| ANOVA for video speed | F = 10.75, p < .001, η² = .181 | Our data |
| Number of t-tests | 25 (5 videos × 5 measures) | Our analysis |
| Bonferroni α | .05/25 = .002 | Our correction |
| Significant after Bonferroni | 0 / 25 | Our result |
| V4 angular range (uncorrected) | t = 2.21, p = .048, d = 0.83 | Our data |
| PA pre→post | 34.52 → 32.15, p = .043, d = −0.33 | Our data |
| Original study effect | p < .001, η² = .295, d = 1.64 | Srivastava et al. |
| Original study N | 50, with 40% moderate-severe | Srivastava et al. |

---

## Common Viva Traps & How to Handle Them

**Trap 1: "Your data is non-normal. Why didn't you use non-parametric tests?"**
→ "T-tests are robust to moderate non-normality. The Central Limit Theorem (Topic 4) ensures sampling distributions approach normality with N=40. We also used Welch's correction for unequal variances. This is standard practice in psychology research."

**Trap 2: "The V4 result was significant. Why do you call it a Type I error?"**
→ "It was p=.048 before correction, but after Bonferroni for 25 tests (α=.002), it's non-significant. Also, the direction is opposite to our hypothesis — depressed individuals explored MORE, not less. With 25 tests, we'd expect ~1.25 false positives by chance at α=.05."

**Trap 3: "What is the effect size and is it meaningful?"**
→ "Cohen's d quantifies how many standard deviations apart the two group means are. d=0.2 small, 0.5 medium, 0.8 large. Most of our effects are tiny (|d| < 0.4), indicating negligible practical differences."

**Trap 4: "Why can't you just run a t-test — why do you need ANCOVA?"**
→ "Because depression and anxiety are correlated (r=.58). A simple t-test on depression groups will also capture anxiety differences. ANCOVA statistically removes the variance due to anxiety, leaving only the unique effect of depression."

**Trap 5: "Did you use any machine learning?"**
→ "No. This analysis uses only classical statistical methods from the BRSM syllabus. ML would be inappropriate for N=40 with 8 in the smaller group due to overfitting risk."

**Trap 6: "What is the Shapiro-Wilk test?"**
→ "It tests the null hypothesis that data is drawn from a normal distribution. W ranges from 0 to 1; values close to 1 indicate normality. If p < .05, we reject the null and conclude the data is non-normal. Our PHQ-9 had W=0.897, p=.002 — significantly non-normal."

**Trap 7: "Explain the Bonferroni correction formula."**
→ "α_corrected = α / m, where m is the number of tests. For us: 0.05 / 25 = 0.002. A result is only significant if its p-value falls below 0.002. This controls the family-wise error rate — the probability of making even ONE Type I error across all 25 tests."
