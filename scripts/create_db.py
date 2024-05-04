from pathlib import Path
import os
import sqlite3
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


PROJECT_ROOT = Path.cwd()
TABLES_PATH = PROJECT_ROOT / 'sql' / 'tables'

connection = sqlite3.connect(PROJECT_ROOT / "todox.sqlite3")


def _create_tables():
    cursor = connection.cursor()
    for f in os.listdir(TABLES_PATH):
        log.info(f"Now running {f}...")
        with open(TABLES_PATH / f, 'r') as sql_file:
            try:
                cursor.execute(sql_file.read())
            except sqlite3.OperationalError:
                log.warning(f"Table {f} already exists. Moving on...")


def main():
    log.info("Attempting to create tables...")
    _create_tables()


if __name__ == '__main__':
    main()
