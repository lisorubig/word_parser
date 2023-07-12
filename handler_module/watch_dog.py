"""

Scan directory and send new files paths

"""
import json
import os

import celery_app
import settings


def read_file_names_storage() -> list:
    """
    Read file names from story file
    """
    if os.path.exists(settings.PROCESSED_FILES):
        with open(settings.PROCESSED_FILES, "r", encoding="utf-8") as f:
            file = f.read()
        return json.loads(file)
    else:
        return []


def write_processed_files(processed_files: list) -> None:
    """
    Write name files, which created tasks
    """
    with open(settings.PROCESSED_FILES, "w", encoding="utf-8") as wf:
        wf.write(json.dumps(processed_files))


def create_parser_task(
    file_name: str,
) -> None:
    """
    Create celery task for parser or error sender
    """
    path_to_file = f"{settings.DIRECTORY_FROM_RESERVATION}/{file_name}"
    try:
        with open(path_to_file, "r", encoding="utf-8") as f:
            f.readline()
    except UnicodeDecodeError:
        celery_app.error_to_process.apply_async(kwargs={"path_to_file": path_to_file})
    else:
        celery_app.task_file_parsing.apply_async(kwargs={"path_to_file": path_to_file})


def watch_dog() -> None:
    """
    Scan directory and send new files paths
    """
    files_in_directory = os.listdir(path=settings.DIRECTORY_FROM_RESERVATION)
    old_files = read_file_names_storage()

    new_files = set(files_in_directory) - set(old_files)

    for file_name in new_files:
        create_parser_task(file_name)
        old_files.append(file_name)
        write_processed_files(old_files)
