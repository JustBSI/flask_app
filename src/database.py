from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import Config

engine = create_engine(Config.DATABASE_URL)
session_maker = sessionmaker(engine, expire_on_commit=False, class_=Session)


class DbRequest:
    def __init__(self):
        self.session = session_maker()

    def execute_query(self, query: Any) -> Any | None:
        result = self.session.execute(query)
        return result

    def execute_stmt(self, stmt: Any) -> None:
        self.session.execute(stmt)
        try:
            self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()
