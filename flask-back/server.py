import json
import random
import sys

from flask import Flask
from configparser import ConfigParser

from block import Block
from blocks.responders.echo import Echo
from blocks.responders.machineModel import MachineModel
from blocks.responder import Responder
from blocks.responders.textInput import TextInput
from dbconnector import DBConnector
from blocks.schema import Schema
import threading
import hashlib

app = Flask(__name__)

forbiddenSchemas = [""]

templateSchemas = {"empty": '{"nodes": [], "edges": []}'}


class Server:
    def __init__(self,
                 config_file: str,
                 target_config_section: str,
                 template_config_section: str
                 ):
        """
        Creates a flask-back instance with a given config file and two config sections.
        The config options are validated to make sure that they have the same keys.
        This is to ensure that a template version of the flask-back configuration is always maintained.
        :param config_file: Target ini file to load sections from.
        :param target_config_section: Config section to actually load.
        :param template_config_section: Config section to validate target against.
        """
        # Create a config parser and check that we can access the template and target config in the given file
        config = ConfigParser()
        config.read(config_file)
        assert config.has_section(template_config_section), \
            f"No configuration for specified option {template_config_section} in {config_file}"
        assert config.has_section(target_config_section), \
            f"No configuration for specified option {target_config_section} in {config_file}"

        # Load both the template config and the target config
        template_config_section_dict = config[template_config_section]
        target_config_section_dict = config[target_config_section]

        # Check that every key in the template exists in the target
        for key, val in template_config_section_dict.items():
            assert key in target_config_section_dict, \
                f"{key} key in {config[template_config_section]} does not exist in {target_config_section} of config file"

        # Vice versa, check that every key in the target exists in the template
        for key, val in target_config_section_dict.items():
            assert key in template_config_section_dict, \
                f"{key} key in {target_config_section} does not exist in {config[template_config_section]} of config file"

        # Finally grab the Flask app instance and load our config options into it
        self.app_i = app
        for key, val in target_config_section_dict.items():
            self.app_i.config[key] = val

        # Make sure there is a database reference in the config
        assert 'database' in self.app_i.config, \
            f"No 'database' option specified in {target_config_section}"

        # Attaches a self-reference to the app instance
        self.app_i.config['flask-back'] = self
        self.dbc = DBConnector(self.app_i.config['database'], log=False)
        self.secret_key = self.app_i.config['secret_key']

        # Database initiation using config
        self.init_db()

        # Server-side, non-persistent storage
        self.sessionkeys = {}

    def get_url_map(self
                    ):
        return self.app_i.url_map

    def get_app_config(self
                       ):
        return self.app_i.config.items()

    def init_db(self
                ):
        self.init_user_table()
        self.init_schema_table()

        # TODO: REMOVE THIS TEMPORARY SOLUTION
        self.schema_instances = {}

    def init_user_table(self
                        ):
        self.run_query("CREATE TABLE IF NOT EXISTS Users("
                       "userid INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "username varchar(255) NOT NULL,"
                       "password varchar(255) NOT NULL"
                       ");")

    def init_schema_table(self
                          ):
        self.run_query("CREATE TABLE IF NOT EXISTS Schemas("
                       "schemaid INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "schemaname VARCHAR(255) NOT NULL,"
                       "userid INTEGER NOT NULL,"
                       "blueprint VARCHAR(255) NOT NULL,"
                       "FOREIGN KEY (userid) REFERENCES Users(userid)"
                       ");")

    def get_user_info(self,
                      username
                      ) -> list[tuple]:
        ret = self.run_query(f"SELECT userid, username, password FROM users WHERE users.username == '{username}'")
        return ret

    def get_schema_info(self,
                        userid,
                        schemaname
                        ) -> list[tuple]:
        ret = self.run_query(
            f"SELECT schemaid, schemaname, userid, blueprint FROM schemas WHERE schemas.userid == '{userid}' AND schemas.schemaname == '{schemaname}'")
        return ret

    def get_schema_list(self,
                        username
                        ) -> (int, list[str]):
        user_id = self.get_user_info(username)[0][0]
        ret = self.run_query(
            f"SELECT schemaid, schemaname, userid, blueprint FROM schemas WHERE schemas.userid == '{user_id}';")

        schemas = ([s[1] for s in ret])
        [schemas.append(templateName) for templateName in templateSchemas.keys()]
        return 0, schemas

    def add_user(self,
                 username,
                 password,
                 confirm_password
                 ):
        # todo: sanitize username and passwords for characters
        # Usernames must be between 2 and 15 alphanumeric characters

        if password != confirm_password:
            return -3
        if not 2 <= len(username) <= 15:
            return -4
        if not username.isalnum():
            return -5
        # Passwords must be at least 6 characters
        if not 6 <= len(password):
            return -6

        ret = self.get_user_info(username)
        if len(ret) >= 1:
            # user already exists
            return -2

        encrypted_password = self.encrypt_text(password)

        ret = self.run_query(
            f"INSERT OR IGNORE INTO Users(username,password) VALUES ('{username}', '{encrypted_password}');")

        return ret

    def change_password(self,
                        username,
                        old_password,
                        new_password
                        ):
        ret = self.get_user_info(username)
        if len(ret) != 1:
            print("user doesn't exist!")
            return

        if self.validate_password(username, old_password):
            password = self.encrypt_text(new_password)
            ret = self.run_query(f"UPDATE users SET password = '{password}' WHERE users.username == '{username}';")
        return

    def create_schema(self,
                      username,
                      schemaName,
                      content
                      ):
        if schemaName in templateSchemas:
            print('cant set a new schema using a template schemas name')
            return -1
        if schemaName in forbiddenSchemas:
            print('cant set a new schema using a forbidden schemas name')
            return -1

        user_id = self.get_user_info(username)[0][0]

        if len(self.get_schema_info(user_id, schemaName)) > 0:
            print("duplicate schema name")
            return -1

        ret = self.run_query(
            f"INSERT OR IGNORE INTO Schemas(schemaname,userid,blueprint) VALUES ('{schemaName}', {user_id},'{content}');")

        return 0

    def update_schema(self,
                      username,
                      schemaName,
                      content
                      ):
        if schemaName in templateSchemas:
            print('cant override a template schema')
            return -1
        if schemaName in forbiddenSchemas:
            print('cant set a new schema using a forbidden schemas name')
            return -1

        user_id = self.get_user_info(username)[0][0]

        ret = self.run_query(
            f"UPDATE Schemas SET blueprint = '{content}' WHERE schemas.userid == '{user_id}' AND schemas.schemaname == '{schemaName}';")

        return 0

    def read_schema(self,
                    username,
                    schemaName
                    ) -> (int, str):

        if schemaName in templateSchemas:
            return 0, templateSchemas[schemaName]

        user_id = self.get_user_info(username)[0][0]

        blueprint = self.get_schema_info(user_id, schemaName)[0][3]

        return 0, blueprint

    def encrypt_text(self,
                     text
                     ):
        encrypt_text = hashlib.sha256(usedforsecurity=True)
        encrypt_text.update(self.secret_key.encode('UTF-8'))
        encrypt_text.update(text.encode('UTF-8'))
        return encrypt_text.hexdigest()

    def validate_password(self,
                          username,
                          password
                          ):
        ret = self.get_user_info(username)
        if len(ret) == 1:
            user_info = ret[0]
            db_pw = user_info[2]
            return db_pw == self.encrypt_text(password)
        return None

    def gen_sessionkey(self,
                       username,
                       password
                       ):
        if self.validate_password(username, password):
            sessionkey = self.encrypt_text(str(random.randint(1, sys.maxsize)))
            self.sessionkeys[username] = sessionkey
            return sessionkey
        return -1

    def auth_sessionkey(self,
                        username,
                        sessionkey
                        ):
        if username in self.sessionkeys:
            return self.sessionkeys[username] == sessionkey
        return False

    def filter_sessionkeys(self,
                           cutoff
                           ):
        # todo
        pass

    def run_query(self,
                  query
                  ):
        return self.dbc.run_query(query)

    def run_queries(self,
                    queries
                    ):
        return [self.run_query(query) for query in queries]

    def make_schema_instance(self,
                             username,
                             schemaName
                             ):
        if username not in self.schema_instances:
            self.schema_instances[username] = {}
        if schemaName not in self.schema_instances[username]:
            self.schema_instances[username][schemaName] = {0: None}
        target_schema_instances = self.schema_instances[username][schemaName]
        id_list = [ID for ID in target_schema_instances.keys()]
        # todo : update when schema instances can be deleted
        next_schemaID = max(id_list) + 1
        new_schema = Schema(block_id=0, name=schemaName)
        self.schema_instances[username][schemaName][next_schemaID] = new_schema

        # next we recreate the schema from the blueprint
        user_id = self.get_user_info(username)[0][0]
        blueprint = self.get_schema_info(user_id, schemaName)
        blueprint_dict = (json.loads(blueprint[0][3]))

        schema_functions = []
        schema_blocks = []
        schema_edges = []

        nodes = blueprint_dict["nodes"]
        for node in nodes:
            id = node["id"]
            label = node["data"]["label"]
            isJoin = node["data"]["isJoin"]
            blockType = node["data"]["blockType"]
            # input_type = node["data"]["input"]

            new_block = None

            match blockType:
                case "System":
                    # validate that if ID is 0 it has all the properties of START
                    if int(id) == 0:
                        new_block = None
                    else:
                        new_block = Block(block_id=int(id),
                                          name=label,
                                          in_groups=[],
                                          join=isJoin,
                                          )

                case "Responder":
                    subtype = node["data"]["subtype"]
                    content = node["data"]["content"]
                    output_type = node["data"]["output"]
                    credentials = node["data"]["credentials"]
                    this_response_generator = None
                    match subtype:
                        case "Echo":
                            this_response_generator = Echo(content)
                            schema_functions.append(this_response_generator)
                        case "User Text Input":
                            this_response_generator = TextInput()
                            schema_functions.append(this_response_generator)
                        case "Model":
                            if credentials == "ADMIN openai":
                                this_response_generator = MachineModel(
                                    make="openai",
                                    model="gpt-4o",
                                    api_key=self.app_i.config['personal_openai_key']
                                )
                                schema_functions.append(this_response_generator)
                            else:
                                print("bad credentials!")
                        case _:
                            print("not yet implmeneted, fool")
                    if this_response_generator is not None:
                        new_block = Responder(block_id=int(id),
                                              output_type=output_type,
                                              name=label,
                                              in_groups=['public'],
                                              join=isJoin,
                                              out_groups=['public'],
                                              rg_ref=this_response_generator
                                              )

                case "Switch":
                    pass

                case "Component":
                    pass

                case _:
                    print("not yet implmeneted, fool")

            if new_block is not None:
                schema_blocks.append(new_block)
                new_schema.add_block(new_block)
            else:
                pass

        edges = blueprint_dict["edges"]
        for edge in edges:
            if edge["data"]["dependent"]:
                new_schema.add_dependency(int(edge["target"]), int(edge["source"]))
            else:
                new_schema.add_flow(int(edge["source"]), int(edge["target"]))

        return 0, next_schemaID

    def get_schema_i(self,
                     username,
                     schemaName,
                     schemaID
                     ) -> Schema:
        return self.schema_instances[username][schemaName][schemaID]

    def get_schema_state(self,
                         username,
                         schemaName,
                         schemaID
                         ):
        schema_i = self.get_schema_i(username, schemaName, int(schemaID))

        content = {
            "schemaName": schemaName,
            "schemaID": schemaID,
            "currentBlockID": schema_i.current_block_id,
            "executionQueue": list(schema_i.execution_queue.queue),
            "ledger": self.get_ledger(username, schemaName, schemaID)[1]
        }

        return 0, content

    def execute_next(self,
                     username,
                     schemaName,
                     schemaID
                     ):
        schemaID = int(schemaID)
        schema_i = self.get_schema_i(username, schemaName, schemaID)
        schema_i.execute_next()

        return self.get_ledger(username, schemaName, schemaID)

    def run_schema(self,
                     username,
                     schemaName,
                     schemaID
                     ):
        schemaID = int(schemaID)
        schema_i = self.get_schema_i(username, schemaName, schemaID)
        schema_i.run(False, False, False)

        return 0

    def run_schema_to_unprepared(self,
                     username,
                     schemaName,
                     schemaID
                     ):
        schemaID = int(schemaID)
        schema_i = self.get_schema_i(username, schemaName, schemaID)
        thread = threading.Thread(target=schema_i.run_to_unprepared)
        thread.start()

        return 0

    def deliver_content(self,
                        username,
                        schemaName,
                        schemaID,
                        blockID,
                        content
                        ):
        schemaID = int(schemaID)
        schema_i = self.get_schema_i(username, schemaName, schemaID)
        schema_i.deliver_content(blockID, content)

        return 0

    def get_schema_instances(self,
                             username,
                             schemaName
                             ):
        if username not in self.schema_instances:
            self.schema_instances[username] = {}
        if schemaName not in self.schema_instances[username]:
            self.schema_instances[username][schemaName] = {0: None}
        target_schema_instances = self.schema_instances[username][schemaName]
        return [k for k in target_schema_instances.keys()][1:]

    def get_ledger(self,
                   username,
                   schemaName,
                   schemaID
                   ) -> (int, list[dict]):
        ledger = self.schema_instances[username][schemaName][int(schemaID)].get_ledger()
        return 0, [message.dict() for message in ledger]

    def authorized_request(self,
                           request) -> int:
        pass