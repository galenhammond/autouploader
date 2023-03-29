import sys

sys.path.append("..")
from config import Config
from .base import ProjectParser
from auth.upload_policy import UploadPolicy
from typing import Optional


def download(url, path):
    """
    Download a file from a URL to a given path
    """
    import requests
    import os

    # Create the path if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)

    # Get the file name from the URL
    file_name = url.split("/")[-1]

    # Create the full path to the file
    full_path = os.path.join(path, file_name)

    # Download the file
    r = requests.get(url, stream=True)
    with open(full_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return full_path


def try_and_get_project(
    project_path, parser = None
):
    """
    Checks if the project is uploadable or queueable. Returns project if it is, none otherwise.
    """
    # TODO: update
    if Config.get_env("USER_UPLOAD_POLICY") == UploadPolicy.NEVER_UPLOAD:
        return None

    if parser:
        return parser.parse(project_path)

    # check if parser exists for
    try:
        parser_clazzes = [
            subclass for subclass in ProjectParser.__subclasses__(ProjectParser)
        ]
        for parser_clazz in parser_clazzes:
            if parser_clazz.is_project_file(project_path):
                return parser_clazz.parse(project_path)
        return None
    except ModuleNotFoundError:
        return None
