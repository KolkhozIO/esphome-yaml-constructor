from typing import Union

from db.dals import GoogleDAL
from db.schemas import ShowUser


async def _create_google_auth(user_id, name, surname, email, session) -> ShowUser:
    async with session.begin():
        user_dal = GoogleDAL(session)
        user = await user_dal.create_user(
            user_id=user_id,
            name=name,
            surname=surname,
            email=email
        )
        return ShowUser(
            user_id=user.user_id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_active=user.is_active,
        )


async def _get_google_user(email, session) -> Union[ShowUser, None]:
    async with session.begin():
        user_dal = GoogleDAL(session)
        user = await user_dal.get_google_user(
            email=email,
        )
        if user is not None:
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active,
            )
