from flask import Blueprint, request, jsonify, make_response
from enum import Enum
from server import server

sandbox = Blueprint("sandbox", __name__, url_prefix="/sandbox")

class StatusCode(Enum):
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

@sandbox.route("/")
def home():
    return make_response(jsonify({"message": "Unauthorized"}), StatusCode.UNAUTHORIZED.value)


@sandbox.route("/refresh/")
def refresh():
    server_i = server.app.config['flask-back']
    server_i.dbc.query_queue.put("hello!")

    # init flask-back values if DNE
    try:
        server_i.sandbox
    except:
        server_i.sandbox = {"refresh": 0}
    # grab and increment
    server_i.sandbox["refresh"] = server_i.sandbox["refresh"] + 1
    server_value = server_i.sandbox["refresh"]

    # init DB values if DNE
    server_i.run_queries(["CREATE TABLE IF NOT EXISTS sandbox(key, value, PRIMARY KEY (key));",
                          "INSERT OR IGNORE INTO sandbox VALUES ('refresh',0);"])
    kv_dict = {k: v for k, v in server_i.run_query("SELECT * from sandbox;")}
    # grab and increment
    db_value = kv_dict["refresh"] + 1
    server_i.run_query(f"UPDATE sandbox SET value = {db_value} WHERE key = 'refresh';")

    ret = (f"Let's do a DB test!\n"
           f"Since resetting the flask-back this page has been hit {server_value} times\n"
           f"But the DB has maintained that the total is {db_value} times\n")

    return {"content": ret}


@sandbox.route("/get_server_map/")
def get_server_map():
    server_i = server.app.config['flask-back']
    return f"{server_i.get_url_map()}"


@sandbox.route("/schema_list/")
def get_schema_list():
    status = -1
    content = ""

    server_i = server.app.config['flask-back']
    username = request.headers['username'].replace("'", "''")
    sessionkey = request.headers['sessionkey'].replace("'", "''")
    authorized = server_i.auth_sessionkey(username, sessionkey)

    if not authorized:
        status = -1
    else:
        status, content = server_i.get_schema_list(username)

    return {"status": status, "content": content}


@sandbox.route("/schema/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def schema():
    status = -1
    content = ""

    server_i = server.app.config['flask-back']
    username = request.headers['username'].replace("'", "''")
    sessionkey = request.headers['sessionkey'].replace("'", "''")
    authorized = server_i.auth_sessionkey(username, sessionkey)


    if not authorized:
        status = -1
    else:
        data = request.data.decode("utf-8")
        schemaName = request.headers['schemaName'].replace("'", "''")
        match request.method:
            case 'GET':
                status, content = server_i.read_schema(username, schemaName)
            case 'POST':
                status = server_i.update_schema(username, schemaName, data)
            case 'PUT':
                status = server_i.create_schema(username, schemaName, data)
            case 'DELETE':
                status = 0

    return {"status": status, "content": content}


@sandbox.route("/make_schema_instance/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def make_schema_instance():
    status = -1
    content = ""

    server_i = server.app.config['flask-back']
    username = request.headers['username'].replace("'", "''")
    sessionkey = request.headers['sessionkey'].replace("'", "''")
    authorized = server_i.auth_sessionkey(username, sessionkey)

    if not authorized:
        status = -1
    else:
        schemaName = request.headers['schemaName'].replace("'", "''")
        status, content = server_i.make_schema_instance(username, schemaName)

    return {"status": status, "content": content}


@sandbox.route("/get_ledger/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_ledger():
    status = -1
    content = ""

    server_i = server.app.config['flask-back']
    username = request.headers['username'].replace("'", "''")
    sessionkey = request.headers['sessionkey'].replace("'", "''")
    authorized = server_i.auth_sessionkey(username, sessionkey)

    if not authorized:
        status = -1
    else:
        schemaName = request.headers['schemaName'].replace("'", "''")
        schemaID = request.headers['schemaID'].replace("'", "''")
        status, content = server_i.get_ledger(username, schemaName, schemaID)

    return {"status": status, "content": content}

@sandbox.route("/execute_next/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def execute_next():
    status = -1
    content = ""

    server_i = server.app.config['flask-back']
    username = request.headers['username'].replace("'", "''")
    sessionkey = request.headers['sessionkey'].replace("'", "''")
    authorized = server_i.auth_sessionkey(username, sessionkey)

    if not authorized:
        status = -1
    else:
        schemaName = request.headers['schemaName'].replace("'", "''")
        schemaID = request.headers['schemaID'].replace("'", "''")
        status, content = server_i.execute_next(username, schemaName, schemaID)

    return {"status": status, "content": content}


@sandbox.route("/get_schema_instances/", methods=['GET'])
def get_schema_instances():
    status = -1
    content = ""

    server_i = server.app.config['flask-back']
    username = request.headers['username'].replace("'", "''")
    sessionkey = request.headers['sessionkey'].replace("'", "''")
    authorized = server_i.auth_sessionkey(username, sessionkey)

    if not authorized:
        status = -1
    else:
        schemaName = request.headers['schemaName'].replace("'", "''")
        content = server_i.get_schema_instances(username, schemaName)

    return {"status": status, "content": content}


@sandbox.route("/get_response/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_response():
    status = -1
    content = ""

    server_i = server.app.config['flask-back']
    username = request.headers['username'].replace("'", "''")
    sessionkey = request.headers['sessionkey'].replace("'", "''")
    authorized = server_i.auth_sessionkey(username, sessionkey)

    if not authorized:
        status = -1
    else:
        schemaName = request.headers['schemaName'].replace("'", "''")

        # zeroth, make a py_schema! have a py_schema!
        # first, check what stage of the py_schema we're at

    return {"status": status, "content": content}


@sandbox.route("/get_state/")
def get_state():
    status = -1
    content = ""

    server_i = server.app.config['flask-back']
    username = request.headers['username'].replace("'", "''")
    sessionkey = request.headers['sessionkey'].replace("'", "''")
    authorized = server_i.auth_sessionkey(username, sessionkey)

    if not authorized:
        status = -1
    else:
        schemaName = request.headers['schemaName'].replace("'", "''")
        schemaID = request.headers['schemaID'].replace("'", "''")

        status, content = server_i.get_schema_state(username, schemaName, schemaID)

    return {"status": status, "content": content}


@sandbox.route("/deliver_content/")
def deliver_content():
    status = -1
    content = ""

    server_i = server.app.config['flask-back']
    username = request.headers['username'].replace("'", "''")
    sessionkey = request.headers['sessionkey'].replace("'", "''")
    authorized = server_i.auth_sessionkey(username, sessionkey)

    if not authorized:
        status = -1
    else:
        schemaName = request.headers['schemaName'].replace("'", "''")
        schemaID = request.headers['schemaID'].replace("'", "''")
        blockID = request.headers['blockID'].replace("'", "''")
        content = request.headers['content'].replace("'", "''")

        # TODO: remove placeholder!
        blockID = 1

        print(f"blockID={blockID},content={content}")

        status = server_i.deliver_content(username, schemaName, schemaID, blockID, content)

    return {"status": status}


@sandbox.route("/run/")
def run():
    status = -1
    content = ""

    server_i = server.app.config['flask-back']
    username = request.headers['username'].replace("'", "''")
    sessionkey = request.headers['sessionkey'].replace("'", "''")
    authorized = server_i.auth_sessionkey(username, sessionkey)

    if not authorized:
        status = -1
    else:
        schemaName = request.headers['schemaName'].replace("'", "''")
        schemaID = request.headers['schemaID'].replace("'", "''")

        status = server_i.run_schema(username, schemaName, schemaID)

    return {"status": status}


@sandbox.route("/run_to_unprepared/")
def run_to_unprepared():
    status = -1
    content = ""

    server_i = server.app.config['flask-back']
    username = request.headers['username'].replace("'", "''")
    sessionkey = request.headers['sessionkey'].replace("'", "''")
    authorized = server_i.auth_sessionkey(username, sessionkey)

    if not authorized:
        status = -1
    else:
        schemaName = request.headers['schemaName'].replace("'", "''")
        schemaID = request.headers['schemaID'].replace("'", "''")

        status = server_i.run_schema_to_unprepared(username, schemaName, schemaID)

    return {"status": status}



@sandbox.route("/deliver_and_run/")
def deliver_and_run():
    status = -1
    content = ""

    server_i = server.app.config['flask-back']
    username = request.headers['username'].replace("'", "''")
    sessionkey = request.headers['sessionkey'].replace("'", "''")
    authorized = server_i.auth_sessionkey(username, sessionkey)

    if not authorized:
        status = -1
    else:
        schemaName = request.headers['schemaName'].replace("'", "''")
        schemaID = request.headers['schemaID'].replace("'", "''")
        blockID = request.headers['blockID'].replace("'", "''")
        content = request.headers['content'].replace("'", "''")

        # TODO: remove placeholder!
        blockID = 1

        print(f"blockID={blockID},content={content}")

        status = server_i.deliver_content(username, schemaName, schemaID, blockID, content)
        if status == 0:
            status = server_i.run_schema_to_unprepared(username, schemaName, schemaID)
        else:
            status = -1

    return {"status": status}
