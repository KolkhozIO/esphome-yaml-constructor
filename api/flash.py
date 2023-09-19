import json
import os
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse, JSONResponse

from db.connect import get_db
from db.dals import ConfigDAL
from lib.methods import _execute_function

flash_router = APIRouter()


@flash_router.get("/{file_name}")
async def get_manifest(file_name: uuid.UUID, db: AsyncSession = Depends(get_db)):
    info_file = await _execute_function(ConfigDAL,
                                        ConfigDAL.get_config,
                                        session=db,
                                        name_config=file_name)
    if info_file is None:
        return JSONResponse(
            status_code=404,
            content={"message": f"A configuration with that name has not yet been compiled."},
        )
    platform = info_file.platform
    bin_path = f"/manifest/bin/{file_name}.bin"
    with open("manifest.json", 'r') as file:
        data = json.load(file)
    data['builds'][0]['chipFamily'] = platform
    data['builds'][0]['parts'][0]['path'] = bin_path
    return JSONResponse(content=data, media_type="application/json")


@flash_router.get("/bin/{file_name}.bin")
async def get_manifest(file_name: str):
    bin_path = f"./compile_files/{file_name}.bin"
    if not os.path.exists(bin_path):
        return JSONResponse(
            status_code=404,
            content={
                'message': 'The manifest contains a path to a file that does not exist.'
            }
        )
    return FileResponse(bin_path)
