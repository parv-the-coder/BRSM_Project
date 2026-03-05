"""
config.py — Shared configuration, paths, and visual settings.
"""

import os
import warnings
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
HEADTRACK_DIR = os.path.join(DATA_DIR, 'headtracking-data')
FIG_DIR = os.path.join(BASE_DIR, 'figures')
os.makedirs(FIG_DIR, exist_ok=True)

# ── Visual settings ────────────────────────────────────────────────────────────
sns.set_theme(style='whitegrid', context='paper', font_scale=1.2)
plt.rcParams.update({
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'font.family': 'serif',
})

PALETTE_DEP = {'Non-Depressed': '#4C72B0', 'Depressed': '#DD8452'}

VIDEO_NAMES = {
    'v1': 'V1: Abandoned Buildings',
    'v2': 'V2: Beach',
    'v3': 'V3: Campus',
    'v4': 'V4: Horror (Nun)',
    'v5': 'V5: Tahiti Surf',
}
VIDEO_ORDER = ['v1', 'v2', 'v3', 'v4', 'v5']

# ── Clinical cutoffs ───────────────────────────────────────────────────────────
PHQ_CUTOFF = 10  # ≥10 is moderate depression (Kroenke et al., 2001)
