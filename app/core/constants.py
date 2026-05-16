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

# Константы времени
SECONDS_IN_MINUTE: int = 60
SECONDS_IN_HOUR: int = 3600

# Константы для JWT
JWT_LIFETIME_SECONDS: int = SECONDS_IN_HOUR

# Константы для модели User
USER_EMAIL_MAX_LENGTH: int = 320
USER_PASSWORD_HASH_MAX_LENGTH: int = 1024

# Константы для Google API
GOOGLE_SHEETS_SCOPE: str = "https://www.googleapis.com/auth/spreadsheets"
GOOGLE_DRIVE_SCOPE: str = "https://www.googleapis.com/auth/drive.file"
GOOGLE_AUTH_URI: str = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URI: str = "https://oauth2.googleapis.com/token"
GOOGLE_AUTH_PROVIDER_X509_CERT_URL: str = (
    "https://www.googleapis.com/oauth2/v1/certs"
)

# Шаблон для создания таблицы
GOOGLE_SPREADSHEET_BODY_TEMPLATE: dict = {
    "properties": {
        "title": "",
    }
}