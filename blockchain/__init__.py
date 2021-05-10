from flask import Flask
from blockchain.views import mine_blueprint


def create_app(config):
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(mine_blueprint)

    return app
