from flask import Flask

from .routes import routes
from .dB import create_tables

def create_app():
    app = Flask(__name__)

    app.register_blueprint(routes, url_prefix='/')

    create_tables()
    

    return app