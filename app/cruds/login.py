from sqlalchemy.orm import Session

from app.entities.user import User
from app.schemas.user import UserDTO
from app.utils.password import verify_password


async def get_user_by_id(db: Session, user_id: str):
    user = db.query(User).filter(User.userid == user_id).first()
    if user:
        return UserDTO.from_orm(user)
    else:
        return "None"


def authenticate_user(plain_password: str, hashed_password: str) -> bool:
    return verify_password(plain_password, hashed_password)