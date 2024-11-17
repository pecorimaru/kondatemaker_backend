from sqlalchemy.orm import Session

from app.core.base_service import BaseService
from app.models.display import UserDisp
from app.crud.user_crud import UserCrud


class LoginService(BaseService):
    def __init__(self, user_id: int, db: Session):
        super().__init__(user_id, db)


    def login(self, email: str ,password: str) -> UserDisp:

        try:
            user_crud = UserCrud(None, self.db)
            user = user_crud.get_user(email)

            if user:
                if user.password == password:
                    return UserDisp.from_user(user)

            return None

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))
