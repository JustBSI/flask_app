from .strings import ExceptionStrings


class NoFileFound(Exception, ExceptionStrings):
    def __init__(self, status_code=404, message=ExceptionStrings.NO_FILE_FOUND):
        super().__init__()
        self.status_code = status_code
        self.message = message


class NoFileCheckPath(Exception, ExceptionStrings):
    def __init__(self, status_code=404, message=ExceptionStrings.NO_FILE_CHECK_PATH):
        super().__init__()
        self.status_code = status_code
        self.message = message


class FileAlreadyExist(Exception, ExceptionStrings):
    def __init__(self, status_code=409, message=ExceptionStrings.FILE_ALREADY_EXIST):
        super().__init__()
        self.status_code = status_code
        self.message = message
