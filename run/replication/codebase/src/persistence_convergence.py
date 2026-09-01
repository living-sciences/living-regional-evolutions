"""Step 3: cross-sectional persistence & convergence regressions (Figs 1,2,4,9)."""
import argparse, json, pathlib, sys
import numpy as np, pandas as pd
import statsmodels.api as sm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from states_meta import POSTALS, fig2_group


def avg_annual_loggrowth(sub, col, y0, y1):
    """Average annual change in log(col) over [y0,y1] using available endpoints."""
    s = sub[(sub.year >= y0) & (sub.year <= y1)][["year", col]].dropna()
    if len(s) < 2:
        return np.nan
    a, b = s.iloc[0], s.iloc[-1]
    yr = b["year"] - a["year"]
    if yr <= 0:
        return np.nan
    return (np.log(b[col]) - np.log(a[col])) / yr


def ols(y, x):
    x = np.asarray(x, float); y = np.asarray(y, float)
    m = ~(np.isnan(x) | np.isnan(y))
    X = sm.add_constant(x[m])
    r = sm.OLS(y[m], X).fit()
    return dict(slope=float(r.params[1]), intercept=float(r.params[0]),
                t=float(r.tvalues[1]), r2=float(r.rsquared), n=int(m.sum()))


def main(panel, out, figdir):
    df = pd.read_parquet(panel)
    res = {}

    # (i) employment persistence: growth 1970-90 on growth 1950-70
    g5070, g7090, states = {}, {}, []
    for p in POSTALS:
        sub = df[df.state == p]
        a = avg_annual_loggrowth(sub, "emp_nonfarm", 1950, 1970)
        b = avg_annual_loggrowth(sub, "emp_nonfarm", 1970, 1990)
        g5070[p] = a; g7090[p] = b
        if np.isfinite(a) and np.isfinite(b):
            states.append(p)
    x = [g5070[p] for p in states]; y = [g7090[p] for p in states]
    r = ols(y, x)
    res["emp_persistence_slope"] = r["slope"]
    res["emp_persistence_r2"] = r["r2"]
    res["emp_persistence_n"] = r["n"]

    # (ii) exclude AZ, FL, NV
    keep = [p for p in states if p not in ("AZ", "FL", "NV")]
    r2 = ols([g7090[p] for p in keep], [g5070[p] for p in keep])
    res["emp_persistence_r2_ex_AZ_FL_NV"] = r2["r2"]
    res["emp_persistence_slope_ex_AZ_FL_NV"] = r2["slope"]

    # figure 1 scatter
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.scatter([v * 100 for v in x], [v * 100 for v in y], s=12)
    for p in states:
        ax.annotate(p, (g5070[p] * 100, g7090[p] * 100), fontsize=6)
    xs = np.linspace(min(x), max(x), 50)
    ax.plot([v * 100 for v in xs], [(r["intercept"] + r["slope"] * v) * 100 for v in xs], "r-")
    ax.set_xlabel("Annual employment growth 1950-70 (%)")
    ax.set_ylabel("Annual employment growth 1970-90 (%)")
    ax.set_title(f"Fig 1 persistence: slope={r['slope']:.2f}, R2={r['r2']:.2f}")
    fig.savefig(pathlib.Path(figdir) / "fig1_persistence.png", dpi=120, bbox_inches="tight")
    plt.close(fig)

    # (iii) cumulative relative employment growth 1947-1990
    cum_rows = []
    for p in POSTALS:
        sub = df[df.state == p].sort_values("year")
        s = sub[["year", "rel_emp_logdev"]].dropna()
        if len(s) == 0:
            continue
        base = s.iloc[0]["rel_emp_logdev"]
        for _, rr in s.iterrows():
            cum_rows.append(dict(state=p, year=int(rr["year"]),
                                 group=fig2_group(p),
                                 cum_rel_emp=float(rr["rel_emp_logdev"] - base)))
    cum = pd.DataFrame(cum_rows)
    cum_path = pathlib.Path(panel).parent / "cumulative_rel_emp_growth.csv"
    cum.to_csv(cum_path, index=False)

    # fig 2: grouped by region
    fig, ax = plt.subplots(figsize=(9, 6))
    groups = ["newengland", "midatlantic", "coal", "rustbelt", "sunbelt", "farm", "oil"]
    for grp in groups:
        gs = cum[cum.group == grp]
        if len(gs) == 0:
            continue
        gm = gs.groupby("year")["cum_rel_emp"].mean()
        ax.plot(gm.index, gm.values, label=grp, linewidth=1.5)
    ax.axhline(0, color="k", lw=0.5)
    ax.legend(fontsize=8); ax.set_xlabel("year")
    ax.set_ylabel("cumulative rel. employment (log dev from 1947)")
    ax.set_title("Fig 2: cumulative relative employment by region group")
    fig.savefig(pathlib.Path(figdir) / "fig2_cumulative_rel_emp.png", dpi=120, bbox_inches="tight")
    plt.close(fig)

    # (iv) convergence regressions
    # manufacturing-wage convergence: NOT reconstructable (no mfg AHE). Use pcinc proxy AND
    # report the pcinc convergence the paper also requests.
    # pcinc convergence 1948-90: avg annual growth on log(1948 level)
    gpc, base48, states_pc = {}, {}, []
    for p in POSTALS:
        sub = df[df.state == p]
        g = avg_annual_loggrowth(sub, "pcinc", 1948, 1990)
        b0 = sub[sub.year == 1948]["pcinc"]
        b0 = float(b0.values[0]) if len(b0) and pd.notna(b0.values[0]) else np.nan
        gpc[p] = g; base48[p] = b0
        if np.isfinite(g) and np.isfinite(b0):
            states_pc.append(p)
    rpc = ols([gpc[p] for p in states_pc], [np.log(base48[p]) for p in states_pc])
    res["pcinc_convergence_slope"] = rpc["slope"]
    res["pcinc_convergence_t"] = rpc["t"]
    res["pcinc_convergence_r2"] = rpc["r2"]
    res["pcinc_convergence_n"] = rpc["n"]
    # mfg wage fields flagged not reconstructable
    res["mfg_wage_convergence_slope"] = None
    res["mfg_wage_convergence_t"] = None
    res["mfg_wage_convergence_r2"] = None
    res["mfg_wage_convergence_note"] = ("Manufacturing production-worker AHE (1947-1990, "
        "SIC basis) is not reconstructable from free modern APIs; per-capita income "
        "convergence (pcinc_convergence_*) is the reported reconstructable analogue.")

    # convergence figure (pcinc)
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.scatter([np.log(base48[p]) for p in states_pc], [gpc[p] * 100 for p in states_pc], s=12)
    for p in states_pc:
        ax.annotate(p, (np.log(base48[p]), gpc[p] * 100), fontsize=6)
    ax.set_xlabel("log per-capita income 1948")
    ax.set_ylabel("avg annual pcinc growth 1948-90 (%)")
    ax.set_title(f"Fig 4 analogue (income convergence): slope={rpc['slope']:.3f}, t={rpc['t']:.1f}")
    fig.savefig(pathlib.Path(figdir) / "fig4_income_convergence.png", dpi=120, bbox_inches="tight")
    plt.close(fig)

    # (v) wage-growth persistence -> use pcinc growth 1948-70 vs 1970-90 (proxy)
    a_, b_, st2 = {}, {}, []
    for p in POSTALS:
        sub = df[df.state == p]
        a_[p] = avg_annual_loggrowth(sub, "pcinc", 1948, 1970)
        b_[p] = avg_annual_loggrowth(sub, "pcinc", 1970, 1990)
        if np.isfinite(a_[p]) and np.isfinite(b_[p]):
            st2.append(p)
    corr = float(np.corrcoef([a_[p] for p in st2], [b_[p] for p in st2])[0, 1])
    res["wage_growth_persistence_corr"] = corr
    res["wage_growth_persistence_note"] = "proxy: per-capita income growth 1948-70 vs 1970-90 (mfg AHE not reconstructable)"

    # (vi) employment growth vs relative wages -> proxy with relative pcinc level (1970-90 avg)
    eg, relw, st3 = {}, {}, []
    for p in POSTALS:
        sub = df[df.state == p]
        eg[p] = avg_annual_loggrowth(sub, "emp_nonfarm", 1970, 1990)
        rw = sub[(sub.year >= 1970) & (sub.year <= 1990)]["rel_pcinc_logdev"].mean()
        relw[p] = float(rw)
        if np.isfinite(eg[p]) and np.isfinite(relw[p]):
            st3.append(p)
    r6 = ols([eg[p] for p in st3], [relw[p] for p in st3])
    res["empgrowth_vs_relwage_slope"] = r6["slope"]
    res["empgrowth_vs_relwage_t"] = r6["t"]
    res["empgrowth_vs_relwage_note"] = "proxy: employment growth 1970-90 on mean relative per-capita income 1970-90 (mfg wage not reconstructable)"

    pathlib.Path(out).write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))
    print("wrote", out, "and", cum_path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", default="data/panel.parquet")
    ap.add_argument("--out", default="results/persistence_convergence.json")
    ap.add_argument("--fig", default="figures/")
    a = ap.parse_args()
    main(a.panel, a.out, a.fig)
