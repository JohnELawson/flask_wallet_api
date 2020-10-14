# Flask application factory
import os
from flask import Flask
from . import db
from . import wallet

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # env vars
        SECRET_KEY=os.environ.get("SECRET_KEY", "DEV"),
        DATABASE=os.path.join(app.instance_path, 'wallet.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)

    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # # a simple page that says hello
    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World!'

    # init db for app
    db.init_app(app)

    # register wallet blueprint
    app.register_blueprint(wallet.bp)

    return app
