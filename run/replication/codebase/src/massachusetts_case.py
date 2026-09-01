"""Step 10: Massachusetts case study (descriptive, reconstructable parts).

Uses annual series direct from FRED (extends past the 1990 panel to include 1991).
"""
import argparse, json, pathlib, sys
import numpy as np, pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from fred_util import fetch_series, to_annual


def gr(emp, y):
    """log employment growth (percent) from y-1 to y."""
    if (y in emp.index) and ((y - 1) in emp.index):
        return 100.0 * (np.log(emp[y]) - np.log(emp[y - 1]))
    return np.nan


def avg_gr(emp, y0, y1):
    if (y0 in emp.index) and (y1 in emp.index):
        return 100.0 * (np.log(emp[y1]) - np.log(emp[y0])) / (y1 - y0)
    return np.nan


def main(out, notes):
    ma_emp = to_annual(fetch_series("MANAN"), "mean")
    us_emp = to_annual(fetch_series("PAYNSA"), "mean")
    ma_ur = to_annual(fetch_series("MAUR"), "mean")
    us_ur = to_annual(fetch_series("UNRATENSA"), "mean")

    # (i)
    growth_1980_85 = avg_gr(ma_emp, 1980, 1985)
    us_1980_85 = avg_gr(us_emp, 1980, 1985)
    gap_1980_85 = growth_1980_85 - us_1980_85
    n_below = 0
    for y in range(1948, 1980):
        gm = gr(ma_emp, y); gu = gr(us_emp, y)
        if np.isfinite(gm) and np.isfinite(gu) and gm < gu:
            n_below += 1

    # (ii)
    def rel_u(y):
        return float(ma_ur[y] - us_ur[y]) if (y in ma_ur.index and y in us_ur.index) else None
    unemp_rel_1979 = rel_u(1979)
    unemp_rel_1985 = rel_u(1985)

    # (iii) late-1980s bust 1985-1991
    egrow = {}
    for y in range(1985, 1992):
        egrow[str(y)] = dict(MA=gr(ma_emp, y), US=gr(us_emp, y),
                             gap=(gr(ma_emp, y) - gr(us_emp, y)))
    avg_85_91 = avg_gr(ma_emp, 1985, 1991)
    us_85_91 = avg_gr(us_emp, 1985, 1991)

    res = dict(
        growth_1980_85=growth_1980_85,
        us_growth_1980_85=us_1980_85,
        gap_vs_us_1980_85=gap_1980_85,
        n_years_below_us_1948_79=n_below,
        unemp_rel_1979=unemp_rel_1979,
        unemp_rel_1985=unemp_rel_1985,
        mfg_wage_rel_1979=None,
        mfg_wage_rel_1985=None,
        cps_wage_rel_1979=None,
        cps_wage_rel_1985=None,
        mfg_wage_note="manufacturing production-worker AHE and CPS-controlled wage not reconstructable (archival)",
        emp_growth_by_year_1985_91=egrow,
        avg_growth_1985_91=avg_85_91,
        us_avg_growth_1985_91=us_85_91,
        gap_vs_us_1985_91=(avg_85_91 - us_85_91),
        growth_1990=gr(ma_emp, 1990),
        growth_1991=gr(ma_emp, 1991),
        unemp_rel_1991=rel_u(1991),
    )
    pathlib.Path(out).write_text(json.dumps(res, indent=2, default=lambda o: None if not np.isfinite(o) else float(o)))
    pathlib.Path(notes).write_text(
        "# Massachusetts case-study notes\n\n"
        "- Employment=FRED MANAN/PAYNSA (annual mean of NSA monthly); extended to 1991.\n"
        "- Unemployment relative to U.S. reconstructable for 1979, 1985, 1991 (LAUS >=1976).\n"
        "- **Not reconstructable:** manufacturing production-worker AHE (relative MA-U.S. wage) "
        "and the CPS worker-characteristic-controlled wage (1979-1989). Fields returned null "
        "and flagged.\n")
    print(json.dumps(res, indent=2, default=lambda o: None if not np.isfinite(o) else float(o)))
    print("wrote", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/massachusetts.json")
    ap.add_argument("--notes", default="notes/mass_notes.md")
    a = ap.parse_args()
    main(a.out, a.notes)
