from flask import Flask

from python.model.base import db
from python.model.user import User
from python.model.portfolio import Portfolio
from python.model.stock import Stock
from python.model.Record import Record

app = Flask(__name__)
app.config.from_pyfile('config.py')
# app.config['MYSQL_HOST'] = '127.0.0.1'
# app.config['MYSQL_PORT'] = 6443
# app.config['MYSQL_USER'] = 'zpeng'
# app.config['MYSQL_PASSWORD'] = 'P@ssw0rd'
# app.config['MYSQL_DB'] = 'port-tracker'
db.init_app(app)

@app.route('/')
def hello_world():
    db.create_all()
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
