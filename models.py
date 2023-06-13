from sqlalchemy import Column, Integer, String, MetaData, Table, Boolean, DATE, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ChatTable:
    def __init__(self, chat_id):
        self.table_name = f"table_{chat_id}"
        metadata = MetaData()
        self.table = Table(self.table_name, metadata,
                           Column('data', String(255)),
                           Column('is_birthday', Boolean, default=False),
                           Column('date', DATE, default=func.current_date()))
