import os
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
# r2/ lives one level below the project root
R2_DIR   = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(R2_DIR)

DATA_DIR      = os.path.join(BASE_DIR, 'data')
HEADTRACK_DIR = os.path.join(DATA_DIR, 'headtracking-data')
FIG_DIR       = os.path.join(BASE_DIR, 'figures', 'r2')
STATS_OUT     = os.path.join(FIG_DIR, 'stats_output.json')

os.makedirs(FIG_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Clinical cut-offs
# ---------------------------------------------------------------------------
PHQ_CUTOFF = 10          # PHQ-9 >= 10 => moderate depression (Kroenke et al., 2001)

# ---------------------------------------------------------------------------
# Video metadata
# ---------------------------------------------------------------------------
VIDEO_ORDER = ['v1', 'v2', 'v3', 'v4', 'v5']

VIDEO_NAMES = {
    'v1': 'V1: Abandoned\nBuildings',
    'v2': 'V2: Beach',
    'v3': 'V3: Campus',
    'v4': 'V4: Horror\n(Nun)',
    'v5': 'V5: Tahiti\nSurf',
}

VIDEO_NAMES_SHORT = {
    'v1': 'V1: Abandoned',
    'v2': 'V2: Beach',
    'v3': 'V3: Campus',
    'v4': 'V4: Horror',
    'v5': 'V5: Tahiti',
}

# ---------------------------------------------------------------------------
# Visual settings
# ---------------------------------------------------------------------------
PALETTE_DEP = {'Non-Depressed': '#4C72B0', 'Depressed': '#DD8452'}

VIDEO_COLORS = ['#4C72B0', '#55A868', '#C44E52', '#8172B2', '#CCB974']

sns.set_theme(style='whitegrid', context='paper', font_scale=1.2)
plt.rcParams.update({
    'figure.dpi':    150,
    'savefig.dpi':   300,
    'savefig.bbox':  'tight',
    'font.family':   'serif',
})
