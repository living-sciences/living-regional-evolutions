# Blanchard & Katz (1992), "Regional Evolutions" — re-estimated through 2025

**What this is.** A unified re-estimation of the paper's four headline claims on annual state
panels (51 units) extended from the original 1952/1976–1990 samples through **2025**, using the
replication's ported VAR/IRF code with data pulled fresh from FRED/BLS (verified 2026-08). Every
window is a pooled fixed-effects OLS system; bands are 5–95th percentile from a 200-rep
state-cluster bootstrap. The flagship C3 result uses **household (LAUS) employment** throughout
(the paper's fn-37 variant, benchmark migration share **0.40**); establishment/payroll enters as a
1990+ robustness check. Original values below are read from the replication artifacts on disk
(`/workspace/eval/replication/codebase/results/*.json`) or the paper's printed numbers.

## C1 — Employment shocks are permanent; growth differences persist. **Shock-permanence HELD; cross-generation growth persistence FADED.**
- Fig-1 persistence slope of 1970–90 growth on 1950–70 growth = **0.71** (R² 0.76), essentially
  the paper's 0.70/0.75 (replication: 0.698/0.754). But the slope **decays across generations**:
  1970–90→1990–2007 = **0.64** (R² 0.67); 1990–2007→2007–2025 = **0.37** (R² 0.46). A state's
  growth *rank* is markedly less sticky in the most recent generation than in the paper's.
- AR(4) in Δn (relative payroll employment): the implied level response stays **permanent in every
  20-yr window** — year-4 IR 1.5–2.4, year-20 plateau 1.5–2.0; the most recent window (2006–2025)
  gives **1.62 / 1.52**, almost exactly the paper's 1.67 / ~1.5. Shocks to *relative* employment
  are still not undone.

## C2 — Relative unemployment mean-reverts quickly. **HELD (with the paper's own caveat).**
- AR(2) in the *level* of relative UR: the year-10 impulse response is **≈ 0 in every 15-yr window**
  (−0.03 to +0.02); year-5 fluctuates 0.0–0.33 around the paper's 0.29 (replication 0.08 on the
  short LAUS window; ours 0.08 on 1976–90, rising to 0.33 in GFC-centred windows). Deviations remain
  transitory.
- Cross-section: the **raw** 10-yr UR persistence slope is now higher (2015→2025 = **0.52**;
  2013→2023 = 0.34) than the paper's 1975→1985 = 0.03 — but this is the level-means artifact the
  paper itself flagged (its 1970→1990 raw slope was 0.41, 0.24 ex-farm). **After demeaning by
  1976–2025 state means the slope collapses to 0.28 / 0.004.** Persistent cross-state UR *gaps* are
  fixed effects, not slow mean-reversion.

## C3 — Adjustment runs through mobility, not job recovery. **Mechanism HELD, but migration's role has WEAKENED.**
- The transitory margins are intact: the UR response to a −1% employment shock still peaks at
  **+0.20 to +0.40 pp** in year 1 and has a **half-life of 3–4 years** in every window (paper: +0.32 pp,
  gone by 5–7 yrs).
- **The out-migration share of year-1 adjustment fell from 0.38 (1978–90) to ~0.24–0.28 in the
  2010s–2020s windows** (household basis; full-sample 0.33). On the establishment/payroll basis it
  eased from ~0.77 to **0.63** (2011–2025), around the paper's 0.65. States now absorb a larger part
  of a shock through unemployment and participation and a smaller part through people leaving.
- Employment shocks also became **less permanent recently**: the year-10 employment response shrank
  from −0.79% (1978–90) toward **≈ 0** in COVID-dominated windows (V-shaped 2020–21 recovery), and is
  −0.31% for 2011–2025. COVID-dummied series (thin overlay) track the baseline closely, so this is
  not purely a 2020–21 artifact.
- This is exactly the direction **Dao–Furceri–Loungani (2017)** reported with data through ~2013 —
  migration's share of regional adjustment has fallen and the unemployment/participation margins
  absorb more — and it is consistent with the well-documented secular decline in US interstate
  migration since the 1980s.

## C4 — Wages/incomes respond weakly; convergence. **Income response HELD; convergence STALLED.**
- Bivariate (Δn, relative log PCPI) VAR: per-capita-income trough after a −1% employment shock =
  **−0.83%** at year ~2 for 1952–90 (paper −0.9%; replication −0.83%). It **deepened to ~−1.5%** in
  1994–2019 windows and reverted to −0.85% most recently — income responds at least as much as in the
  original, always transitory, trough at year 2. Wage/price adjustment is still a modest, not a
  dominant, channel.
- Convergence: the slope of 20-yr PCPI growth on start-of-window log level **faded from −0.019
  (windows ending ~1975) to ~−0.005 (recent)**, vs the paper's −0.01 analogue. Income convergence has
  largely **stalled after ~1990**, the **Ganong–Shoag (2017)** finding, reproduced here inside the
  paper's own specification.

## Bottom line
The *question* — how US states absorb asymmetric shocks — is unchanged and again policy-relevant
(COVID, WFH-driven reallocation, falling mobility). The paper's structural facts survive: relative
employment shocks are permanent, relative unemployment is transitory, and the transitory margins die
out in a few years. What has **changed by 2025** is the *composition* of adjustment — **out-migration
does less of the work than it did in 1978–90** (~⅓ less on a household basis) — and the **stalling of
income convergence**. The headline mechanism is intact; its quantitative mix has drifted in the
direction the post-2010 literature predicted.

### What each number uses / caveats
- **C3 baseline = household (LAUS) survey employment**, 1976–2025 (migration benchmark 0.40); payroll
  (establishment) shown as 1990+ robustness (benchmark 0.65). C1/C4 use **payroll** employment;
  C2/C3 unemployment & participation are LAUS.
- LAUS state estimates are model-based, revised, and smoother than the paper's 1980s CPS numbers,
  which can mechanically raise measured persistence slightly.
- **No SIC→NAICS splice was needed**: FRED's reconstructed state total-nonfarm series (`{ST}NAN`)
  is continuous 1939–2025, so C1's long window uses one series (`splice_ratios.csv` records ratio =
  1.0). This replaces the instruction's download.bls.gov SIC splice — a simplification, not a gap.
- Out of scope as in the replication: the composition-adjusted CPS wage and manufacturing
  production-worker AHE (SIC, ends 2002) — per-capita income is the extendable wage-side measure the
  paper itself reported (Fig 13); pre-1976 state unemployment (LAUS starts 1976); the defense-Bartik IV.
