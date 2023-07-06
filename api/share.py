import os
import uuid

from fastapi import APIRouter, status, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from db.connect import get_db
from db.dals import ConfigDAL
from db.schemas import ShareConfigResponse
from lib.methods import save_config_json, _execute_function_config

share_router = APIRouter()


@share_router.post("", status_code=status.HTTP_201_CREATED)
async def create_share_file(request: Request, db: AsyncSession = Depends(get_db)):
    name_config = (await save_config_json(request, db))['name_config']
    return ShareConfigResponse(uuid=name_config, url=f"{os.environ.get('REACT_APP_APP_URL')}/config?uuid={name_config}")
    # return ShareConfigResponse(uuid=name_config, url=url)


@share_router.get("", status_code=status.HTTP_200_OK)
async def get_share_file(file_name:uuid.UUID, db: AsyncSession = Depends(get_db)):
    # fetches json from database and returns it
    info_file = await _execute_function_config(ConfigDAL.get_config,
                                               session=db,
                                               name_config=file_name)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'json_text': info_file.config_json}
    )
