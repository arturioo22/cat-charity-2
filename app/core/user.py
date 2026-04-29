from fastapi_users import FastAPIUsers
from fastapi_users.exceptions import FastAPIUsersException, UserInactive

from app.core.auth import auth_backend, get_user_manager
from app.core.exceptions import (user_inactive_handler,
                                 user_not_authenticated_handler)
from app.models.user import User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

fastapi_users.user_not_authenticated_exception_handler = (
    user_not_authenticated_handler
)
fastapi_users.user_inactive_exception_handler = user_inactive_handler

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

__all__ = [
    "current_user",
    "current_superuser",
    "fastapi_users",
]
