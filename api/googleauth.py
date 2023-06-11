from datetime import timedelta

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

import settings
from db.connect import get_db
from db.schemas import Token
from lib.googleauth import _create_google_auth, _get_google_user
from lib.login import create_access_token

google_router = APIRouter()


@google_router.post("/login", response_model=Token)
async def google_login(
        request: Request, db: AsyncSession = Depends(get_db)
):
    req = await request.json()
    user = await _get_google_user(email=req['email'], session=db)
    if user is None:
        user = await _create_google_auth(user_id=req['googleId'], name=req['familyName'], surname=req['givenName'], email=req['email'], session=db)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
