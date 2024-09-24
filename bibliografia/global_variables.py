# Define Global Variables

import tomllib

config_path = "./Data/"
CACHE_PATH = config_path + "cache/"
CONFIG_FILE = config_path + "config.toml"
CREDENTIALS_FILE = config_path + "credentials/ident.toml"
HISTORIAL = config_path + "HistorialAFIN/include/"

with open(CONFIG_FILE, "rb") as f:
    config = tomllib.load(f)

with open(CREDENTIALS_FILE, "rb") as f:
    ident = tomllib.load(f)

LIBRARY = ident["library"]
API_ID = ident["api_id"]
API_KEY = ident["api_key"]

FILBREAK = "\\filbreak"
ITEM = "\\item "
