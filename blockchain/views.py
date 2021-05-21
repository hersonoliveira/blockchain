from flask import Blueprint, current_app, request

mine_bp = Blueprint("mine", __name__, url_prefix="/mine")
transactions_bp = Blueprint("transactions", __name__, url_prefix="/transactions")
chain_bp = Blueprint("chain", __name__, url_prefix="/chain")


@mine_bp.route("/", methods=["GET"])
def mine():
    return "Mine a new block"


@transactions_bp.route("/new", methods=["POST"])
def new_transaction():
    req_values = request.get_json()

    # Check if all values are in request
    required = ["sender", "recipient", "amount"]
    if not all(k in req_values for k in required):
        return "Missing values", 400

    # Create a new transaction
    index = current_app.blockchain.new_transaction(
        sender=req_values["sender"],
        recipient=req_values["recipient"],
        amount=req_values["amount"]
    )

    response = {"message": f"Transaction will be added to Block {index}"}
    return response, 201


@chain_bp.route("/", methods=["GET"])
def full_chain():
    response = {
        "chain": current_app.blockchain.chain,
        "length": len(current_app.blockchain.chain),
    }
    return response, 200
