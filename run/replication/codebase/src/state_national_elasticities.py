"""Step 4: state-national employment elasticities (Table 2) + region-year decomposition."""
import argparse, json, pathlib, sys
import numpy as np, pandas as pd
import statsmodels.api as sm

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from states_meta import POSTALS, EMP_START, division, region


def r2_group(y, groups):
    """R^2 of a pure group-fixed-effect model (fitted = group mean)."""
    dfg = pd.DataFrame({"y": y, "g": groups}).dropna()
    gm = dfg.groupby("g")["y"].transform("mean")
    sstot = ((dfg["y"] - dfg["y"].mean()) ** 2).sum()
    ssres = ((dfg["y"] - gm) ** 2).sum()
    return float(1 - ssres / sstot)


def main(panel, out):
    df = pd.read_parquet(panel)
    lnUS = df.groupby("year")["emp_us"].first().apply(np.log)

    per_state = []
    adjr2s = []
    nsig = 0
    for p in POSTALS:
        sub = df[df.state == p].copy()
        start = max(1948, EMP_START.get(p, 1948))
        sub = sub[(sub.year >= start) & (sub.year <= 1990)]
        s = sub[["year", "emp_nonfarm"]].dropna()
        if len(s) < 5:
            continue
        y = np.log(s["emp_nonfarm"].values)
        x = lnUS.loc[s["year"].values].values
        X = sm.add_constant(x)
        r = sm.OLS(y, X).fit()
        beta = float(r.params[1]); se = float(r.bse[1])
        t_vs1 = (beta - 1) / se if se > 0 else np.nan
        sig = bool(abs(t_vs1) > 1.96)
        if sig:
            nsig += 1
        adjr2s.append(float(r.rsquared_adj))
        per_state.append(dict(state=p, beta=beta, se=se,
                              t_vs_1=float(t_vs1), sig_diff_from_1=sig,
                              adj_r2=float(r.rsquared_adj), n=int(len(s))))

    # (ii) region-year variance decomposition of annual Δ ln state employment
    df = df.sort_values(["state", "year"])
    df["dln_emp"] = df.groupby("state")["emp_nonfarm"].transform(lambda z: np.log(z).diff())
    pool = df[(df.year >= 1948) & (df.year <= 1990) & df.dln_emp.notna()].copy()
    div_share = r2_group(pool["dln_emp"].values,
                         (pool["division"] + "_" + pool["year"].astype(str)).values)
    reg_share = r2_group(pool["dln_emp"].values,
                         (pool["region"] + "_" + pool["year"].astype(str)).values)
    year_share = r2_group(pool["dln_emp"].values, pool["year"].astype(str).values)

    res = dict(
        per_state=per_state,
        avg_adj_r2=float(np.mean(adjr2s)),
        n_states_beta_sig_diff_1=int(nsig),
        n_states=len(per_state),
        region_year=dict(census_division_share=div_share,
                         census_region_share=reg_share,
                         national_year_share=year_share),
    )
    pathlib.Path(out).write_text(json.dumps(res, indent=2))
    print("n_states:", len(per_state), "avg_adj_r2:", round(res["avg_adj_r2"], 4),
          "n_beta_sig_diff_1:", nsig)
    print("shares: national-year =", round(year_share, 3),
          "| 4-region-year =", round(reg_share, 3),
          "| 9-division-year =", round(div_share, 3))
    betas = [s["beta"] for s in per_state]
    print("beta range:", round(min(betas), 2), "to", round(max(betas), 2),
          "| median", round(float(np.median(betas)), 2))
    print("wrote", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", default="data/panel.parquet")
    ap.add_argument("--out", default="results/table2_and_regionyear.json")
    a = ap.parse_args()
    main(a.panel, a.out)
