import os
import shutil
import sqlite3
import sys
import tarfile
import time
import urllib.request

from .... import __db_target_usda__, USDA_DB_NAME
from ... import NUTRA_DIR


# Onboarding function
def usda_init():
    # TODO: validate version against __db_target_usda__, return <True or False>
    # TODO: handle resource moved on Bitbucket or version mismatch due to manual overwrite?
    if USDA_DB_NAME not in os.listdir(NUTRA_DIR):
        """Downloads and unpacks the nt-sqlite3 db"""

        def reporthook(count, block_size, total_size):
            """Shows download progress"""
            global start_time
            if count == 0:
                start_time = time.time()
                time.sleep(0.01)
                return
            duration = time.time() - start_time
            progress_size = int(count * block_size)
            speed = int(progress_size / (1024 * duration))
            percent = int(count * block_size * 100 / total_size)
            sys.stdout.write(
                "\r...%d%%, %d MB, %d KB/s, %d seconds passed"
                % (percent, progress_size / (1024 * 1024), speed, duration)
            )
            sys.stdout.flush()

        # Download usda.sqlite.tar.xz
        url = f"https://bitbucket.org/dasheenster/nutra-utils/downloads/{USDA_DB_NAME}-{__db_target_usda__}.tar.xz"
        print(f"curl -L {url} -o {USDA_DB_NAME}.tar.xz")
        urllib.request.urlretrieve(
            url,
            f"{NUTRA_DIR}/{USDA_DB_NAME}.tar.xz",
            reporthook,
        )
        print()

        # Extract the archive
        # NOTE: in sql.__init__() we verify version == __db_target_usda__, and if needed invoke this method with force_install=True
        with tarfile.open(f"{NUTRA_DIR}/{USDA_DB_NAME}.tar.xz", mode="r:xz") as f:
            try:
                print(f"tar xvf {USDA_DB_NAME}.tar.xz")
                f.extractall(NUTRA_DIR)
            except Exception as e:
                print(repr(e))
                print("ERROR: corrupt tarball, removing. Please try init again")
                print("rm -rf ~/.nutra/usda")
                # shutil.rmtree(NUTRA_DIR)
                exit()
        print(f"==> done downloading {USDA_DB_NAME}")


# verify_usda(__db_target_usda__)

# Connect to DB
# TODO: support as customizable env var ?
db_path = os.path.join(NUTRA_DIR, USDA_DB_NAME)
if os.path.isfile(db_path):
    con = sqlite3.connect(db_path)
    # con.row_factory = sqlite3.Row  # see: https://chrisostrouchov.com/post/python_sqlite/
else:
    # print("warn: usda database doesn't exist, please run init")
    # print("info: init not implemented, manually copy")
    con = None


def _sql(query, headers=False):
    """Executes a SQL command to usda.sqlite"""
    # TODO: DEBUG flag or VERBOSITY level in prefs.json ... Print off all queries

    cur = con.cursor()
    result = cur.execute(query)
    rows = result.fetchall()
    if headers:
        headers = [x[0] for x in result.description]
        return headers, rows
    return rows
