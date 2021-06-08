from uuid import uuid4

from flask import Flask

from blockchain.models import Blockchain
from blockchain.views import chain_bp, mine_bp, transactions_bp


def create_app(config):
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(mine_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(chain_bp)

    app.node_identifier = str(uuid4()).replace("-", "")

    # Create blockchain instance
    app.blockchain = Blockchain()
    
    return app
