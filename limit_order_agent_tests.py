import unittest
from unittest.mock import Mock
from trading_framework.execution_client import ExecutionException
from limit_order_agent import LimitOrderAgent

class LimitOrderAgentTest(unittest.TestCase):
    def setUp(self):
        self.execution_client = Mock()
        self.agent = LimitOrderAgent(self.execution_client)

    def test_buy_order_executed(self):
        self.agent.add_order(True, 'IBM', 1000, 100)
        self.agent.on_price_tick('IBM', 99)
        self.execution_client.buy.assert_called_with('IBM', 1000)

    def test_sell_order_executed(self):
        self.agent.add_order(False, 'IBM', 1000, 100)
        self.agent.on_price_tick('IBM', 101)
        self.execution_client.sell.assert_called_with('IBM', 1000)

    def test_buy_order_not_executed(self):
        self.agent.add_order(True, 'IBM', 1000, 100)
        self.agent.on_price_tick('IBM', 101)
        self.execution_client.buy.assert_not_called()

    def test_sell_order_not_executed(self):
        self.agent.add_order(False, 'IBM', 1000, 100)
        self.agent.on_price_tick('IBM', 99)
        self.execution_client.sell.assert_not_called()

    def test_execution_exception_handled(self):
        self.agent.add_order(True, 'IBM', 1000, 100)
        self.execution_client.buy.side_effect = ExecutionException('Execution failed')
        self.agent.on_price_tick('IBM', 99)
        self.execution_client.buy.assert_called_with('IBM', 1000)
        self.assertEqual(len(self.agent.orders), 1)  

if __name__ == '__main__':
    unittest.main()
