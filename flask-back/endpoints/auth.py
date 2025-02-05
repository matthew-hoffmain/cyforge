from flask import Blueprint, request
from server import server

auth = Blueprint("auth", __name__, url_prefix="/auth")


auth_api_contract = {
       "status": "",
       "message": "",
       "data": {}
     }


@auth.route("/add_user/")
def add_user():
    server_i = server.app.config['flask-back']
    username = request.headers['username'].replace("'", "''")
    password = request.headers['password'].replace("'", "''")
    confirm_password = request.headers['confirmPassword'].replace("'", "''")

    ret = server_i.add_user(username, password, confirm_password)

    return {"content": ret}


@auth.route("/change_password/")
def change_password():
    server_i = server.app.config['flask-back']
    server_i.change_password("lax", "cool", "coolio")

    ret = "done"

    return {"content": ret}


@auth.route("/login/")
def login():
    username = request.headers['username'].replace("'", "''")
    password = request.headers['password'].replace("'", "''")
    server_i = server.app.config['flask-back']
    ret = server_i.gen_sessionkey(username, password)
    return {"content": ret}


@auth.route("/check_session/")
def check_session():
    server_i = server.app.config['flask-back']
    username = request.headers['username'].replace("'", "''")
    sessionkey = request.headers['sessionkey'].replace("'", "''")
    ret = server_i.auth_sessionkey(username, sessionkey)

    return {"content": ret}
