"""Cached FRED data fetching for the Blanchard-Katz replication."""
import os, io, time, pathlib
import requests
import pandas as pd

RAW = pathlib.Path(__file__).resolve().parent.parent / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)
KEY = os.environ.get("FRED_API_KEY", "")
BASE = "https://api.stlouisfed.org/fred/series/observations"
_last_call = [0.0]
MIN_INTERVAL = 0.9  # seconds between FRED calls (stay under ~120/min)


def fetch_series(series_id, retries=4):
    """Return a pandas Series indexed by date (monthly or annual). Cached to data/raw."""
    cache = RAW / f"{series_id}.csv"
    if cache.exists():
        df = pd.read_csv(cache, parse_dates=["date"])
        return pd.Series(df["value"].values, index=df["date"], name=series_id)
    last = None
    for a in range(retries):
        try:
            dt = time.time() - _last_call[0]
            if dt < MIN_INTERVAL:
                time.sleep(MIN_INTERVAL - dt)
            _last_call[0] = time.time()
            if KEY:
                r = requests.get(BASE, params=dict(series_id=series_id, api_key=KEY,
                                 file_type="json"), timeout=40)
                r.raise_for_status()
                obs = r.json()["observations"]
                df = pd.DataFrame(obs)[["date", "value"]]
            else:
                url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
                r = requests.get(url, timeout=40); r.raise_for_status()
                df = pd.read_csv(io.StringIO(r.text))
                df.columns = ["date", "value"]
            df["date"] = pd.to_datetime(df["date"])
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            df = df.dropna(subset=["value"])
            df.to_csv(cache, index=False)
            return pd.Series(df["value"].values, index=df["date"], name=series_id)
        except Exception as e:
            last = e
            wait = 20.0 if ("429" in str(e)) else 1.5 * (a + 1)
            time.sleep(wait)
    raise RuntimeError(f"FRED fetch failed for {series_id}: {last}")


def to_annual(s, how="mean"):
    """Collapse a (monthly or annual) series to calendar-year values."""
    g = s.groupby(s.index.year)
    out = g.mean() if how == "mean" else g.last()
    out.index = out.index.astype(int)
    return out
