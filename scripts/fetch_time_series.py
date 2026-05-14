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
    """Call the Twelve Data time_series endpoint and return the values list."""
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
    """Write a list of OHLCV dicts to a CSV file."""
    fieldnames = list(values[0].keys())

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(values)


def default_output_path(symbol: str, interval: str) -> str:
    safe_symbol = symbol.replace("/", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{safe_symbol}_{interval}_{timestamp}.csv"


def main() -> None:
    args = parse_args()

    api_key = os.environ.get("TWELVE_DATA_API_KEY")
    if not api_key:
        print(
            "Error: TWELVE_DATA_API_KEY environment variable is not set.\n"
            "Run with: dotenvx run -- python scripts/fetch_time_series.py",
            file=sys.stderr,
        )
        sys.exit(1)

    output_path = args.output or default_output_path(args.symbol, args.interval)

    print(f"Fetching {args.size} candlesticks for {args.symbol} @ {args.interval} ...")
    values = fetch_time_series(api_key, args.symbol, args.interval, args.size)

    write_csv(values, output_path)
    print(f"Wrote {len(values)} rows to {output_path}")


if __name__ == "__main__":
    main()
