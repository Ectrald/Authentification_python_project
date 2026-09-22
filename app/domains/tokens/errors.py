from app.core.exception_handlers import AppError


class TokenError(AppError):
    pass


class InvalidVerificationToken(TokenError):
    status_code = 400
    detail = "Неверный или просроченный токен"


class InvalidAccessToken(TokenError):
    status_code = 401
    detail = "Не удалось проверить токен"
    headers = {"WWW-Authenticate": "Bearer"}