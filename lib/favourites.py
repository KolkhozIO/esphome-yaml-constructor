from db.dals import FavouritesDAL


async def _create_favourites(session, user_id, name_config, name_esphome):
    async with session.begin():
        favourites_dal = FavouritesDAL(session)
        yaml_config = await favourites_dal.create_favourites(
            user_id=user_id,
            name_config=name_config,
            name_esphome=name_esphome
        )
        return yaml_config


async def _get_favourites_all(user_id, session):
    async with session.begin():
        favourites_dal = FavouritesDAL(session)
        favourites_configs = await favourites_dal.get_favourites_all(
            user_id=user_id,
        )
        return [{"name_config": row[0].name_config, "name_esphome": row[0].name_esphome} for row in favourites_configs]


async def _get_favourites_by_name_config(user_id, name_config, session):
    async with session.begin():
        favourites_dal = FavouritesDAL(session)
        favourites_configs = await favourites_dal.get_favourites_by_name_config(
            user_id=user_id,
            name_config=name_config
        )
        return favourites_configs


async def _delete_yaml_config(user_id, name_config, session):
    async with session.begin():
        favourites_dal = FavouritesDAL(session)
        deleted_favourites = await favourites_dal.delete_favourites(
            user_id=user_id,
            name_config=name_config
        )
        return deleted_favourites
