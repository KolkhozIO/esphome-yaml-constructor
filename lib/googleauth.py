from typing import Union

from db.dals import GoogleDAL
from db.schemas import ShowUser


async def _execute_function_with_args(func, session, *args, **kwargs):
    async with session.begin():
        dal = GoogleDAL(session)
        result = await func(dal, *args, **kwargs)
        return result


async def _create_google_auth(user_id, name, surname, email, session) -> ShowUser:
    user = await _execute_function_with_args(GoogleDAL.create_user,
                                      session,
                                      user_id=user_id,
                                      name=name,
                                      surname=surname,
                                      email=email)
    return ShowUser(
        user_id=user.user_id,
        name=user.name,
        surname=user.surname,
        email=user.email,
        is_active=user.is_active,
    )


async def _get_google_user(email, session) -> Union[ShowUser, None]:
    user = await _execute_function_with_args(GoogleDAL.get_google_user,
                                             session,
                                             email=email)
    if user is not None:
        return ShowUser(
            user_id=user.user_id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_active=user.is_active,
        )
