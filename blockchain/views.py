from flask import Blueprint, current_app, request

mine_bp = Blueprint("mine", __name__, url_prefix="/mine")
transactions_bp = Blueprint("transactions", __name__, url_prefix="/transactions")
chain_bp = Blueprint("chain", __name__, url_prefix="/chain")
nodes_bp = Blueprint("nodes", __name__, url_prefix="/nodes")


@mine_bp.route("/", methods=["GET"])
def mine():
    # Run the proof of work algorithm
    last_block = current_app.blockchain.last_block
    last_proof = last_block["proof"]
    proof = current_app.blockchain.proof_of_work(last_proof)

    current_app.blockchain.new_transaction(
        sender="0",
        recipient=current_app.node_identifier,
        amount=1
    )

    #Add new block to the chain
    previous_hash = current_app.blockchain.hash(last_block)
    block = current_app.blockchain.new_block(proof, previous_hash)

    response = {
        "message": "New Block Forged",
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"]
    }

    return response, 200


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


@nodes_bp.route("/register", methods=["POST"])
def register_node():
    pass


@nodes_bp.route("/resolve", methods=["GET"])
def consensus():
    pass
