from python.model.base import db


class Stock(db.Model):
    ticker = db.Column(db.String(8), primary_key=True)
    sector = db.Column(db.String(50), default='unknown')


