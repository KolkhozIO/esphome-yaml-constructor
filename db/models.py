import uuid

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
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

    user_id = Column(String, primary_key=True, unique=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)

    # Add a unique constraint to the user_id column
    __table_args__ = (UniqueConstraint('user_id'),)


class User_Config(Base):
    __tablename__ = 'user_config'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    name_config = Column(UUID(as_uuid=True), ForeignKey("config.name_config"))
    name_esphome = Column(String)
