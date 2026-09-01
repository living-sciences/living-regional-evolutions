"""Step 8: trivariate VAR of employment, unemployment (via le) and participation (lp),
Figure 7, plus the Okun coefficient (C18).

System variables (relative to U.S.), 2 lags, recursive ordering [de, le, lp] so a shock
to employment (de) is contemporaneously the labor-demand shock:
  de = Delta(log relative employment)
  le = log(employment / labor force) relative to U.S.  (higher le = lower unemployment)
  lp = log(labor force / working-age pop) relative to U.S.  (participation)
Pooled across 51 states with state FE over 1978-1990 (LAUS window).
"""
import argparse, json, pathlib, sys
import numpy as np, pandas as pd
import statsmodels.api as sm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from states_meta import POSTALS, FARM_STATES


def build_var_data(df, y0, y1, states=None):
    states = states or POSTALS
    recs = []
    for p in states:
        sub = df[df.state == p].sort_values("year").copy()
        sub["de"] = sub["rel_emp_logdev"].diff()
        s = sub[["year", "de", "le", "lp", "state"]].dropna()
        recs.append(s)
    d = pd.concat(recs, ignore_index=True)
    d = d[(d.year >= y0 - 2) & (d.year <= y1)]
    return d


def estimate_var(d, y0, y1, nlags=2):
    varn = ["de", "le", "lp"]
    # build lagged panel
    rows = []
    for p, g in d.groupby("state"):
        g = g.sort_values("year").set_index("year")
        for yr in g.index:
            if yr < y0 or yr > y1:
                continue
            if not all((yr - k) in g.index for k in range(1, nlags + 1)):
                continue
            cur = [g.loc[yr, v] for v in varn]
            lags = []
            for k in range(1, nlags + 1):
                lags += [g.loc[yr - k, v] for v in varn]
            rows.append([p] + cur + lags)
    cols = ["state"] + varn + [f"{v}_l{k}" for k in range(1, nlags + 1) for v in varn]
    D = pd.DataFrame(rows, columns=cols)
    # within transform (state FE) on all numeric cols
    for c in cols[1:]:
        D[c] = D[c] - D.groupby("state")[c].transform("mean")
    Xcols = [f"{v}_l{k}" for k in range(1, nlags + 1) for v in varn]
    X = D[Xcols].values
    A = []  # coefficient rows per equation
    resid = []
    for v in varn:
        r = sm.OLS(D[v].values, X).fit()
        A.append(r.params)
        resid.append(r.resid)
    A = np.array(A)                      # 3 x (3*nlags)
    E = np.array(resid).T                # n x 3
    Sigma = np.cov(E, rowvar=False)
    return A, Sigma, len(D)


def irf(A, Sigma, nlags=2, H=12, shock_emp=-0.01):
    k = 3
    A1 = A[:, 0:3]; A2 = A[:, 3:6]
    # companion form
    F = np.zeros((k * nlags, k * nlags))
    F[0:k, 0:k] = A1; F[0:k, k:2 * k] = A2
    F[k:2 * k, 0:k] = np.eye(k)
    P = np.linalg.cholesky(Sigma)        # lower triangular, ordering [de,le,lp]
    e1 = np.array([1.0, 0, 0])
    delta = P @ e1                       # impact response of [de,le,lp] to unit struct shock 1
    scale = shock_emp / delta[0]
    delta = delta * scale
    R = np.zeros(k * nlags); R[0:k] = delta
    responses = []
    v = R[0:k].copy()
    responses.append(v.copy())
    for h in range(1, H + 1):
        R = F @ R
        responses.append(R[0:k].copy())
    responses = np.array(responses)      # (H+1) x 3 : columns de, le, lp
    de = responses[:, 0]; le = responses[:, 1]; lp = responses[:, 2]
    emp_level = np.cumsum(de)            # employment level response
    unemp = -le                          # unemployment rate response (approx)
    partic = lp
    return emp_level, unemp, partic


def okun(df, states, y0, y1):
    """Okun coef = -slope of Delta(rel_urate) on Delta(rel_emp), pooled state FE."""
    rows = []
    for p in states:
        sub = df[df.state == p].sort_values("year").copy()
        sub["du"] = sub["rel_urate"].diff()
        sub["de"] = sub["rel_emp_logdev"].diff()
        s = sub[(sub.year >= y0) & (sub.year <= y1)][["state", "du", "de"]].dropna()
        rows.append(s)
    d = pd.concat(rows, ignore_index=True)
    for c in ["du", "de"]:
        d[c] = d[c] - d.groupby("state")[c].transform("mean")
    r = sm.OLS(d["du"].values, d[["de"]].values).fit()
    return dict(coef=float(-r.params[0]), t=float(-r.tvalues[0]), n=int(len(d)))


def main(panel, out, fig):
    df = pd.read_parquet(panel)
    d = build_var_data(df, 1978, 1990)
    A, Sigma, n = estimate_var(d, 1978, 1990, nlags=2)
    emp, unemp, partic = irf(A, Sigma, H=12, shock_emp=-0.01)

    irf_dict = {str(h): dict(employment=float(emp[h]), unemployment=float(unemp[h]),
                             participation=float(partic[h])) for h in range(13)}
    # dieout: first year (>=2) where |unemp| and |partic| < 10% of their peak abs
    def dieout(series):
        peak = np.max(np.abs(series))
        for h in range(2, len(series)):
            if abs(series[h]) < 0.1 * peak:
                return h
        return None
    emp_peak = float(emp[np.argmax(np.abs(emp))])
    emp_plateau = float(emp[-1])
    du_year = dieout(unemp); dp_year = dieout(partic)

    # per-worker terms (C17): decompose the year-1 employment decline via the identity
    #   d(emp) = d(emp/lf) + d(lf/pop) + d(pop)  ==>  emp = -unemp + partic + migration
    # shares (of the |year-1 employment response|) absorbed by each margin:
    e1 = emp[1]  # year-1 cumulative employment response (~ -1.7%)
    absorb = abs(e1)
    unemp_share = float(unemp[1] / absorb)             # higher unemployment
    partic_share = float(-partic[1] / absorb)          # lower participation
    mig_share = float(1.0 - unemp_share - partic_share)  # net out-migration
    per_worker = dict(unemployment=unemp_share, participation=partic_share,
                      implied_net_migration=mig_share,
                      basis="shares of the year-1 employment response")

    ok_all = okun(df, POSTALS, 1977, 1990)
    ok_farm = okun(df, FARM_STATES, 1977, 1990)

    res = dict(
        window="1978-1990 (LAUS)", n_obs=n,
        irf=irf_dict,
        year1=dict(unemployment_response=float(unemp[1]),
                   participation_response=float(partic[1])),
        employment_peak=emp_peak, employment_plateau=emp_plateau,
        unemp_partic_dieout_year=dict(unemployment=du_year, participation=dp_year),
        per_worker=per_worker,
        okun=dict(all_states=ok_all, farm_states=ok_farm),
        note=("unemployment response approximated as -le; participation as lp; working-age "
              "population proxied by resident population (see data_sources.md)."),
    )
    pathlib.Path(out).write_text(json.dumps(res, indent=2))

    yrs = list(range(13))
    figu, ax = plt.subplots(figsize=(8, 5))
    ax.plot(yrs, emp * 100, "-o", label="employment (level)", ms=3)
    ax.plot(yrs, unemp * 100, "-s", label="unemployment rate", ms=3)
    ax.plot(yrs, partic * 100, "-^", label="participation", ms=3)
    ax.axhline(0, color="k", lw=0.5)
    ax.set_xlabel("years after shock"); ax.set_ylabel("response (%)")
    ax.set_title("Fig 7: trivariate VAR response to a -1% employment shock")
    ax.legend()
    figu.savefig(fig, dpi=120, bbox_inches="tight")
    plt.close(figu)

    print("emp IRF (%):", [round(x * 100, 2) for x in emp])
    print("unemp IRF (%):", [round(x * 100, 2) for x in unemp])
    print("partic IRF (%):", [round(x * 100, 2) for x in partic])
    print("year1: unemp=%.4f partic=%.4f" % (unemp[1], partic[1]))
    print("emp peak=%.4f plateau=%.4f dieout unemp=%s partic=%s" % (emp_peak, emp_plateau, du_year, dp_year))
    print("per_worker:", {k: round(v, 3) if isinstance(v, float) else v for k, v in per_worker.items()})
    print("okun all:", ok_all, "| farm:", ok_farm)
    print("wrote", out, fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", default="data/panel.parquet")
    ap.add_argument("--out", default="results/trivariate_var.json")
    ap.add_argument("--fig", default="figures/fig7_trivariate_irf.png")
    a = ap.parse_args()
    main(a.panel, a.out, a.fig)
