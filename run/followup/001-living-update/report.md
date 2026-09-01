# Follow-up study — Blanchard & Katz (1992), "Regional Evolutions," re-estimated 1978–2025

## Question
The paper established that US states absorb asymmetric local shocks mainly through **labor
mobility** (people leave) rather than job recovery: relative employment shocks are *permanent*,
relative unemployment and participation effects are *transitory* (gone in ~5–7 years), and wages/
incomes respond only weakly. This follow-up re-estimates the paper's four main claims (C1
persistence/permanence, C2 unemployment mean-reversion, C3 the mobility-driven adjustment VAR, C4
income response & convergence) on data **extended through 2025**, using the replication's ported
fixed-effects panel-VAR/IRF code, and traces how each finding evolved from the original sample to now
— in 15/20-year rolling windows and named eras, with COVID handled explicitly and 90% state-cluster
bootstrap bands.

## Approach
- **Reused from the replication** (`/workspace/eval/replication/codebase/`): the IRF engines
  `trivariate_var.irf` (C3 companion-form Cholesky IRF, ordering [Δe, le, lp]), `bivariate_irfs.irf_bivar`
  (C4a), `univariate_irfs.ma_coefs` (C1b/C2 AR→IRF), and `states_meta` (51-unit metadata). The raw
  FRED CSVs the replication had already downloaded (`data/raw/`) — these turned out to already span
  **through mid-2026**, so no re-download of state UR/LF/PCPI/payroll was needed.
- **Added data** (fresh from FRED, verified 2026-08): state participation `LBSSA{FIPS}` (×51) and the
  national SA counterparts `CE16OV, CLF16OV, CIVPART, UNRATE, PAYEMS` — series the replication had not
  pulled because it only needed 1947–1990.
- **New code (in `workspace/`)**: `build_panel_annual.py` constructs the annual panel with the
  follow-up's *exact* variable definitions (household `E_hh = L·(1−UR/100)`, `POP = L/(LFPR/100)`,
  `le = ln(E_hh/L) − US`, `lp = ln(L/POP) − US`, `n = ln E_pay − ln PAYEMS`, `y = ln PCPI − ln PCPI_US`).
  `estimate_windows.py` wraps the reused IRF math in rolling windows + a state-cluster bootstrap
  (precomputing within-demeaned per-state blocks, which is exactly the pooled-FE estimator and makes
  200-rep bootstraps run in <0.1 s/window). `run_sweep.py` produces `estimates_by_window.csv`;
  `make_figures.py` produces the two figures.
- **Sanity gate first.** Before extending, the original-sample numbers were reproduced (see table).
  All gates pass except C2's year-5 IR, which lands at 0.08 rather than the [0.15, 0.45] target — but
  this matches the replication's own 0.08 exactly and is a documented consequence of the LAUS-only
  (1976+) short window; the sweep proceeds and findings.md flags it.

## Results

**Sanity gate (original sample) vs paper / replication.** All from my run unless noted.

| Claim | Statistic | Paper | Replication (on disk) | This study |
|---|---|---|---|---|
| C1a | Fig-1 slope 1970–90 on 1950–70 | 0.70 (R² .75) | 0.698 (R² .754) | **0.713 (R² .758)** |
| C1b | AR(4) emp IR yr4 / yr20 | 1.67 / ~1.5 | 1.63 / 1.53 | **1.63 / 1.53** |
| C2 | AR(2) UR IR yr5 / yr10 | 0.29 / ~0 | 0.077 / −0.013 | **0.079 / −0.013** |
| C3 | year-1 UR response (pp) | +0.32 | — (est. basis) | **+0.37** (household) |
| C3 | year-1 migration share | 0.40 hh / 0.65 est. | 0.601 (est.) | **0.383** (household) |
| C4a | income trough (%) / year | −0.9 / 2 | −0.83 / 1 | **−0.83 / ~1–2** |

Sources: paper text; replication `results/{persistence_convergence,table1_irfs,trivariate_var,bivariate_irfs}.json`.

**Evolution 1978→2025 (named eras, C3 household basis; 90% bootstrap bands).**

| Statistic | 1978–90 | 1991–2007 | 2008–2019 | 2011–2025 | full 1978–2025 |
|---|---|---|---|---|---|
| year-1 UR resp. (pp) | 0.37 | 0.21 | 0.28 | 0.20 | 0.32 |
| UR half-life (yr) | 3 | 3 | 3 | 3 | 4 |
| year-10 emp resp. (%) | −0.79 | −0.45 | −0.17 | −0.31 | −1.32 |
| **year-1 migration share** | **0.38** | **0.36** | **0.24** | **0.28** | **0.33** |

**Headline findings** (full detail in `results/findings.md`):
- **C1 — shock permanence HELD; growth persistence FADED.** Relative-employment shocks stay permanent
  in every window (AR(4) plateau 1.5–2.0 throughout). But cross-generation growth persistence decays:
  Fig-1 slope 0.71 → 0.64 → **0.37** across successive 20-yr pairs. States' growth ranks are less sticky.
- **C2 — mean-reversion HELD.** Year-10 UR impulse response ≈ 0 in every window. The *raw* 10-yr
  cross-section slope rose (0.52 for 2015→2025) but **collapses to ~0 after demeaning by state means** —
  the level-heterogeneity caveat the paper itself raised.
- **C3 — mechanism HELD, migration's role WEAKENED.** UR/participation still peak small and die out in
  3–4 years, but the **out-migration share of year-1 adjustment fell from 0.38 to ~0.24–0.28**
  (household; 0.77→0.63 on payroll). Employment shocks also became **less permanent** recently
  (year-10 response toward 0; V-shaped COVID recovery, robust to 2020–21 dummies). This matches
  **Dao–Furceri–Loungani (2017)** and the secular fall in interstate migration.
- **C4 — income response HELD; convergence STALLED.** Income trough −0.83% at year ~2 (deepening to
  −1.5% mid-sample), always transitory. Convergence slope faded from −0.019 to ~−0.005 — the
  **Ganong–Shoag** post-1990 convergence stall, inside the paper's own spec.

**Figures.** `results/bk_living_update.png/.pdf` — 2×2 C3 flagship (year-1 UR, UR half-life,
year-10 employment, migration share) vs window-end year, with 90% bands, BK-1992 star, printed
reference lines, COVID overlay. `results/bk_supporting.png` — C1 (Fig-1 pairs + AR(4) permanence),
C2 (UR IR over windows), C4 (income trough + convergence stall), and the household-vs-payroll
migration split.

**Artifacts.** `results/estimates_by_window.csv` (481 tidy rows incl. `window_start=orig` headline
rows), the two figures, `results/data/panel_annual.csv` (constructed 1939–2025 panel),
`results/data/splice_ratios.csv`, and `results/findings.md`.

## Deviations & limitations
1. **No SIC→NAICS splice** (deviation from the instruction's download.bls.gov step): FRED's
   reconstructed state total-nonfarm series `{ST}NAN` is a single continuous series 1939–2025, so C1's
   long window needs no splice. `splice_ratios.csv` records link ratio = 1.0 with this rationale. This
   is simpler and avoids the BLS-403 failure mode entirely; total nonfarm is concept-identical across
   the eras, so the effect on C1 is nil (Fig-1 slope reproduces 0.70).
2. **C2 year-5 gate low (0.08 vs [0.15, 0.45]).** Reproduces the replication's own 0.08; driven by the
   LAUS-only start (1976, vs the paper's 1972 with constructed pre-1976 data) and revised, smoother
   LAUS estimates. Does not affect the qualitative claim (year-10 ≈ 0). Flagged in findings.md.
3. **Household year-1 UR response 0.37 pp** (vs paper's establishment-basis printed 0.32) and
   **household year-10 employment −0.79%** (shallower than the establishment −1.3 to −1.8): expected
   — the paper's fn-37 notes the household variant has near-identical *shapes* but a different level;
   the payroll robustness rows reproduce the deeper establishment plateau (−1.5%).
4. **Out of scope** (unchanged from the replication): composition-adjusted CPS wage & manufacturing
   production-worker AHE (per-capita income is the extendable wage-side proxy, as in the paper's Fig 13),
   pre-1976 state unemployment, and the defense-contract Bartik IV.
5. **Optional C4b (house prices)** was not run — the four required claims and all mandatory outputs
   were completed first and the optional stretch was left to conserve scope.
