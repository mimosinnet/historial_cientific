#!/usr/bin/env python
from .collection import Collection
from .collections import Collections, config


# Collection {{{


def download_collection(collection_id: str) -> None:
    """Download a specific collection by its ID."""
    Collection(collection_id, False).download_collection()


def get_collections_reg0(collection_id: str, latex: bool) -> None:
    """Fetch reg0 data for a given collection."""
    Collection(collection_id, latex).get_reg0()


def get_items(collection_id: str, latex: bool) -> None:
    """Retrieve and print reference items from a collection."""
    collection = Collection(collection_id, latex)
    items = collection.get_refs()
    for i in items:
        print(i)


def write_collection(collection_id: str, latex: bool) -> None:
    """Write the collection references to disk/output."""
    collection = Collection(collection_id, latex)
    collection.write_refs()


# }}}

#  Collections {{{


def show_server_collections() -> None:
    """Display the collections available on the server."""
    Collections(config).show_server_collections()


def show_collections() -> None:
    """Display local collections and their sections."""
    coll = Collections(config)
    print("Show collections: ")
    coll.show_collections()
    print("Show sections: ")
    coll.show_sections()


def download_collections() -> None:
    """Download all configured collections."""
    coll = Collections(config)
    coll.show_collections()
    coll.download()


# }}}
