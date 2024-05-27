from dataclasses import dataclass


@dataclass
class NoFileFound(Exception):
    status_code: int = 404
    message: str = "No file found."


@dataclass
class NoFileCheckPath(Exception):
    status_code: int = 404
    message: str = "File not found, check path."


@dataclass
class FileAlreadyExist(Exception):
    status_code: int = 409
    message: str = "File already exists."
