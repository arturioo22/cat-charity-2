from http import HTTPStatus

from fastapi import HTTPException

from app.models.charity_project import CharityProject


def check_project_exists(project: CharityProject | None) -> CharityProject:
    """Проверить существование проекта."""
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Проект не найден"
        )
    return project


def check_project_not_closed(project: CharityProject) -> None:
    """Проверить, что проект не закрыт."""
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!"
        )


def check_project_name_unique(project: CharityProject | None) -> None:
    """Проверить уникальность имени проекта."""
    if project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект с таким именем уже существует!"
        )


def check_project_can_be_deleted(project: CharityProject) -> None:
    """Проверить, что проект можно удалить."""
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!"
        )


def check_full_amount_can_be_updated(
    new_full_amount: int,
    invested_amount: int,
) -> None:
    """Проверить, что значение full_amount не меньше уже вложенной суммы."""
    if new_full_amount < invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                "Нельзя установить значение full_amount "
                "меньше уже вложенной суммы."
            )
        )
