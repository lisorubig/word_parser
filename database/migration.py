"""

Migrations for database

"""
from . import db_connect


CREATE_TABLE_WORDS: str = """
        CREATE TABLE IF NOT EXISTS words (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        word VARCHAR(100) NOT NULL UNIQUE,
        count_words INT,
        in_files TEXT NOT NULL,
        INDEX USING BTREE (id),
        INDEX USING BTREE (word)
        );
    """


MIGRATIONS: list = [
    CREATE_TABLE_WORDS,
]


def migrate() -> None:
    """
    Create migrations in database
    """
    with db_connect.DBConnection() as connection:
        for command in MIGRATIONS:
            connection.cursor.execute(command)


if __name__ == "__main__":
    migrate()
