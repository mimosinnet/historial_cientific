# Read and save zotero collections
import json
from pyzotero import zotero
from .global_variables import LIBRARY, API_ID, API_KEY, CACHE_PATH, config


class Collections:
    def __init__(self, config):
        self.collections = config["keys"]
        self.library = LIBRARY
        self.api_id = API_ID
        self.api_key = API_KEY
        self.keys = config["keys"].keys()
        self.coll_sections = config["keys"].values()
        self.zot = zotero.Zotero(self.api_id, self.library, self.api_key)

    def show_server_collections(self):
        collections = self.zot.collections()
        coll = {}
        for i in collections:
            coll[i["data"]["key"]] = i["data"]["name"]

        for i in coll:
            print(i, coll[i])

    def download(self):
        for i in self.keys:
            file = CACHE_PATH + i + ".json"
            print(file)
            with open(file, "w", encoding="utf-8") as f:
                json.dump(self.zot.everything(self.zot.collection_items(i)), f)

    def show_collections(self):
        print(self.keys)
        for i in self.keys:
            print(i, self.collections[i])

    def show_sections(self):
        for i in self.coll_sections:
            key = config["section"][i]["key"]
            title = config["section"][i]["title"]
            types = ",".join([x for x in config["section"][i]["types"]])
            print(key, i, types, title)
