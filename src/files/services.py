from shutil import copyfileobj
from datetime import datetime
from pathlib import Path

from flask import send_file, Response
from sqlalchemy import select, insert, delete, update

from files.orm_models import File
from database import DbRequest
from files.errors import NoFileFound, NoFileCheckPath, FileAlreadyExist


class BaseService:

    def __init__(self, storage: str) -> None:
        self.storage = Path(storage)
        self.db = DbRequest()

    def _file_path_to_attr(self, file_path: str) -> (str, str, str):
        self.file_path = Path(file_path)

        name = self.file_path.stem
        extension = self.file_path.suffix
        path = str(self.file_path.parent)
        if path != '/':
            path += '/'

        return name, extension, path

    def _check_file_exists(self, file_path: str) -> Path:
        file_full_path = self.storage / file_path[1:]
        if not file_full_path.is_file():
            raise NoFileCheckPath()
        else:
            return file_full_path

    def get_file_info(self, file_id: int) -> File:

        query = select(File).where(File.id == file_id)

        result = self.db.execute_query(query)

        if not result:
            raise NoFileCheckPath()
        else:
            return result[0]


class FileService(BaseService):

    def upload_file(self, file: any, path: str = '/',
                    comment: str | None = None,
                    exist_ok: bool = False) -> File:

        full_path = self.storage / path[1:]
        full_path.mkdir(parents=True, exist_ok=True)
        file_full_path = full_path / file.filename
        updated_at = None if not file_full_path.exists() else datetime.now()
        if file_full_path.exists() and not exist_ok:
            raise FileAlreadyExist()

        with open(file_full_path, 'wb') as f:
            copyfileobj(file, f)

        file_info = {
            'name': file_full_path.stem,
            'extension': file_full_path.suffix,
            'size': file_full_path.stat().st_size,
            'path': path,
            'updated_at': updated_at,
            'comment': comment
        }

        if updated_at:
            stmt = (update(File)
                    .values(updated_at=updated_at)
                    .where(File.name == file_info['name'],
                           File.extension == file_info['extension'],
                           File.path == file_info['path']))
        else:
            stmt = insert(File).values(**file_info)
        self.db.execute_stmt(stmt)

        query = select(File).where(File.name == file_info['name'],
                                   File.extension == file_info['extension'],
                                   File.path == file_info['path'])

        new_file_info = self.db.execute_query(query)[0]

        return new_file_info

    def delete_file(self, file_id: int) -> File:

        file_info = self.get_file_info(file_id)

        stmt = (delete(File)
                .where(File.name == file_info.name,
                       File.extension == file_info.extension,
                       File.path == file_info.path))

        self.db.execute_stmt(stmt)

        (Path(str(self.storage) + file_info.path + file_info.name +
              file_info.extension)).unlink()

        return file_info

    def download_file(self, file_id: int) -> Response:
        file_info = self.get_file_info(file_id)
        file_full_path = Path(
            str(self.storage) + file_info.path + file_info.name +
            file_info.extension)

        return send_file(file_full_path, as_attachment=True)

    def update_file_info(self, file_id: int,
                         new_name: str | None = None,
                         new_path: str | None = None,
                         new_comment: str | None = None) -> File:

        file_info = self.get_file_info(file_id)

        if new_name or new_path or new_comment:
            updated_at = datetime.now()
        else:
            updated_at = file_info.updated_at

        new_name = new_name or file_info.name
        new_path = new_path or file_info.path
        new_comment = new_comment or file_info.comment

        new_full_path = self.storage / new_path[1:]

        new_full_path.mkdir(parents=True, exist_ok=True)

        file_full_path = Path(
            str(self.storage) + file_info.path + file_info.name +
            file_info.extension)

        file_full_path.replace(
            new_full_path / (new_name + file_info.extension))

        stmt = (update(File).values(name=new_name,
                                    path=new_path,
                                    comment=new_comment,
                                    updated_at=updated_at)
                .where(File.name == file_info.name,
                       File.extension == file_info.extension,
                       File.path == file_info.path))

        self.db.execute_stmt(stmt)

        new_file_info = self.get_file_info(file_id)

        return new_file_info


class StorageService(BaseService):

    def get_all_files_infos(self) -> list[File]:
        result = self.db.execute_query(select(File))

        if not result:
            raise NoFileFound()
        else:
            return result

    def get_files_infos_by_path(self, path: str = '/') -> list[File]:
        query = select(File).where(File.path == '/' + path)
        result = self.db.execute_query(query)

        if not result:
            raise NoFileFound()
        else:
            return result

    def sync_db_with_storage(self) -> dict[str, list[File]]:
        deleted_files, added_files = [], []
        files_in_db_full = self.db.execute_query(select(File)) or []
        files_in_db = {Path(file.path) / (file.name + file.extension)
                       for file in files_in_db_full}
        files_in_storage = set(self.storage.rglob('*.*'))

        for file_path, file_info in zip(files_in_db, files_in_db_full):
            if self.storage / str(file_path)[1:] not in files_in_storage:
                name, extension, path = self._file_path_to_attr(file_path)

                deleted_files.append(file_info)

                stmt = (delete(File)
                        .where(File.name == name,
                               File.extension == extension,
                               File.path == path))
                self.db.execute_stmt(stmt)

        files_in_db = {self.storage / str(file)[1:] for file in files_in_db}
        for file in files_in_storage:
            if file not in files_in_db:
                path = '/'
                if file.parent != self.storage:
                    path += ('/'.join(file.parts[len(self.storage.parts):-1])
                             + '/')
                file_data = {
                    'name': file.stem,
                    'extension': file.suffix,
                    'size': file.stat().st_size,
                    'path': path
                }

                stmt = (insert(File)
                        .values(name=file_data['name'],
                                extension=file_data['extension'],
                                size=file_data['size'],
                                path=file_data['path']))
                self.db.execute_stmt(stmt)

                query = (select(File)
                         .where(File.path == file_data['path'],
                                File.extension == file_data['extension'],
                                File.name == file_data['name']))

                file_info = self.db.execute_query(query)[0]

                added_files.append(file_info)

        return {'deleted': deleted_files, 'added': added_files}
