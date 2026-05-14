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

Perform the following analyses on the data you read using **only** Dow Theory and Horizontal Support & Resistance. **Name every technique explicitly** in your output.

#### Dow Theory — Trend Structure

- **Identify the primary trend** by examining the sequence of swing highs and swing lows:
  - **Uptrend**: Higher highs (HH) and higher lows (HL)
  - **Downtrend**: Lower highs (LH) and lower lows (LL)
- **Assess trend health**:
  - *Intact* — price continues making HH + HL (or LH + LL)
  - *Weakening* — a new swing fails to exceed the prior one (e.g., a lower high in an uptrend is the first warning)
  - *Broken* — price violates the last significant swing low in an uptrend (or swing high in a downtrend)
- **Identify the trend phase** (accumulation / public participation / excess for bull; distribution / panic / capitulation for bear).
- **Volume confirmation** (if volume data is available) — volume should expand in the direction of the primary trend and contract on counter-trend moves. Rising price on falling volume is suspicious.

#### Horizontal Support & Resistance — Key Levels

- Identify key **support and resistance levels** from swing highs and lows across all available timeframes.
- Prioritize levels with:
  - **Multiple touches** — two or more rejections at the same price strengthen the level
  - **Clean reversals** — sharp bounces carry more weight than slow grinding turns
  - **Round numbers** — psychologically significant prices that attract orders
- Check for **role reversal (polarity)** — a broken support level that may now act as resistance, or vice versa.
- Look for **reaction candles** at key levels on the most recent candles (pin bar, engulfing, hammer, doji) that confirm the level is holding or breaking.

#### Multi-Timeframe Confluence

- Cross-reference Dow Theory trend structure and S/R levels across all available timeframes (15min, 1h, 4h, 1day).
- A Dow-confirmed trend on a higher timeframe combined with an S/R bounce on a lower timeframe carries more weight than either signal alone.
- Note where S/R levels align with Dow Theory swing points — these are the highest-conviction zones.

### 3. Produce Predictions

For each of the following horizons, give a **conditional prediction**:

| Horizon | Description |
|---------|-------------|
| **15 min** | Very short-term — focus on the latest candle reaction at nearby S/R levels |
| **30 min** | Short-term — incorporate nearest S/R levels and minor trend structure |
| **1 h** | Intra-session — weigh Dow Theory trend structure and key S/R zones |
| **4 h** | Intra-day / swing — assess primary trend health and major S/R levels |

Each prediction MUST follow this pattern:

> **{Horizon}:** If {specific condition, e.g., "the price breaks above the 147.20 resistance (tested 3 times)" or "the pullback holds above the 146.80 higher low"}, then {expected move, e.g., "expect a continued push toward 147.50 as the Dow Theory uptrend remains intact and the S/R role reversal at 147.20 provides new support"}.
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

### Dow Theory — Trend Structure
(trend direction, HH/HL or LH/LL sequence, trend phase, and health per timeframe)

### Horizontal Support & Resistance — Key Levels
(identified S/R levels with touch count, role reversals, and reaction candles)

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

- Always state the specific Dow Theory and S/R techniques by name so the user can verify independently.
- When support/resistance levels are cited, give the **exact price** derived from the data and the number of times the level has been tested.
- If data for a timeframe is missing, skip that timeframe's analysis and note it.
