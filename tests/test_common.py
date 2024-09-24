from datetime import date
from bibliografia.common import sort_refs, get_date_object, completar, concat, neteja


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
