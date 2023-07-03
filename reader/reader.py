"""

Read from database of determine level and write to file

"""
import logging
from datetime import datetime

import settings
from database import db_connect


LOGGER = logging.getLogger(__name__)

SELECT_WORDS = """
    SELECT words.id, words.word, words.count_words, words.in_files 
    FROM words WHERE count_words>=%s
    """


DELETE_WORDS = """
    DELETE FROM words WHERE id=%s  
    """


def reader() -> None:
    """
    Read from database of determine level and write to file
    """
    with db_connect.DBConnection() as connection:

        connection.cursor.execute(SELECT_WORDS % settings.FRINGE_WRITE_TO_FILE)
        fetch = connection.cursor.fetchall()

        for row in fetch:
            try:
                connection.cursor.execute(DELETE_WORDS % row[0])
                with open(
                        f"{settings.BASE_DIR}result/{row[1]} {datetime.now()}",
                        mode="w",
                        encoding="utf-8",
                ) as file:
                    file.write(f"{row[1]}\n{row[3]}")
            except OSError as exception:
                LOGGER.error("%s row: %s" % (exception, row))
                connection.connection.rollback()
            else:
                connection.connection.commit()


if __name__ == "__main__":
    reader()
