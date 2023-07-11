import uuid

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from db.connect import get_db
from db.dals import ConfigDAL, FavouritesDAL
from db.models import User
from lib.login import get_current_user_from_token
from lib.methods import save_config_json, _execute_function

favourites_router = APIRouter()


@favourites_router.post("")
async def create_favourites(
        request: Request,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    info_save_config = await save_config_json(request, db)
    name_config = info_save_config['name_config']
    name_esphome = info_save_config['name_esphome']

    info_old_favourites = await _execute_function(FavouritesDAL,
                                                  FavouritesDAL.get_favourites_by_name_config,
                                                  session=db,
                                                  name_config=name_config,
                                                  user_id=current_user.user_id)
    if info_old_favourites is None:
        return await _execute_function(FavouritesDAL,
                                       FavouritesDAL.create_favourites,
                                       session=db,
                                       user_id=current_user.user_id,
                                       name_config=name_config,
                                       name_esphome=name_esphome)
    else:
        return info_old_favourites


@favourites_router.delete("")
async def delete_favourites(
        name_config: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    return await _execute_function(FavouritesDAL,
                                   FavouritesDAL.delete_favourites,
                                   session=db,
                                   user_id=current_user.user_id,
                                   name_config=name_config)


@favourites_router.get("/all")
async def get_favourites_all_by_id(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    favourites_configs = await _execute_function(FavouritesDAL,
                                                 FavouritesDAL.get_favourites_all,
                                                 session=db,
                                                 user_id=current_user.user_id)
    return [{"name_config": row[0].name_config, "name_esphome": row[0].name_esphome} for row in favourites_configs]


@favourites_router.get("/one")
async def get_favourites_json_by_id(
        name_config: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    favourites_availability = await _execute_function(FavouritesDAL,
                                                      FavouritesDAL.get_favourites_by_name_config,
                                                      session=db,
                                                      user_id=current_user.user_id,
                                                      name_config=name_config)
    if favourites_availability is None:
        raise HTTPException(status_code=404, detail=f"Favorites with the name of the {name_config} are not found.")
    info_config = await _execute_function(ConfigDAL,
                                          ConfigDAL.get_config,
                                          session=db,
                                          name_config=name_config)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'json_text': info_config.config_json}
    )


@favourites_router.post("/edit")
async def update_user_by_id(
        name_config: uuid.UUID,
        request: Request,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    await _execute_function(FavouritesDAL,
                            FavouritesDAL.delete_favourites,
                            session=db,
                            user_id=current_user.user_id,
                            name_config=name_config)
    info_save_config = await save_config_json(request, db)
    name_config = info_save_config['name_config']
    name_esphome = info_save_config['name_esphome']

    info_old_favourites = await _execute_function(FavouritesDAL,
                                                  FavouritesDAL.get_favourites_by_name_config,
                                                  session=db,
                                                  name_config=name_config,
                                                  user_id=current_user.user_id)
    if info_old_favourites is None:
        return await _execute_function(FavouritesDAL,
                                       FavouritesDAL.create_favourites,
                                       session=db,
                                       user_id=current_user.user_id,
                                       name_config=name_config,
                                       name_esphome=name_esphome)
    else:
        return info_old_favourites
