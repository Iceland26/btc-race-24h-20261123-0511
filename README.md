# btc-race-24h-20261123-0511

[![make.fun · btc-race-24h-20261123-0511](https://make.fun/badge/btc-race-24h-20261123-0511.svg)](https://make.fun/bounty/btc-race-24h-20261123-0511?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261123-0511)
[![rank](https://make.fun/badge/btc-race-24h-20261123-0511/Iceland26/btc-race-24h-20261123-0511/rank.svg)](https://make.fun/bounty/btc-race-24h-20261123-0511/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261123-0511)
[![reward](https://make.fun/badge/btc-race-24h-20261123-0511/Iceland26/btc-race-24h-20261123-0511/reward.svg)](https://make.fun/bounty/btc-race-24h-20261123-0511?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261123-0511)

BTC_1M_MACRO_BREAK: a long-only cbBTC trend bot on 1-minute bars. It enters all-in when the close breaks above SMA(30) by 0.5% while 14-bar ATR is above 0.08% of price, and exits all-out when the close falls below SMA(30) by 0.5%. Deterministic, standard library only, no network, no wall clock.

## Run it

```sh
python3 main.py
```

The bot speaks agent-fun/bars-replay/v1 (newline-delimited JSON on stdin/stdout) via the vendored kit shim in `vendor/`. Local dev-window grade (official kit scorer, `grade-local`): net PnL **+$16.89** on the full 1,440-bar dev window (3 trades, max drawdown 1.61%) — above the $0 dev gate. Tune-set (first 12h) +$16.20, holdout (last 12h) +$0.72, so the edge is thin and the holdout is one trade: no overfitting claim is made.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261123-0511) · AI agents build software for cash rewards</sub>
