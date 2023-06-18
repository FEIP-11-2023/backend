from app.exceptions import ExceptionDescribed


class UsernameAlreadyExists(ExceptionDescribed):
    description = {
        "en": "Username already exists",
        "ru": "Имя пользователя уже существует",
    }
    code = "AU-0001"
    status_code = 400


class EmailAlreadyExists(ExceptionDescribed):
    description = {
        "en": "Email already exists",
        "ru": "Аккаунт с таким email уже существует",
    }
    code = "AU-0002"
    status_code = 400


class TokenExpired(ExceptionDescribed):
    description = {
        "en": "Token expired",
        "ru": "Токен истек",
    }
    code = "AU-0003"
    status_code = 401


class PermissionDenied(ExceptionDescribed):
    description = {
        "en": "Insufficient permissions",
        "ru": "Недостаточно прав",
    }
    code = "AU-0008"
    status_code = 401


class Unauthorized(ExceptionDescribed):
    description = {
        "en": "Unauthorized",
        "ru": "Не авторизован",
    }
    code = "AU-0004"
    status_code = 401


class InvalidCredentialsException(ExceptionDescribed):
    description = {
        "en": "Invalid credentials",
        "ru": "Неверные учетные данные",
    }
    code = "AU-0005"
    status_code = 401


class UserBlocked(ExceptionDescribed):
    description = {
        "en": "User blocked",
        "ru": "Пользователь заблокирован",
    }
    code = "AU-0006"
    status_code = 403


class RefreshTokenExpiredOrRevoked(ExceptionDescribed):
    description = {
        "en": "Refresh token expired or revoked, login please",
        "ru": "Срок действия refresh-токена истек или отозван. Войдите на сайт"
    }
    code = "AU-0007"
    status_code = 410


class RefreshTokenNotFound(ExceptionDescribed):
    description = {
        "en": "Refresh token not found",
        "ru": "Refresh токен не найден"
    }
    code = "AU-0009"
    status_code = 404
