from datetime import datetime
from typing import Any


def invest_after_create(
    target: Any,
    sources: list[Any],
) -> list[Any]:
    """Инвестирует средства из источников в цель или наоборот."""
    changed_objects = []

    for source in sources:
        target_need = target.full_amount - target.invested_amount
        source_available = source.full_amount - source.invested_amount

        if target_need <= 0:
            break

        investment = min(target_need, source_available)

        source.invested_amount += investment
        target.invested_amount += investment

        if source.invested_amount >= source.full_amount:
            source.fully_invested = True
            source.close_date = datetime.now()
            changed_objects.append(source)

        if target.invested_amount >= target.full_amount:
            target.fully_invested = True
            target.close_date = datetime.now()
            changed_objects.append(target)
            break

    if target.fully_invested and target not in changed_objects:
        changed_objects.append(target)

    return changed_objects
