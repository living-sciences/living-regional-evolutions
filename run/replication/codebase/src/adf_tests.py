"""Step 5: Augmented Dickey-Fuller unit-root tests on relative employment & wages.

Employment (eq. 1): Delta n = a1 + sum_{j=1..4} a2j Delta n_{t-j} + a3 n_{t-1} + a4 t
  over 1952-1990, with linear trend. Report a3, its ADF t-stat, 5% rejection.
Wages (eq. 3): analogous on relative wages, 4 lags, NO trend, 1952-1990.
  Manufacturing AHE not reconstructable -> relative per-capita income used as proxy.
"""
import argparse, json, pathlib, sys
import numpy as np, pandas as pd
import statsmodels.api as sm

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from states_meta import POSTALS

# MacKinnon (2010) approximate 5% critical values, T~40
CRIT_CT = -3.50   # constant + trend
CRIT_C = -2.94    # constant only


def adf_manual(series_by_year, y0, y1, nlags=4, trend=True):
    """Run the paper's ADF regression manually; return (level_coef, tstat, n)."""
    s = series_by_year.dropna().sort_index()
    s = s[(s.index >= y0 - nlags - 1) & (s.index <= y1)]
    lv = s.copy()
    d = lv.diff()
    rows = []
    for yr in lv.index:
        if yr < y0 or yr > y1:
            continue
        if (yr - 1) not in lv.index or pd.isna(d.get(yr, np.nan)):
            continue
        lags = [d.get(yr - j, np.nan) for j in range(1, nlags + 1)]
        if any(pd.isna(lags)):
            continue
        rows.append((yr, d[yr], lv[yr - 1], *lags))
    if len(rows) < nlags + 4:
        return None
    arr = np.array(rows, float)
    yr = arr[:, 0]; dy = arr[:, 1]; lev = arr[:, 2]; dlags = arr[:, 3:]
    cols = [np.ones(len(dy)), lev]
    names = ["const", "level"]
    if trend:
        cols.append(yr - yr.mean()); names.append("trend")
    for j in range(nlags):
        cols.append(dlags[:, j]); names.append(f"dlag{j+1}")
    X = np.column_stack(cols)
    r = sm.OLS(dy, X).fit()
    coef = float(r.params[1]); tst = float(r.tvalues[1])
    return coef, tst, int(len(dy))


def run_block(df, col, trend, crit):
    per, nrej, nneg, rej_states = [], 0, 0, []
    for p in POSTALS:
        sub = df[df.state == p][["year", col]].dropna()
        if len(sub) < 12:
            continue
        s = pd.Series(sub[col].values, index=sub["year"].astype(int).values)
        out = adf_manual(s, 1952, 1990, nlags=4, trend=trend)
        if out is None:
            continue
        coef, tst, n = out
        rej = bool(tst < crit)
        if rej:
            nrej += 1; rej_states.append(p)
        if coef < 0:
            nneg += 1
        per.append(dict(state=p, lagged_level_coef=coef, adf_tstat=tst,
                        rejects_5pct=rej, n=n))
    return dict(per_state=per, n_reject_5pct=nrej, reject_states=rej_states,
               n_negative_coef=nneg, n_states=len(per), crit_5pct=crit)


def main(panel, out):
    df = pd.read_parquet(panel)
    emp = run_block(df, "rel_emp_logdev", trend=True, crit=CRIT_CT)
    wage = run_block(df, "rel_pcinc_logdev", trend=False, crit=CRIT_C)
    wage["note"] = ("Manufacturing AHE not reconstructable; relative per-capita income "
                    "used as proxy for the relative-wage ADF spec.")
    res = dict(employment=emp, wages=wage)
    pathlib.Path(out).write_text(json.dumps(res, indent=2))
    print("EMPLOYMENT: n=%d, reject 5%%=%d %s, negative-coef=%d" %
          (emp["n_states"], emp["n_reject_5pct"], emp["reject_states"], emp["n_negative_coef"]))
    print("WAGES(pcinc proxy): n=%d, reject 5%%=%d, negative-coef=%d" %
          (wage["n_states"], wage["n_reject_5pct"], wage["n_negative_coef"]))
    print("wrote", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", default="data/panel.parquet")
    ap.add_argument("--out", default="results/adf_tests.json")
    a = ap.parse_args()
    main(a.panel, a.out)
