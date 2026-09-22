from sqlalchemy.orm import Session

from app.core.security import get_hashed_password
from app.domains.users.models import User
from app.domains.users.schemas import UserCreate


def create_user(db: Session, user_data: UserCreate) -> User:
    user = User(
        username=user_data.username,
        email=user_data.email,
        password=get_hashed_password(user_data.password),
    )
    db.add(user)
    db.flush()
    return user


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email.lower()).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def verify_user(db: Session, user: User) -> None:
    user.is_verified = True
    db.commit()
