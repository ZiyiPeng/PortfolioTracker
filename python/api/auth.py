import flask
from flask import Blueprint
from sqlalchemy.exc import IntegrityError

from base import app
from python.model.model import guard, db
from python.model.portfolio import Portfolio
from python.model.user import User

auth = Blueprint('auth', __name__, template_folder='frontend/public')

@app.route('/api/login', methods=['POST'])
def login():
    req = flask.request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    user = guard.authenticate(username, password)
    ret = {'access_token': guard.encode_jwt_token(user)}
    return ret, 200

@app.route('/api/register', methods=['POST'])
def register():
    req = flask.request.get_json(force=True)
    try:
        hashed_pass = guard.hash_password(req['password'])
        user = User(username=req['username'], password_hash=hashed_pass)
        portfolio = Portfolio(name=f'{user.username} portfolio')
        user.portfolio = portfolio
        db.session.add(user)
        db.session.commit()
        user = guard.authenticate(user.username, req['password'])
        ret = {'access_token': guard.encode_jwt_token(user), 'message': 'successfully registered user'}
        return ret, 200
    except IntegrityError:
        ret = {'status': 'failure',
               'message': 'user already exist'}
        return ret, 420
    except Exception as e:
        ret = {'status': 'failure',
                  'message': repr(e)}
        print(repr(e))
        return ret, 420

# @app.route('/', methods=['GET'])
# def index():
#     hashed_password = guard.hash_password('pass')
#     me = User(username='name', password_hash=hashed_password)
#     db.session.add(me)
#     db.session.commit()
#     return 'hello, world'
