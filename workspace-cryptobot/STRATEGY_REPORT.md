# Experimental Strategy Research Report
**Date:** March 11, 2026  
**Data:** BTC 1h (501 candles)  
**Initial Balance:** $10,000

---

## Top 3 Strategies Found

### #1: Ultimate Oscillator
- **Return:** 6.60%
- **Trades:** 7
- **Final Balance:** $10,660
- **Timeframe:** 1h
- **Parameters:** period1=7, period2=14, period3=28, oversold=30, overbought=70
- **Why it works:** Combines 3 different timeframes to reduce false signals. Only trades on strong momentum across all periods.

### #2: Williams %R
- **Return:** 5.98%
- **Trades:** 32
- **Final Balance:** $10,598
- **Timeframe:** 1h
- **Parameters:** period=14, oversold=-80, overbought=-20
- **Why it works:** Classic oversold/overbought reversal. Higher trade count provides more opportunities.

### #3: EMA Aggressive (50/100)
- **Return:** 5.91%
- **Trades:** 3
- **Final Balance:** $10,591
- **Timeframe:** 1h
- **Parameters:** fast=50, slow=100
- **Why it works:** Long-term trend following with very few false signals. Captures major trend changes.

---

## Additional Promising Strategies

| Rank | Strategy | Return | Trades | Notes |
|------|----------|--------|--------|-------|
| 4 | Bollinger (10, 1.5 std) | 5.83% | 31 | Tight bands = more signals |
| 5 | ADX Trend | 5.80% | 10 | Filters weak trends |
| 6 | RSI Divergence | 5.23% | 39 | Captures reversals |
| 7 | Volatility Squeeze | 5.63% | 18 | Pre-breakout detection |
| 8 | TRIX | 4.03% | 23 | Triple-smoothed momentum |
| 9 | KST | 4.01% | 21 | Know Sure Thing |
| 10 | EMA 8/21/55 | 3.72% | 11 | Triple EMA alignment |

---

## Methodology

- Tested 37+ strategy variations
- Timeframes: 1h (primary), simulated 10m/4h
- Indicator combinations: RSI, MACD, EMA, Bollinger, ADX, Stochastic, Williams %R, TRIX, KST, Aroon, MFI, Chaikin, Ultimate Oscillator
- Unusual parameters: Extreme oversold/overbought levels, long-period EMAs, divergence detection

---

## Files Saved
- `williams_%r_1h_1.json`
- `bollinger_1h_2.json`  
- `adx_trend_1h_3.json`
- `creative_ultimate_osc_1.json`
- `creative_ema_aggressive_2.json`
- `creative_rsi_divergence_3.json`

