from flask import Blueprint, request, jsonify, make_response
from enum import Enum
import server

test = Blueprint("test", __name__, url_prefix="/test")

# @test.route("/")
# def home():
#     return make_response(jsonify({"message": "Unauthorized"}), StatusCode.UNAUTHORIZED.value)
