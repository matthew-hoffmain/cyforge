from flask import Blueprint

test = Blueprint("test", __name__, url_prefix="/test")

# @test.route("/")
# def home():
#     return make_response(jsonify({"message": "Unauthorized"}), StatusCode.UNAUTHORIZED.value)
