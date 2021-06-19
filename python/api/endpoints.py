import flask
import flask_praetorian
from flask import Blueprint
from flask_praetorian import auth_required

from python.api.helper import response_on_error
from python.model.model import db
from base import app
from python.model.portfolio import Portfolio
from python.model.record import Record
from python.model.stock import Stock
from python.model.user import User

endpoints = Blueprint('endpoints', __name__, template_folder='frontend/public')

@response_on_error(error_msg='fail to load stock', error_code=400)
@app.route('/api/stock', methods=['GET'])
def load_stock():
    ticker = flask.request.values.get('ticker')
    stock = Stock.get_or_create(ticker)
    return stock.to_dict(), 200

@response_on_error(error_msg='fail to load portfolio', error_code=400)
@app.route('/api/portfolio', methods=['GET'])
@auth_required
def load_portfolio():
    user = flask_praetorian.current_user()
    return user.portfolio.to_dict(), 200

@response_on_error(error_msg='fail to add records', error_code=400)
@app.route('/api/records', methods=['POST'])
@auth_required
def add_records():
    req = flask.request.get_json(force=True)
    # [{'ticker': ..., 'amount': ..}]
    data = req.get('data', None)
    records = list(map(lambda d: Record.create(ticker=d['ticker'], amount=d['amount'],
                                               price=d['price'] if 'price' in d else None), data))
    user = flask_praetorian.current_user()
    user.portfolio.add_records(records)
    db.session.commit()
    return {'message': 'success'}, 200

@response_on_error(error_msg='fail to delete records', error_code=400)
@app.route('/api/delete_records', methods=['POST'])
@auth_required
def delete_record():
    req = flask.request.get_json(force=True)
    record_ids = req.get('record_ids', None)
    user = flask_praetorian.current_user()
    user.portfolio.delete_records(record_ids)
    db.session.commit()
    return {'message': 'delete_records success'}, 200








