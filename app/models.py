from sqlalchemy import Column, MetaData, String, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ChatTable:
    """Chat model"""
    def __init__(self, chat_id):
        self.table_name = f"table_{chat_id}"
        metadata = MetaData()
        self.table = Table(
            self.table_name,
            metadata,
            Column("data", String(255)),
            Column("is_birthday", String(255), default=False),
            Column("date", String(255)),
        )


class Holiday:
    """Holiday model"""
    def __init__(self):
        self.is_birthday = False
        self.holiday_name = ""
