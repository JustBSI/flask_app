from flask import Blueprint, request, jsonify, Response

from files.errors import NoFileFound, NoFileCheckPath, FileAlreadyExist
from files.injectors import Injector
from files.orm_models import File

router = Blueprint('router', __name__)


@router.get("/")
def get_all_files_infos() -> list[File]:
    return Injector.storage().get_all_files_infos()


@router.get("/file")
def get_file_info() -> Response:
    """
    File path example: /pics/cats/Photo.jpg or /Photo.jpg\n
    '/' path means storage path.
    """
    file_path = request.args.get("file_path")
    return jsonify(Injector.file().get_file_info(file_path))


@router.post("/upload")
def upload_file() -> Response:
    """
    Path example: /pics/cats/ or /\n
    '/' path means storage path.\n
    If "exist_ok"=True, file will be overwritten if exists, else raise error.
    """
    file = request.files['file']
    path = request.args.get("path") or '/'
    comment = request.args.get("comment") or None
    exist_ok = request.args.get("exist_ok") or False

    return jsonify(Injector.file().upload_file(file, path, comment, exist_ok))


@router.delete("/delete")
def delete_file() -> Response:
    """
    File path example: /pics/cats/Photo.jpg or /Photo.jpg\n
    '/' path means storage path.
    """
    file_path = request.args.get("file_path")

    return jsonify(Injector.file().delete_file(file_path))


@router.get("/path")
def get_files_infos_by_path() -> list[File]:
    """
    Path example: /pics/cats/\n
    '/' path means storage path.
    """
    path = request.args.get("path") or '/'

    return Injector.storage().get_files_infos_by_path(path)


@router.get("/download")
def download_file() -> Response:
    """
    File path example: /pics/cats/Photo.jpg or /Photo.jpg\n
    '/' path means storage path.
    """
    file_path = request.args.get("file_path")

    return Injector.file().download_file(file_path)


@router.patch("/update")
def update_file_info() -> Response:
    """
    File path example: /pics/cats/Photo.jpg or /Photo.jpg\n
    '/' path or new_path means storage path.\n
    If new_path is None, file will be updated without change path.
    """
    file_path = request.args.get("file_path")
    new_name = request.args.get("new_name") or None
    new_path = request.args.get("new_path") or None
    new_comment = request.args.get("new_comment") or None

    return jsonify(Injector.file().update_file_info(file_path,
                                                    new_name,
                                                    new_path,
                                                    new_comment))


@router.get("/sync")
def sync_db_with_storage() -> dict[str: list[File]]:
    return Injector.storage().sync_db_with_storage()


@router.errorhandler(NoFileFound)
@router.errorhandler(NoFileCheckPath)
@router.errorhandler(FileAlreadyExist)
def exception(e) -> tuple[dict[int, str], int]:
    return {e.status_code: e.message}, e.status_code
