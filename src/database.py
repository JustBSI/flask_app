from typing import Any

from sqlalchemy import create_engine, Executable
from sqlalchemy.orm import sessionmaker, Session

from config import config

engine = create_engine(config.database_url)
session_maker = sessionmaker(engine, expire_on_commit=False, class_=Session)


class DbRequest:
    def __init__(self) -> None:
        self.session = session_maker()

    def execute_query(self, query: Executable) -> Any:
        result = self.session.execute(query)
        result = result.scalars().all()
        return result

    def execute_stmt(self, stmt: Executable) -> None:
        self.session.execute(stmt)
        try:
            self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()
