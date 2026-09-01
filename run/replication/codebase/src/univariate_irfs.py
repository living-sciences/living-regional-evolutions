"""Step 6: pooled univariate models & implied impulse responses (Table 1) + per-state
long-run employment responses.

- employment: AR(4) in Delta n (relative employment change), state FE, 1952-1990.
    Level response to a unit innovation = cumulative sum of the MA coefficients of Delta n;
    plateau = 1/(1 - sum phi).
- unemployment: AR(2) in the level of relative unemployment, state FE. Paper used 1972-90;
    LAUS only reconstructs 1976-1990, so that shortened window is used (documented).
- wage: AR(4) in the level of relative wage, state FE, 1952-1990. Manufacturing AHE not
    reconstructable -> relative per-capita income used as proxy.
"""
import argparse, json, pathlib, sys
import numpy as np, pandas as pd
import statsmodels.api as sm

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from states_meta import POSTALS


def pooled_ar(df, col, nlags, y0, y1, diff=False):
    """Pooled AR(nlags) with state fixed effects (within transform). Returns phi coefs+se."""
    rows = []
    for p in POSTALS:
        sub = df[df.state == p][["year", col]].dropna().sort_values("year")
        s = pd.Series(sub[col].values, index=sub["year"].astype(int).values)
        if diff:
            s = s.diff()
        s = s.dropna()
        for yr in s.index:
            if yr < y0 or yr > y1:
                continue
            lags = [s.get(yr - j, np.nan) for j in range(1, nlags + 1)]
            if any(pd.isna(lags)):
                continue
            rows.append((p, s[yr], *lags))
    cols = ["state", "y"] + [f"l{j}" for j in range(1, nlags + 1)]
    d = pd.DataFrame(rows, columns=cols)
    # within transform (state FE)
    for c in ["y"] + [f"l{j}" for j in range(1, nlags + 1)]:
        d[c] = d[c] - d.groupby("state")[c].transform("mean")
    X = d[[f"l{j}" for j in range(1, nlags + 1)]].values
    r = sm.OLS(d["y"].values, X).fit()
    phi = r.params.tolist(); se = r.bse.tolist()
    return phi, se, int(len(d))


def ma_coefs(phi, H):
    """MA(inf) coefficients psi_0..psi_H of AR(p): x_t = sum phi_j x_{t-j} + e_t."""
    p = len(phi)
    psi = [0.0] * (H + 1)
    psi[0] = 1.0
    for h in range(1, H + 1):
        psi[h] = sum(phi[j] * psi[h - j - 1] for j in range(p) if h - j - 1 >= 0)
    return psi


def main(panel, out, notes):
    df = pd.read_parquet(panel)
    H = 25

    # employment: AR(4) in Delta n
    phi_e, se_e, n_e = pooled_ar(df, "rel_emp_logdev", 4, 1952, 1990, diff=True)
    psi_de = ma_coefs(phi_e, H)              # MA of Delta n
    lvl_e = np.cumsum(psi_de)                # level response = cumulative sum
    plateau_e = 1.0 / (1.0 - sum(phi_e))
    emp_irf = {f"year{h}": float(lvl_e[h]) for h in [1, 2, 3, 4, 5, 10, 20]}
    emp_irf["plateau"] = float(plateau_e)

    # unemployment: AR(2) in level, 1976-1990 (shortened)
    phi_u, se_u, n_u = pooled_ar(df, "rel_urate", 2, 1978, 1990, diff=False)
    psi_u = ma_coefs(phi_u, 12)
    unemp_irf = {f"year{h}": float(psi_u[h]) for h in range(1, 11)}

    # wage (pcinc proxy): AR(4) in level
    phi_w, se_w, n_w = pooled_ar(df, "rel_pcinc_logdev", 4, 1952, 1990, diff=False)
    psi_w = ma_coefs(phi_w, H)
    wage_irf = {f"year{h}": float(psi_w[h]) for h in [1, 2, 3, 4, 5, 10, 20]}

    # (iii) per-state long-run employment response (state-by-state AR(4) in Delta n)
    indiv = []
    for p in POSTALS:
        sub = df[df.state == p][["year", "rel_emp_logdev"]].dropna().sort_values("year")
        s = pd.Series(sub["rel_emp_logdev"].values, index=sub["year"].astype(int).values).diff().dropna()
        rows = []
        for yr in s.index:
            if yr < 1952 or yr > 1990:
                continue
            lags = [s.get(yr - j, np.nan) for j in range(1, 5)]
            if any(pd.isna(lags)):
                continue
            rows.append((s[yr], *lags))
        if len(rows) < 10:
            continue
        arr = np.array(rows, float)
        r = sm.OLS(arr[:, 0], arr[:, 1:]).fit()
        sp = float(sum(r.params))
        lr = 1.0 / (1.0 - sp) if sp < 1 else np.nan
        indiv.append(dict(state=p, sum_phi=sp, long_run_emp_response=lr))
    vals = [x["long_run_emp_response"] for x in indiv if np.isfinite(x["long_run_emp_response"])]
    med = float(np.median(vals)); q1, q3 = np.percentile(vals, [25, 75])
    for x in indiv:
        lr = x["long_run_emp_response"]
        x["flag"] = ("high" if np.isfinite(lr) and lr > q3 + 1.5 * (q3 - q1)
                     else "low" if np.isfinite(lr) and lr < q1 - 1.5 * (q3 - q1)
                     else "")

    res = dict(
        coefficients=dict(
            employment_change=dict(phi=phi_e, se=se_e, n=n_e, sum_phi=float(sum(phi_e))),
            unemployment=dict(phi=phi_u, se=se_u, n=n_u),
            wage=dict(phi=phi_w, se=se_w, n=n_w, note="pcinc proxy"),
        ),
        impulse_responses=dict(employment=emp_irf, unemployment=unemp_irf, wage=wage_irf),
        individual_long_run=indiv,
        individual_median=med,
    )
    pathlib.Path(out).write_text(json.dumps(res, indent=2))
    pathlib.Path(notes).write_text(
        "# Univariate model notes\n\n"
        "- Employment: AR(4) in Delta(relative employment), state FE, 1952-1990. "
        f"sum phi = {sum(phi_e):.3f}; implied level plateau = {plateau_e:.3f}.\n"
        "- Unemployment: AR(2) in level of relative unemployment, state FE. The paper used "
        "1972-1990; LAUS only reconstructs state unemployment from 1976, so the estimation "
        "window is **1978-1990** (2 lags off a 1976 start). This shortened window is a "
        "documented consequence of the pre-1976 data gap.\n"
        "- Wage: AR(4) in level of relative wage, state FE, 1952-1990. Manufacturing "
        "production-worker AHE is not reconstructable; **relative per-capita income is used "
        "as the proxy** for the wage process.\n"
    )
    print("emp AR4 phi:", [round(x, 3) for x in phi_e], "sum=", round(sum(phi_e), 3),
          "plateau=", round(plateau_e, 3))
    print("emp level IRF:", {k: round(v, 3) for k, v in emp_irf.items()})
    print("unemp AR2 phi:", [round(x, 3) for x in phi_u],
          "IRF y1,y5,y10:", round(psi_u[1], 3), round(psi_u[5], 3), round(psi_u[10], 3))
    print("wage(pcinc) plateau proxy IRF y1,y5,y20:",
          round(psi_w[1], 3), round(psi_w[5], 3), round(psi_w[20], 3))
    print("per-state long-run emp response median:", round(med, 3),
          "range:", round(min(vals), 2), "-", round(max(vals), 2))
    print("wrote", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", default="data/panel.parquet")
    ap.add_argument("--out", default="results/table1_irfs.json")
    ap.add_argument("--notes", default="notes/univariate_notes.md")
    a = ap.parse_args()
    main(a.panel, a.out, a.notes)
