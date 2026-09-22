from app.core.exception_handlers import AppError


class UserError(AppError):
    pass


class EmailAlreadyRegistered(UserError):
    status_code = 400
    detail = "Email уже зарегистрирован"


class UsernameAlreadyTaken(UserError):
    status_code = 400
    detail = "Username уже занят"


class UserNotFound(UserError):
    status_code = 404
    detail = "Пользователь не найден"


class InvalidCredentials(UserError):
    status_code = 401
    detail = "Неверный username/email или пароль"
    headers = {"WWW-Authenticate": "Bearer"}


class EmailNotVerified(UserError):
    status_code = 403
    detail = "Подтвердите почту, перейдя по ссылке из письма"


class EmailSendFailed(UserError):
    status_code = 502
    detail = "Не удалось отправить письмо. Проверьте адрес и попробуйте ещё раз"