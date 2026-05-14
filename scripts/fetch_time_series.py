"""Fetch OHLCV time-series data from the Twelve Data API and write it to CSV."""

import argparse
import csv
import os
import sys
from datetime import datetime

import requests

API_URL = "https://api.twelvedata.com/time_series"

INTERVAL_CHOICES = [
    "1min", "5min", "15min", "30min", "45min",
    "1h", "2h", "4h", "8h",
    "1day", "1week", "1month",
]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the Twelve Data time-series fetcher.

    Defines four optional flags that control what data is fetched and where
    it is saved:
      --symbol   : The trading pair or ticker (e.g. "USD/JPY", "EUR/USD",
                   "AAPL"). Forex pairs use a slash separator.
      --interval : The candlestick timeframe. Must be one of the intervals
                   supported by Twelve Data (e.g. "1min", "15min", "1day").
      --size     : How many candlesticks (data points) to request. The
                   Twelve Data API accepts up to 5000 per call.
      --output   : Explicit CSV file path. When omitted, a filename is
                   auto-generated from the symbol, interval, and current
                   timestamp so that successive runs never overwrite each other.

    Returns:
        argparse.Namespace with attributes: symbol, interval, size, output.
    """
    parser = argparse.ArgumentParser(
        description="Fetch candlestick data from Twelve Data and save as CSV.",
    )
    parser.add_argument(
        "--symbol",
        default="USD/JPY",
        help="Currency pair or ticker symbol (default: USD/JPY)",
    )
    parser.add_argument(
        "--interval",
        default="15min",
        choices=INTERVAL_CHOICES,
        help="Candlestick interval (default: 15min)",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=192,
        help="Number of candlesticks to retrieve, max 5000 (default: 192)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output CSV path (default: auto-generated from symbol/interval/timestamp)",
    )
    return parser.parse_args()


def fetch_time_series(
    api_key: str, symbol: str, interval: str, outputsize: int
) -> list[dict]:
    """Call the Twelve Data ``time_series`` endpoint and return OHLCV rows.

    Sends a GET request to https://api.twelvedata.com/time_series with the
    provided parameters. The response JSON looks like::

        {
          "meta": { "symbol": "USD/JPY", ... },
          "values": [
            {"datetime": "...", "open": "...", "high": "...",
             "low": "...", "close": "...", "volume": "..."},
            ...
          ],
          "status": "ok"
        }

    This function extracts and returns the ``values`` list. Rows are
    requested in ascending chronological order (oldest first) so that the
    resulting CSV is naturally sorted for time-series analysis.

    Note: The API returns all numeric values as *strings*. This function
    preserves them as-is; downstream consumers should cast if needed.

    Args:
        api_key:    Twelve Data API key (passed as the ``apikey`` query param).
        symbol:     Trading pair or ticker, e.g. "USD/JPY" or "AAPL".
        interval:   Candlestick interval, e.g. "15min", "1h", "1day".
        outputsize: Number of candlesticks to return (1–5000).

    Returns:
        A list of dicts, each containing: datetime, open, high, low, close,
        and volume.

    Exits:
        Prints an error and exits with code 1 if the API returns an error
        status or an empty result set.
    """
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "order": "asc",
        "apikey": api_key,
    }

    resp = requests.get(API_URL, params=params, timeout=30)
    resp.raise_for_status()

    data = resp.json()

    if data.get("status") == "error":
        print(f"API error: {data.get('message', 'unknown error')}", file=sys.stderr)
        sys.exit(1)

    values = data.get("values")
    if not values:
        print("No data returned from the API.", file=sys.stderr)
        sys.exit(1)

    return values


def write_csv(values: list[dict], output_path: str) -> None:
    """Write a list of OHLCV dicts to a CSV file.

    Column headers are derived from the keys of the first element in
    ``values``, which for the Twelve Data time_series endpoint will be:
    datetime, open, high, low, close, volume.

    The file is written with ``newline=""`` as required by the csv module
    on all platforms to prevent extra blank lines on Windows.

    Args:
        values:      List of dicts as returned by ``fetch_time_series()``.
        output_path: Destination file path for the CSV.
    """
    fieldnames = list(values[0].keys())

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(values)


def build_output_path(symbol: str, interval: str, values: list[dict]) -> str:
    """Build the output CSV path from the symbol, interval, and data range.

    Creates a symbol directory and names the file after the interval and
    time range of the data::

        USDJPY/15min_202605121515_202605141400.csv

    Specifically:
      1. The symbol directory strips non-alphanumeric characters
         (e.g. "USD/JPY" -> "USDJPY").
      2. The directory is created automatically if it doesn't exist.
      3. The filename is ``{interval}_{start}_{end}.csv`` where each
         timestamp is the ``datetime`` field of the first / last element
         formatted as ``YYYYMMDDHHmm``.

    Args:
        symbol:   Trading pair or ticker, e.g. "USD/JPY".
        interval: Candlestick interval string, e.g. "15min".
        values:   The OHLCV rows returned by ``fetch_time_series()`` (must
                  be in ascending order so that the first element is the
                  earliest and the last is the latest).

    Returns:
        The full relative path to the CSV file, e.g.
        ``USDJPY/15min_202605121515_202605141400.csv``.
    """
    symbol_dir = "".join(ch for ch in symbol if ch.isalnum())
    os.makedirs(symbol_dir, exist_ok=True)

    dt_fmt = "%Y-%m-%d %H:%M:%S" if " " in values[0]["datetime"] else "%Y-%m-%d"
    start_dt = datetime.strptime(values[0]["datetime"], dt_fmt)
    end_dt = datetime.strptime(values[-1]["datetime"], dt_fmt)
    filename = f"{interval}_{start_dt.strftime('%Y%m%d%H%M')}_{end_dt.strftime('%Y%m%d%H%M')}.csv"

    return os.path.join(symbol_dir, filename)


def main() -> None:
    """Entry point: parse args, fetch data, and write the CSV.

    Orchestrates the full pipeline:
      1. Parse CLI arguments (symbol, interval, size, output path).
      2. Read the ``TWELVE_DATA_API_KEY`` environment variable.  This is
         expected to be injected by ``dotenvx run --`` which decrypts
         the ``.env`` file at runtime, but any mechanism that sets the
         env var (Docker, CI secrets, ``export``) works equally well.
      3. Call the Twelve Data API to retrieve candlestick data.
      4. Determine the output path — either the explicit ``--output`` value,
         or an auto-generated path under ``<SYMBOL>/`` named after the
         interval and time range of the fetched data.
      5. Write the result to a CSV file and print a summary to stdout.
    """
    args = parse_args()

    api_key = os.environ.get("TWELVE_DATA_API_KEY")
    if not api_key:
        print(
            "Error: TWELVE_DATA_API_KEY environment variable is not set.\n"
            "Run with: dotenvx run -- python scripts/fetch_time_series.py",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Fetching {args.size} candlesticks for {args.symbol} @ {args.interval} ...")
    values = fetch_time_series(api_key, args.symbol, args.interval, args.size)

    output_path = args.output or build_output_path(args.symbol, args.interval, values)

    write_csv(values, output_path)
    print(f"Wrote {len(values)} rows to {output_path}")


if __name__ == "__main__":
    main()
