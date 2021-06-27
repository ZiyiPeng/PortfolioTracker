import base

app = base.app

from python.api.auth import auth
from python.api.endpoints import endpoints
app.register_blueprint(auth)
app.register_blueprint(endpoints)

if __name__ == '__main__':
    app.run()