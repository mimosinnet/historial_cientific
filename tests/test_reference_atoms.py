from bibliografia.reference_atoms import Author


def test_get_auth_1() -> None:
    creators = ""
    author = Author(creators).get_auth()
    assert author == "NoAuthor"


def test_get_auth_2() -> None:
    creators = [
        {
            "creatorType": "author",
            "name": "",
            "firstName": "",
            "lastName": "San Román, Beatriz",
        },
        {
            "creatorType": "author",
            "name": "",
            "firstName": "Joan",
            "lastName": "Pujol-Tarres",
        },
        {
            "creatorType": "editor",
            "name": "",
            "firstName": "Joan",
            "lastName": "Pujol-Tarres",
        },
        {
            "creatorType": "author",
            "name": "Montenegro-Martínez, Marisela",
            "firstName": "Marisela",
            "lastName": "Montenegro-Martínez",
        },
    ]
    author = Author(creators).get_auth()
    assert (
        author
        == "San Román, Beatriz; "
        + "Pujol-Tarres, Joan; "
        + "Montenegro-Martínez, Marisela"
    )
