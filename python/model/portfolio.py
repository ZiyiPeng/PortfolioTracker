from dataclasses import dataclass

from python.model.model import db
from sqlalchemy_serializer import SerializerMixin

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