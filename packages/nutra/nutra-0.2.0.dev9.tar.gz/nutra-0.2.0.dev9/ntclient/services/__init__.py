import os

from .. import NT_DB_NAME, NUTRA_DIR, ROOT_DIR
from ..ntsqlite.sql import build_ntsqlite
from ..persistence.sql.usda import usda_init

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))


def _init():
    """
    TODO:   Check for:
        1. .nutra folder
        2. usda
        3a. nt
        3b. default profile?
        4. prefs.json
    """
    print("Nutra directory  ", end="")
    if not os.path.isdir(NUTRA_DIR):
        os.makedirs(NUTRA_DIR, 0o755)
    print(u"\u2713")

    # TODO: print off checks, return False if failed
    print("USDA db          ", end="")
    usda_init()
    print(u"\u2713")

    print("Nutra db         ", end="")
    build_ntsqlite()
    ntsqlite_buildpath = os.path.join(ROOT_DIR, "ntsqlite", "sql", NT_DB_NAME)
    # TODO: don't overwrite, verbose toggle for download, option to upgrade
    ntsqlite_destination = os.path.join(NUTRA_DIR, NT_DB_NAME)
    if os.path.isfile(ntsqlite_destination):
        print(u"\u2713")
        print(
            "WARN: upgrades not supported, please remove ntdb file or ignore this warning"
        )
    else:
        os.rename(ntsqlite_buildpath, ntsqlite_destination)
        print(u"\u2713")

    print("\nAll checks have passed!")
    return True
