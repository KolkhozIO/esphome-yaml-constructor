from typing import Union
from uuid import UUID

from sqlalchemy import select, update, and_, cast, delete, null
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User, Config, User_Config


class ConfigDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_yaml_config(self, name_esphome: str = None, hash_yaml: str = None, platform: str = None, config_json: str = None):
        new_yaml_config = Config(
            name_esphome=name_esphome,
            hash_yaml=hash_yaml,
            platform=platform,
            config_json=config_json
        )
        self.db_session.add(new_yaml_config)
        await self.db_session.flush()
        return new_yaml_config

    async def delete_yaml_config(self, name_config: str):
        query = delete(Config).where(Config.name_config == name_config)
        await self.db_session.execute(query)
        await self.db_session.commit()
        return "Config deleted"

    async def get_yamlconfig_by_hashyaml(self, hash_yaml: str) -> Union[Config, None]:
        query = select(Config).where(and_(Config.hash_yaml == hash_yaml, Config.compile_test == True))
        res = await self.db_session.execute(query)
        yaml_config_row = res.fetchone()
        if yaml_config_row is not None:
            return yaml_config_row[0]

    async def get_config_by_config_json(self, hash_yaml: str) -> Union[Config, None]:
        query = select(Config).where(and_(Config.hash_yaml == hash_yaml, Config.config_json != None, null))
        res = await self.db_session.execute(query)
        yaml_config_row = res.fetchone()
        if yaml_config_row is not None:
            return yaml_config_row[0]

    async def get_config(self, hash_yaml: str = None, name_config: UUID = None) -> Union[Config, None]:
        query = None
        if hash_yaml:
            query = select(Config).where(Config.hash_yaml == hash_yaml)
        elif name_config:
            query = select(Config).where(Config.name_config == name_config)
        if query is not None:
            res = await self.db_session.execute(query)
            config_row = res.fetchone()
            if config_row is not None:
                return config_row[0]
        return None

    async def update_yaml_config(self, name_config: str) -> Union[Config, None]:
        query = (
            update(Config)
            .where(Config.name_config == name_config)
            .values(compile_test=True)
            .returning(Config.name_config)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]

    async def update_config_json(self, hash_yaml: str, config_json: str):
        query = (
            update(Config)
            .where(Config.hash_yaml == hash_yaml)
            .values(config_json=config_json)
            .returning(Config.name_config)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]

    async def update_config(self, hash_yaml: str, name_esphome: str, platform: str):
        query = (
            update(Config)
            .where(Config.hash_yaml == hash_yaml)
            .values(name_esphome=name_esphome, platform=platform)
            .returning(Config.name_config)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]


class FavouritesDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_favourites(self, user_id: UUID, name_config: UUID, name_esphome: str):
        new_favourites = User_Config(
            user_id=user_id,
            name_config=name_config,
            name_esphome=name_esphome
        )
        self.db_session.add(new_favourites)
        await self.db_session.flush()
        return new_favourites

    async def get_favourites_all(self, user_id: UUID):
        query = select(User_Config).where(User_Config.user_id == user_id)
        res = await self.db_session.execute(query)
        yaml_config_rows = res.fetchall()
        if yaml_config_rows is not None:
            return yaml_config_rows

    async def get_favourites_by_name_config(self, user_id: UUID, name_config: UUID):
        query = select(User_Config).where(
            and_(User_Config.user_id == user_id, User_Config.name_config == name_config))
        res = await self.db_session.execute(query)
        yaml_config_rows = res.fetchone()
        if yaml_config_rows is not None:
            return yaml_config_rows[0]

    async def delete_favourites(self, user_id: UUID, name_config: UUID):
        query = delete(User_Config).where(
            and_(User_Config.name_config == name_config, User_Config.user_id == user_id))
        await self.db_session.execute(query)
        await self.db_session.commit()
        return "favourites deleted"


class GoogleDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
            self, user_id: str, name: str, surname: str, email: str
    ) -> User:
        new_user = User(
            user_id=user_id, name=name, surname=surname, email=email
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def get_google_user(self, email: str) -> Union[User, None]:
        query = select(User).where(User.email == email)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]
