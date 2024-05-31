from flask import Blueprint, request, jsonify, Response, json

from files.errors import NoFileFound, NoFileCheckPath, FileAlreadyExist
from files.injectors import Injector
from files.orm_models import File

router = Blueprint('router', __name__)


@router.get("/")
def get_all_files_infos() -> list[File]:
    return Injector.storage().get_all_files_infos()


@router.get("/<int:file_id>")
def get_file_info(file_id: int) -> Response:
    return jsonify(Injector.file().get_file_info(file_id))


@router.post("/")
def upload_file() -> Response:
    """
    Path example: /pics/cats/ or /\n
    '/' path means storage path.\n
    If "exist_ok"=True, file will be overwritten if exists, else raise error.
    """
    file = request.files['file']
    data = json.loads(request.form.get('data'))

    path = data.get("path") or '/'
    comment = data.get("comment") or None
    exist_ok = data.get("exist_ok") or False

    return jsonify(Injector.file().upload_file(file, path, comment, exist_ok))


@router.delete("/<int:file_id>")
def delete_file(file_id: int) -> Response:
    return jsonify(Injector.file().delete_file(file_id))


@router.get("/<path:path>")
def get_files_infos_by_path(path: str) -> list[File]:
    """
    Path example: /pics/cats/\n
    '/' path means storage path.
    """

    return Injector.storage().get_files_infos_by_path(path)


@router.get("/<int:file_id>/download")
def download_file(file_id: int) -> Response:
    return Injector.file().download_file(file_id)


@router.patch("/<int:file_id>")
def update_file_info(file_id: int) -> Response:
    """
    File path example: /pics/cats/Photo.jpg or /Photo.jpg\n
    '/' path or new_path means storage path.\n
    If new_path is None, file will be updated without change path.
    """
    new_name = request.json.get("new_name", None)
    new_path = request.json.get("new_path", None)
    new_comment = request.json.get("new_comment", None)

    return jsonify(Injector.file().update_file_info(file_id,
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
