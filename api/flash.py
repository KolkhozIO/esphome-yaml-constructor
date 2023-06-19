import json
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse, JSONResponse

from db.connect import get_db
from lib.config import get_config_by_name_or_hash

flash_router = APIRouter()


@flash_router.get("/{file_name}")
async def get_manifest(file_name: uuid.UUID, db: AsyncSession = Depends(get_db)):
    info_file = await get_config_by_name_or_hash(name_config=file_name, session=db)
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
    return FileResponse(bin_path)