from db.dals import FavouritesDAL


async def _execute_function_with_args(func, session, *args, **kwargs):
    async with session.begin():
        dal = FavouritesDAL(session)
        result = await func(dal, *args, **kwargs)
        return result


async def _create_favourites(session, user_id, name_config, name_esphome):
    return await _execute_function_with_args(FavouritesDAL.create_favourites,
                                             session,
                                             user_id=user_id,
                                             name_config=name_config,
                                             name_esphome=name_esphome)


async def _get_favourites_all(user_id, session):
    favourites_configs = await _execute_function_with_args(FavouritesDAL.get_favourites_all,
                                                           session,
                                                           user_id=user_id)
    return [{"name_config": row[0].name_config, "name_esphome": row[0].name_esphome} for row in favourites_configs]


async def _get_favourites_by_name_config(user_id, name_config, session):
    return await _execute_function_with_args(FavouritesDAL.get_favourites_by_name_config,
                                         session,
                                         user_id=user_id,
                                         name_config=name_config)


async def _delete_yaml_config(user_id, name_config, session):
    return await _execute_function_with_args(FavouritesDAL.delete_favourites,
                                             session,
                                             user_id=user_id,
                                             name_config=name_config)
