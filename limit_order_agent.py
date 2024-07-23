from trading_framework.execution_client import ExecutionClient, ExecutionException
from trading_framework.price_listener import PriceListener

class LimitOrderAgent(PriceListener):
    def __init__(self, execution_client: ExecutionClient) -> None:
        super().__init__()
        self.execution_client = execution_client
        self.orders = []

    def add_order(self, is_buy: bool, product_id: str, amount: int, limit: float) -> None:
       
        self.orders.append({
            'is_buy': is_buy,
            'product_id': product_id,
            'amount': amount,
            'limit': limit
        })

    def on_price_tick(self, product_id: str, price: float) -> None:
        for order in self.orders[:]:
            if order['product_id'] == product_id:
                if order['is_buy'] and price <= order['limit']:
                    try:
                        self.execution_client.buy(product_id, order['amount'])
                        self.orders.remove(order)
                    except ExecutionException as e:
                        print(f"Buy order failed: {e}")
                elif not order['is_buy'] and price >= order['limit']:
                    try:
                        self.execution_client.sell(product_id, order['amount'])
                        self.orders.remove(order)
                    except ExecutionException as e:
                        print(f"Sell order failed: {e}")
