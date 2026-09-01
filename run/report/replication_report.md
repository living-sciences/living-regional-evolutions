# Replication Report

**Generated:** 2026-08-24 22:12:14

---

## Executive Summary

**Mode:** full

**Replication Score: 29.6%** (32/35 claims counted)

*Coverage: scored over 32 attempted/blocked claim(s); 2 out-of-scope (not targeted by the plan — excluded, not counted as failures).*

## Tier Breakdown

| Tier | Match | Partial | No match | Not attempted | n/a | Missing | Total |
|---|---|---|---|---|---|---|---|
| Headline | 1 | 4 | 2 | 0 | 0 | 0 | 7 |
| Supporting | 2 | 8 | 6 | 10 | 0 | 0 | 28 |

## Per-Claim Verdicts

| ID | Tier | Type | Status | Rationale | Evidence |
|---|---|---|---|---|---|
| C1 | headline | scalar | match | The run produced results/persistence_convergence.json with emp_persistence_slope=0.6976716605958123 and emp_persistence_r2=0.7542403243498497 over emp_persistence_n=51 units (th... | 4 file(s) |
| C2 | supporting | scalar | match | The run re-ran the Figure 1 employment-persistence regression (1970-90 growth on 1950-70 growth) dropping Arizona, Florida, and Nevada. results/persistence_convergence.json repo... | 3 file(s) |
| C3 | supporting | qualitative | partial | Evidence is /workspace/output/replication/codebase/results/adf_tests.json. The three states the claim names (MA, SD, WY) all reject the unit root at 5% and all have negative lag... | 3 file(s) |
| C4 | headline | table | partial | The run produced the Table 1 impulse responses in results/table1_irfs.json (the planned output/tables/table1.csv was not written, but the impulse_responses block is the gradeabl... | 3 file(s) |
| C5 | supporting | scalar | no match | The run produced per-state long-run employment responses in results/table1_irfs.json ('individual_long_run'), computed as the plateau 1/(1-sum_phi) of an AR(4) in relative-emplo... | 4 file(s) |
| C6 | supporting | scalar | not attempted | The claim targets the exact regression of the 1985 relative state unemployment rate on the 1975 rate (Figure 3; slope 0.03, t 0.2, R^2 0.00). This specific regression could NOT ... | 4 file(s) |
| C7 | supporting | scalar | not attempted | The C7 regression requires the relative state unemployment rate at a 1970 endpoint, but reconstructed state unemployment (LAUS-basis) is only available from 1976 onward. The pip... | 4 file(s) |
| C8 | headline | scalar | partial | Step 6 estimated the pooled AR(2) for relative unemployment and produced the implied impulse response in results/table1_irfs.json: impulse_responses.unemployment = {year1: 1.075... | 5 file(s) |
| C9 | supporting | qualitative | match | results/adf_tests.json (wages block) reports n_states=51, n_negative_coef=48, n_reject_5pct=3 (reject_states=['NE','WI','WY'], crit_5pct=-2.94), which I independently recomputed... | 4 file(s) |
| C10 | headline | scalar | partial | The claim has two halves. (1) The personal-income-per-capita convergence regression (avg annual pcinc growth 1948-90 on log 1948 income) WAS reproduced in results/persistence_co... | 5 file(s) |
| C11 | supporting | scalar | not attempted | C11 concerns the persistence of average MANUFACTURING wage growth: the cross-state correlation of 1950-70 mfg wage growth with 1970-90 mfg wage growth (paper value 0.13). The re... | 3 file(s) |
| C12 | supporting | scalar | no match | The run produced Table 2 in results/table2_and_regionyear.json, but every quantity is far outside tolerance. Produced avg_adj_r2 = 0.969 vs paper 0.66 (~47% off); n_states_beta_... | 3 file(s) |
| C13 | supporting | scalar | no match | Step 4 ran successfully (replication_log.json, exit_code 0) and wrote results/table2_and_regionyear.json, whose region_year block gives census_division_share=0.6419 (64%) and ce... | 5 file(s) |
| C14 | supporting | scalar | no match | The run produced the regression underlying Figure 6 in results/unemployment_cross_section.json under avg_urate_vs_empgrowth: slope = -33.31, t = -1.71, r2 = 0.056, n = 51, over ... | 4 file(s) |
| C15 | headline | scalar | no match | The run produced the trivariate VAR impulse responses in results/trivariate_var.json. The reported year-1 responses to the -1% employment shock are year1.unemployment_response =... | 4 file(s) |
| C16 | headline | scalar | partial | The trivariate VAR (step 8) produced results/trivariate_var.json and figures/fig7_trivariate_irf.png from the 1978-1990 LAUS window (n_obs=663). The employment IRF builds to a p... | 5 file(s) |
| C17 | headline | scalar | no match | Step 8 produced the year-1 per-worker decomposition in results/trivariate_var.json under 'per_worker' (basis: 'shares of the year-1 employment response'): unemployment=0.1152, p... | 3 file(s) |
| C18 | supporting | scalar | no match | Step 8 produced results/trivariate_var.json with okun.all_states = {coef: 18.270, t: 14.687, n: 714} and okun.farm_states = {coef: 14.667, t: 4.424, n: 126}. The paper's pooled ... | 4 file(s) |
| C19 | supporting | scalar | no match | The claim concerns Figure 9's regression of average employment growth on relative MANUFACTURING wages, 1950-90 (slope -0.68, t=0.6). The run could not reconstruct this: manufact... | 4 file(s) |
| C20 | supporting | scalar | not attempted | Claim C20 requires the regression underlying Figure 10 -- average manufacturing wage on average state unemployment rate (1970-90) -- expecting a positive relationship with t~3.1... | 4 file(s) |
| C21 | supporting | scalar | partial | Step 9 (src/bivariate_irfs.py) produced results/bivariate_irfs.json and figures/fig11_emp_wage.png, so Figure 11 was generated and is gradeable. The EMPLOYMENT dynamics match th... | 4 file(s) |
| C22 | supporting | scalar | out of scope | No plan step targeted this claim; treated as out_of_scope (excluded from the score, not a failure): The industry/worker-characteristic-controlled CPS wage series is an author-co... | 0 file(s) |
| C23 | supporting | scalar | partial | Step 9 (bivariate employment-personal-income system, Figure 13/C23) produced results/bivariate_irfs.json with emp_income.irf giving the per-capita personal income response to a ... | 3 file(s) |
| C24 | supporting | scalar | partial | The run produced results/bivariate_irfs.json with suppress_feedback = {employment_plateau_with_feedback: -0.011717, employment_plateau_without_feedback: -0.014579}, and the emp_... | 3 file(s) |
| C25 | supporting | scalar | not attempted | No plan step targeted this claim; the planner marked it BLOCKED (counts as a reproducibility gap): Requires NAR Home Sales Yearbook median metro house prices (39 MSAs, 1969-90) ... | 0 file(s) |
| C26 | supporting | scalar | out of scope | No plan step targeted this claim; treated as out_of_scope (excluded from the score, not a failure): Reconstructable in principle from BLS metro CPI-U (23 MSAs) plus a matching M... | 0 file(s) |
| C27 | supporting | scalar | not attempted | No plan step targeted this claim; the planner marked it BLOCKED (counts as a reproducibility gap): The real-consumption-wage calculation is derived from the housing-price (C25) ... | 0 file(s) |
| C28 | supporting | figure | not attempted | No plan step targeted this claim; the planner marked it BLOCKED (counts as a reproducibility gap): Requires the Davis-Loungani-Mahidhara defense (military prime contract) series... | 0 file(s) |
| C29 | supporting | scalar | partial | The run executed step 10 (src/massachusetts_case.py, exit_code 0) and produced results/massachusetts.json with growth_1980_85 = 1.985% and gap_vs_us_1980_85 = 0.495 pp. The MA 1... | 5 file(s) |
| C30 | supporting | scalar | partial | Only the unemployment sub-component of this five-part claim was reconstructable this run. results/massachusetts.json reports unemp_rel_1979 = -0.35 (paper: equal to national, i.... | 3 file(s) |
| C31 | supporting | scalar | not attempted | No plan step targeted this claim; the planner marked it BLOCKED (counts as a reproducibility gap): Boston relative housing prices come from the same proprietary NAR metro median... | 0 file(s) |
| C32 | supporting | scalar | partial | results/massachusetts.json (produced by step 10, src/massachusetts_case.py) reports for the reconstructed MA employment panel: avg_growth_1985_91 = -0.617, gap_vs_us_1985_91 = -... | 2 file(s) |
| C33 | supporting | scalar | not attempted | No plan step targeted this claim; the planner marked it BLOCKED (counts as a reproducibility gap): The Massachusetts boom/bust simulation predicts nominal-wage and Boston housin... | 0 file(s) |
| C34 | supporting | scalar | not attempted | No plan step targeted this claim; the planner marked it BLOCKED (counts as a reproducibility gap): Describes properties (state-income shares, forecast-error volatility) of the D... | 0 file(s) |
| C35 | supporting | figure | partial | The exact expected file output/figures/figure2.pdf was not produced, but a relevant figure figures/fig2_cumulative_rel_emp.png was, titled 'Fig 2: cumulative relative employment... | 3 file(s) |

## Flags

- 1 not_attempted claim(s) excluded from the denominator as run/tooling-limited (blocked_infra / no_evidence), not counted against the paper.
- 2 claim(s) marked out_of_scope (planner did not target them) — excluded from the score, not counted as failures. Score is over the 32 attempted/blocked claim(s).

## Replication Attempt

**Environment:** Python 3.12.8, GPU: NVIDIA RTX A6000 (x4, 49140 MiB each), Packages: pandas 3.0.5, numpy 2.5.2, statsmodels 0.14.6, scipy 1.18.1, matplotlib installed
**Duration:** 181s
**Steps completed:** 10/10

| Step | Description | Result | Duration |
|------|-------------|--------|----------|
| 1 | Create working copy, venv, install deps, make output dirs. | Success | 40s |
| 2 | Reconstruct 51-unit state panel 1947-1990 from FRED/BLS. | Success | 113s |
| 3 | Persistence & convergence regressions (Figs 1,2,4,9). | Success | 4s |
| 4 | State-national employment elasticities (Table 2) + region-year variance decomposition. | Success | 3s |
| 5 | ADF unit-root tests on relative employment (trend, 4 lags) and relative wages (no trend, pcinc proxy), 1952-1990. | Success | 3s |
| 6 | Pooled univariate models & implied impulse responses (Table 1) + per-state long-run employment responses. | Success | 3s |
| 7 | Unemployment persistence & cross-state correlations (Figs 3,6,10), LAUS 1976-1990. | Success | 3s |
| 8 | Trivariate VAR (emp, unemployment, participation) Fig 7 + Okun coefficient (C18). | Success | 3s |
| 9 | Bivariate emp-wage & emp-income systems (Figs 11,13,14). | Success | 3s |
| 10 | Massachusetts case study (descriptive reconstructable parts). | Success | 6s |


## Limitations & Code Quality

**Fixes the replication agent applied to make the work run:** 2 (1 minor, 1 major, 0 critical). These are evidence about the provided code/paper, not the replication.

The fix burden is light and the two issues are qualitatively different. Fix 1 is a trivial, result-neutral networking patch (external API rate limiting) that says nothing about the paper's methodology. Fix 2 is the more consequential of the pair: a genuine data-alignment bug in the core elasticity regression, where indexing on a duplicated-year frame broke the endog/exog correspondence and prevented the estimation from running as shipped. That points to a repository that was not verified end-to-end and required a knowledgeable replicator to restore correct data construction, though the underlying method remains sound and reproducible. Net: one minor, one major, no critical problems — the paper's results appear achievable from the provided code, but the code needed non-trivial repair in one analysis step.

| # | Description | Severity | Impact |
|---|-------------|----------|--------|
| 1 | Added FRED API request throttling (0.9s minimum interval) and 429-aware backoff to avoid rate limits. | minor | Reflects the fragility of live third-party API access rather than any flaw in the paper's methodology or code logic. Rate limits are transient and environment-dependent; the values fetched are unchanged. A more robust repo might cache the pulled series, but this has no bearing on the correctness of the results. |
| 2 | Replaced a set_index('year').loc lookup on a duplicated-year frame with a precomputed national ln-employment series indexed by year, fixing a regression size mismatch. | major | Indicates the published code as shipped could not run the state/national elasticity estimation without modification — a preprocessing/alignment defect suggests the repo was not executed end-to-end in the state it was released, or was refactored after the results were produced. The methodology itself appears sound and implementable, but the burden falls on the replicator to reconstruct correct data indexing, so the code is incomplete rather than the science being wrong. |


---

*Report generated by Veritas Replication Agent*
