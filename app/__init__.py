from flask import Flask
from flask_login import LoginManager

import os
from dotenv import load_dotenv


from .dB import create_tables

loggin_manager = LoginManager()
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')


def create_app():

    from .routes import routes
    app = Flask(__name__)

    app.register_blueprint(routes, url_prefix='/')
    app.config['SECRET_KEY'] = SECRET_KEY
    

    loggin_manager.init_app(app)
    create_tables()
    

    return app
