from dataclasses import dataclass

from python.model.model import db
from python.model.stock import Stock
import yfinance as yf
from sqlalchemy_serializer import SerializerMixin

@dataclass
class Record(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)
    stock_ticker = db.Column(db.String(8), db.ForeignKey('stock.ticker'))
    stock = db.relationship('Stock', lazy=True)

    @classmethod
    def create(cls, ticker, amount, price=None):
        stock = Stock.get_or_create(ticker)
        if not price:
            info = yf.Ticker(ticker).info
            price = info['bid'] if amount > 0 else info['ask']
        record = cls(amount=amount, stock=stock, price=price)
        return record
