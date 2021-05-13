from flask import Blueprint, current_app

mine_bp = Blueprint("mine", __name__, url_prefix="/mine")
transactions_bp = Blueprint("transactions", __name__, url_prefix="/transactions")
chain_bp = Blueprint("chain", __name__, url_prefix="/chain")


@mine_bp.route("/", methods=["GET"])
def mine():
    return "Mine a new block"


@transactions_bp.route("/new", methods=["POST"])
def new_transaction():
    return "New transaction"


@chain_bp.route("/", methods=["GET"])
def full_chain():
    response = {
        "chain": current_app.blockchain.chain,
        "length": len(current_app.blockchain.chain),
    }
    return response, 200
