import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.config import settings
from app.db.database import get_db
from app.domains.tokens.errors import InvalidAccessToken
from app.domains.users import crud as user_crud
from app.domains.users.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidAccessToken()
    except InvalidTokenError:
        raise InvalidAccessToken()

    user = user_crud.get_user_by_id(db, int(user_id))
    if user is None:
        raise InvalidAccessToken()
    return user