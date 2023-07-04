import os
import uuid

from fastapi import APIRouter, status, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from db.connect import get_db
from db.schemas import ShareConfigResponse
from lib.methods import save_config_json
from lib.config import get_config_by_name_or_hash

share_router = APIRouter()


@share_router.post("", status_code=status.HTTP_201_CREATED)
async def create_share_file(request: Request, db: AsyncSession = Depends(get_db)):
    info_config = await save_config_json(request, db)
    name_config = info_config['name_config']
    url_front = os.environ.get('REACT_APP_APP_URL')
    url = f"{url_front}/config?uuid={name_config}"
    return ShareConfigResponse(uuid=name_config, url=url)


@share_router.get("", status_code=status.HTTP_200_OK)
async def get_share_file(file_name:uuid.UUID, db: AsyncSession = Depends(get_db)):
    # fetches json from database and returns it
    info_file = await get_config_by_name_or_hash(name_config=file_name, session=db)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'json_text': info_file.config_json}
    )
