import uuid

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.connect import get_db
from db.models import User
from db.schemas import ShowUser, UserCreate, DeleteUserResponse, UpdatedUserResponse, UpdateUserRequest
from lib.login import get_current_user_from_token
from lib.user import _create_new_user, _delete_user, _get_user_by_id, _update_user

user_router = APIRouter()


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    return await _create_new_user(body=body, session=db)


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
) -> DeleteUserResponse:

    deleted_user_id = await _delete_user(user_id=current_user.user_id, session=db)
    if deleted_user_id is None:
        raise HTTPException(status_code=404, detail=f"User with id {current_user.user_id} is not found.")
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(
        user_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
) -> ShowUser:

    user = await _get_user_by_id(user_id=user_id, session=db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return user


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
        user_id: uuid.UUID,
        body: UpdateUserRequest,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
) -> UpdatedUserResponse:

    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(status_code=422, detail="At least one parameter for user update info should be provided")
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    updated_user_id = await _update_user(updated_user_params=updated_user_params, session=db, user_id=user_id)
    return UpdatedUserResponse(updated_user_id=updated_user_id)