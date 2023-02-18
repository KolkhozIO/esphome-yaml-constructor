from sqlalchemy import Column, Integer, String
from db.db_connect import Base


class Filename(Base):
    __tablename__ = 'filename'

    id = Column(Integer, primary_key=True, index=True)
    name_yaml = Column(String)
    name_esphome = Column(String)
