import flask_cors
import flask_praetorian
import flask_sqlalchemy
from flask import Flask
from flask_migrate import Migrate
from python.model.user import User
from python.model.stock import Stock
from python.model.record import Record
from python.model.portfolio import Portfolio
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_pyfile('config.py')

from python.model.model import db, guard

db.init_app(app)
guard.init_app(app, User)

migrate = Migrate(app, db)

from python.api.auth import auth
app.register_blueprint(auth)
