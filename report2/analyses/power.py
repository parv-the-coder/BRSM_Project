
import numpy as np
from statsmodels.stats.power import TTestIndPower


# ---------------------------------------------------------------------------

def run_power_analysis(n_dep: int = 8, n_nondep: int = 32) -> dict:
    original_eta2 = 0.295        # Srivastava et al. (2025)
    original_d    = 2 * np.sqrt(original_eta2 / (1 - original_eta2))
    ratio         = n_nondep / n_dep   # e.g., 4

    pa = TTestIndPower()

    # Observed power at the original effect size
    power_original = pa.solve_power(
        effect_size=original_d, nobs1=n_dep,
        ratio=ratio, alpha=0.05, alternative='two-sided',
    )

    # Minimum detectable effect at 80% power with current N
    mde = pa.solve_power(
        nobs1=n_dep, ratio=ratio,
        alpha=0.05, power=0.80, alternative='two-sided',
    )

    # Depressed-group N needed for 80% power at original d
    n_needed = pa.solve_power(
        effect_size=original_d, power=0.80,
        ratio=ratio, alpha=0.05, alternative='two-sided',
    )

    # Power curve data  (for plotting)
    d_range = list(np.linspace(0.05, 2.0, 200))
    power_current = [
        pa.solve_power(effect_size=d, nobs1=n_dep, ratio=ratio,
                       alpha=0.05, alternative='two-sided')
        for d in d_range
    ]
    power_doubled = [
        pa.solve_power(effect_size=d, nobs1=n_dep * 2, ratio=ratio,
                       alpha=0.05, alternative='two-sided')
        for d in d_range
    ]
    power_needed = [
        pa.solve_power(effect_size=d, nobs1=int(np.ceil(n_needed)),
                       ratio=ratio, alpha=0.05, alternative='two-sided')
        for d in d_range
    ]

    print(f"\n[Power] Original d = {original_d:.3f}  "
          f"(eta2={original_eta2})")
    print(f"  Power at original d (n_dep={n_dep}): {power_original:.3f}")
    print(f"  MDE at 80% power (current N):        d = {mde:.3f}")
    print(f"  n_dep needed for 80% power:          {int(np.ceil(n_needed))}")

    return {
        'original_eta2':        original_eta2,
        'original_d':           round(original_d, 3),
        'power_at_original_d':  round(power_original, 3),
        'n_dep_current':        n_dep,
        'n_nondep_current':     n_nondep,
        'mde_80pct':            round(mde, 3),
        'n_dep_needed_80pct':   int(np.ceil(n_needed)),
        'd_range':              d_range,
        'power_current':        power_current,
        'power_doubled':        power_doubled,
        'power_needed':         power_needed,
    }
