import uuid

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID, JSONB

Base = declarative_base()


class Config(Base):
    __tablename__ = 'config'

    name_config = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hash_yaml = Column(String)
    compile_test = Column(Boolean, default=False)
    name_esphome = Column(String)
    platform = Column(String)
    config_json = Column(JSONB)


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)
    hashed_password = Column(String, nullable=False)


class User_Config(Base):
    __tablename__ = 'user_config'
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    name_config = Column(UUID(as_uuid=True), ForeignKey("config.name_config"))
    name_esphome = Column(String)
