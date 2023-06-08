import os

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.favourites import favourites_router
from api.flash import flash_router
from api.login import login_router
from api.share import share_router
from api.user import user_router
from api.config import config_router

app = FastAPI()

origins = [os.environ.get('REACT_APP_APP_URL')]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(login_router, prefix="/login", tags=["login"])
app.include_router(share_router, prefix="/share", tags=["share"])
app.include_router(config_router, prefix="/config", tags=["config"])
app.include_router(flash_router, prefix="/manifest", tags=["flash"])
app.include_router(favourites_router, prefix="/favourites", tags=["favourites_router"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
