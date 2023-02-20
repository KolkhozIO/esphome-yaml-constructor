from sqlalchemy import Column, Integer, String, Boolean
from db.connect import Base


class Filename(Base):
    __tablename__ = 'filename'

    id = Column(Integer, primary_key=True, index=True)
    name_yaml = Column(String)
    name_esphome = Column(String)
    hash_yaml = Column(String)
    compile_test = Column(Boolean, default=False)
