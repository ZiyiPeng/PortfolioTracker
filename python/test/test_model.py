import unittest

from python.model.record import Record
from python.model.portfolio import Portfolio
from python.model.stock import Stock
from python.model.user import User


class TestModelSchema(unittest.TestCase):
    # some sanity check to make sure database schema is functional
    # a user can have 1 portfolio, each portfolio has many records
    def test_schema(self):
        stock = Stock(ticker='AAPL', sector='tech')
        record = Record(amount=100, stock=stock)
        portfolio = Portfolio(name='test-port', records=[record])
        user = User(username='name', password_hash='pass', portfolio=portfolio)
        self.assertEqual(len(user.portfolio.records), 1)
        stock_name = user.portfolio.records[0].stock.ticker
        self.assertEqual(stock_name, stock.ticker)

if __name__ == '__main__':
    unittest.main()
