# Living Update Spec — Blanchard & Katz (1992), "Regional Evolutions" (BPEA 1:1992)

You are the FOLLOWUP agent. You are seeded from a completed replication of this paper and keep
its ported codebase (pooled fixed-effects panel VARs, impulse responses). Your job is to
re-estimate the paper's main claims on data extended through 2025 (monthly source data run
through mid-2026; use complete calendar years, so the last estimation year is 2025) and show
how each finding evolved from the original sample to now.

All estimation is annual-frequency panel OLS on 51 units (50 states + DC). Everything runs in
minutes in Python (pandas + numpy/statsmodels). Reuse the replication's IRF/VAR code where it
exists; otherwise the specs below are self-contained.

## The paper's main claims (what you are updating)

**C1 — Employment shocks are permanent; state growth differences are persistent.**
- Fig 1: OLS of state average annual log-employment growth 1970–90 on growth 1950–70:
  slope **0.70**, R² **0.75** (nonfarm payroll employment, 51 units).
- Table 1 col 1: pooled AR(4) with state FE in Δn_it (n = log state employment − log US
  employment), 1952–90. Implied impulse response to a unit innovation: **1.67 at year 4,
  plateau ≈ 1.5 at year 20** (hump then permanent level effect).

**C2 — Relative unemployment rates mean-revert quickly (no permanent effect).**
- Table 1 col 2: pooled AR(2) with state FE in the *level* of u_it (state UR − US UR),
  1972–90. Impulse response: **0.29 of the shock left after 5 years, ≈ 0 after 10**.
- Fig 3: cross-section of state UR in 1985 on UR in 1975: slope **0.03**, R² **0.00**.

**C3 (the famous one) — Adjustment happens through labor mobility, not job recovery.**
Trivariate pooled VAR, state FE, **2 lags**, sample **1978–90** (data from 1976), in:
  - Δe_it = Δ(log E_it − log E_US,t)  (relative employment growth)
  - le_it = log(E/L)_i − log(E/L)_US  (≈ −relative unemployment rate)
  - lp_it = log(L/POP)_i − log(L/POP)_US  (relative participation)
Ordering: Δe is predetermined within the year; le and lp equations include *current* Δe plus
2 lags of everything. Shock = −1% innovation to the Δe equation. Headline IRs:
  - year-1: UR **+0.32 pp**, participation **−0.17 pp**
  - employment: trough **−2.0%** at year 4, plateau **≈ −1.3%**
  - UR and participation effects **vanish after 5–7 years** → a state recovers because
    workers leave, not because jobs come back; implied year-1 out-migration **0.65** workers
    per job lost (0.40 when household employment is used — footnote 37; you will use the
    household-based number as your comparable baseline).

**C4 — Wages/incomes respond weakly; wage adjustment does not drive recovery.**
- Fig 13 (per capita income variant — the one you will update): bivariate pooled VAR, state
  FE, **4 lags**, 1952–90, in Δe_it and relative log per-capita personal income; income
  trough **−0.9%** at year 2 after a −1% employment shock, slowly back to 0.
- Fig 4 (convergence): growth of state mfg wage 1950–90 on log 1950 level: slope **−0.01**
  (t = 5.4, R² = 0.39). You will update convergence with per-capita income.
- (Optional C4b, Fig 15): house prices trough ≈ −2% at years 4–5 and are transitory.

## Data — all verified 2026-08-23; exact sources

**FRED public CSV endpoint (no key needed):**
`https://fred.stlouisfed.org/graph/fredgraph.csv?id={SERIES}` returns
`observation_date,{SERIES}` CSV. If it rate-limits or returns HTML, fall back to the FRED API
with the provided key:
`https://api.stlouisfed.org/fred/series/observations?series_id={SERIES}&api_key=$FRED_API_KEY&file_type=json`.

Per-state series (replace `{ST}` = 2-letter postal, `{FF}` = 2-digit state FIPS):
| Variable | FRED ID | Freq/Adj | Verified coverage |
|---|---|---|---|
| State unemployment rate (LAUS) | `{ST}UR` (e.g. MAUR, CAUR, DCUR, HIUR) | monthly SA | 1976-01 → 2026-06 |
| State civilian labor force (LAUS) | `{ST}LF` (MALF, CALF) | monthly SA, persons | 1976-01 → 2026-06 |
| State labor force participation rate (LAUS) | `LBSSA{FF}` (LBSSA25=MA, LBSSA06=CA, LBSSA11=DC) | monthly SA, % | 1976-01 → 2026-07 |
| State total nonfarm payroll employment (CES/SAE, NAICS) | `{ST}NA` (MANA, CANA, WYNA, INNA, ORNA, DCNA, AKNA) | monthly SA, thousands | 1990-01 → 2026-07 |
| State per capita personal income (BEA) | `{ST}PCPI` (MAPCPI, NDPCPI) | annual | 1929 → 2025 |
| State all-transactions house price index (FHFA) | `{ST}STHPI` (MASTHPI) | quarterly | 1975Q1 → 2026Q1 |

National counterparts (FRED): `PAYEMS` (payroll employment, 1939→), `CE16OV` (household
employment, 1948→), `CLF16OV` (labor force, 1948→), `CIVPART` (participation rate, 1948→),
`UNRATE`, `A792RC0A052NBEA` or simply use `PCPI` national = personal income / population; easier:
compute the US per-capita income counterpart as the employment-weighted... **no** — use FRED
series `A229RC0A052NBEA` (US per capita personal income, annual); if that ID fails, probe
`PCPI` alternatives via the API search, or construct US as the population-weighted mean of the
51 state PCPIs (states' own aggregate; acceptable since only relative logs matter).

**Historical SIC-era state payroll employment, 1939–2002 (to reproduce/extend C1's long window):**
BLS discontinued "SA" database on `download.bls.gov` — requires a User-Agent header with a
contact email or you get 403. Verified working:
```
curl -s -A "research contact (haokun@sai.science)" \
  https://download.bls.gov/pub/time.series/sa/sa.data.22a.Massachusetts
```
- Directory: `https://download.bls.gov/pub/time.series/sa/` (files `sa.data.{n}[a-i].{StateName}`,
  one or more per state, numbered alphabetically 1=Alabama … 53=Wyoming; plus `sa.series`,
  `sa.txt`).
- Series ID inside the data files: `SAU{FIPS}00000000001` = statewide total nonfarm, all
  employees, NSA, thousands. Verified: `SAU2500000000001` (MA) has annual (`M13`) values
  1939–2002 (1939 M13 = 1367.6). Use `M13` rows = annual averages.
  Note: a state's series may be split across its lettered files (22a holds up to ~1983);
  download all files for each state and concatenate.
- SIC mfg production-worker AHE also exists (`SAU{FIPS}00003000016`, data type 6) but only
  from 1972 — this is why C4 is carried by per-capita income, not the mfg wage.

**Splice** the payroll series: SIC `SAU…` annual 1947–1989 ratio-linked to NAICS `{ST}NA`
annual averages at 1990 (compute both in overlap 1990–2002 if you download SIC through 2002;
total nonfarm is conceptually identical across SIC/NAICS so the link ratio should be ≈ 1 —
report it per state; investigate any state where it deviates by > 2%). Result: state total
nonfarm employment 1947–2025, 51 units (AK from 1960, HI from 1955, DC wage/emp per paper
appendix — accept later starts, drop pre-start years for those states as the paper did).

**Optional (only if time permits):** QCEW average annual pay by state for a wage-proper
robustness check: API CSV verified for 2014–2024:
`https://data.bls.gov/cew/data/api/{year}/a/area/{FIPS}000.csv` (e.g. 25000 = MA; field
`avg_annual_pay`, aggregation row `own_code=0, industry_code=10`). Years before 2014 are NOT
on that API (404); use zips `https://data.bls.gov/cew/data/files/{year}/csv/{year}_annual_singlefile.zip`
(verified HTTP 200 for 1990). Do not build the main deliverable on this.

**Do NOT attempt:** IPUMS/CPS microdata (key pending — the paper's composition-adjusted CPS
wage is therefore out of scope), the paper's pre-1976 constructed LMA unemployment rates
(infeasible; start all UR analysis in 1976), and the defense-contracts/Bartik-mix IV section
(source series DLM 1951–88 is not publicly downloadable; skip).

## Variable construction (annual state panel)

1. Pull monthly series, average calendar years → annual. Last complete year = 2025.
2. Household side (1976–2025): `L` = {ST}LF; `UR` = {ST}UR; `E_hh = L*(1-UR/100)`;
   `LFPR` = LBSSA{FF}; `POP = L/(LFPR/100)` (civilian noninstitutional pop 16+, back-derived).
3. National: `E_hh_US = CE16OV`, `L_US = CLF16OV`, `LFPR_US = CIVPART`, `UR_US = UNRATE`.
4. Relative logs exactly as the paper: `e = ln E − ln E_US`; `le = ln(E/L) − ln(E_US/L_US)`;
   `lp = ln(L/POP) − ln(L_US/POP_US)`; `u = UR − UR_US` (pp); `n = ln E_payroll − ln PAYEMS`;
   relative income `y = ln PCPI_state − ln PCPI_US`.
5. Baseline for C3 uses **household (LAUS) employment** (consistent 1976–2025). The paper's
   baseline used establishment employment (year-1 migration 0.65); its household variant gave
   0.40 with near-identical shapes (fn. 37) — **compare your estimates to the 0.40/household
   benchmark**, and run the payroll-employment variant on 1990+ windows as a robustness check.

## Estimation per claim, and windows

Sanity gate first: reproduce the original-sample numbers before extending. Targets (accept
within tolerance given data revisions): C3 on 1978–90 should give year-1 UR response ≈ 0.3 pp
(sign and hump shape mandatory), UR/participation effects ≈ 0 by year 7, long-run employment
response between −1 and −2; C2 on 1976–90 AR(2) IR at year 5 in [0.15, 0.45]; C1 Fig-1-style
slope on (1950–70, 1970–90) ≈ 0.7 with the spliced payroll data. If a gate fails, debug
construction (most likely: relative-variable definition or annual averaging) before proceeding.

**C3 flagship — rolling trivariate VAR.** Pooled FE, 2 lags, spec above. Windows: 15-year
rolling windows of estimation years, first window 1978–1992, stepping 1 year to 2011–2025
(≈ 34 windows; each is one OLS system — cheap). Also estimate four named eras for the table:
1978–1990 (original), 1991–2007, 2008–2019, 2011–2025 (or 2012–2025 if lags force it), and
full 1978–2025. From each window's IRFs to a −1% employment innovation record:
  - `ur_yr1`: year-1 unemployment-rate response in pp (convert from le: multiply by minus the
    window-mean of E/L as the paper does, ≈ 0.94);
  - `ur_cum10`: sum of UR responses years 1–10 (cumulative unemployment burden);
  - `ur_halflife`: first year the UR response falls below half its peak;
  - `emp_lr`: employment response at year 10 (%);
  - `mig_yr1`: implied year-1 migration per job lost = 1 − (UR workers) − (LFP workers),
    computed with the worker-count conversion in the paper (p. 34): ΔUnemp ≈ −Δle·(E/L)·L,
    ΔLF ≈ Δlp·L, per unit ΔE.
Confidence bands: nonparametric bootstrap resampling **states** (clusters) with replacement,
200 reps per window, 5th–95th percentile bands on each statistic. COVID handling: run each
window that includes 2020–21 twice — baseline, and with year dummies 2020+2021 interacted
out (simply add those two year dummies to every equation); report both in the CSV
(`covid_dummies` column), plot the baseline and show the dummied variant as a light overlay.

**C1 — persistence of growth / permanence of shocks.**
(a) Fig-1 update: for period pairs (1950–70, 1970–90), (1970–90, 1990–2007), (1990–2007,
2007–2025): OLS of mean annual Δln E (payroll, spliced) in the later window on the earlier;
record slope, SE, R². The original point: slope 0.70/R² 0.75.
(b) AR(4) in Δn, pooled FE, on 20-year rolling windows 1952–2025 (step 2 years to keep it
light); record IR at year 4 and year 20 (original: 1.67 / ~1.5) with the same state-cluster
bootstrap.

**C2 — unemployment persistence.** AR(2) in u (level), pooled FE, on 15-year rolling windows
1976–2025 (step 1); record IR at years 5 and 10 (original: 0.29 / ~0) + bootstrap bands.
Also the scatter update: UR 2015 vs 2025 and UR 2013 vs 2023 slopes (original 1975 vs 1985:
0.03). Flag in the note that state means differ (the paper's own caveat: 1970 vs 1990 slope
was 0.41 driven by heterogeneous means, dropping farm states 0.24) — report both raw slope
and slope after demeaning by 1976–2025 state means.

**C4 — income response + convergence stall.**
(a) Bivariate pooled FE VAR, 4 lags, in (Δn, y) with y = relative log PCPI, payroll
employment; 20-year rolling windows 1952–2025 (step 2); record income trough (%, and its
year) after a −1% employment shock (original: −0.9% at year 2).
(b) Convergence: OLS of average annual growth of real-terms-irrelevant nominal PCPI over each
20-year window on log PCPI at window start; record slope (original analogue: −0.01). This
connects to the known post-1990 convergence stall (Ganong–Shoag) — say so in the note.

**C4b (optional stretch, do only if everything above is done):** bivariate FE VAR (2 lags) in
(Δe, relative log {ST}STHPI annual avg), 1976–2025 windows; house-price trough and whether the
effect is transitory (original MSA result: −2% trough, transitory).

## Outputs (write to `outputs/` in the container)

1. `estimates_by_window.csv` — tidy: one row per (claim_id, statistic, window_start,
   window_end, covid_dummies, estimate, lo90, hi90, n_states, n_obs). Include the original
   paper's headline value as rows with `window_start=orig` (estimate = printed number,
   no bands).
2. **Flagship figure** `bk_living_update.png` (+ `.pdf`): a 2×2 panel, x = rolling-window END
   year on every panel:
   - (a) year-1 UR response to a −1% employment shock (C3 `ur_yr1`), with 90% band;
   - (b) UR half-life in years (C3), with band;
   - (c) year-10 employment response (C3 `emp_lr`), with band;
   - (d) implied year-1 out-migration share (C3 `mig_yr1`), with band, and a dashed reference
     line at the paper's household-basis 0.40.
   On each panel: shade the original 1978–90 sample span, mark the original-sample estimate
   with a distinct point/star labeled "BK 1992", draw the paper's printed headline value as a
   dashed horizontal reference where comparable (0.32 pp on (a)). Shade 2020–21 lightly and
   overlay the covid-dummied series as a thin line. Title the figure so a reader instantly
   gets it, e.g. "Do states still recover by out-migration? Blanchard–Katz (1992), re-estimated
   1978–2025".
3. `bk_supporting.png`: panels for C1 (Fig-1 slopes across period pairs + AR(4) long-run IR
   over windows), C2 (year-5 IR over windows), C4 (income trough over windows + convergence
   slope over windows), each with the original estimate marked.
4. `findings.md` — ≤ 1.5 pages: per claim, held up / strengthened / faded / reversed, with
   the numbers. Frame honestly against what the literature already knows: Dao–Furceri–Loungani
   (2017) found with data through ~2013 that migration's share of adjustment fell and
   unemployment/participation absorb more; interstate migration has trended down since the
   1980s; income convergence stalled after ~1990 (Ganong–Shoag). Your value-added: a unified
   re-estimation of the original specs through 2025, including the COVID shock and after.
   State clearly which employment concept each number uses (household vs establishment).
5. `data/panel_annual.csv` — the constructed panel (state, year, all variables), plus
   `data/splice_ratios.csv` for the SIC/NAICS link.

## Failure modes and fallbacks

- `fredgraph.csv` returns HTML or 429 → sleep+retry once, then switch to the FRED API with
  `$FRED_API_KEY` (same series IDs). Batch politely (~1 req/sec is fine; 51×4 series total).
- A `{ST}NA` / `{ST}UR` / `LBSSA{FF}` ID unexpectedly missing → search the FRED API
  (`/fred/series/search?search_text=...`) for the state's series; do not silently drop a state.
- `download.bls.gov` 403 → you forgot the User-Agent header. If it blocks entirely even with
  UA, run C1(a) first pair from the replication's own historical dataset if it ships one;
  otherwise restrict C1 to (1970–90 from replication data if present) and 1990–2025 pairs
  from FRED and say so in findings.md. C2/C3/C4 do not depend on the SIC file.
- Any window where the FE-VAR is near-singular (shouldn't happen with 51×15 obs) → report NA
  for that window rather than crashing the sweep.
- If the original-sample sanity gate cannot be hit after genuine debugging, still run the
  sweep, but lead findings.md with the discrepancy and its suspected cause (data revisions in
  LAUS history are real but small).

## Honest-framing notes (carry these into findings.md)

- The economic question is the same one today — how do US states absorb asymmetric shocks —
  and is again policy-relevant (WFH-driven reallocation, COVID, the long decline in interstate
  migration). No SIC→NAICS issue contaminates the headline C3 result (it is total-economy,
  household-survey based).
- Caveats to state: LAUS model-based estimates are revised and smoother than the paper's
  1980s CPS-based numbers (may mechanically raise measured persistence a bit); household vs
  establishment employment changes the migration split (0.40 vs 0.65 in the paper itself);
  the paper's composition-adjusted CPS wage and pre-1976 unemployment could not be extended
  (IPUMS access pending / source discontinued); mfg production-worker AHE ends as a concept
  in 2002 (SIC) — income per capita is the extendable wage-side measure, and the paper itself
  reported it (Fig 13) as consistent with the wage results.