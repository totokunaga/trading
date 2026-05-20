# Skill: Suggest Positions

## Goal

Analyze OHLCV candlestick data in a user-specified directory and suggest whether a trader should take a long or short position for respective timeframes. Specifically, provide the following for each timeframe:

- **Direction**: long or short
- **Aimed Pattern**: bounce or breakout at which Support/Resistance level
- **Entry Price**: the price at which the trader should enter the position
  - More specifically, give what kind of candle pattern or price action formation would trigger the entry
- **Stop Loss**: the price at which the trader should exit the position if it moves against them
- **Take Profit**: the price at which the trader should exit the position if it moves in their favor
- **Confidence**: confidence level in percentage (0-100%)

## Input

Ask the user to input a **directory name** (e.g., `USDJPY`). This directory is expected to live at the project root and contain CSV files at various intervals.

## Steps

### 1. Discover and Read Data

- List all CSV files in the provided directory.
- Each CSV file is named `{interval}_{startDate}_{endDate}.csv` (e.g., `15min_202604141645_202605141630.csv`).
- Columns: `datetime`, `open`, `high`, `low`, `close` (prices as decimal numbers).
- Read the **most recent rows** from each available timeframe. Focus on at least the last 50–100 candles per file to capture recent structure while keeping context manageable.

### 2. Technical Analysis

Perform the following analyses on the data you read using mainly Dow Theory and Horizontal Support & Resistance.
- Refer to @theories/dow.md for the details of Dow Theory analysis
- Refer to @theories/horizontal_sr_level.md for the details of Support & Resistance analysis

#### Multi-Timeframe Confluence

- Cross-reference Dow Theory trend structure and S/R levels across all available timeframes (15min, 1h, 4h, 1day).
- A Dow-confirmed trend on a higher timeframe combined with an S/R bounce on a lower timeframe carries more weight than either signal alone.
- Note where S/R levels align with Dow Theory swing points — these are the highest-conviction zones.

### 3. Produce Proposals & Reasonings

For each of the following horizons, give a **conditional prediction**:

| Horizon | Description |
|---------|-------------|
| **15 min** | Very short-term — focus on the latest candle reaction at nearby S/R levels |
| **30 min** | Short-term — incorporate nearest S/R levels and minor trend structure |
| **1 h** | Intra-session — weigh Dow Theory trend structure and key S/R zones |
| **4 h** | Intra-day / swing — assess primary trend health and major S/R levels |

A proposal for each horizon should produce the followings as said in the goal section:

- Direction
- Aimed Pattern
- Entry Price
- Stop Loss
- Take Profit
- Confidence

Also, produce a summary of the proposal reasonings for each horizon. Such as:

- What **technical patterns** (in a single timeframe or multi-timeframe) are observed and why they are significant to back up the proposal
  - What indicators used to identify the patterns and how they were used
  - What technical theories were applied and how they were applied
- What potential psychological patterns or trends are observed and why they are significant to back up the proposal (if any)

## Generate Output

Create a new directory `preds/{input_dir_name}` if not exists, and save the analysis in a markdown file there. The filename should be `{YYYYMMDD_HH:MM}.md`.

Structure the response as follows:

```
## Analysis Overview {currency_pair} {YYYY-MM-DD HH:MM}

| Timeframe | Direction | Pattern | Entry | Stop Loss | Take Profit | Confidence |
|-----------|-----------|---------|-------|-----------|-------------|------------|
| 15m | {long/short} | {bounce/breakout} | {entry price} | {stop loss} | {take profit} | {confidence} |
| 1h | {long/short} | {bounce/breakout} | {entry price} | {stop loss} | {take profit} | {confidence} |
| 4h | {long/short} | {bounce/breakout} | {entry price} | {stop loss} | {take profit} | {confidence} |
| 1d | {long/short} | {bounce/breakout} | {entry price} | {stop loss} | {take profit} | {confidence} |

### Current Price Context
(latest price, today's range, recent trend summary)

### Dow Theory — Trend Structure
(trend direction, HH/HL or LH/LL sequence, trend phase, and health per timeframe)

### Horizontal Support & Resistance — Key Levels
(In table representation, identified S/R levels with touch count, role reversals, and reaction candles)

## Proposal & Reasonings

### 15-Minute
**Direction**: {direction}, **Pattern**: {pattern}, **Confidence**: {confidence}

| Field | Value |
|-------|-------|
| **Entry Price** | {entry price} |
| **Stop Loss** | {stop loss} |
| **Take Profit** | {take profit} |
| **Trigger** | {candle pattern and/or price action formation} |

**Reasoning**:
{proposal reasoning generated in step 3}


### 1-Hour
{Follow the same structure as 15-Minute}

### 4-Hour
{Follow the same structure as 15-Minute}

### 1-Day
{Follow the same structure as 15-Minute}

```

## Important Notes

- Always state the specific Dow Theory and S/R techniques by name so the user can verify independently.
- When support/resistance levels are cited, give the **exact price** derived from the data and the number of times the level has been tested.
- If data for a timeframe is missing, skip that timeframe's analysis and note it.
