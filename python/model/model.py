import flask_cors
import flask_praetorian
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
guard = flask_praetorian.Praetorian()
cors = flask_cors.CORS()