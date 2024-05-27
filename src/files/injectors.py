from files.services import StorageService as Storage, FileService as File
from config import config


class Injector:

    @staticmethod
    def file():
        return File(config.storage_path)

    @staticmethod
    def storage():
        return Storage(config.storage_path)
