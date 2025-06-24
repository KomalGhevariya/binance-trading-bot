import logging
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException

# Configure logging
logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'

    def place_market_order(self, symbol, side, quantity):
        try:
            logging.info(f"Placing MARKET {side} order for {symbol}, qty: {quantity}")
            order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY if side.lower() == 'buy' else SIDE_SELL,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            logging.info(f"Order executed: {order}")
            return order
        except BinanceAPIException as e:
            logging.error(f"Market order failed: {e}")
            return {"error": str(e)}

    def place_limit_order(self, symbol, side, quantity, price):
        try:
            logging.info(f"Placing LIMIT {side} order for {symbol} at {price}, qty: {quantity}")
            order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY if side.lower() == 'buy' else SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                quantity=quantity,
                timeInForce=TIME_IN_FORCE_GTC,
                price=price
            )
            logging.info(f"Order executed: {order}")
            return order
        except BinanceAPIException as e:
            logging.error(f"Limit order failed: {e}")
            return {"error": str(e)}

def main():
    api_key = "41ae61c5d9c640bd2b48bbf876b9369978f20d2cc3855b9f4a4560f647f83b13"
    api_secret = "975a87bbc339e8a2d99e557cd75e4400b6fc51449909b2c3c8689aa523313c0c"

    bot = BasicBot(api_key, api_secret)

    symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
    side = input("Buy or Sell: ").lower()
    order_type = input("Order type (market/limit): ").lower()
    quantity = float(input("Enter quantity: "))

    if order_type == 'market':
        response = bot.place_market_order(symbol, side, quantity)
    elif order_type == 'limit':
        price = input("Enter limit price: ")
        response = bot.place_limit_order(symbol, side, quantity, price)
    else:
        print("Invalid order type!")
        return

    print("Order Response:")
    print(response)

if __name__ == "__main__":
    main()
