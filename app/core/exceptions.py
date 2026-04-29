from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi_users.exceptions import FastAPIUsersException, UserInactive


async def user_not_authenticated_handler(
    request: Request,
    exc: FastAPIUsersException,
) -> JSONResponse:
    """Обработчик для неавторизованных запросов."""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Unauthorized"},
    )


async def user_inactive_handler(
    request: Request,
    exc: UserInactive,
) -> JSONResponse:
    """Обработчик для неактивного пользователя."""
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "Forbidden"},
    )
