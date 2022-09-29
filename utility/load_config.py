import json, os, sys

def load_config():
    if not os.path.isfile("./config.json"):
        sys.exit("'config.json' not found! Please add it and try again.")
    else:
        with open("config.json") as file:
            return json.load(file)