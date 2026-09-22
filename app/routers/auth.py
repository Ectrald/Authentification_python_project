import aiosmtplib
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.email import send_verification_email
from app.core.security import create_access_token, verify_password
from app.db.database import get_db
from app.domains.tokens import crud as token_crud
from app.domains.tokens.errors import InvalidVerificationToken
from app.domains.tokens.schemas import (
    ResendRequest,
    TokenResponse,
    TokenVerify,
    VerifyResponse,
)
from app.domains.users import crud as user_crud
from app.domains.users.errors import (
    EmailAlreadyRegistered,
    EmailNotVerified,
    EmailSendFailed,
    InvalidCredentials,
    UsernameAlreadyTaken,
    UserNotFound,
)
from app.domains.users.models import User
from app.domains.users.schemas import UserCreate

router = APIRouter(tags=["auth"])


@router.post("/register", status_code=201)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if user_crud.get_user_by_email(db, user_data.email):
        raise EmailAlreadyRegistered()

    if user_crud.get_user_by_username(db, user_data.username):
        raise UsernameAlreadyTaken()

    user = user_crud.create_user(db, user_data)
    token = token_crud.create_verification_token(db, user.id)

    try:
        await send_verification_email(user.email, token.token)
    except (aiosmtplib.SMTPException, OSError):
        db.rollback()
        raise EmailSendFailed()

    db.commit()
    db.refresh(user)

    return {"message": "Пользователь создан. Проверьте почту для подтверждения."}


@router.post("/resend-verification")
async def resend_verification(body: ResendRequest, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, body.email)
    if not user:
        raise UserNotFound()

    if user.is_verified:
        return {"message": "Почта уже подтверждена"}

    token_crud.invalidate_user_tokens(db, user.id)
    token = token_crud.create_verification_token(db, user.id)

    try:
        await send_verification_email(user.email, token.token)
    except (aiosmtplib.SMTPException, OSError):
        db.rollback()
        raise EmailSendFailed()

    db.commit()

    return {"message": "Письмо с подтверждением отправлено повторно"}


@router.post("/verify-email", response_model=VerifyResponse)
def verify_email(body: TokenVerify, db: Session = Depends(get_db)):
    token = token_crud.get_valid_token(db, body.token)
    if not token:
        raise InvalidVerificationToken()

    user = db.query(User).filter(User.id == token.user_id).first()
    if not user:
        raise UserNotFound()

    user_crud.verify_user(db, user)
    token_crud.mark_token_used(db, token)

    access_token = create_access_token(subject=user.id)
    return VerifyResponse(
        message="Почта подтверждена. Вы авторизованы.",
        access_token=access_token,
    )


@router.post("/token", response_model=TokenResponse)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = user_crud.get_user_by_username(db, form_data.username) or user_crud.get_user_by_email(
        db, form_data.username
    )
    if not user or not verify_password(form_data.password, user.password):
        raise InvalidCredentials()

    if not user.is_verified:
        raise EmailNotVerified()

    access_token = create_access_token(subject=user.id)
    return TokenResponse(access_token=access_token)
