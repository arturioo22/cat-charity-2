from fastapi import APIRouter

from app.api.endpoints import charity_project, donation
from app.core.auth import auth_backend
from app.core.user import fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

main_router = APIRouter()

main_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
main_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

users_router = fastapi_users.get_users_router(UserRead, UserUpdate)

users_router.routes = [
    route for route in users_router.routes
    if "DELETE" not in route.methods
]

main_router.include_router(
    users_router,
    prefix="/users",
    tags=["users"],
)

main_router.include_router(
    charity_project.router,
    tags=["charity_projects"],
)
main_router.include_router(
    donation.router,
    tags=["donations"],
)
