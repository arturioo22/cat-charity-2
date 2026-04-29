from datetime import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_full_amount_can_be_updated,
                                check_project_can_be_deleted,
                                check_project_exists,
                                check_project_name_unique,
                                check_project_not_closed)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.models.donation import Donation
from app.models.user import User
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import invest_after_create

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    "/charity_project/",
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(session: SessionDep):
    """Показать список всех целевых проектов."""
    return await charity_project_crud.get_all(session)


@router.post(
    "/charity_project/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    status_code=HTTPStatus.OK,
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: SessionDep,
    user: User = Depends(current_superuser),
):
    """Создать целевой проект."""
    existing_project = await charity_project_crud.get_by_name(
        project.name, session
    )
    check_project_name_unique(existing_project)

    new_project = await charity_project_crud.create(
        obj_data=project.model_dump(),
        session=session,
        commit=False,
    )

    donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested.is_(False)
        ).order_by(Donation.create_date)
    )
    sources = donations.scalars().all()

    changed_objects = invest_after_create(new_project, sources)

    if changed_objects:
        session.add_all(changed_objects)

    await session.commit()
    await session.refresh(new_project)

    return new_project


@router.patch(
    "/charity_project/{project_id}",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def update_charity_project(
    project_id: int,
    project_update: CharityProjectUpdate,
    session: SessionDep,
    user: User = Depends(current_superuser),
):
    """Редактировать целевой проект."""
    project_db = await charity_project_crud.get_by_id(project_id, session)

    project = check_project_exists(project_db)

    check_project_not_closed(project)

    update_data = project_update.model_dump(exclude_unset=True)

    if "name" in update_data:
        existing_project = await charity_project_crud.get_by_name(
            update_data["name"], session
        )
        if existing_project and existing_project.id != project_id:
            check_project_name_unique(existing_project)

    if "full_amount" in update_data:
        check_full_amount_can_be_updated(
            update_data["full_amount"],
            project.invested_amount
        )

    updated_project = await charity_project_crud.update(
        project, update_data, session, commit=False
    )

    if updated_project.invested_amount >= updated_project.full_amount:
        updated_project.fully_invested = True
        updated_project.close_date = datetime.now()

    await session.commit()
    await session.refresh(updated_project)

    return updated_project


@router.delete(
    "/charity_project/{project_id}",
    response_model=CharityProjectDB,
)
async def delete_charity_project(
    project_id: int,
    session: SessionDep,
    user: User = Depends(current_superuser),
):
    """Удалить целевой проект."""
    project_db = await charity_project_crud.get_by_id(project_id, session)

    project = check_project_exists(project_db)

    check_project_can_be_deleted(project)

    await charity_project_crud.delete(project, session)

    return project
