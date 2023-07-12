"""

Word parser files in parsing directory

"""
import re
import typing

from database import db_connect

COUNT_WORDS: str = """
    INSERT INTO words (word, count_words, in_files) 
    VALUES ('%(word)s', %(count_words)s, '%(file_name)s') 
    ON DUPLICATE KEY UPDATE 
    count_words=count_words+%(count_words)s, 
    in_files=CONCAT(in_files,', %(file_name)s');
"""


def count_words_in_file(path_to_file: str) -> dict:
    """
    Counts words in file and create hash map
    """
    hash_map: typing.Dict[str, int] = {}
    with open(path_to_file, "r", encoding="utf-8") as f:
        lines = f.read()
        words = re.findall("[a-zA-Z]+|[а-яА-Я]+", lines)
        for word in words:
            lower_case_word = hash_map.get(word.lower(), 0)
            hash_map[word.lower()] = lower_case_word + 1

    return hash_map


def parse_word(path_to_file):
    """
    Create rows to DB from hashmap
    """
    file_name = path_to_file.split("/")[-1]

    hash_map = count_words_in_file(path_to_file)

    with db_connect.DBConnection() as connection:
        for word, count_words in hash_map.items():
            insert_or_update_words = COUNT_WORDS % {
                "word": word,
                "count_words": count_words,
                "file_name": file_name,
            }
            connection.cursor.execute(insert_or_update_words)
