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


# def neteja puntuació final #<
def neteja(text):
    return text.strip().removesuffix(";").removesuffix(",").removesuffix(".")


# #>


# def formar author #<
def format_author(auth_type, name, firstName, lastName):
    final_firstName, final_lastName = "", ""

    case_string = (
        string_null(name) + string_null(firstName) * 2 + string_null(lastName) * 4
    )

    match case_string:
        case 1 | 5:  # name
            final_firstName, final_lastName = comma_split(name)
        case 4:  # lastName
            final_firstName, final_lastName = comma_split(lastName)
        case 6 | 7:  # firstName lastName
            final_firstName, final_lastName = firstName, lastName

    # Output based on auth_type
    if auth_type == "editor":
        return f"{final_firstName} {final_lastName}, "
    else:
        return f"{final_lastName}, {final_firstName}; "


# #>

# Complementary functions #<


# def string_null, check if string is not null #<
def string_null(string):
    if string:
        return 1
    else:
        return 0


# #>


# def comma_split #<
def comma_split(string):
    if "," in string:
        lastName, firstName = string.split(",", 1)
        return [firstName.strip(), lastName.strip()]
    else:
        return ["", string.strip()]


# #>

# #>

# vim: foldmarker=#<,#>
