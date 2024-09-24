#!/usr/bin/env python
from .collection import Collection
from .collections import Collections, config


# Collection {{{


def download_collection(id):
    Collection(id, False).download_collection()


def get_collections_reg0(id, latex):
    Collection(id, latex).get_reg0()


def get_items(id, latex):
    collection = Collection(id, latex)
    # items = collection.get_items()
    # items = collection.get_creators()
    # items = collection.get_authors()
    # items = collection.get_editors()
    # items = collection.get_years()
    # items = collection.get_titles()
    # items = collection.get_journals()
    items = collection.get_refs()
    for i in items:
        print(i)


def write_collection(id, latex):
    collection = Collection(id, latex)
    collection.write_refs()


# }}}

#  Collections {{{


def show_server_collections():
    Collections(config).show_server_collections()


def show_collections():
    coll = Collections(config)
    print("Show collections: ")
    coll.show_collections()
    print("Show sections: ")
    coll.show_sections()


def download_collections():
    coll = Collections(config)
    coll.show_collections()
    coll.download()


# }}}
