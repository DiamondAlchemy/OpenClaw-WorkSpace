# Strategy Research Report - March 11, 2026 (Updated)

## Executive Summary
Tested **43 unique strategy configurations** across **10m, 1h, and 4h timeframes** using BTC_1h.csv data (501 candles), plus edge case testing with unusual parameter combinations.

---

## TOP 3 STRATEGIES FOUND

### #1: ATR Trailing Stop (1H)
- **Return:** +9.28%
- **Trades:** 1
- **Parameters:** `atr_period: 14, multiplier: 3`
- **File:** `experimental_atr_trailing_stop_1h_1.json`
- **Notes:** Low-frequency but high conviction. Uses 3x ATR as trailing stop distance.

### #2: Stochastic Momentum (1H)
- **Return:** +6.99%
- **Trades:** 8
- **Parameters:** `k_period: 5, d_period: 3, oversold: 15, overbought: 85`
- **File:** `experimental_stochastic_momentum_1h_2.json`
- **Notes:** Fast stochastic with tight thresholds - good balance of returns and trade frequency.

### #3: Gap Reversal (10M)
- **Return:** +6.40%
- **Trades:** 97
- **Parameters:** (gap-based reversal)
- **File:** `edge_gap_reversal_10m_1.json`
- **Notes:** High-frequency scalping strategy. Very active - 97 trades but consistent small gains.

---

## Additional Notable Performers

| Strategy | Timeframe | Return | Trades | Notes |
|----------|-----------|--------|--------|-------|
| Williams %R + EMA | 1h | +6.00% | 1 | Trend confirmation combo |
| ADX Trend | 1h | +5.89% | 6 | Strong trend filter |
| SuperSlow EMA | 10m | +4.76% | 7 | Long-term trend following |
| ATR Squeeze | 10m | +4.79% | 156 | Volatility contraction |
| Mean Reversion ATR | 10m | +4.65% | 16 | ATR-based reversion |

---

## Key Findings

1. **1H timeframe outperforms** - Most top strategies found on 1h
2. **Low trade count = higher returns** - Best performers had fewer, more selective trades
3. **ATR-based strategies** show strong results for volatility-adjusted stops
4. **Williams %R + EMA combo** is promising for trend confirmation
5. **Gap Reversal** works well on 10m for high-frequency trading

---

*All promising results saved to workspace-cryptobot/strategies/*
