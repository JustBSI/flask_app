from src.files.strings import ExceptionStrings


class Error(Exception, ExceptionStrings):
    @classmethod
    def no_file_found(cls):
        return {
            404: cls.NO_FILE_FOUND
        }

    @classmethod
    def no_file_check_path(cls):
        return {
            404: cls.NO_FILE_CHECK_PATH
        }

    @classmethod
    def file_already_exist(cls):
        return {
            409: cls.FILE_ALREADY_EXIST
        }
