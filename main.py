import os

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.favourites import favourites_router
from api.flash import flash_router
from api.googleauth import google_router
from api.share import share_router
from api.config import config_router

app = FastAPI()

origins = [os.environ.get('REACT_APP_APP_URL')]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(share_router, prefix="/share", tags=["share"])
app.include_router(config_router, prefix="/config", tags=["config"])
app.include_router(flash_router, prefix="/manifest", tags=["flash"])
app.include_router(favourites_router, prefix="/favourites", tags=["favourites_router"])
app.include_router(google_router, prefix="/google", tags=["google auth"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
