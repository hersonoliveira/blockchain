from flask import Blueprint

mine_blueprint = Blueprint("mine", __name__, url_prefix="/mine")


@mine_blueprint.route("/")
def mine():
    return "Mine a new block"
