from typing import Optional
from app.utils.api_utils import CamelModel
from app.models import User


class UserDisp(CamelModel):
    user_id: Optional[int]=None
    user_nm: str

    @classmethod
    def from_user(cls, user: User):
        return cls(
            user_id = user.user_id,
            user_nm = user.user_nm,
        )