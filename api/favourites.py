import uuid

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from db.connect import get_db
from db.models import User
from lib.favourites import _create_favourites, _get_favourites_all, _delete_yaml_config, _get_favourites_by_name_config
from lib.login import get_current_user_from_token
from lib.methods import save_config_json
from lib.config import _get_yamlconfig_by_nameyaml

favourites_router = APIRouter()


@favourites_router.post("/")
async def create_favourites(
        request: Request,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    info_save_config = await save_config_json(request, db)
    name_config = info_save_config['name_config']
    name_esphome = info_save_config['name_esphome']

    info_old_favourites = await _get_favourites_by_name_config(name_config=name_config,
                                                               user_id=current_user.user_id,
                                                               session=db)
    if info_old_favourites is None:
        return await _create_favourites(session=db,
                                        user_id=current_user.user_id,
                                        name_config=name_config,
                                        name_esphome=name_esphome)
    else:
        return info_old_favourites


@favourites_router.delete("/")
async def delete_favourites(
        name_config: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    return await _delete_yaml_config(user_id=current_user.user_id, name_config=name_config, session=db)


@favourites_router.get("/all")
async def get_favourites_all_by_id(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    return await _get_favourites_all(session=db, user_id=current_user.user_id)


@favourites_router.get("/one")
async def get_favourites_json_by_id(
        name_config: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    favourites_availability = await _get_favourites_by_name_config(user_id=current_user.user_id, name_config=name_config, session=db)
    if favourites_availability is None:
        raise HTTPException(status_code=404, detail=f"Favorites with the name of the {name_config} are not found.")
    info_config = await _get_yamlconfig_by_nameyaml(name_config=name_config, session=db)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'json_text': info_config.config_json}
    )
