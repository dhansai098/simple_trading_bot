import logging
import argparse
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException

# Configure logging
logging.basicConfig(filename='trading_bot.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        logging.info("Bot initialized with testnet=%s", testnet)

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        try:
            if order_type == 'MARKET':
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=SIDE_BUY if side == 'BUY' else SIDE_SELL,
                    type=ORDER_TYPE_MARKET,
                    quantity=quantity
                )
            elif order_type == 'LIMIT':
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=SIDE_BUY if side == 'BUY' else SIDE_SELL,
                    type=ORDER_TYPE_LIMIT,
                    timeInForce=TIME_IN_FORCE_GTC,
                    quantity=quantity,
                    price=price
                )
            elif order_type == 'STOP_MARKET':
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=SIDE_BUY if side == 'BUY' else SIDE_SELL,
                    type=ORDER_TYPE_STOP_MARKET,
                    stopPrice=stop_price,
                    quantity=quantity,
                    timeInForce=TIME_IN_FORCE_GTC
                )
            else:
                logging.error("Unsupported order type: %s", order_type)
                return None

            logging.info("Order placed: %s", order)
            print("Order placed successfully:", order)
            return order
        except BinanceAPIException as e:
            logging.error("Binance API error: %s", e)
            print("Binance API error:", e)
        except Exception as e:
            logging.error("General error: %s", e)
            print("Error occurred:", e)


def parse_args():
    parser = argparse.ArgumentParser(description='Simplified Binance Futures Trading Bot')
    parser.add_argument('--api_key', required=True, help='Your Binance API Key')
    parser.add_argument('--api_secret', required=True, help='Your Binance API Secret')
    parser.add_argument('--symbol', required=True, help='Trading pair symbol (e.g., BTCUSDT)')
    parser.add_argument('--side', required=True, choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('--type', required=True, choices=['MARKET', 'LIMIT', 'STOP_MARKET'], help='Order type')
    parser.add_argument('--quantity', type=float, required=True, help='Order quantity')
    parser.add_argument('--price', type=float, help='Order price (for LIMIT orders)')
    parser.add_argument('--stop_price', type=float, help='Stop price (for STOP_MARKET orders)')
    return parser.parse_args()


def main():
    args = parse_args()
    bot = BasicBot(args.api_key, args.api_secret)

    if args.type == 'LIMIT' and not args.price:
        print("Price is required for LIMIT orders.")
        return
    if args.type == 'STOP_MARKET' and not args.stop_price:
        print("Stop price is required for STOP_MARKET orders.")
        return

    bot.place_order(args.symbol, args.side, args.type, args.quantity, args.price, args.stop_price)


if __name__ == '__main__':
    main()
