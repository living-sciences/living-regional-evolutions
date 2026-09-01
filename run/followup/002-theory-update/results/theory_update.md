# Regional Evolutions, the theory updated to 2026

*A recalibration of Blanchard & Katz's (1992) migration-adjustment model on state
data through 2025, with the minimal amendment the new evidence demands.*

Every quantitative claim below is labelled **[ESTIMATED]** (computed from data),
**[CALIBRATED]** (a parameter set to match a moment), or **[PROPOSED]** (a
theoretical suggestion consistent with the evidence but not itself tested).
Paper-era comparison numbers are read from the replication artifacts on disk and
from follow-up 001's `estimates_by_window.csv`; sources are cited inline.

---

## 1. The original model, in brief

Blanchard & Katz close their paper with a small structural model of how a US state
absorbs an asymmetric shock (their "Allowing for Unemployment" block, paper eq. 7,
p. 20–21). In deviations from US aggregates it is four equations in the relative wage
`w`, relative unemployment `u`, relative labor demand position `z`, and the (log)
relative labor force `n*`:

```
(labor demand)     w_it   = −d (n*_it − u_it) + z_it
(wage curve)       u_it   = −c · w_it
(migration)        n*_{i,t+1} − n*_it = x_si + b·w_it − g·u_it + ε^s_{i,t+1}
(firm mobility)    z_{i,t+1} − z_it   = x_di − a·w_it + ε^d_{i,t+1}
```

The **migration equation is the heart of the model**: workers leave a state when its
relative wage is low (`b`) and, once unemployment is admitted, when its relative
unemployment is high (`g`). Firms trickle in when wages are low (`a`). After an
adverse demand shock, the wage falls, unemployment rises, workers leave and firms
slowly arrive, until the wage is back to normal and **employment is permanently
lower** — quantities, not prices, do the long-run adjusting. The paper's headline
facts follow: relative employment shocks are permanent; relative unemployment and
participation are transitory, dying out in **5–7 years** (the central policy object:
*how long a local slump lasts*); and out-migration does most of the year-1 work
(share ≈ **0.40** on a household basis, **0.65** on an establishment basis; paper
fn. 37 and Fig. 7).

The closed form (paper p. 18) makes the role of migration explicit. To a −1 labor-
demand innovation, the wage gap decays geometrically at rate `λ = a + d·b`, and the
long-run employment loss is `−b/(a + d·b)`. **A weaker migration response `b` means
a slower `λ` — a longer-lasting slump — and a smaller permanent employment loss.**
That comparative static is exactly what we take to the 2026 data.

---

## 2. What the new evidence demands

Follow-up 001 re-estimated the four headline claims through 2025. The structural
facts survived (employment shocks permanent, unemployment transitory), but **one
channel moved**: the out-migration share of year-1 adjustment fell from **0.383
(1978–90) to 0.276 (2011–25)** on the household basis, and from **0.77 (1990–2004)
to 0.63 (2011–25)** on the payroll basis (001 `estimates_by_window.csv`, C3 /
C3_payroll `mig_yr1`). 001 attributed this to the secular decline in US interstate
migration (Dao–Furceri–Loungani 2017; Ganong–Shoag 2017) but did not re-estimate the
structural migration parameter itself. This study does.

**New structural estimate [ESTIMATED].** We estimate the migration equation directly
— relative labor-force (and population) growth on lagged relative unemployment, state
fixed effects, state-clustered SEs — exactly BK's pooled-FE estimator, on 001's
extended panel:

| migration responsiveness `m = −∂(Δn)/∂u` | paper-era 1976–90 | recent 2010–25 | decline |
|---|---|---|---|
| labor force (Δn\*) | 0.00474 (se 0.00072) | 0.00225 (se 0.00049) | **−53%** |
| population (Δpop)  | 0.00339 (se 0.00057) | 0.00118 (se 0.00031) | **−65%** |

Both are ~7σ from zero in the paper era and roughly **halve** by 2026 (`m_LF`) — a
second, independent identification of the same weakening 001 saw in the VAR share.
Controlling for the relative wage (income) barely changes the unemployment
coefficient and the wage coefficient is small and mostly insignificant, so the
weakening is in the response to **job availability / unemployment** (`g`), not the
wage channel — consistent with the migration literature BK cite.

The migration channel of BK's model is therefore materially weaker in 2026 than in
1992. **The theory needs to accommodate a lower migration elasticity while still
reproducing the paper-era facts.**

---

## 3. The updated model: one time-varying parameter

**The amendment.** Make the migration responsiveness a **declining, time-varying
parameter** `m_t` (equivalently `g_t`), and leave the rest of BK's structure intact:

```
(migration, amended)   n*_{i,t+1} − n*_it = x_si + b·w_it − g_t·u_it + ε^s ,   g_t ↓ over time
```

Economically, `g_t` is the inverse of a **real cost of moving**. The well-documented
rise in the price of housing in high-productivity destination states (Ganong–Shoag
2017; Hsieh–Moretti 2019) raises the wage differential a mover must clear to make a
move pay, muting the migration response to any given local unemployment gap. A rising
moving cost `κ_t` maps one-for-one to a falling `g_t = g_0 /(1+κ_t)`. So the single
declining parameter *is* the housing/cost-of-moving margin the update calls for — in
its most parsimonious, directly-estimable form.

**Alternative considered and rejected.** We considered adding an explicit
house-price/moving-cost margin as a separate equation — migration responding to
`u` only after paying a state-specific moving cost tied to relative house prices.
We rejected it for three reasons: (i) it requires a state house-price panel that
001 did not build and that is out of this follow-up's reuse scope; (ii) it adds at
least two new parameters (a cost level and its trend) that are **not separately
identified** from the same two moments (the migration share and the unemployment
half-life) we have — it is observationally equivalent to a lower `g_t`; and (iii)
parsimony: one time-varying parameter reproduces both eras, so a richer margin is
unwarranted by the evidence. The declining-`g_t` form keeps the added structure to
the single degree of freedom the data actually pin down, while naming the mechanism
(housing) behind it.

**Calibration.** We discretise BK's adjustment block to the two margins the data
identify — out-migration and job recovery closing the unemployment gap `u = n* − J`:

```
n*_{t+1} = n*_t − m·u_t ;   J_{t+1} = J_t + a·u_t ;   u_t = (1−S)^t,  S ≡ m+a
```

so the year-1 migration share is `σ_m = m/S` and the unemployment-gap half-life is
`H = ln0.5 / ln(1−S)`. Given the two estimated moments `(σ_m, H)` per era, the
parameters are exactly identified: `S = 1 − 0.5^{1/H}`, `m = σ_m·S`, `a = (1−σ_m)·S`.

### Calibration table (paper-era vs 2026, household basis)

| parameter | symbol | paper-era 1978–90 | 2026 (2011–25) | label |
|---|---|---|---|---|
| year-1 migration share | σ_m | 0.383 | 0.276 | [ESTIMATED] |
| UR-gap half-life (yr) | H | 3.0 | 3.0 | [ESTIMATED] |
| migration clearing rate | m | 0.079 | 0.057 | [CALIBRATED] |
| job-recovery clearing rate | a | 0.127 | 0.149 | [CALIBRATED] |
| long-run rel-employment loss | −m/S | −0.383 | −0.276 | [CALIBRATED] |

(Full table incl. payroll basis and the direct FE elasticities: `calibration_table.csv`.)

The recalibration tells a sharper story than "migration got weaker." Holding the
observed UR half-life fixed, **the migration clearing rate `m` fell 28% (0.079→0.057)
while the job-recovery rate `a` rose 17% (0.127→0.149)**. The composition of
adjustment rotated from *permanent out-migration* toward *transitory job recovery /
unemployment cycling*. This is why the paper's headline permanence weakened in
001's recent windows (year-10 employment response toward 0, the V-shaped COVID
recovery): with `m` down and `a` up, the model's long-run employment loss shrinks
(from −0.38 toward −0.21 in the COVID window), exactly as `−m/S` predicts.

---

## 4. Validation

**(a) The one-off unemployment half-life did *not* lengthen — and the model says why.**
Because the fall in `m` is offset by a rise in `a`, the clearing rate `S = m+a` is
essentially unchanged (0.206 in both household eras), so the calibrated model
reproduces the empirically stable ~3-year UR half-life across 001's rolling windows
(Figure, panel D: `ur_halflife` sits at 3–4 in every window). An honest reading of
BK's central policy object is therefore: *for a one-off shock, local slumps are no
longer than in 1992 — but they are cleared differently, with less of the burden
carried by people leaving and more by jobs cycling back.*

**(b) Where weaker migration bites: severe, persistent shocks.** The exception is the
Great-Recession-centred window (1995–2009), where the migration share dipped to 0.32
**and** the UR half-life rose to **5 years** with cumulative 10-year excess
unemployment of **1.56** vs **0.33** in the paper-era window (001 C3 `ur_cum10`).
Calibrated to that window the model gives `S = 0.13`, `H = 5.0 yr`, and a
time-to-80%-recovery of **11.6 years** — a materially longer slump. When a large
shock is persistent rather than one-off, weak migration can no longer clear the pool
of displaced workers quickly, and the slump deepens and lengthens. The model
reproduces the ordering of the empirical `ur_cum10` (paper-era 3.5 model / 0.33 data;
GFC 5.0 model / 1.56 data) — the deepest, longest troughs are the GFC windows, on
both the model and the data.

**(c) Counterfactual — the price of immobility.** Holding 2026 job dynamics fixed
(`a = 0.149`) but restoring the paper-era migration rate (`m = 0.079`), the one-off
slump half-life falls from **3.0 to 2.7 years** and cumulative 10-year excess
unemployment falls **10%** (3.47 → 3.13). So even where the raw half-life looks
unchanged, ~0.3 years of every local slump — and a tenth of its cumulative pain — is
attributable to the erosion of labor mobility since 1990. [CALIBRATED]

**(d) Held-out check.** We estimated the migration elasticity on **pre-2015** data
(`m = 0.00370`) and tested it on the **held-out 2015–2024** window (`m = 0.00076`).
The pre-2015 elasticity over-predicts out-migration out of sample (held-out RMSE
0.00983 using the pre-2015 `m` vs 0.00966 using the true held-out `m`), and the
held-out elasticity is **5× smaller** than the pre-2015 one. Migration
responsiveness kept falling out of sample — the decline is not an artifact of the
estimation window. [ESTIMATED]

**(e) The episode the original cannot explain — COVID 2020.** BK's original
calibration (high `m`, permanent employment loss −0.38 to −1.3) predicts that a
sharp 2020 employment shock leaves a persistent relative-employment scar. The data
show the opposite: a **V-shaped** recovery with the year-10 employment response near
zero (001 C3, 2006–2020 window `emp_lr = −0.22`). The updated model with a collapsed
migration rate (`m = 0.043`) and an elevated transitory job-recovery rate
(`a = 0.163`, `σ_m = 0.21`) reproduces a small, non-permanent employment response
(model long-run loss −0.21) — the original model, with migration doing 40% of the
work, cannot. [CALIBRATED]

---

## 5. What the update implies going forward

1. **The mechanism is intact; its mix has rotated.** US states still absorb
   asymmetric shocks the BK way — quantities adjust, prices barely — but the
   quantity that adjusts is **less "people leaving" and more "jobs cycling back."**
   The single amendment that reconciles 1992 and 2026 is a **declining migration
   responsiveness `g_t`**, the reduced-form shadow of rising real moving costs. [PROPOSED]

2. **One-off local slumps are no longer, but more of their burden is local.** With
   out-migration muted, a larger share of an adverse shock is now borne *inside* the
   state as unemployment and non-participation rather than exported via out-migration.
   The policy-relevant duration (UR half-life) is stable at ~3 years for ordinary
   shocks. [ESTIMATED/CALIBRATED]

3. **Severe, persistent shocks are the danger zone.** When shocks are large and
   drawn-out (GFC), weak mobility lets the displaced-worker pool linger: half-life
   ~5 years, 80%-recovery ~12 years, cumulative excess unemployment ~5× the paper-era
   one-off. Place-based policy (relocation assistance, housing supply in booming
   destinations, local demand support) has a larger marginal return in 2026 than in
   1992, precisely because the automatic migration stabilizer is weaker. [CALIBRATED/PROPOSED]

4. **A living-paper parameter to watch.** `m_t` (and its housing driver) is now a
   first-class structural parameter of regional adjustment, not a fixed constant.
   The 2026 vintage: `m_LF ≈ 0.0022`, `σ_m ≈ 0.28` (household) / `0.63` (payroll),
   down ~50% and ~18% respectively from the paper era.

---

### Notes on data, scope, and honesty of labels
- Migration/labor-force and unemployment series are LAUS-based (state coverage from
  1976); the wage side uses relative per-capita income as BK's Fig-13 wage proxy
  (composition-adjusted CPS wages and SIC manufacturing AHE remain unreconstructable,
  as in the replication and 001). The direct migration elasticity is a genuine
  structural [ESTIMATED] quantity; the two-margin `(m, a)` split is [CALIBRATED] to
  the VAR share and the UR half-life and is a *stylized single-mode* reduction of
  BK's richer dynamics — it is a calibration device for the slump-duration
  counterfactual, not a new estimated IRF.
- No new data were downloaded; all inputs are reused from 001's
  `results/data/panel_annual.csv` and `estimates_by_window.csv` and the replication
  codebase's IRF engines. Compute was estimation + calibration only, per the brief.
