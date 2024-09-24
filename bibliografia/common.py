# general functions
from dateutil import parser
from datetime import date


# sort_refs: sort dictionary by keys and return values #<
def sort_refs(refs):
    sorted_keys = dict(sorted(refs.items()))
    sorted_refs = []
    for i in sorted_keys:
        sorted_refs.append(refs[i])

    return sorted_refs


# #>


# get date object from string #<
def get_date_object(string):
    try:
        return parser.parse(string, dayfirst=True, fuzzy=True)
    except ValueError:
        return date(1111, 11, 11)


# #>


# completar si està vuit #<
def completar(text):
    if text == "":
        return "FALTA COMPLETAR"
    else:
        return text


# #>


def concat(inici, final, *args):  # #<
    text = [s for s in args if s]
    return inici + ", ".join(text) + final  # #>


# def nejeja #<
def neteja(text):
    return text.strip().removesuffix(";").removesuffix(",").removesuffix(".")


# #>

# vim: foldmarker=#<,#>
