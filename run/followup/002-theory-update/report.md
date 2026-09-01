# Follow-up 002 — Calibrated theory update: Blanchard & Katz (1992) migration-adjustment model, recalibrated to 2026

## Question

Seeded from the completed replication and from follow-up 001 (which re-estimated BK's
four headline claims through 2025 and found the migration channel weakened and income
convergence stalled), produce the **next intellectual step**: a calibrated, updated
version of BK's own migration-adjustment model — recalibrate its central structural
parameter (the migration elasticity) on the latest data, make the *minimal* amendment
that reconciles the 1992 and 2026 evidence, validate it out-of-sample and on the
episodes the original cannot explain, and quantify what slower adjustment implies for
BK's central policy object: **the duration of a local slump.**

## Approach

- **Re-read the paper's model** (`inputs/paper.pdf`, "Simple Models of Regional
  Evolutions", eq. 4–7, pp. 15–22, and the closed form on p. 18). The migration/labor-
  supply equation (eq. 7, line 3) is the object of the update: migration responds to
  relative wage `b` and relative unemployment `g`; the wage-gap decays at `λ = a+d·b`,
  so a weaker migration response lengthens the slump and shrinks the permanent
  employment loss.
- **Reused from 001** (no new downloads, per the brief): the extended annual panel
  `001/results/data/panel_annual.csv` (51 states, 1939–2025) and the estimated moments
  `001/results/estimates_by_window.csv` (C3 migration share, UR half-life, cumulative
  UR, long-run employment). **Reused from the replication codebase:** the pooled-FE
  AR→IRF engine (`src/univariate_irfs.py: pooled_ar, ma_coefs`) for the empirical UR
  impulse-responses in the figure.
- **New estimation** (`workspace/estimate_migration_elasticity.py`): directly estimate
  BK's migration equation — relative labor-force and population growth on lagged
  relative unemployment (± relative income), state FE, state-clustered SEs — per era
  and in 15-year rolling windows → `results/data/migration_elasticity.csv`. This is a
  *new structural estimate of BK's migration parameter*, independent of 001's VAR share.
- **Calibration + validation** (`workspace/calibrate_model.py`): map the two estimated
  moments (σ_m, H) to the two-margin adjustment parameters (m, a) per era; build the
  paper-vs-2026 calibration table; run the slump-duration counterfactual; and validate
  with (i) a held-out pre-2015→2015-24 elasticity test and (ii) the COVID episode.
- **Figure** (`workspace/make_figure.py`): four panels, original vs updated.

## Results

### The structural migration parameter roughly halved [ESTIMATED]

Direct FE estimation of BK's migration equation:

| migration responsiveness `m = −∂(Δn)/∂u` | paper-era 1976–90 | recent 2010–25 | change |
|---|---|---|---|
| labor force (Δn\*) | 0.00474 (se 0.00072) | 0.00225 (se 0.00049) | **−53%** |
| population (Δpop)  | 0.00339 (se 0.00057) | 0.00118 (se 0.00031) | **−65%** |

Both paper-era estimates are ~7σ from zero; both roughly halve by 2026. Controlling
for relative income leaves the unemployment coefficient essentially unchanged and the
wage coefficient small/insignificant — the weakening is in the response to job
availability, matching 001's VAR-share finding through a second, independent channel.

### Calibration: paper-era vs 2026 (household basis)

| parameter | symbol | paper-era 1978–90 | 2026 (2011–25) | label |
|---|---|---|---|---|
| year-1 migration share | σ_m | 0.383 | 0.276 | [ESTIMATED] |
| UR-gap half-life (yr) | H | 3.0 | 3.0 | [ESTIMATED] |
| migration clearing rate | m | 0.079 | 0.057 | [CALIBRATED] |
| job-recovery clearing rate | a | 0.127 | 0.149 | [CALIBRATED] |
| long-run rel-employment loss | −m/S | −0.383 | −0.276 | [CALIBRATED] |

**The composition of adjustment rotated:** migration's clearing rate fell 28%, job
recovery's rose 17%. Because they offset, the one-off UR half-life is unchanged (~3 yr).

### Comparison to the original values (read from disk)

| quantity | original (source) | this study | note |
|---|---|---|---|
| yr-1 migration share, household | 0.40 (paper fn.37) / 0.383 001 C3 `mig_yr1` 1978-90 | 0.276 (2011-25) | −28% |
| yr-1 migration share, payroll | 0.65 (paper) / 0.77 001 C3_payroll 1990-04 | 0.630 (2011-25) | −18% |
| migration elasticity `m` (structural) | not estimated by paper/001 | 0.00474→0.00225 | **new [ESTIMATED]** |
| UR-gap half-life (one-off) | 5–7 yr (paper) / 3 yr (001 1978-90) | 3 yr (2011-25) | stable for one-off shocks |
| UR half-life, GFC window | — | 5 yr (1995-2009) | slump lengthens for severe/persistent shocks |
| long-run rel-emp loss | −0.38 to −1.3 (paper/001) | −0.28 (2026); −0.21 (COVID) | permanence weakened |

Sources: `inputs/paper.pdf` p.18/fn.37; `001/results/estimates_by_window.csv`
(C3, C3_payroll); this study's `results/data/migration_elasticity.csv` and
`calibration_table.csv`.

### Slump duration — the policy object [CALIBRATED]

- **One-off shocks: no longer, but more locally borne.** UR half-life stable at ~3 yr;
  the model attributes this to job recovery `a` rising as migration `m` falls.
- **Severe, persistent shocks (GFC 1995–2009): materially longer.** σ_m→0.32, H→5 yr,
  time-to-80%-recovery ~11.6 yr, cumulative 10-yr excess UR **1.56 vs 0.33** paper-era.
- **Counterfactual "price of immobility":** holding 2026 job dynamics, restoring
  paper-era migration cuts the one-off half-life 3.0→2.7 yr and cumulative slump 10%.
- **COVID 2020 — the episode the original can't explain:** V-shaped recovery
  (`emp_lr = −0.22`, near-zero year-10); the updated model (m=0.043, a=0.163)
  reproduces a small non-permanent loss (−0.21); the high-migration original does not.
- **Held-out check:** migration elasticity fit on pre-2015 (0.00370) over-predicts
  out-migration in held-out 2015–24, where the true elasticity is 5× smaller (0.00076).

### The updated theory

The minimal amendment is a **declining, time-varying migration-responsiveness
parameter `g_t`** — the reduced-form footprint of rising real moving costs (housing;
Ganong–Shoag 2017, Hsieh–Moretti 2019). It reproduces both eras with a single added
degree of freedom. An explicit house-price/moving-cost margin was considered and
**rejected** (needs unavailable state HPI data; adds ≥2 unidentified parameters;
observationally equivalent to a lower `g_t`). Full write-up in
`results/theory_update.md`.

## Deviations & limitations

1. **The two-margin `(m, a)` model is a stylized single-mode reduction** of BK's
   richer dynamics, calibrated (exactly identified) to two moments (VAR migration
   share, UR half-life). It is a calibration device for the slump-duration
   counterfactual, **not** a newly estimated multi-equation IRF. The *directly
   estimated* migration elasticity (§ "roughly halved") is the genuine [ESTIMATED]
   structural quantity; the `(m,a)` split is [CALIBRATED] and labelled as such.
2. **The one-off UR half-life did not lengthen** — an honest tension with the
   instruction's premise that slower migration → longer slumps. It resolves as a
   *composition* rotation (m↓, a↑) plus a genuine lengthening confined to severe
   persistent shocks (GFC window, H 3→5). Reported as found, not massaged.
3. **Paper-era anchor.** For internal consistency the paper-era column uses 001's
   same-pipeline 1978–90 window (σ_m 0.383, H 3); the paper's *printed* values
   (σ_m 0.40, H 5–7) are shown alongside. The paper's longer printed half-life partly
   reflects the small-sample persistence bias its own discussant (R. Hall) flagged.
4. **Data scope unchanged from 001/replication:** LAUS state coverage from 1976;
   relative per-capita income as the wage-side proxy (composition-adjusted CPS wages
   and SIC manufacturing AHE remain unreconstructable). No house-price panel was
   built, so the housing mechanism is named and modelled as reduced-form `g_t`, not
   estimated from HPI directly. No new data downloaded; compute was estimation +
   calibration only.

### Artifacts (under `results/`)
- `theory_update.md` — the "Theory, updated to 2026" section (main deliverable).
- `calibration_table.csv` — paper-era vs 2026 parameters, sources, labels.
- `fig1_bk_theory_update.png` / `.pdf` — 4-panel original-vs-updated figure.
- `data/migration_elasticity.csv` — direct FE migration-elasticity estimates (172 rows).
- `data/calibration_full.csv`, `data/model_summary.json` — per-era calibration + validation.
