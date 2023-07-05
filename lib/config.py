from typing import Union
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from db.dals import ConfigDAL
from db.models import Config


async def _execute_function_with_args(func, session, *args, **kwargs):
    async with session.begin():
        dal = ConfigDAL(session)
        result = await func(dal, *args, **kwargs)
        return result


async def _create_new_yaml_config(session, name_esphome: str = None, hash_yaml: str = None, platform: str = None, config_json: str = None):
    return await _execute_function_with_args(
        ConfigDAL.create_yaml_config,
        session,
        name_esphome=name_esphome,
        hash_yaml=hash_yaml,
        platform=platform,
        config_json=config_json)


async def get_config_by_name_or_hash(session, name_config: UUID = None, hash_yaml: str = None) -> Union[Config, None]:
    return await _execute_function_with_args(ConfigDAL.get_config,
                                             session,
                                             name_config=name_config,
                                             hash_yaml=hash_yaml)


async def _delete_yaml_config(name_config, session):
    return await _execute_function_with_args(ConfigDAL.delete_yaml_config,
                                             session,
                                             name_config=name_config)


async def _update_yaml_config(name_config, session):
    return await _execute_function_with_args(ConfigDAL.update_yaml_config,
                                             session,
                                             name_config=name_config)


async def _update_config(hash_yaml, name_esphome, platform, session):
    return await _execute_function_with_args(ConfigDAL.update_config,
                                             session,
                                             hash_yaml=hash_yaml,
                                             name_esphome=name_esphome,
                                             platform=platform)


async def _update_config_json(hash_yaml, config_json, session):
    return await _execute_function_with_args(ConfigDAL.update_config_json,
                                             session,
                                             hash_yaml=hash_yaml,
                                             config_json=config_json)
