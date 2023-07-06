from datetime import timedelta

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

import settings
from db.connect import get_db
from db.dals import GoogleDAL
from db.schemas import Token
from lib.login import create_access_token
from lib.methods import _execute_function_google

google_router = APIRouter()


@google_router.post("/login", response_model=Token)
async def google_login(
        request: Request, db: AsyncSession = Depends(get_db)
):
    req = await request.json()
    user = await _execute_function_google(GoogleDAL.get_google_user,
                                          session=db,
                                          email=req['email'])
    if user is None:
        user = await _execute_function_google(GoogleDAL.create_user,
                                              session=db,
                                              user_id=req['googleId'],
                                              name=req['familyName'],
                                              surname=req['givenName'],
                                              email=req['email'])
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
