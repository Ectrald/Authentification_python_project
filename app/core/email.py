from email.message import EmailMessage

import aiosmtplib

from app.config import settings


async def send_verification_email(email: str, token: str) -> None:
    verification_url = f"{settings.frontend_url}/verify?token={token}"

    message = EmailMessage()
    message["From"] = settings.smtp_from
    message["To"] = email
    message["Subject"] = "Подтверждение регистрации"
    message.set_content(
        f"Перейдите по ссылке для подтверждения почты:\n{verification_url}"
    )

    await aiosmtplib.send(
        message,
        hostname=settings.smtp_host,
        port=settings.smtp_port,
        username=settings.smtp_user,
        password=settings.smtp_password,
        use_tls=False,
        start_tls=True,
    )
