#!/usr/bin/env python3
"""
Experimental Strategy Research - Creative Indicator Testing
Tests unusual parameters, multi-indicator combos, and edge cases
"""
import pandas as pd
import numpy as np
import json
import os

# ===== LOAD DATA =====
def load_data(path):
    df = pd.read_csv(path)
    df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    return df

# Generate simulated 10m and 4h data
def generate_timeframe_data(df_1h, target_tf):
    """Generate simulated data for different timeframes"""
    df = df_1h.copy()
    
    if target_tf == '10m':
        # Upsample: each 1h = 6 x 10m candles (add noise)
        rows = []
        for _, row in df.iterrows():
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
        # Downsample: every 4 candles = 1 x 4h
        rows = []
        for i in range(0, len(df) - 3, 4):
            subset = df.iloc[i:i+4]
            rows.append({
                'timestamp': subset.iloc[0]['timestamp'],
                'open': subset.iloc[0]['open'],
                'high': subset['high'].max(),
                'low': subset['low'].min(),
                'close': subset.iloc[-1]['close'],
                'volume': subset['volume'].sum()
            })
        return pd.DataFrame(rows)
    
    return df

# ===== INDICATORS =====

def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_ema(prices, period):
    return prices.ewm(span=period, adjust=False).mean()

def calculate_sma(prices, period):
    return prices.rolling(window=period).mean()

def calculate_atr(high, low, close, period=14):
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()

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

def calculate_stochastic(high, low, close, k_period=14, d_period=3):
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    k = 100 * (close - lowest_low) / (highest_high - lowest_low)
    d = k.rolling(window=d_period).mean()
    return k, d

def calculate_bollinger_bands(prices, period=20, std_dev=2):
    sma = calculate_sma(prices, period)
    std = prices.rolling(window=period).std()
    upper = sma + (std * std_dev)
    lower = sma - (std * std_dev)
    return upper, sma, lower

def calculate_williams_r(high, low, close, period=14):
    highest_high = high.rolling(window=period).max()
    lowest_low = low.rolling(window=period).min()
    return -100 * (highest_high - close) / (highest_high - lowest_low)

def calculate_momentum(prices, period=10):
    return prices - prices.shift(period)

def calculate_roc(prices, period=12):
    return 100 * (prices - prices.shift(period)) / prices.shift(period)

def calculate_trix(prices, period=15):
    ema1 = calculate_ema(prices, period)
    ema2 = calculate_ema(ema1, period)
    ema3 = calculate_ema(ema2, period)
    return ema3.pct_change() * 100

def calculate_donchian(high, low, period=20):
    upper = high.rolling(window=period).max()
    lower = low.rolling(window=period).min()
    middle = (upper + lower) / 2
    return upper, middle, lower

def calculate_keltner(high, low, close, ema_period=20, atr_period=10, multiplier=2):
    ema = calculate_ema(close, ema_period)
    atr = calculate_atr(high, low, close, atr_period)
    upper = ema + multiplier * atr
    lower = ema - multiplier * atr
    return upper, ema, lower

# ===== EXPERIMENTAL STRATEGIES =====

class ExperimentalStrategy:
    def __init__(self, name, params):
        self.name = name
        self.params = params
        
    def generate_signals(self, df):
        raise NotImplementedError

# Creative Strategy 1: ATR Volatility Breakout
class ATRBreakoutStrategy(ExperimentalStrategy):
    def __init__(self, atr_period=14, multiplier=2.5):
        super().__init__("ATR Breakout", {'atr_period': atr_period, 'multiplier': multiplier})
        
    def generate_signals(self, df):
        df = df.copy()
        df['atr'] = calculate_atr(df['high'], df['low'], df['close'], self.params['atr_period'])
        df['upper'] = df['close'] + (self.params['multiplier'] * df['atr'])
        df['lower'] = df['close'] - (self.params['multiplier'] * df['atr'])
        
        df['signal'] = 0
        df.loc[df['close'] > df['upper'].shift(1), 'signal'] = 1
        df.loc[df['close'] < df['lower'].shift(1), 'signal'] = -1
        return df

# Creative Strategy 2: RSI Extreme Reversal
class RSIXtremeStrategy(ExperimentalStrategy):
    def __init__(self, oversold=20, overbought=80, confirm_ema=50):
        super().__init__("RSI Extreme", {'oversold': oversold, 'overbought': overbought, 'confirm_ema': confirm_ema})
        
    def generate_signals(self, df):
        df = df.copy()
        df['rsi'] = calculate_rsi(df['close'])
        df['ema'] = calculate_ema(df['close'], self.params['confirm_ema'])
        
        df['signal'] = 0
        # Buy when RSI extreme oversold AND price above EMA (trend confirmation)
        df.loc[(df['rsi'] < self.params['oversold']) & (df['close'] > df['ema']), 'signal'] = 1
        # Sell when RSI extreme overbought AND price below EMA
        df.loc[(df['rsi'] > self.params['overbought']) & (df['close'] < df['ema']), 'signal'] = -1
        return df

# Creative Strategy 3: EMA Ribbon Trend
class EMARibbonStrategy(ExperimentalStrategy):
    def __init__(self, periods=[8, 21, 55, 100]):
        super().__init__("EMA Ribbon", {'periods': periods})
        
    def generate_signals(self, df):
        df = df.copy()
        ema_cols = []
        for p in self.params['periods']:
            col = f'ema_{p}'
            df[col] = calculate_ema(df['close'], p)
            ema_cols.append(col)
        
        # All EMAs aligned = strong trend
        df['all_above'] = (df[ema_cols[0]] > df[ema_cols[1]]) & (df[ema_cols[1]] > df[ema_cols[2]])
        df['all_below'] = (df[ema_cols[0]] < df[ema_cols[1]]) & (df[ema_cols[1]] < df[ema_cols[2]])
        
        df['signal'] = 0
        df.loc[df['all_above'], 'signal'] = 1
        df.loc[df['all_below'], 'signal'] = -1
        return df

# Creative Strategy 4: Stochastic Momentum
class StochasticMomentumStrategy(ExperimentalStrategy):
    def __init__(self, k_period=5, d_period=3, oversold=15, overbought=85):
        super().__init__("Stochastic Momentum", {'k_period': k_period, 'd_period': d_period, 'oversold': oversold, 'overbought': overbought})
        
    def generate_signals(self, df):
        df = df.copy()
        df['k'], df['d'] = calculate_stochastic(df['high'], df['low'], df['close'], self.params['k_period'], self.params['d_period'])
        
        df['signal'] = 0
        df.loc[(df['k'] < self.params['oversold']) & (df['k'] > df['d']), 'signal'] = 1
        df.loc[(df['k'] > self.params['overbought']) & (df['k'] < df['d']), 'signal'] = -1
        return df

# Creative Strategy 5: Williams %R Extreme
class WilliamsRExtremeStrategy(ExperimentalStrategy):
    def __init__(self, period=20, oversold=-90, overbought=-10):
        super().__init__("Williams %R Extreme", {'period': period, 'oversold': oversold, 'overbought': overbought})
        
    def generate_signals(self, df):
        df = df.copy()
        df['wr'] = calculate_williams_r(df['high'], df['low'], df['close'], self.params['period'])
        
        df['signal'] = 0
        df.loc[df['wr'] < self.params['oversold'], 'signal'] = 1
        df.loc[df['wr'] > self.params['overbought'], 'signal'] = -1
        return df

# Creative Strategy 6: Donchian Breakout
class DonchianStrategy(ExperimentalStrategy):
    def __init__(self, period=20, breakout_pct=0.01):
        super().__init__("Donchian Breakout", {'period': period, 'breakout_pct': breakout_pct})
        
    def generate_signals(self, df):
        df = df.copy()
        df['upper'], df['middle'], df['lower'] = calculate_donchian(df['high'], df['low'], self.params['period'])
        
        df['signal'] = 0
        # Breakout above upper band
        df.loc[df['close'] > df['upper'] * (1 + self.params['breakout_pct']), 'signal'] = 1
        # Breakdown below lower band
        df.loc[df['close'] < df['lower'] * (1 - self.params['breakout_pct']), 'signal'] = -1
        return df

# Creative Strategy 7: Keltner Channel Trend
class KeltnerStrategy(ExperimentalStrategy):
    def __init__(self, ema_period=20, atr_period=10, multiplier=1.5):
        super().__init__("Keltner Trend", {'ema_period': ema_period, 'atr_period': atr_period, 'multiplier': multiplier})
        
    def generate_signals(self, df):
        df = df.copy()
        df['upper'], df['ema'], df['lower'] = calculate_keltner(df['high'], df['low'], df['close'], 
                                                                  self.params['ema_period'], self.params['atr_period'],
                                                                  self.params['multiplier'])
        
        df['signal'] = 0
        df.loc[df['close'] > df['upper'], 'signal'] = 1
        df.loc[df['close'] < df['lower'], 'signal'] = -1
        return df

# Creative Strategy 8: Momentum Divergence
class MomentumDivergenceStrategy(ExperimentalStrategy):
    def __init__(self, roc_period=12, threshold=5):
        super().__init__("Momentum Divergence", {'roc_period': roc_period, 'threshold': threshold})
        
    def generate_signals(self, df):
        df = df.copy()
        df['momentum'] = calculate_momentum(df['close'], self.params['roc_period'])
        df['roc'] = calculate_roc(df['close'], self.params['roc_period'])
        
        df['signal'] = 0
        # Strong positive momentum = buy
        df.loc[df['roc'] > self.params['threshold'], 'signal'] = 1
        # Strong negative momentum = sell
        df.loc[df['roc'] < -self.params['threshold'], 'signal'] = -1
        return df

# Creative Strategy 9: TRIX Reversal
class TRIXStrategy(ExperimentalStrategy):
    def __init__(self, period=15, signal=9):
        super().__init__("TRIX", {'period': period})
        
    def generate_signals(self, df):
        df = df.copy()
        df['trix'] = calculate_trix(df['close'], self.params['period'])
        
        df['signal'] = 0
        df.loc[df['trix'] > 0.1, 'signal'] = 1
        df.loc[df['trix'] < -0.1, 'signal'] = -1
        return df

# Creative Strategy 10: Dual RSI Confirmation
class DualRSIStrategy(ExperimentalStrategy):
    def __init__(self, fast_period=7, slow_period=21, oversold=30, overbought=70):
        super().__init__("Dual RSI", {'fast_period': fast_period, 'slow_period': slow_period, 'oversold': oversold, 'overbought': overbought})
        
    def generate_signals(self, df):
        df = df.copy()
        df['rsi_fast'] = calculate_rsi(df['close'], self.params['fast_period'])
        df['rsi_slow'] = calculate_rsi(df['close'], self.params['slow_period'])
        
        df['signal'] = 0
        # Both oversold = buy signal
        df.loc[(df['rsi_fast'] < self.params['oversold']) & (df['rsi_slow'] < self.params['oversold']), 'signal'] = 1
        # Both overbought = sell signal
        df.loc[(df['rsi_fast'] > self.params['overbought']) & (df['rsi_slow'] > self.params['overbought']), 'signal'] = -1
        return df

# Creative Strategy 11: ATR Trailing Stop
class ATRTrailingStopStrategy(ExperimentalStrategy):
    def __init__(self, atr_period=14, multiplier=3):
        super().__init__("ATR Trailing Stop", {'atr_period': atr_period, 'multiplier': multiplier})
        
    def generate_signals(self, df):
        df = df.copy()
        df['atr'] = calculate_atr(df['high'], df['low'], df['close'], self.params['atr_period'])
        
        # Simple trailing stop logic
        df['stop_level'] = df['close'] - (self.params['multiplier'] * df['atr'])
        
        df['signal'] = 0
        df.loc[df['close'] > df['stop_level'].shift(1), 'signal'] = 1
        df.loc[df['close'] < df['stop_level'].shift(1), 'signal'] = -1
        return df

# Creative Strategy 12: Volume-Price Trend
class VPTPriceStrategy(ExperimentalStrategy):
    def __init__(self, ma_period=20):
        super().__init__("VPT Price", {'ma_period': ma_period})
        
    def generate_signals(self, df):
        df = df.copy()
        # Volume Price Trend
        df['price_change'] = df['close'].pct_change()
        df['vpt'] = (df['price_change'] * df['volume']).rolling(window=20).sum()
        df['vpt_ma'] = df['vpt'].rolling(window=self.params['ma_period']).mean()
        
        df['signal'] = 0
        df.loc[df['vpt'] > df['vpt_ma'], 'signal'] = 1
        df.loc[df['vpt'] < df['vpt_ma'], 'signal'] = -1
        return df

# ===== BACKTESTER =====

def backtest(df, strategy, initial_balance=10000, position_size=0.1):
    df = strategy.generate_signals(df)
    
    balance = initial_balance
    position = 0
    entry_price = 0
    trades = []
    
    for i in range(50, len(df)):  # Skip first 50 for warmup
        row = df.iloc[i]
        prev_row = df.iloc[i-1]
        
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
    
    return {
        'initial': initial_balance,
        'final': balance,
        'return_pct': return_pct,
        'trades': len(trades)
    }

# ===== MAIN =====
def main():
    # Load data
    df_1h = load_data('/tmp/cryptobot_extracted/data/BTC_1h.csv')
    
    # Generate different timeframes
    timeframes = {
        '10m': generate_timeframe_data(df_1h, '10m'),
        '1h': df_1h,
        '4h': generate_timeframe_data(df_1h, '4h')
    }
    
    # Define experimental strategies
    strategies = [
        # ATR Strategies
        ATRBreakoutStrategy(atr_period=14, multiplier=2.5),
        ATRBreakoutStrategy(atr_period=7, multiplier=2.0),
        ATRTrailingStopStrategy(atr_period=14, multiplier=3),
        
        # RSI Strategies
        RSIXtremeStrategy(oversold=20, overbought=80, confirm_ema=50),
        RSIXtremeStrategy(oversold=15, overbought=85, confirm_ema=100),
        DualRSIStrategy(fast_period=7, slow_period=21),
        DualRSIStrategy(fast_period=5, slow_period=14),
        
        # EMA Strategies
        EMARibbonStrategy(periods=[8, 21, 55, 100]),
        EMARibbonStrategy(periods=[5, 15, 50, 200]),
        
        # Stochastic Strategies
        StochasticMomentumStrategy(k_period=5, d_period=3, oversold=15, overbought=85),
        StochasticMomentumStrategy(k_period=10, d_period=5, oversold=20, overbought=80),
        
        # Williams %R
        WilliamsRExtremeStrategy(period=20, oversold=-90, overbought=-10),
        WilliamsRExtremeStrategy(period=10, oversold=-85, overbought=-15),
        
        # Channel Strategies
        DonchianStrategy(period=20, breakout_pct=0.01),
        DonchianStrategy(period=10, breakout_pct=0.02),
        KeltnerStrategy(ema_period=20, atr_period=10, multiplier=1.5),
        KeltnerStrategy(ema_period=50, atr_period=20, multiplier=2.0),
        
        # Momentum Strategies
        MomentumDivergenceStrategy(roc_period=12, threshold=5),
        MomentumDivergenceStrategy(roc_period=20, threshold=3),
        
        # TRIX
        TRIXStrategy(period=15),
        TRIXStrategy(period=10),
        
        # VPT
        VPTPriceStrategy(ma_period=20),
    ]
    
    results = []
    
    print("=" * 70)
    print("EXPERIMENTAL STRATEGY RESEARCH - CREATIVE TESTING")
    print("=" * 70)
    
    for tf_name, df in timeframes.items():
        print(f"\n>>> Testing {tf_name} timeframe ({len(df)} candles)")
        
        for strategy in strategies:
            try:
                result = backtest(df, strategy)
                result_dict = {
                    'name': strategy.name,
                    'timeframe': tf_name,
                    'return_pct': result['return_pct'],
                    'trades': result['trades'],
                    'final': result['final'],
                    'params': strategy.params
                }
                results.append(result_dict)
                
                print(f"  {strategy.name}: {result['return_pct']:+.2f}% ({result['trades']} trades)")
            except Exception as e:
                print(f"  ERROR {strategy.name}: {e}")
    
    # Sort by return
    results.sort(key=lambda x: x['return_pct'], reverse=True)
    
    # Get top 3
    top_3 = results[:3]
    
    print("\n" + "=" * 70)
    print("TOP 3 STRATEGIES FOUND")
    print("=" * 70)
    
    for i, r in enumerate(top_3, 1):
        print(f"\n#{i}: {r['name']} ({r['timeframe']})")
        print(f"   Return: {r['return_pct']:+.2f}%")
        print(f"   Trades: {r['trades']}")
        print(f"   Final Balance: ${r['final']:.2f}")
        print(f"   Parameters: {r['params']}")
    
    # Save results
    output_dir = '/Users/m/.openclaw/workspace/workspace-cryptobot/strategies'
    os.makedirs(output_dir, exist_ok=True)
    
    for i, r in enumerate(top_3, 1):
        filename = f"experimental_{r['name'].lower().replace(' ', '_')}_{r['timeframe']}_{i}.json"
        filepath = os.path.join(output_dir, filename)
        
        save_data = {
            'name': r['name'],
            'timeframe': r['timeframe'],
            'return_pct': r['return_pct'],
            'trades': r['trades'],
            'final_balance': r['final'],
            'parameters': r['params'],
            'description': f"Experimental strategy - top {i} performer"
        }
        
        with open(filepath, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        print(f"\nSaved: {filepath}")
    
    return top_3

if __name__ == '__main__':
    main()
