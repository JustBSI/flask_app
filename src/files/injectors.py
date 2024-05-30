from files.services import StorageService, FileService
from config import config


class Injector:

    @staticmethod
    def file() -> FileService:
        return FileService(config.storage_path)

    @staticmethod
    def storage() -> StorageService:
        return StorageService(config.storage_path)
