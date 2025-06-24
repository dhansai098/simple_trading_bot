# Binance Futures Trading Bot (Testnet)

This Python bot allows you to trade on Binance Futures Testnet using the official Binance API.

## Features
- Market and Limit orders
- Stop-Market order support (Bonus)
- Supports BUY and SELL
- CLI-based input validation
- Logging of all actions

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the bot:
```bash
python bot.py --api_key YOUR_KEY --api_secret YOUR_SECRET --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

3. For LIMIT order:
```bash
--type LIMIT --price 60000
```

4. For STOP_MARKET order:
```bash
--type STOP_MARKET --stop_price 61000

## Log File
Logs are stored in `trading_bot.log`.

## Testnet Info
Use: https://testnet.binancefuture.com
