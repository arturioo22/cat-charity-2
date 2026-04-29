from app.crud.base import CRUDBase
from app.models.donation import Donation


class CRUDDonation(CRUDBase[Donation]):
    """CRUD для пожертвований."""


donation_crud = CRUDDonation(Donation)
