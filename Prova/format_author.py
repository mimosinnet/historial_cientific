# https://fortierq.github.io/python-import/
from pathlib import Path
import sys
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

#-----------------------------------

from bibliografia.common import (
    format_author,
)


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
        print(format_author(i[0], i[1], i[2], i[3]))

    for i in test_editor:
        print(format_author(i[0], i[1], i[2], i[3]))


test_format_author()
