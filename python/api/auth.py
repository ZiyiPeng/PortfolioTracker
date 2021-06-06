import flask
from flask import Blueprint

from base import app
from python.model.model import guard, db
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
        db.session.add(user)
        db.session.commit()
        ret = {'status': 'success', 'message': 'successfully registered user {}'.format(user)}
        return ret, 200
    except Exception as e:
        ret = {'status': 'failure',
                  'message': 'failed to register user',
                  'errors': repr(e)}
        return ret, 420

@app.route('/', methods=['GET'])
def index():
    hashed_password = guard.hash_password('pass')
    me = User(username='name', password_hash=hashed_password)
    db.session.add(me)
    db.session.commit()
    return 'hello, world'