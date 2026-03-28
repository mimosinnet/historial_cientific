from datetime import date
from bibliografia.common import (
    comma_split,
    sort_refs,
    get_date_object,
    completar,
    concat,
    neteja,
    format_author,
    string_null,
)


def test_get_date_object() -> None:
    dates = [
        get_date_object("11-12-1964"),
        get_date_object("1964-12-11"),
        get_date_object(""),
    ]
    value = []
    for i in dates:
        assert isinstance(i, date)
        value.append(i.strftime("%d-%m-%Y"))

    assert value[0] == "11-12-1964"
    # assert value[1] == "11-12-1964"  # ATENCIÓ: DONA ERROR
    assert value[2] == "11-11-1111"


def test_sort_refs() -> None:
    dictionary = {"b": "segon", "a": "primer", "c": "tercer"}
    sorted_dic = sort_refs(dictionary)
    assert sorted_dic == ["primer", "segon", "tercer"]


def test_completar() -> None:
    comp = completar("")
    assert comp == "FALTA COMPLETAR"
    comp = completar("Completat")
    assert comp == "Completat"


def test_concat() -> None:
    concatenate = concat(", ", ".", "one", "two")
    assert concatenate == ", one, two."


def test_neteja() -> None:
    string = [" prova ", " prova, ", " prova; ", " prova. "]

    for i in string:
        assert neteja(i) == "prova"


def test_format_author() -> None:
    test_author = [
        ["author", "Joan", "Joan", "Pujol"],
        ["author", "", "Joan", "Pujol"],
        ["author", "Pujol, Joan", "", "Pujol, Joan"],
        ["author", "Pujol, Joan", "", ""],
        ["author", "", "", "Pujol, Joan"],
    ]
    test_editor = [
        ["editor", "Joan", "Joan", "Pujol"],
        ["editor", "", "Joan", "Pujol"],
        ["editor", "Pujol, Joan", "", "Pujol, Joan"],
        ["editor", "Pujol, Joan", "", ""],
        ["editor", "", "", "Pujol, Joan"],
    ]
    for i in test_author:
        print(i)
        assert format_author(i[0], i[1], i[2], i[3]) == "Pujol, Joan; "

    for i in test_editor:
        assert format_author(i[0], i[1], i[2], i[3]) == "Joan Pujol, "


def test_string_null() -> None:
    assert string_null("") == 0
    assert string_null("test") == 1


def test_comma_split() -> None:
    assert comma_split("lastName, firstName") == ["firstName", "lastName"]
    assert comma_split("Name with no comma") == ["", "Name with no comma"]
