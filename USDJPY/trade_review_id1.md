# USDJPY Trade Review — ID 1

**Date reviewed:** 2026-05-20

---

## Trade Summary

| Field | Value |
|-------|-------|
| ID | 1 |
| Type | Limit |
| Side | Buy |
| Entry Price | 159.139 |
| Take Profit | 159.356 |
| Stop Loss | 159.027 |
| Entered (JST) | 2026/5/19 18:21:29 |
| Closed (JST) | 2026/05/19 21:41:14 |
| Result | Lost |
| Profit | -0.112 |

---

## Reason I Entered (from sheet)

> I drew a resistance zone ranging 159.036 ~ 159.075 because the price got rejected twice or more between May 18th 12:45 and May 19th 15:30. Then, the price went higher than the resistance zone and got pushed back to the zone again. Later, the price looked bounced at the zone, so I understood it as the role reversal happened and the zone became a support.

## Self-Reflection (from sheet)

> The price breakout was false positive actually. The chart later on shows the price went below the zone again, and then the zone worked as a resistance back again. I should've had a proper confirmation to make sure if the price breakout was false positive or real.

---

## Verification Against Price Data

### Zone Identification (159.036 ~ 159.075) — Correct

Confirmed rejections from the zone:

| Time (JST) | High | Close | Verdict |
|------------|------|-------|---------|
| May 18 13:00 | 159.068 | 159.022 | Rejection (wick into zone, closed below) |
| May 19 15:00 | 159.049 | 159.014 | Rejection (wick into zone, closed below) |
| May 19 15:15 | 159.048 | 159.035 | Rejection (wick into zone, closed below) |

### Breakout and Pullback — Correct

- **15:45** — Price broke above 159.075 (high 159.103)
- **16:00** — High 159.148, clearly above zone
- **16:30–16:45** — Price pulled back to ~159.055 (back into the zone)
- **17:00–17:45** — Bounced back up from 159.05 to 159.139

### False Breakout Observation — Correct

- The breakout lasted only ~1 hour before price returned to the zone
- At 21:30, price crashed to 158.825 — well below the zone
- Stop loss at 159.027 was triggered during this move
- Loss: 159.139 - 159.027 = 0.112 (matches the sheet)

### "Zone Worked as Resistance Again" — Partially Correct

- After the crash, price oscillated around the zone (159.04–159.24) rather than being cleanly rejected by it
- More accurate to say the zone became a "pivot/midpoint" rather than strict resistance
- Slight oversimplification, but the core observation is valid

---

## What I Should Have Done — Step-by-Step Checklist

### Step 1: Identify the Zone
- Draw a resistance zone where price got rejected 2+ times
- Zone: 159.036 ~ 159.075 — validated by multiple rejections

### Step 2: Wait for a Convincing Breakout Above the Zone
- Don't just see price "poke above" the zone briefly
- Confirm with a **full 1H candle CLOSE** above the zone (159.075)
- The price should be **15-20+ pips above zone top** at the close
- If price returns INTO the zone within 1 hour of breaking out, treat breakout as suspect

### Step 3: Wait for the Pullback to the Zone
- After breakout, wait for price to come back down to the zone (now expected support)

### Step 4: Check Pullback Volume (Tick Volume on TradingView)
- During the pullback, volume should be **decreasing** (weak selling = healthy retrace)
- If volume is high during pullback, sellers are aggressive — zone may not hold

### Step 5: Wait for a Bullish Reversal Candlestick Pattern at the Zone

Reference: [Dukascopy — Reversal Candlestick Patterns](https://www.dukascopy.com/swiss/english/marketwatch/articles/reversal-candlestick-patterns/)

| Pattern | What to Look For |
|---------|-----------------|
| **Hammer** | Small body at top, lower wick >= 3x body length, showing buyers stepping in at the zone |
| **Bullish Engulfing** | A large bullish candle completely swallowing the prior bearish candle's body |
| **Morning Star** | 3-candle: bearish -> small/doji -> strong bullish close into the first candle |
| **Piercing Line** | Bearish candle, then bullish candle opening below and closing above 60%+ of prior body |

### Step 6: Confirm Reversal Candle Volume
- The reversal candle should have **>= 1.5x the 20-candle average volume**
- This confirms buyers are stepping in with conviction

### Step 7: Enter the Trade
- Place Buy order after the reversal pattern completes
- SL below the zone bottom (below 159.036)
- TP at next resistance / favorable R:R ratio

---

## Summary: What Was Missing in My Entry

```
1. [done]    Identify resistance zone (2+ rejections)
2. [done]    Wait for breakout above the zone
3. [MISSED]  Confirm breakout: full 1H candle CLOSE above zone + 15-20 pips distance
4. [done]    Wait for pullback to the zone
5. [MISSED]  Check: pullback volume is LOW (weak selling)
6. [MISSED]  Wait for a bullish reversal pattern (Hammer/Engulfing/Morning Star)
7. [MISSED]  Confirm: reversal candle volume is HIGH (>= 1.5x recent average)
```

---

## Breakout Confirmation Guidelines (15min Timeframe)

**Minimum confirmation:**
- 1H candle CLOSE above the zone (not just wicks)
- AND price is >= 15-20 pips above zone top at that close

**Stronger confirmation:**
- 4H candle CLOSE above the zone
- This filters out most false breakouts

**Quick rejection rule:**
- If price returns INTO the zone within 1 hour of breaking out, treat the breakout as suspect — do NOT enter on the first bounce

**In this trade:** By 16:45 (just 45 minutes after breakout), price was already back inside the zone at 159.055. That rapid return was a red flag.

---

## TradingView: How to See Tick Volume

- **Indicator name:** "Volume" (built-in)
- For forex pairs, TradingView automatically shows tick volume
- Enable "Volume MA" in settings (20-period) to see the average line
- Green bars = bullish close; Red bars = bearish close
- A "volume spike" = bar >= 1.5x taller than surrounding bars

**How to read for this trade setup:**
1. Pullback candles should have LOW volume (below MA line)
2. Reversal candle should have HIGH volume (above MA line, ideally 1.5x+)
3. If bounce happens on average/below-average volume = likely dead-cat bounce

---

## Key Lesson

> The breakout was above the zone for only ~1 hour (15:45-16:45) before returning. A conservative approach requires: (1) higher timeframe close confirmation, (2) a clear bullish reversal pattern at the support zone, and (3) volume spike on the reversal candle. Entering on "assumption of support" without these confirmations led to a false breakout trap.
