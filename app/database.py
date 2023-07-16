"""Create the connection with the database"""
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///chats.db")
metadata = MetaData()
Session = sessionmaker(bind=engine)
session = Session()
