"""

"""

from server.server import Server, app
from argparse import ArgumentParser

from endpoints.auth import auth
from endpoints.sandbox import sandbox

app.register_blueprint(auth)
app.register_blueprint(sandbox)

# Checks commandline arguments for config options
parser = ArgumentParser()
parser.add_argument('config_file', type=str, default="DEFAULT")
parser.add_argument('target_config', type=str, default="DEFAULT")


if __name__ == '__main__':
    # Get config file and the target config option from commandline arguments
    args = vars(parser.parse_args())
    config_file = args['config_file']
    target_config = args['target_config'].upper()
    # Instantiate serverapp with config options
    server_i = Server(config_file, target_config, 'TEMPLATE')
    try:
        query_list = [
        ]
        for query in query_list:
            res = server_i.run_query(query)

        server_i.app_i.run()
    finally:
        print("closing safely")


