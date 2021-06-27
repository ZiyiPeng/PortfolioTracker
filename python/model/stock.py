from dataclasses import dataclass
from sqlalchemy_serializer import SerializerMixin
from python.model.model import db
import yfinance as yf

@dataclass
class Stock(db.Model, SerializerMixin):
    ticker = db.Column(db.String(8), primary_key=True)
    sector = db.Column(db.String(50), default='unknown')
    industry = db.Column(db.String(50), default='unknown')

    @classmethod
    def get_or_create(cls, ticker):
        stock = cls.query.get(ticker)
        if not stock:
            info = yf.Ticker(ticker).info
            stock = cls(ticker=ticker, industry=info['industry'], sector=info['sector'])
            db.session.add(stock)
            db.session.commit()
        return stock
