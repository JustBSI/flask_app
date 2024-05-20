from pathlib import Path

from flask import Flask, jsonify, request

from src.config import Config
from src.files.injectors import Injector

app = Flask(__name__)

Path(Config.STORAGE_PATH).mkdir(parents=True, exist_ok=True) if Config.DOCKER == 'False' else None


@app.get("/")
def get_all_files_infos():
    return jsonify(Injector.storage().get_all_files_infos())


@app.get("/file")
def get_file_info():
    """
    File path example: /pics/cats/Photo.jpg or /Photo.jpg\n
    '/' path means storage path.
    """
    file_path = request.args.get("file_path")
    return jsonify(Injector.file().get_file_info(file_path))


@app.post("/upload")
def upload_file():
    """
    Path example: /pics/cats/ or /\n
    '/' path means storage path.\n
    If "exist_ok"=True, file will be overwritten if exists, else raise error.
    """
    file = request.files['file']
    path = request.args.get("path") or '/'
    comment = request.args.get("comment")
    exist_ok = request.args.get("exist_ok") or False
    Injector.file().upload_file(file, path, comment, exist_ok)

    return {201: 'File upload successfully.'}


@app.delete("/delete")
def delete_file():
    """
    File path example: /pics/cats/Photo.jpg or /Photo.jpg\n
    '/' path means storage path.
    """
    file_path = request.args.get("file_path")
    return jsonify(Injector.file().delete_file(file_path))


@app.get("/path")
def get_files_infos_by_path():
    """
    Path example: /pics/cats/\n
    '/' path means storage path.
    """
    path = request.args.get("path") or '/'
    return jsonify(Injector.storage().get_files_infos_by_path(path))


@app.get("/download")
def download_file():
    """
    File path example: /pics/cats/Photo.jpg or /Photo.jpg\n
    '/' path means storage path.
    """
    file_path = request.args.get("file_path")
    return Injector.file().download_file(file_path)


@app.patch("/update")
def update_file_info():
    """
    File path example: /pics/cats/Photo.jpg or /Photo.jpg\n
    '/' path or new_path means storage path.\n
    If new_path is None, file will be updated without change path.
    """
    file_path = request.args.get("file_path")
    new_name = request.args.get("new_name")
    new_path = request.args.get("new_path")
    new_comment = request.args.get("new_comment")
    return jsonify(Injector.file().update_file_info(file_path, new_name, new_path, new_comment))


@app.get("/sync")
def sync_db_with_storage():
    return jsonify(Injector.storage().sync_db_with_storage())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
