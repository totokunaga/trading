# Trading Data Fetcher

A Python script that fetches OHLC candlestick data from the [Twelve Data API](https://twelvedata.com/docs#time-series) and exports it to CSV.

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) - fast Python package manager
- [dotenvx](https://dotenvx.com/) - encrypted environment variable management

## Setup

### 1. Create the virtual environment and install dependencies

```bash
uv venv
uv pip install -r requirements.txt
```

### 2. Configure your API key

Copy the example env file and add your [Twelve Data API key](https://twelvedata.com/account/api-keys):

```bash
cp .env.example .env
# Edit .env and replace "your_api_key_here" with your actual key
```

Then encrypt the `.env` file with dotenvx:

```bash
dotenvx encrypt
```

This encrypts `.env` in-place and creates a `.env.keys` file containing the decryption key. The `.gitignore` is configured to exclude both `.env.keys` and any generated CSV files from version control.

## Usage

Run the script through `dotenvx run --` so the encrypted API key is decrypted and injected as an environment variable:

```bash
dotenvx run -- .venv/bin/python scripts/fetch_time_series.py
```

### CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `--symbol` | `USD/JPY` | Currency pair or ticker symbol (e.g. `EUR/USD`, `AAPL`) |
| `--interval` | `15min` | Candlestick interval: `1min`, `5min`, `15min`, `30min`, `45min`, `1h`, `2h`, `4h`, `8h`, `1day`, `1week`, `1month` |
| `--size` | `192` | Number of candlesticks to fetch (max 5000) |
| `--output` | auto-generated | Output CSV file path |

### Examples

Fetch the default 192 candles of USD/JPY at 15-minute intervals:

```bash
dotenvx run -- .venv/bin/python scripts/fetch_time_series.py
```

Fetch 500 hourly candles for EUR/USD and save to a specific file:

```bash
dotenvx run -- .venv/bin/python scripts/fetch_time_series.py \
  --symbol EUR/USD --interval 1h --size 500 --output eur_usd_1h.csv
```

Fetch daily candles for a stock:

```bash
dotenvx run -- .venv/bin/python scripts/fetch_time_series.py \
  --symbol AAPL --interval 1day --size 365
```

### Output

When `--output` is omitted, the script generates a filename from the symbol, interval, and current timestamp (e.g. `USD_JPY_15min_20260514_140826.csv`), so successive runs never overwrite each other.

The CSV contains one row per candlestick in ascending chronological order:

```
datetime,open,high,low,close
2026-05-12 15:15:00,157.6514,157.68858,157.63715,157.66698
2026-05-12 15:30:00,157.66825,157.74948,157.66648,157.7475
2026-05-12 15:45:00,157.74463,157.76464,157.1174,157.35356
```

> **Note:** Equity symbols (e.g. AAPL) include a `volume` column; forex pairs typically do not.

## Project Structure

```
trading/
  .env.example      # Template for the API key env var
  .gitignore         # Excludes .env.keys, .venv/, *.csv, __pycache__/
  requirements.txt   # Pinned Python dependencies
  scripts/
    fetch_time_series.py   # Main script
```

## Notes

- Consider market open times
- Adding predictions based on fundamental analysis from banks would be helpful
- Adding scenario-based entry/exit strategies for bearish and bullish positions based on technical analysis
