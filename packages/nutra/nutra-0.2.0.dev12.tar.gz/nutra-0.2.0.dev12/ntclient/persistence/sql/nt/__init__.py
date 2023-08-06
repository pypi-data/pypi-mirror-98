import os
import sqlite3

from .... import NT_DB_NAME, NUTRA_DIR, __db_target_usda__

# Connect to DB
db_path = os.path.join(NUTRA_DIR, NT_DB_NAME)
if os.path.isfile(db_path):
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
else:
    # print("warn: nt database doesn't exist, please run init")
    # print("info: init not implemented, manually build db with ntsqlite README")
    con = None


def _sql(query, args=None, headers=False):
    """Executes a SQL command to nt.sqlite"""
    cur = con.cursor()

    # TODO: DEBUG flag in prefs.json ... Print off all queries
    if args:
        if type(args) == list:
            result = cur.executemany(query, args)
        else:  # tuple
            result = cur.execute(query, args)
    else:
        result = cur.execute(query)
    rows = result.fetchall()
    if headers:
        headers = [x[0] for x in result.description]
        return headers, rows
    return rows
