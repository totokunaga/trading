# Skill: Suggest Positions

## Goal

Analyze OHLCV candlestick data in a user-specified directory and suggest whether a trader should take a **long** or **short** position for the day. Provide conditional price-movement predictions across multiple timeframes grounded in technical analysis.

## Input

Ask the user to input a **directory name** (e.g., `USDJPY`). This directory is expected to live at the project root and contain CSV files at various intervals.

## Steps

### 1. Discover and Read Data

- List all CSV files in the provided directory.
- Each CSV file is named `{interval}_{startDate}_{endDate}.csv` (e.g., `15min_202604141645_202605141630.csv`).
- Columns: `datetime`, `open`, `high`, `low`, `close` (prices as decimal numbers).
- Read the **most recent rows** from each available timeframe. Focus on at least the last 50–100 candles per file to capture recent structure while keeping context manageable.

### 2. Technical Analysis

Perform the following analyses on the data you read. **Name every indicator and technique explicitly** in your output.

#### Price Action & Structure
- Identify the current **trend direction** (higher highs / higher lows vs. lower highs / lower lows).
- Mark key **support and resistance levels** from recent swing highs/lows across multiple timeframes.
- Look for **candlestick patterns** on the most recent candles (e.g., doji, engulfing, hammer, shooting star, pin bar).

#### Moving Averages
- Compute or estimate **SMA / EMA** values (e.g., 20-period, 50-period, 200-period) on the 15min and 1h charts.
- Note crossovers (golden cross / death cross) or price's position relative to these averages.

#### Momentum & Oscillators
- **RSI (Relative Strength Index)** — assess whether the asset is overbought (>70) or oversold (<30) on each timeframe.
- **MACD (Moving Average Convergence Divergence)** — check for signal-line crossovers and histogram direction.
- **Stochastic Oscillator** — look for %K/%D crossovers in overbought/oversold zones.

#### Volume & Volatility (if volume data is available)
- Note any unusual volume spikes that confirm or contradict the move.
- Estimate recent **ATR (Average True Range)** to gauge volatility.

#### Multi-Timeframe Confluence
- Cross-reference signals across the available timeframes (15min, 1h, 4h, 1day).
- Signals that align across multiple timeframes carry more weight.

### 3. Produce Predictions

For each of the following horizons, give a **conditional prediction**:

| Horizon | Description |
|---------|-------------|
| **15 min** | Very short-term — focus on the latest candle structure and momentum |
| **30 min** | Short-term — include nearest support/resistance levels |
| **1 h** | Intra-session — incorporate moving-average positioning |
| **4 h** | Intra-day / swing — weigh higher-timeframe trend and key levels |

Each prediction MUST follow this pattern:

> **{Horizon}:** If {specific condition, e.g., "the price breaks above the 147.20 resistance" or "RSI on the 15min crosses back below 70"}, then {expected move, e.g., "expect a continued push toward 147.50 as buyers step in above the 20-EMA"}.
> Conversely, if {opposite condition}, then {opposite outcome}.

### 4. Final Recommendation

Summarize with a clear **Long** or **Short** bias (or **Neutral / Wait** if signals conflict), including:

- **Bias**: Long / Short / Neutral
- **Confidence**: Low / Medium / High (based on how many signals align)
- **Key invalidation level**: The price at which this thesis breaks down
- **Reasoning summary**: A 2–3 sentence paragraph tying together the most compelling signals

## Output Format

Create a new directory `preds/{input_dir_name}` if not exists, and save the analysis in a markdown file there.

Structure the response as follows:

```
## Market Analysis: {Symbol}
### Current Price Context
(latest price, today's range, recent trend summary)

### Technical Indicators Summary
(table or bullet list of indicator readings per timeframe)

### Predictions
#### 15-Minute Outlook
(conditional prediction)

#### 30-Minute Outlook
(conditional prediction)

#### 1-Hour Outlook
(conditional prediction)

#### 4-Hour Outlook
(conditional prediction)

### Position Recommendation
(bias, confidence, invalidation, reasoning)
```

## Important Notes

- Always state the specific technical indicators and techniques by name so the user can verify independently.
- When support/resistance levels are cited, give the **exact price** derived from the data.
- If data for a timeframe is missing, skip that timeframe's analysis and note it.
