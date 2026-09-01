"""Step 2: reconstruct the Blanchard-Katz (1992) state panel from public sources.

Sources (all via FRED, reconstructing the paper's archival BLS "Employment and
Earnings" series):
  employment  : {POSTAL}NAN  total nonfarm NSA (monthly, 1939+) -> annual mean
  pcinc       : {POSTAL}PCPI per-capita personal income (annual, 1929+, BEA)
  population  : {POSTAL}POP  resident population (annual)
  urate       : {POSTAL}UR   unemployment rate NSA (monthly, 1976+, LAUS) -> annual mean
  labor force : {POSTAL}LF   civilian labor force (monthly, 1976+, LAUS) -> annual mean

National aggregates: PAYNSA (US nonfarm NSA), UNRATENSA (US urate),
A792RC0A052NBEA (US per-capita PI), POPTHM (US population).

Manufacturing production-worker AHE (paper's headline wage series) is archival
SIC-basis data available only in the printed "Employment and Earnings"; it is
NOT reconstructable from any modern free API (see notes/data_sources.md). Per
the plan, per-capita income is used as the reconstructable relative-wage proxy.
"""
import argparse, pathlib, sys
import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from states_meta import STATES, POSTALS, EMP_START, division, region, ahe_start, fig2_group
from fred_util import fetch_series, to_annual

YEARS = list(range(1947, 1991))  # 1947..1990 inclusive


def build():
    rows = []
    # national aggregates (annual)
    us_emp = to_annual(fetch_series("PAYNSA"), "mean")
    us_ur = to_annual(fetch_series("UNRATENSA"), "mean")
    us_pcinc = to_annual(fetch_series("A792RC0A052NBEA"), "mean")
    us_pop = to_annual(fetch_series("POPTHM"), "mean")
    us_lf = to_annual(fetch_series("CLF16OV"), "mean")  # civilian labor force (thousands)

    per_state = {}
    for p in POSTALS:
        emp = to_annual(fetch_series(f"{p}NAN"), "mean")           # thousands
        pci = to_annual(fetch_series(f"{p}PCPI"), "mean")          # dollars
        pop = to_annual(fetch_series(f"{p}POP"), "mean")           # thousands
        ur = to_annual(fetch_series(f"{p}UR"), "mean")             # percent
        lf = to_annual(fetch_series(f"{p}LF"), "mean")             # persons
        per_state[p] = dict(emp=emp, pci=pci, pop=pop, ur=ur, lf=lf)

    for p in POSTALS:
        d = per_state[p]
        emp_start = EMP_START.get(p, 1947)
        for y in YEARS:
            emp = d["emp"].get(y, np.nan)
            if y < emp_start:
                emp = np.nan
            pci = d["pci"].get(y, np.nan)
            pop = d["pop"].get(y, np.nan)
            ur = d["ur"].get(y, np.nan)
            lf = d["lf"].get(y, np.nan)
            rows.append(dict(
                state=p, year=y,
                division=division(p), region=region(p), fig2_group=fig2_group(p),
                emp_nonfarm=emp, emp_us=us_emp.get(y, np.nan),
                pcinc=pci, pcinc_us=us_pcinc.get(y, np.nan),
                pop=pop, pop_us=us_pop.get(y, np.nan),
                urate=ur, urate_us=us_ur.get(y, np.nan),
                labor_force=lf, lf_us=us_lf.get(y, np.nan) * 1000.0,  # thousands->persons
            ))
    df = pd.DataFrame(rows).sort_values(["state", "year"]).reset_index(drop=True)

    # ---- relative variables (log deviations from national aggregate) ----
    df["rel_emp_logdev"] = np.log(df["emp_nonfarm"]) - np.log(df["emp_us"])
    df["rel_pcinc_logdev"] = np.log(df["pcinc"]) - np.log(df["pcinc_us"])
    df["rel_urate"] = df["urate"] - df["urate_us"]

    # Manufacturing wage: not reconstructable (archival SIC AHE). Placeholder columns.
    df["mfg_ahe"] = np.nan
    df["mfg_ahe_us"] = np.nan
    df["rel_wage_logdev"] = np.nan  # see notes; per-capita income is the proxy used downstream

    # ---- participation / employment-labor-force system (le, lp) ----
    # LAUS employment level = labor_force * (1 - urate/100). Normalize establishment
    # nonfarm employment so it matches LAUS employment in base year 1976 (appendix).
    df["laus_emp"] = df["labor_force"] * (1 - df["urate"] / 100.0)
    us_laus_emp = (us_lf * 1000.0) * (1 - us_ur / 100.0)

    le_list, lp_list = [], []
    for p in POSTALS:
        sub = df[df["state"] == p]
        base = sub[sub["year"] == 1976]
        if len(base) and pd.notna(base["laus_emp"].values[0]) and pd.notna(base["emp_nonfarm"].values[0]):
            k = base["laus_emp"].values[0] / (base["emp_nonfarm"].values[0] * 1000.0)
        else:
            k = np.nan
        for _, r in sub.iterrows():
            est = r["emp_nonfarm"] * 1000.0 * k  # normalized establishment employment (persons)
            unemp = r["labor_force"] * r["urate"] / 100.0
            lf_paper = est + unemp
            wap = r["pop"] * 1000.0  # working-age proxy: resident population (documented)
            # US counterparts
            y = r["year"]
            est_us = us_laus_emp.get(y, np.nan)  # US employment (persons)
            lf_us = us_lf.get(y, np.nan) * 1000.0
            wap_us = us_pop.get(y, np.nan) * 1000.0
            le = np.log(est / lf_paper) - np.log(est_us / lf_us) if lf_paper > 0 else np.nan
            lp = np.log(lf_paper / wap) - np.log(lf_us / wap_us) if wap > 0 else np.nan
            le_list.append(le); lp_list.append(lp)
    df["le"] = le_list
    df["lp"] = lp_list
    df["participation"] = df["labor_force"] / (df["pop"] * 1000.0)
    return df


def write_notes(df, path):
    cov = []
    for p in POSTALS:
        sub = df[(df.state == p) & df.emp_nonfarm.notna()]
        e0 = int(sub.year.min()) if len(sub) else None
        cov.append((p, e0, ahe_start(p)))
    lines = [
        "# Data Sources — Blanchard & Katz (1992) 'Regional Evolutions' replication\n",
        "Reconstructed from public APIs (FRED), standing in for the paper's archival",
        "BLS *Employment and Earnings* and CPS *Geographic Profile* series.\n",
        "## Series, source, vintage, units, coverage\n",
        "| variable | FRED id | source | units | coverage | notes |",
        "|---|---|---|---|---|---|",
        "| emp_nonfarm | {POSTAL}NAN | BLS CES/SAE (state, NSA) | thousands of jobs | 1939-1990 (AK 1960, HI 1958) | monthly NSA averaged to calendar year; BLS reconstruction on current basis stands in for 'Employment and Earnings' total nonagricultural employment |",
        "| emp_us | PAYNSA | BLS CES (US, NSA) | thousands | 1939-1990 | national aggregate for relative employment |",
        "| pcinc | {POSTAL}PCPI | BEA SAINC1 | dollars/person/yr | 1929-1990 (AK/HI 1950) | per-capita personal income |",
        "| pcinc_us | A792RC0A052NBEA | BEA | dollars/person/yr | 1929-1990 | US per-capita personal income |",
        "| pop | {POSTAL}POP | Census / BEA | thousands | 1900-1990 | resident population |",
        "| urate | {POSTAL}UR | BLS LAUS | percent | 1976-1990 | monthly NSA averaged to year |",
        "| labor_force | {POSTAL}LF | BLS LAUS | persons | 1976-1990 | civilian labor force |",
        "| urate_us | UNRATENSA | BLS CPS | percent | 1948-1990 | US unemployment rate |\n",
        "## Relative variables",
        "- rel_emp_logdev = ln(emp_state) - ln(emp_US)",
        "- rel_pcinc_logdev = ln(pcinc_state) - ln(pcinc_US)",
        "- rel_urate = urate_state - urate_US",
        "- le = ln(est.employment / labor force) minus US counterpart; establishment nonfarm",
        "  employment normalized to equal LAUS employment in base year 1976 (per appendix).",
        "- lp = ln(labor force / working-age population) minus US counterpart. Working-age",
        "  population approximated by resident population (state CPS out-of-labor-force by year",
        "  is not available from free APIs); documented approximation.\n",
        "## KNOWN GAPS (not reconstructable from free modern APIs)",
        "1. **Manufacturing production-worker AHE, 1947-1990** (the paper's headline wage",
        "   series, from printed *Employment and Earnings*, SIC basis). Modern BLS SM AHE",
        "   series begin only 2001 (NAICS); Census ASM API begins 1997; BEA industry wages",
        "   need a registration key and begin 1969. No overlap with the 1947-1990 window is",
        "   available. **Per-capita personal income (1948-1990) is used as the reconstructable",
        "   relative-wage proxy** in all wage-convergence/persistence/VAR steps, labeled as",
        "   such. The CPS worker-characteristic-controlled wage (1979-1989) is likewise not",
        "   reconstructable here.",
        "2. **State unemployment before 1976.** The paper backfilled 1970-1975 (10 large",
        "   states from 1970; the rest from LMA rates provided by H. Courtney, normalized to",
        "   the 1976 CPS). LAUS only begins 1976, so pre-1976 relative unemployment,",
        "   participation, le and lp are NOT reconstructable. All unemployment/participation",
        "   analyses are therefore run on 1976-1990.\n",
        "## Per-state employment coverage start (reconstructed) vs. appendix AHE start",
        "| state | emp start | appendix AHE start |",
        "|---|---|---|",
    ]
    for p, e0, a in cov:
        lines.append(f"| {p} | {e0} | {a} |")
    pathlib.Path(path).write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/panel.parquet")
    ap.add_argument("--notes", default="notes/data_sources.md")
    a = ap.parse_args()
    df = build()
    outp = pathlib.Path(a.out)
    df.to_parquet(outp, index=False)
    df.to_csv(outp.with_suffix(".csv"), index=False)
    write_notes(df, a.notes)
    nstates = df.state.nunique()
    yr = (int(df.year.min()), int(df.year.max()))
    print(f"panel: {len(df)} rows, {nstates} units, years {yr}")
    print("emp non-null:", int(df.emp_nonfarm.notna().sum()),
          "| pcinc non-null:", int(df.pcinc.notna().sum()),
          "| urate non-null:", int(df.urate.notna().sum()))
    print("cols:", list(df.columns))
