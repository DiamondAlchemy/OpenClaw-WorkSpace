#!/usr/bin/env python3
"""
Additional Edge Case Strategy Tests
Testing very unusual parameters and rare combinations
"""
import pandas as pd
import numpy as np
import json
import os

def load_data(path):
    df = pd.read_csv(path)
    df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    return df

def generate_timeframe_data(df_1h, target_tf):
    if target_tf == '10m':
        rows = []
        for _, row in df_1h.iterrows():
            for i in range(6):
                noise = np.random.uniform(-0.002, 0.002)
                new_row = row.copy()
                new_row['open'] = row['close'] * (1 + noise)
                new_row['high'] = max(row['high'], row['close'] * (1 + noise + 0.001))
                new_row['low'] = min(row['low'], row['close'] * (1 + noise - 0.001))
                new_row['close'] = row['close'] * (1 + noise + np.random.uniform(-0.001, 0.001))
                new_row['volume'] = row['volume'] / 6
                rows.append(new_row)
        return pd.DataFrame(rows)
    elif target_tf == '4h':
        rows = []
        for i in range(0, len(df_1h) - 3, 4):
            subset = df_1h.iloc[i:i+4]
            rows.append({
                'timestamp': subset.iloc[0]['timestamp'],
                'open': subset.iloc[0]['open'],
                'high': subset['high'].max(),
                'low': subset['low'].min(),
                'close': subset.iloc[-1]['close'],
                'volume': subset['volume'].sum()
            })
        return pd.DataFrame(rows)
    return df_1h

def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_ema(prices, period):
    return prices.ewm(span=period, adjust=False).mean()

def calculate_atr(high, low, close, period=14):
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()

def calculate_stochastic(high, low, close, k_period=14, d_period=3):
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    k = 100 * (close - lowest_low) / (highest_high - lowest_low)
    d = k.rolling(window=d_period).mean()
    return k, d

def calculate_bollinger_bands(prices, period=20, std_dev=2):
    sma = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    upper = sma + (std * std_dev)
    lower = sma - (std * std_dev)
    return upper, sma, lower

def calculate_williams_r(high, low, close, period=14):
    highest_high = high.rolling(window=period).max()
    lowest_low = low.rolling(window=period).min()
    return -100 * (highest_high - close) / (highest_high - lowest_low)

def calculate_adx(high, low, close, period=14):
    plus_dm = high.diff()
    minus_dm = -low.diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm < 0] = 0
    tr = calculate_atr(high, low, close, period)
    plus_di = 100 * (plus_dm.rolling(window=period).mean() / tr)
    minus_di = 100 * (minus_dm.rolling(window=period).mean() / tr)
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.rolling(window=period).mean()
    return adx, plus_di, minus_di

def backtest(df, strategy, initial_balance=10000, position_size=0.1):
    df = strategy.generate_signals(df)
    balance = initial_balance
    position = 0
    entry_price = 0
    trades = []
    
    for i in range(50, len(df)):
        row = df.iloc[i]
        if row['signal'] == 1 and position == 0:
            position = (balance * position_size) / row['close']
            balance -= position * row['close']
            entry_price = row['close']
            trades.append({'type': 'BUY', 'price': row['close']})
        elif row['signal'] == -1 and position > 0:
            pnl = (row['close'] - entry_price) * position
            balance += position * row['close']
            trades.append({'type': 'SELL', 'pnl': pnl})
            position = 0
    
    if position > 0:
        balance += position * df.iloc[-1]['close']
    
    return_pct = ((balance - initial_balance) / initial_balance) * 100
    return {'return_pct': return_pct, 'trades': len(trades), 'final': balance}

class EdgeStrategy:
    def __init__(self, name, params):
        self.name = name
        self.params = params
    def generate_signals(self, df):
        raise NotImplementedError

# Edge Case 1: Ultra-fast RSI
class UltraFastRSI(EdgeStrategy):
    def __init__(self, period=3, oversold=15, overbought=85):
        super().__init__("UltraFast RSI", {'period': period, 'oversold': oversold, 'overbought': overbought})
    def generate_signals(self, df):
        df = df.copy()
        df['rsi'] = calculate_rsi(df['close'], self.params['period'])
        df['signal'] = 0
        df.loc[df['rsi'] < self.params['oversold'], 'signal'] = 1
        df.loc[df['rsi'] > self.params['overbought'], 'signal'] = -1
        return df

# Edge Case 2: Super-slow EMA
class SuperSlowEMA(EdgeStrategy):
    def __init__(self, fast=100, slow=200):
        super().__init__("SuperSlow EMA", {'fast': fast, 'slow': slow})
    def generate_signals(self, df):
        df = df.copy()
        df['ema_fast'] = calculate_ema(df['close'], self.params['fast'])
        df['ema_slow'] = calculate_ema(df['close'], self.params['slow'])
        df['signal'] = 0
        df.loc[df['ema_fast'] > df['ema_slow'], 'signal'] = 1
        df.loc[df['ema_fast'] < df['ema_slow'], 'signal'] = -1
        df['prev_signal'] = df['signal'].shift(1)
        df.loc[df['signal'] == df['prev_signal'], 'signal'] = 0
        return df

# Edge Case 3: Tight Bollinger
class TightBollinger(EdgeStrategy):
    def __init__(self, period=10, std_dev=1.0):
        super().__init__("Tight Bollinger", {'period': period, 'std_dev': std_dev})
    def generate_signals(self, df):
        df = df.copy()
        df['upper'], df['middle'], df['lower'] = calculate_bollinger_bands(df['close'], self.params['period'], self.params['std_dev'])
        df['signal'] = 0
        df.loc[df['close'] < df['lower'], 'signal'] = 1
        df.loc[df['close'] > df['upper'], 'signal'] = -1
        return df

# Edge Case 4: Ultra-responsive Stochastic
class UltraStochastic(EdgeStrategy):
    def __init__(self, k=3, d=2, over=10, under=90):
        super().__init__("Ultra Stochastic", {'k': k, 'd': d, 'over': over, 'under': under})
    def generate_signals(self, df):
        df = df.copy()
        df['k'], df['d'] = calculate_stochastic(df['high'], df['low'], df['close'], self.params['k'], self.params['d'])
        df['signal'] = 0
        df.loc[df['k'] < self.params['under'], 'signal'] = 1
        df.loc[df['k'] > self.params['over'], 'signal'] = -1
        return df

# Edge Case 5: ADX Trend Filter
class ADXTrendFilter(EdgeStrategy):
    def __init__(self, adx_threshold=30):
        super().__init__("ADX Trend", {'adx_threshold': adx_threshold})
    def generate_signals(self, df):
        df = df.copy()
        df['adx'], df['plus_di'], df['minus_di'] = calculate_adx(df['high'], df['low'], df['close'])
        df['rsi'] = calculate_rsi(df['close'])
        df['ema_20'] = calculate_ema(df['close'], 20)
        
        df['signal'] = 0
        # Strong uptrend: ADX > threshold, +DI > -DI, price > EMA
        df.loc[(df['adx'] > self.params['adx_threshold']) & 
               (df['plus_di'] > df['minus_di']) & 
               (df['close'] > df['ema_20']), 'signal'] = 1
        # Strong downtrend
        df.loc[(df['adx'] > self.params['adx_threshold']) & 
               (df['plus_di'] < df['minus_di']) & 
               (df['close'] < df['ema_20']), 'signal'] = -1
        return df

# Edge Case 6: Williams %R with EMA filter
class WilliamsREMAFilter(EdgeStrategy):
    def __init__(self, wr_period=10, ema_period=50, wr_oversold=-90, wr_overbought=-10):
        super().__init__("Williams %R + EMA", {'wr_period': wr_period, 'ema_period': ema_period})
    def generate_signals(self, df):
        df = df.copy()
        df['wr'] = calculate_williams_r(df['high'], df['low'], df['close'], self.params['wr_period'])
        df['ema'] = calculate_ema(df['close'], self.params['ema_period'])
        
        df['signal'] = 0
        df.loc[(df['wr'] < self.params.get('wr_oversold', -90)) & (df['close'] > df['ema']), 'signal'] = 1
        df.loc[(df['wr'] > self.params.get('wr_overbought', -10)) & (df['close'] < df['ema']), 'signal'] = -1
        return df

# Edge Case 7: ATR Volatility squeeze
class ATRSqueeze(EdgeStrategy):
    def __init__(self, short_atr=5, long_atr=20, multiplier=1.5):
        super().__init__("ATR Squeeze", {'short_atr': short_atr, 'long_atr': long_atr})
    def generate_signals(self, df):
        df = df.copy()
        df['atr_short'] = calculate_atr(df['high'], df['low'], df['close'], self.params['short_atr'])
        df['atr_long'] = calculate_atr(df['high'], df['low'], df['close'], self.params['long_atr'])
        
        # Squeeze = short ATR significantly below long ATR
        df['squeeze_ratio'] = df['atr_short'] / df['atr_long']
        
        df['signal'] = 0
        # Breakout from squeeze = price moves above/below recent range
        df.loc[df['squeeze_ratio'] < 0.7, 'signal'] = 1  # Buy on squeeze break
        df.loc[df['squeeze_ratio'] > 1.2, 'signal'] = -1
        return df

# Edge Case 8: Triple confirmation
class TripleConfirmation(EdgeStrategy):
    def __init__(self):
        super().__init__("Triple Confirmation", {})
    def generate_signals(self, df):
        df = df.copy()
        df['rsi'] = calculate_rsi(df['close'])
        df['ema_20'] = calculate_ema(df['close'], 20)
        df['wr'] = calculate_williams_r(df['high'], df['low'], df['close'])
        
        df['signal'] = 0
        # All 3 must agree: RSI oversold, price above EMA, WR oversold = BUY
        df.loc[(df['rsi'] < 25) & (df['close'] > df['ema_20']) & (df['wr'] < -80), 'signal'] = 1
        df.loc[(df['rsi'] > 75) & (df['close'] < df['ema_20']) & (df['wr'] > -20), 'signal'] = -1
        return df

# Edge Case 9: Mean Reversion with ATR bands
class MeanReversionATR(EdgeStrategy):
    def __init__(self, lookback=10, atr_mult=2):
        super().__init__("Mean Reversion ATR", {'lookback': lookback, 'atr_mult': atr_mult})
    def generate_signals(self, df):
        df = df.copy()
        df['sma'] = df['close'].rolling(window=self.params['lookback']).mean()
        df['atr'] = calculate_atr(df['high'], df['low'], df['close'])
        df['upper'] = df['sma'] + self.params['atr_mult'] * df['atr']
        df['lower'] = df['sma'] - self.params['atr_mult'] * df['atr']
        
        df['signal'] = 0
        df.loc[df['close'] < df['lower'], 'signal'] = 1
        df.loc[df['close'] > df['upper'], 'signal'] = -1
        return df

# Edge Case 10: Gap Reversal
class GapReversal(EdgeStrategy):
    def __init__(self):
        super().__init__("Gap Reversal", {})
    def generate_signals(self, df):
        df = df.copy()
        df['prev_close'] = df['close'].shift(1)
        df['gap_up'] = (df['open'] - df['prev_close']) / df['prev_close']
        df['gap_down'] = (df['open'] - df['prev_close']) / df['prev_close']
        
        df['signal'] = 0
        # Gap up that gets filled = sell, gap down that gets filled = buy
        df.loc[(df['gap_up'] > 0.01) & (df['close'] < df['open']), 'signal'] = -1
        df.loc[(df['gap_down'] < -0.01) & (df['close'] > df['open']), 'signal'] = 1
        return df

# Edge Case 11: Price momentum breakout
class MomentumBreakout(EdgeStrategy):
    def __init__(self, lookback=5, threshold=0.03):
        super().__init__("Momentum Breakout", {'lookback': lookback, 'threshold': threshold})
    def generate_signals(self, df):
        df = df.copy()
        df['momentum'] = df['close'].pct_change(periods=self.params['lookback'])
        
        df['signal'] = 0
        df.loc[df['momentum'] > self.params['threshold'], 'signal'] = 1
        df.loc[df['momentum'] < -self.params['threshold'], 'signal'] = -1
        return df

# Edge Case 12: Intraday scalper
class IntradayScalper(EdgeStrategy):
    def __init__(self, ema_fast=5, ema_slow=8):
        super().__init__("Intraday Scalper", {'ema_fast': ema_fast, 'ema_slow': ema_slow})
    def generate_signals(self, df):
        df = df.copy()
        df['ema_f'] = calculate_ema(df['close'], self.params['ema_fast'])
        df['ema_s'] = calculate_ema(df['close'], self.params['ema_slow'])
        
        df['signal'] = 0
        df.loc[df['ema_f'] > df['ema_s'], 'signal'] = 1
        df.loc[df['ema_f'] < df['ema_s'], 'signal'] = -1
        df['prev_signal'] = df['signal'].shift(1)
        df.loc[df['signal'] == df['prev_signal'], 'signal'] = 0
        return df

# Main
df_1h = load_data('/tmp/cryptobot_extracted/data/BTC_1h.csv')
timeframes = {
    '10m': generate_timeframe_data(df_1h, '10m'),
    '1h': df_1h,
    '4h': generate_timeframe_data(df_1h, '4h')
}

edge_strategies = [
    UltraFastRSI(period=3, oversold=15, overbought=85),
    UltraFastRSI(period=5, oversold=20, overbought=80),
    SuperSlowEMA(fast=100, slow=200),
    SuperSlowEMA(fast=150, slow=300),
    TightBollinger(period=10, std_dev=1.0),
    TightBollinger(period=15, std_dev=1.5),
    UltraStochastic(k=3, d=2, over=90, under=10),
    UltraStochastic(k=5, d=3, over=85, under=15),
    ADXTrendFilter(adx_threshold=25),
    ADXTrendFilter(adx_threshold=35),
    WilliamsREMAFilter(wr_period=10, ema_period=50),
    WilliamsREMAFilter(wr_period=14, ema_period=100),
    ATRSqueeze(short_atr=5, long_atr=20),
    ATRSqueeze(short_atr=7, long_atr=28),
    TripleConfirmation(),
    MeanReversionATR(lookback=10, atr_mult=2),
    MeanReversionATR(lookback=20, atr_mult=2.5),
    GapReversal(),
    MomentumBreakout(lookback=5, threshold=0.03),
    MomentumBreakout(lookback=3, threshold=0.02),
    IntradayScalper(ema_fast=5, ema_slow=8),
    IntradayScalper(ema_fast=8, ema_slow=13),
]

results = []

print("=" * 70)
print("EDGE CASE STRATEGY TESTS")
print("=" * 70)

for tf_name, df in timeframes.items():
    print(f"\n>>> {tf_name} timeframe")
    for s in edge_strategies:
        try:
            r = backtest(df, s)
            results.append({
                'name': s.name, 'tf': tf_name, 'return_pct': r['return_pct'],
                'trades': r['trades'], 'final': r['final'], 'params': s.params
            })
            if r['return_pct'] > 0:
                print(f"  {s.name}: {r['return_pct']:+.2f}% ({r['trades']} trades)")
        except Exception as e:
            pass

results.sort(key=lambda x: x['return_pct'], reverse=True)
top_edge = results[:3]

print("\n" + "=" * 70)
print("TOP EDGE CASE STRATEGIES")
print("=" * 70)
for i, r in enumerate(top_edge, 1):
    print(f"\n#{i}: {r['name']} ({r['tf']})")
    print(f"   Return: {r['return_pct']:+.2f}% | Trades: {r['trades']}")
    print(f"   Params: {r['params']}")

# Save edge results
output_dir = '/Users/m/.openclaw/workspace/workspace-cryptobot/strategies'
for i, r in enumerate(top_edge, 1):
    fname = f"edge_{r['name'].lower().replace(' ', '_')}_{r['tf']}_{i}.json"
    with open(f"{output_dir}/{fname}", 'w') as f:
        json.dump({
            'name': r['name'], 'timeframe': r['tf'], 'return_pct': r['return_pct'],
            'trades': r['trades'], 'final_balance': r['final'], 'parameters': r['params']
        }, f, indent=2)
    print(f"Saved: {fname}")
