from python.model.base import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256))
    portfolio = db.relationship('Portfolio', backref='user', lazy=True)
