from flask import Flask
from blockchain.views import mine_bp, transactions_bp, chain_bp
from blockchain.models import Blockchain


def create_app(config):
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(mine_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(chain_bp)

    # Create blockchain instance
    app.blockchain = Blockchain()
    
    return app
