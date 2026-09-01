"""Step 9: bivariate employment-wage and employment-income systems (Figs 11, 13, 14).

Two-equation VAR in (de, x), 4 lags each, pooled with state FE over 1952-1990, recursive
with employment (de) ordered first (employment innovation = labor-demand shock). IRF to a
-1% employment shock over years 0-20.

  de = Delta(log relative employment); x = relative per-capita income (rel_pcinc_logdev).

Manufacturing production-worker AHE (Fig 11 wage variable) is not reconstructable from any
free modern API (SIC-basis archival; QCEW/ASM/BEA-industry all start >=1990 or need a key),
so the employment-WAGE system is reported using the same reconstructable relative per-capita
income as the employment-INCOME system (Fig 13), and is labeled as such.
"""
import argparse, json, pathlib, sys
import numpy as np, pandas as pd
import statsmodels.api as sm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from states_meta import POSTALS


def estimate_bivar(df, xcol, y0, y1, nlags=4):
    rows = []
    for p in POSTALS:
        sub = df[df.state == p].sort_values("year").copy()
        sub["de"] = sub["rel_emp_logdev"].diff()
        s = sub[["year", "de", xcol, "state"]].dropna().rename(columns={xcol: "x"})
        s = s.set_index("year")
        for yr in s.index:
            if yr < y0 or yr > y1:
                continue
            if not all((yr - k) in s.index for k in range(1, nlags + 1)):
                continue
            cur = [s.loc[yr, "de"], s.loc[yr, "x"]]
            lags = []
            for k in range(1, nlags + 1):
                lags += [s.loc[yr - k, "de"], s.loc[yr - k, "x"]]
            rows.append([p] + cur + lags)
    cols = ["state", "de", "x"] + [f"{v}_l{k}" for k in range(1, nlags + 1) for v in ("de", "x")]
    D = pd.DataFrame(rows, columns=cols)
    for c in cols[1:]:
        D[c] = D[c] - D.groupby("state")[c].transform("mean")
    Xcols = [f"{v}_l{k}" for k in range(1, nlags + 1) for v in ("de", "x")]
    X = D[Xcols].values
    A = np.array([sm.OLS(D[v].values, X).fit().params for v in ("de", "x")])  # 2 x (2*nlags)
    E = np.column_stack([sm.OLS(D[v].values, X).fit().resid for v in ("de", "x")])
    Sigma = np.cov(E, rowvar=False)
    return A, Sigma, len(D)


def irf_bivar(A, Sigma, nlags=4, H=20, shock=-0.01, suppress_feedback=False):
    k = 2
    Amat = A.copy()
    if suppress_feedback:
        # zero coefficients on lagged x in the DE equation (row 0, odd columns = x lags)
        for k_ in range(nlags):
            Amat[0, 2 * k_ + 1] = 0.0
    # companion form (2k*nlags)
    m = k * nlags
    F = np.zeros((m, m))
    for lag in range(nlags):
        F[0:k, lag * k:(lag + 1) * k] = Amat[:, lag * k:(lag + 1) * k]
    if nlags > 1:
        F[k:m, 0:m - k] = np.eye(m - k)
    P = np.linalg.cholesky(Sigma)
    delta = P @ np.array([1.0, 0.0])
    delta *= shock / delta[0]
    R = np.zeros(m); R[0:k] = delta
    resp = [R[0:k].copy()]
    for h in range(1, H + 1):
        R = F @ R
        resp.append(R[0:k].copy())
    resp = np.array(resp)
    de = resp[:, 0]; x = resp[:, 1]
    emp_level = np.cumsum(de)
    return emp_level, x


def main(panel, out, figdir):
    df = pd.read_parquet(panel)
    A, Sigma, n = estimate_bivar(df, "rel_pcinc_logdev", 1952, 1990, nlags=4)

    emp, x = irf_bivar(A, Sigma, H=20, shock=-0.01)
    emp_sup, x_sup = irf_bivar(A, Sigma, H=20, shock=-0.01, suppress_feedback=True)

    def trough(s): return float(s[np.argmin(s)])
    def trough_year(s): return int(np.argmin(s))

    emp_wage = dict(
        irf={str(h): dict(employment=float(emp[h]), wage=float(x[h])) for h in range(21)},
        employment_plateau=float(emp[-1]), wage_trough=trough(x),
        note="pcinc proxy for manufacturing wage (not reconstructable)")
    emp_income = dict(
        irf={str(h): dict(employment=float(emp[h]), pcincome=float(x[h])) for h in range(21)},
        employment_plateau=float(emp[-1]), pcincome_trough_year=trough_year(x),
        pcincome_trough=trough(x))
    suppress = dict(
        employment_plateau_with_feedback=float(emp[-1]),
        employment_plateau_without_feedback=float(emp_sup[-1]),
        note="'without feedback' zeros lagged income/wage coefficients in the employment equation")

    res = dict(n_obs=n, emp_wage=emp_wage, emp_income=emp_income, suppress_feedback=suppress)
    pathlib.Path(out).write_text(json.dumps(res, indent=2))

    # figures
    yrs = list(range(21))
    for fname, title, xlabel, xs in [
        ("fig11_emp_wage.png", "Fig 11 (emp-wage, pcinc proxy)", "rel. wage (pcinc proxy)", x),
        ("fig13_emp_income.png", "Fig 13 (emp-income)", "rel. per-capita income", x)]:
        fg, ax = plt.subplots(figsize=(8, 5))
        ax.plot(yrs, emp * 100, "-o", label="employment (level)", ms=3)
        ax.plot(yrs, xs * 100, "-s", label=xlabel, ms=3)
        ax.axhline(0, color="k", lw=0.5); ax.legend()
        ax.set_xlabel("years after shock"); ax.set_ylabel("response (%)"); ax.set_title(title)
        fg.savefig(pathlib.Path(figdir) / fname, dpi=120, bbox_inches="tight"); plt.close(fg)

    fg, ax = plt.subplots(figsize=(8, 5))
    ax.plot(yrs, emp * 100, "-o", label="with wage/income feedback", ms=3)
    ax.plot(yrs, emp_sup * 100, "-s", label="feedback suppressed", ms=3)
    ax.axhline(0, color="k", lw=0.5); ax.legend()
    ax.set_xlabel("years after shock"); ax.set_ylabel("employment response (%)")
    ax.set_title("Fig 14: employment response with vs without wage/income feedback")
    fg.savefig(pathlib.Path(figdir) / "fig14_suppress_feedback.png", dpi=120, bbox_inches="tight")
    plt.close(fg)

    print("emp-income IRF emp (%):", [round(v * 100, 2) for v in emp])
    print("income IRF (%):", [round(v * 100, 2) for v in x])
    print("emp plateau=%.4f | income trough=%.4f @year %d" % (emp[-1], trough(x), trough_year(x)))
    print("suppress feedback: plateau with=%.4f without=%.4f" % (emp[-1], emp_sup[-1]))
    print("wrote", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", default="data/panel.parquet")
    ap.add_argument("--out", default="results/bivariate_irfs.json")
    ap.add_argument("--fig", default="figures/")
    a = ap.parse_args()
    main(a.panel, a.out, a.fig)
