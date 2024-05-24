class NoFileFound(Exception):
    def __init__(self, status_code=404, message="No file found."):
        super().__init__()
        self.status_code = status_code
        self.message = message


class NoFileCheckPath(Exception):
    def __init__(self, status_code=404, message="File not found, check path."):
        super().__init__()
        self.status_code = status_code
        self.message = message


class FileAlreadyExist(Exception):
    def __init__(self, status_code=409, message="File already exists."):
        super().__init__()
        self.status_code = status_code
        self.message = message
