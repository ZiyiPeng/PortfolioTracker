from dataclasses import dataclass
from collections import defaultdict
from python.model.model import db
from sqlalchemy_serializer import SerializerMixin
import yfinance as yf
from python.model.record import Record


@dataclass
class Portfolio(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    records = db.relationship('Record', uselist=True, lazy=True)

    def add_records(self, records):
        self.records.extend(records)

    def delete_records(self, records_ids):
        Record.query.filter(Record.portfolio_id == self.id and Record.id in records_ids).delete()

    # payloads: [{'record_id': .., 'amount': ..}]
    def update_records(self, payload):
        records = {r['record_id']: r['amount'] for r in payload}
        update_keys = set(records.keys())
        for r in self.records:
            if r.id in update_keys:
                Record.query.get(r.id).amount = records[r.id]

    def composition(self):
        total = sum([abs(r.price * r.amount) for r in self.records])
        industry_comp, sector_comp = defaultdict(float), defaultdict(float)
        for r in self.records:
            exposure = abs(r.price * r.amount) / total
            industry_comp[r.stock.industry] += exposure
            sector_comp[r.stock.sector] += exposure
        return {
            'industry_comp': dict(industry_comp),
            'sector_comp': dict(sector_comp)
        }

    def current_value(self):
        result = 0
        for r in self.records:
            ticker, amount = r.stock_ticker, r.amount
            info = yf.Ticker(ticker).info
            # calculate closing (liquidating) value
            price = info['bid'] if amount < 0 else info['ask']
            result += price * amount
        return result

