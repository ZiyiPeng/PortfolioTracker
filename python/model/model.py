import flask_cors
import flask_praetorian
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={"autoflush": False})
guard = flask_praetorian.Praetorian()
cors = flask_cors.CORS()