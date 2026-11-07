# Regional Evolutions (Blanchard and Katz, BPEA 1992)

This repository holds the working directory of an automated replication and
extension of the paper, produced by [SAI](https://sai.science) agents. It is
the same file tree a signed-in user can browse in the run's workspace, and it
backs the public living-paper page:

**https://livingscience.ai/econ/living-regional-evolutions**

## What is here

- `run/` — the replication working directory: `analyze/` (extracted claims),
  `replication/` (the ported and executed codebase), `verify/` (per-claim
  verdicts and the replication score), `report/` (the run's own report), and
  `followup/` (the extension studies: a re-estimation of the paper's main
  claims on data through 2024-2026, and a refit of the paper's model to the
  combined evidence, each with its report, result card, and figures).
- `referee_report.md` — the referee-style report synthesized from the run.
- Some large input data files are omitted; where that happened,
  `run/LARGE_FILES_OMITTED.md` lists them.

## The paper

Blanchard, O. J., and Katz, L. F. (1992). Regional Evolutions. Brookings Papers on Economic Activity 1992(1), 1-75.

No replication package survives from 1992; the analysis here is reconstructed entirely from public data (BLS, BEA, FRED, FHFA). Files under `run/replication/codebase/` derive from those materials
(possibly modified by the replication agent) and remain under their original
authors' terms. Everything else in this repository is generated output from
the SAI pipeline.

## Caveats

Replication scores measure whether claims reproduce under our agents' effort,
not whether authors did anything wrong. Read the referee report's Notes and
the per-claim verdicts in `run/verify/verdicts.json` before quoting any
number.

## Data sources for the extension studies

The extension studies pulled fresh public data on August 24, 2026, all of it from FRED (Federal Reserve Bank of St. Louis). In full:

- U.S. Bureau of Labor Statistics, Local Area Unemployment Statistics: state unemployment rate, state civilian labor force, and state labor force participation rate, 50 states and DC, monthly, seasonally adjusted, 1976 to 2026, retrieved from FRED.
- U.S. Bureau of Labor Statistics, State and Area Employment: total nonfarm employees by state, monthly, 1939 to 2026, retrieved from FRED.
- U.S. Bureau of Labor Statistics, national series PAYEMS (total nonfarm payrolls, from 1939) and the Current Population Survey series CE16OV, CLF16OV, CIVPART and UNRATE (from 1948), retrieved from FRED.
- U.S. Bureau of Economic Analysis, per capita personal income by state (annual, 1929 to 2025) and for the United States (series A792RC0A052NBEA), retrieved from FRED.

The original paper's data files are not distributed anywhere we could find, so the paper-side comparisons use the published numbers themselves. The theory update fetched no new data; it works entirely from the living update's panel.
