from datetime import timedelta

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

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
    if req is None or req == 'null':
        return JSONResponse(
            status_code=404,
            content={"message": f"No user information received from google"},
        )

    required_keys = ['googleId', 'familyName', 'givenName', 'email']
    missing_keys = [key for key in required_keys if key not in req]
    if missing_keys:
        return JSONResponse(
            status_code=404,
            content={"message": f"Missing required keys: {', '.join(missing_keys)}"},
        )

    user = await _get_google_user(email=req['email'], session=db)
    if user is None:
        user = await _create_google_auth(user_id=req['googleId'], name=req['familyName'], surname=req['givenName'], email=req['email'], session=db)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
