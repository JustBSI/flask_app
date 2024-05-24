from files.services import StorageService as Storage, FileService as File
from config import Config


class Injector:

    @staticmethod
    def file():
        return File(Config.STORAGE_PATH)

    @staticmethod
    def storage():
        return Storage(Config.STORAGE_PATH)
