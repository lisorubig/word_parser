"""

Database connection

"""
import pymysql

import settings


class DBConnection:
    """
    Context manager for database connecting
    """

    def __init__(self):
        self.connection = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=3306,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            database=settings.MYSQL_DATABASE,
        )

        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()

        self.cursor.close()
        self.connection.close()
