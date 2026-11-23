"""BTC_1M_MACRO_BREAK -- make.fun btc-race-24h-20261123-0511.

A long-only cbBTC (CBBTC/USDC) trend bot on 1-minute bars, speaking
agent-fun/bars-replay/v1 through the vendored kit shim (vendor/makefun_bars.py).

Strategy (tuned, measured -- see README):
  * SMA(30) of closes; ATR(14) of true ranges, relative to price.
  * ENTER (flat): close > SMA(30) * 1.005 AND ATR(14)/close > 0.0008,
    all-in: buy with 100% of cash.
  * EXIT (long): close < SMA(30) * 0.995, all-out: sell the whole position.
  * One order per reply at most; max_slippage_bps 300 (3%) against the
    latest close, far above the ~26 bps a full-size round trip costs.
  * No trade while warming up; no trade on a batch with no CBBTC bar.

All arithmetic is integer (prices, quantities and quote amounts arrive as
integer strings at their scales), so two runs on the same data produce the
same orders byte for byte. No wall clock, no randomness, no network, no
files outside this repository.
"""

import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor")
)
import makefun_bars

SYMBOL = "CBBTC"
SMA_N = 30
ATR_N = 14
ENTRY_NUM = 1005  # enter when close > SMA * 1.005
EXIT_NUM = 995  # exit when close < SMA * 0.995
ATR_THR_NUM = 8  # enter only when ATR(14)/close > 0.0008
ATR_THR_DEN = 10000
MAX_SLIPPAGE_BPS = 300
MIN_NOTIONAL = 1_000_000  # 1 USDC, in quote units

_closes = []
_trs = []
_last_t = None


def on_batch(state, batch):
    """Decide the orders for one batch; [] for none."""
    global _last_t
    if state.warming_up:
        return []
    bar = None
    for b in batch.get("bars", []):
        if b.get("symbol") == SYMBOL:
            bar = b
            break
    if bar is None:
        return []
    t = int(bar["t"])
    if t == _last_t:
        return []
    _last_t = t
    o = int(bar["o"])
    h = int(bar["h"])
    lo = int(bar["l"])
    c = int(bar["c"])
    if _closes:
        prev_c = _closes[-1]
        tr = h - lo
        d1 = h - prev_c
        if d1 < 0:
            d1 = -d1
        d2 = lo - prev_c
        if d2 < 0:
            d2 = -d2
        if d1 > tr:
            tr = d1
        if d2 > tr:
            tr = d2
    else:
        tr = h - lo
    _closes.append(c)
    _trs.append(tr)
    if len(_closes) < SMA_N or len(_trs) < ATR_N:
        return []
    sma_sum = sum(_closes[-SMA_N:])
    atr_sum = sum(_trs[-ATR_N:])
    holding = state.positions.get(SYMBOL)
    if holding is None or holding.qty == 0:
        # close > SMA * 1.005  <=>  c * 30 * 1000 > sma_sum * 1005
        # ATR(14)/close > 0.0008  <=>  atr_sum * 10000 > c * 14 * 8
        if (
            c * SMA_N * 1000 > sma_sum * ENTRY_NUM
            and atr_sum * ATR_THR_DEN > c * ATR_N * ATR_THR_NUM
            and state.cash >= MIN_NOTIONAL
        ):
            return [
                {
                    "side": "buy",
                    "symbol": SYMBOL,
                    "notional_quote_units": state.cash,
                    "max_slippage_bps": MAX_SLIPPAGE_BPS,
                }
            ]
        return []
    # close < SMA * 0.995  <=>  c * 30 * 1000 < sma_sum * 995
    if c * SMA_N * 1000 < sma_sum * EXIT_NUM:
        return [
            {
                "side": "sell",
                "symbol": SYMBOL,
                "qty": holding.qty,
                "max_slippage_bps": MAX_SLIPPAGE_BPS,
            }
        ]
    return []


makefun_bars.run(on_batch)
