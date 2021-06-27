import flask
import flask_praetorian
from flask import Blueprint
from flask_praetorian import auth_required

from python.analyze.analyzer import Analyzer
from python.api.helper import response_on_error
from python.model.model import db
from base import app
from python.model.record import Record
from python.model.stock import Stock

endpoints = Blueprint('endpoints', __name__, template_folder='frontend/public')

@app.route('/api/stock', methods=['GET'], endpoint='load_stock')
@response_on_error(error_msg='fail to load stock', error_code=400)
def load_stock():
    ticker = flask.request.values.get('ticker')
    stock = Stock.get_or_create(ticker)
    return stock.to_dict(), 200

@app.route('/api/portfolio', methods=['GET'], endpoint='load_portfolio')
@auth_required
@response_on_error(error_msg='fail to load portfolio', error_code=400)
def load_portfolio():
    user = flask_praetorian.current_user()
    result = {'portfolio': user.portfolio.to_dict()}
    comp = user.portfolio.composition()
    result.update(comp)
    return result, 200

@app.route('/api/records', methods=['POST'], endpoint='add_records')
@auth_required
@response_on_error(error_msg='fail to add records', error_code=400)
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

@app.route('/api/delete_records', methods=['POST'], endpoint='delete_record')
@auth_required
@response_on_error(error_msg='fail to delete records', error_code=400)
def delete_record():
    req = flask.request.get_json(force=True)
    record_ids = req.get('record_ids', None)
    user = flask_praetorian.current_user()
    user.portfolio.delete_records(record_ids)
    db.session.commit()
    return {'message': 'delete_records success'}, 200

@app.route('/api/records', methods=['PATCH'], endpoint='update_records')
@auth_required
@response_on_error(error_msg='fail to update records', error_code=400)
def update_records():
    req = flask.request.get_json(force=True)
    # [{'record_id': ..., 'amount': ..}]
    data = req.get('data', None)
    user = flask_praetorian.current_user()
    user.portfolio.update_records(data)
    db.session.commit()
    return {'message': 'success'}, 200

@app.route('/api/portfolio/current_value', methods=['GET'], endpoint='get_portfolio_current_value')
@auth_required
@response_on_error(error_msg='fail to get portfolio value', error_code=400)
def get_portfolio_current_value():
    user = flask_praetorian.current_user()
    value = user.portfolio.current_value()
    return {'current_value': value}, 200

@app.route('/api/analyze', methods=['POST'], endpoint='optimal_weights')
@auth_required
@response_on_error(error_msg='fail to optimize portfolio weights', error_code=400)
def optimal_weights():
    user = flask_praetorian.current_user()
    req = flask.request.get_json(force=True)
    optimize_rule = req.get('rule', None)
    total_value = req.get('total_value', None)
    tickers = req.get('tickers', [r.stock_ticker for r in user.portfolio.records])
    analyzer = Analyzer(tickers=tickers)
    weights, exp_return, vol, comp, total_value = analyzer.optimal_comp(optimize_rule, total_value)
    return {'weights': weights,
            'expected_return': exp_return,
            'volatility': vol,
            'detail': comp,
            'total_value': total_value}, 200










