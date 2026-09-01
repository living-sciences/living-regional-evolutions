"""Step 7: persistence & cross-state correlations of relative unemployment (Figs 3,6,10).
LAUS reconstructs state unemployment only for 1976-1990, so 10-years-apart pairs whose
earlier endpoint is pre-1976 (1975, 1970) are not reconstructable; nearest available
analogues are reported and labeled.
"""
import argparse, json, pathlib, sys
import numpy as np, pandas as pd
import statsmodels.api as sm

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from states_meta import POSTALS, FARM_STATES


def ols(y, x):
    x = np.asarray(x, float); y = np.asarray(y, float)
    m = ~(np.isnan(x) | np.isnan(y))
    X = sm.add_constant(x[m])
    r = sm.OLS(y[m], X).fit()
    return dict(slope=float(r.params[1]), t=float(r.tvalues[1]),
                r2=float(r.rsquared), n=int(m.sum()))


def relu_by_year(df, year):
    d = df[df.year == year][["state", "rel_urate"]].dropna()
    return dict(zip(d.state, d.rel_urate))


def avg_over(df, col, y0, y1, per="state"):
    d = df[(df.year >= y0) & (df.year <= y1)]
    return d.groupby("state")[col].mean()


def main(panel, out, notes):
    df = pd.read_parquet(panel)
    persistence = []

    # requested pairs and nearest reconstructable analogues
    pairs = [
        ("1985_on_1975", 1985, 1975),   # C6 headline -> earlier endpoint pre-1976
        ("1990_on_1970", 1990, 1970),   # C7 alt -> earlier endpoint pre-1976
        ("1986_on_1976", 1986, 1976),   # nearest available analogue to 1985_on_1975
        ("1990_on_1980", 1990, 1980),   # nearest available analogue to 1990_on_1970
    ]
    for label, ylate, yearly in pairs:
        reconstructable = (yearly >= 1976) and (ylate >= 1976)
        entry = dict(pair_label=label, reconstructable=reconstructable)
        if reconstructable:
            late = relu_by_year(df, ylate); early = relu_by_year(df, yearly)
            common = [s for s in POSTALS if s in late and s in early]
            x = [early[s] for s in common]; y = [late[s] for s in common]
            r = ols(y, x)
            entry.update(slope=r["slope"], t=r["t"], r2=r["r2"], n=r["n"])
            # exclude farm states
            keep = [s for s in common if s not in FARM_STATES]
            rf = ols([late[s] for s in keep], [early[s] for s in keep])
            entry.update(slope_ex_farm=rf["slope"], r2_ex_farm=rf["r2"])
        else:
            entry.update(slope=None, t=None, r2=None, n=0,
                         slope_ex_farm=None, r2_ex_farm=None,
                         note="earlier endpoint pre-1976; not reconstructable from LAUS")
        persistence.append(entry)

    # (ii) avg unemployment vs avg employment growth, available window (1976-1990)
    # employment growth over 1976-1990 (annual log change avg)
    egrow = {}
    for p in POSTALS:
        sub = df[df.state == p][["year", "emp_nonfarm"]].dropna()
        s = sub[(sub.year >= 1976) & (sub.year <= 1990)]
        if len(s) >= 2:
            egrow[p] = (np.log(s.emp_nonfarm.iloc[-1]) - np.log(s.emp_nonfarm.iloc[0])) / (s.year.iloc[-1] - s.year.iloc[0])
    avgu = avg_over(df, "urate", 1976, 1990)
    common = [p for p in POSTALS if p in egrow and p in avgu.index and np.isfinite(avgu[p])]
    r = ols([avgu[p] for p in common], [egrow[p] for p in common])
    avg_urate_vs_empgrowth = dict(slope=r["slope"], t=r["t"], r2=r["r2"], n=r["n"],
                                  window="1976-1990")

    # (iii) avg unemployment vs relative manufacturing wage -> pcinc proxy (1976-1990)
    avg_relpci = avg_over(df, "rel_pcinc_logdev", 1976, 1990)
    common2 = [p for p in POSTALS if p in avgu.index and p in avg_relpci.index]
    r2 = ols([avgu[p] for p in common2], [avg_relpci[p] for p in common2])
    avg_urate_vs_wage = dict(t=r2["t"], r2=r2["r2"], slope=r2["slope"], n=r2["n"],
                             note="manufacturing wage not reconstructable; relative per-capita income proxy, 1976-1990")

    res = dict(persistence=persistence,
               avg_urate_vs_empgrowth=avg_urate_vs_empgrowth,
               avg_urate_vs_wage=avg_urate_vs_wage)
    pathlib.Path(out).write_text(json.dumps(res, indent=2))
    pathlib.Path(notes).write_text(
        "# Unemployment cross-section notes\n\n"
        "LAUS reconstructs state unemployment only for 1976-1990.\n\n"
        "- **1985_on_1975 (C6)**: earlier endpoint 1975 is pre-1976 -> NOT reconstructable. "
        "Nearest available analogue reported as **1986_on_1976**.\n"
        "- **1990_on_1970 (C7)**: earlier endpoint 1970 is pre-1976 -> NOT reconstructable. "
        "Nearest available analogue reported as **1990_on_1980**.\n"
        "- avg-unemployment-vs-employment-growth (Fig 6) and avg-unemployment-vs-wage (Fig 10) "
        "run on 1976-1990. Fig 10 uses relative per-capita income as the wage proxy "
        "(manufacturing AHE not reconstructable).\n"
    )
    for e in persistence:
        print(e["pair_label"], "reconstructable=", e["reconstructable"],
              "slope=", e.get("slope"), "r2=", e.get("r2"))
    print("avg_urate_vs_empgrowth:", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in avg_urate_vs_empgrowth.items()})
    print("avg_urate_vs_wage(pcinc):", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in avg_urate_vs_wage.items()})
    print("wrote", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", default="data/panel.parquet")
    ap.add_argument("--out", default="results/unemployment_cross_section.json")
    ap.add_argument("--notes", default="notes/unemployment_notes.md")
    a = ap.parse_args()
    main(a.panel, a.out, a.notes)
