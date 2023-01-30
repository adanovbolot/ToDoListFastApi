from todo.database.base import BASE, engine
from sqlalchemy import String, Column, Boolean, Integer


class ToDo(BASE):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    is_complete = Column(Boolean, default=False)


BASE.metadata.create_all(bind=engine)

