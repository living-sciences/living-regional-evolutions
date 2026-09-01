# Data Sources — Blanchard & Katz (1992) 'Regional Evolutions' replication

Reconstructed from public APIs (FRED), standing in for the paper's archival
BLS *Employment and Earnings* and CPS *Geographic Profile* series.

## Series, source, vintage, units, coverage

| variable | FRED id | source | units | coverage | notes |
|---|---|---|---|---|---|
| emp_nonfarm | {POSTAL}NAN | BLS CES/SAE (state, NSA) | thousands of jobs | 1939-1990 (AK 1960, HI 1958) | monthly NSA averaged to calendar year; BLS reconstruction on current basis stands in for 'Employment and Earnings' total nonagricultural employment |
| emp_us | PAYNSA | BLS CES (US, NSA) | thousands | 1939-1990 | national aggregate for relative employment |
| pcinc | {POSTAL}PCPI | BEA SAINC1 | dollars/person/yr | 1929-1990 (AK/HI 1950) | per-capita personal income |
| pcinc_us | A792RC0A052NBEA | BEA | dollars/person/yr | 1929-1990 | US per-capita personal income |
| pop | {POSTAL}POP | Census / BEA | thousands | 1900-1990 | resident population |
| urate | {POSTAL}UR | BLS LAUS | percent | 1976-1990 | monthly NSA averaged to year |
| labor_force | {POSTAL}LF | BLS LAUS | persons | 1976-1990 | civilian labor force |
| urate_us | UNRATENSA | BLS CPS | percent | 1948-1990 | US unemployment rate |

## Relative variables
- rel_emp_logdev = ln(emp_state) - ln(emp_US)
- rel_pcinc_logdev = ln(pcinc_state) - ln(pcinc_US)
- rel_urate = urate_state - urate_US
- le = ln(est.employment / labor force) minus US counterpart; establishment nonfarm
  employment normalized to equal LAUS employment in base year 1976 (per appendix).
- lp = ln(labor force / working-age population) minus US counterpart. Working-age
  population approximated by resident population (state CPS out-of-labor-force by year
  is not available from free APIs); documented approximation.

## KNOWN GAPS (not reconstructable from free modern APIs)
1. **Manufacturing production-worker AHE, 1947-1990** (the paper's headline wage
   series, from printed *Employment and Earnings*, SIC basis). Modern BLS SM AHE
   series begin only 2001 (NAICS); Census ASM API begins 1997; BEA industry wages
   need a registration key and begin 1969. No overlap with the 1947-1990 window is
   available. **Per-capita personal income (1948-1990) is used as the reconstructable
   relative-wage proxy** in all wage-convergence/persistence/VAR steps, labeled as
   such. The CPS worker-characteristic-controlled wage (1979-1989) is likewise not
   reconstructable here.
2. **State unemployment before 1976.** The paper backfilled 1970-1975 (10 large
   states from 1970; the rest from LMA rates provided by H. Courtney, normalized to
   the 1976 CPS). LAUS only begins 1976, so pre-1976 relative unemployment,
   participation, le and lp are NOT reconstructable. All unemployment/participation
   analyses are therefore run on 1976-1990.

## Per-state employment coverage start (reconstructed) vs. appendix AHE start
| state | emp start | appendix AHE start |
|---|---|---|
| AL | 1947 | 1949 |
| AK | 1960 | 1961 |
| AZ | 1947 | 1949 |
| AR | 1947 | 1949 |
| CA | 1947 | 1947 |
| CO | 1947 | 1951 |
| CT | 1947 | 1948 |
| DE | 1947 | 1947 |
| DC | 1947 | 1972 |
| FL | 1947 | 1948 |
| GA | 1947 | 1949 |
| HI | 1958 | 1961 |
| ID | 1947 | 1950 |
| IL | 1947 | 1947 |
| IN | 1947 | 1948 |
| IA | 1947 | 1949 |
| KS | 1947 | 1949 |
| KY | 1947 | 1954 |
| LA | 1947 | 1950 |
| ME | 1947 | 1948 |
| MD | 1947 | 1950 |
| MA | 1947 | 1950 |
| MI | 1956 | 1947 |
| MN | 1950 | 1947 |
| MS | 1947 | 1950 |
| MO | 1947 | 1951 |
| MT | 1947 | 1950 |
| NE | 1947 | 1950 |
| NV | 1947 | 1950 |
| NH | 1947 | 1947 |
| NJ | 1947 | 1947 |
| NM | 1947 | 1949 |
| NY | 1947 | 1947 |
| NC | 1947 | 1950 |
| ND | 1947 | 1956 |
| OH | 1947 | 1952 |
| OK | 1947 | 1948 |
| OR | 1947 | 1950 |
| PA | 1947 | 1947 |
| RI | 1947 | 1947 |
| SC | 1947 | 1949 |
| SD | 1947 | 1950 |
| TN | 1947 | 1948 |
| TX | 1947 | 1949 |
| UT | 1947 | 1947 |
| VT | 1947 | 1949 |
| VA | 1947 | 1950 |
| WA | 1947 | 1947 |
| WV | 1947 | 1951 |
| WI | 1947 | 1947 |
| WY | 1947 | 1950 |
