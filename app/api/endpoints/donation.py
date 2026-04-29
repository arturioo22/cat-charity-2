from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import charity_project_crud, donation_crud
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB, DonationFullInfoDB
from app.services.investment import invest_after_create

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    "/donation/",
    response_model=list[DonationFullInfoDB],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: SessionDep,
    user: User = Depends(current_superuser),
):
    """
    Показать список всех пожертвований.
    Только для суперюзеров.
    """
    return await donation_crud.get_all(session)


@router.get(
    "/donation/my",
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_user_donations(
    session: SessionDep,
    user: User = Depends(current_user),
):
    """
    Показать список пожертвований текущего пользователя.
    Только для зарегистрированных пользователей.
    """
    result = await session.execute(
        select(Donation).where(Donation.user_id == user.id)
    )
    return result.scalars().all()


@router.post(
    "/donation/",
    response_model=DonationDB,
    response_model_exclude_none=True,
    status_code=HTTPStatus.OK,
)
async def create_donation_endpoint(
    donation: DonationCreate,
    session: SessionDep,
    user: User = Depends(current_user),
):
    """
    Сделать пожертвование.
    Только для зарегистрированных пользователей.
    """
    donation_data = donation.model_dump()
    donation_data["user_id"] = user.id

    new_donation = await donation_crud.create(
        obj_data=donation_data,
        session=session,
        commit=False,
    )

    projects = await charity_project_crud.get_not_fully_invested(session)

    changed_objects = invest_after_create(new_donation, projects)

    if changed_objects:
        session.add_all(changed_objects)

    await session.commit()
    await session.refresh(new_donation)

    return new_donation
