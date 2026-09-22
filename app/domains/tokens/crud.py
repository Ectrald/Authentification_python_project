from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.config import settings
from app.core.security import generate_token
from app.domains.tokens.models import VerificationToken


def create_verification_token(db: Session, user_id: int) -> VerificationToken:
    token = VerificationToken(
        user_id=user_id,
        token=generate_token(),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=settings.token_expire_minutes),
    )
    db.add(token)
    db.flush()
    return token


def invalidate_user_tokens(db: Session, user_id: int) -> None:
    db.query(VerificationToken).filter(
        VerificationToken.user_id == user_id,
        VerificationToken.is_used == False,
    ).update({VerificationToken.is_used: True})


def get_valid_token(db: Session, token: str) -> VerificationToken | None:
    return (
        db.query(VerificationToken)
        .filter(
            VerificationToken.token == token,
            VerificationToken.is_used == False,
            VerificationToken.expires_at > datetime.now(timezone.utc),
        )
        .first()
    )


def mark_token_used(db: Session, token: VerificationToken) -> None:
    token.is_used = True
    db.commit()
