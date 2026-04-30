"""Константы для приложения QRKot."""

# Константы для валидации названия проекта
NAME_MIN_LENGTH: int = 5
NAME_LENGTH: int = 100

# Константы для валидации описания проекта
DESCRIPTION_MIN_LENGTH: int = 10

# Константы для валидации сумм
FULL_AMOUNT_MIN_VALUE: int = 1
INVESTED_AMOUNT_DEFAULT: int = 0

# Константы для валидации пароля
MIN_PASSWORD_LENGTH: int = 3

# Константы для JWT
JWT_LIFETIME_SECONDS: int = 3600

# Константы для модели User
USER_EMAIL_MAX_LENGTH: int = 320
USER_PASSWORD_HASH_MAX_LENGTH: int = 1024