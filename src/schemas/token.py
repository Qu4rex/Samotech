from pydantic import BaseModel


class Token(BaseModel):
    """Модель токена для ответа API."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Содержимое JWT, которое мы читаем при проверке."""

    sub: str
    exp: int