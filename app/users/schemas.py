from pydantic import BaseModel, ConfigDict, EmailStr, constr


class UserCreate(BaseModel):
    """
    Модель для создания пользователя.

    Эта модель используется для валидации данных, которые пользователь отправляет
    при регистрации. Включает в себя имя пользователя, email и пароль. Все поля
    имеют ограничения по длине и должны удовлетворять определённым условиям.

    Атрибуты:
        username (str): Имя пользователя, длина которого должна быть от 3 до 20 символов.
        email (EmailStr): Электронная почта пользователя, которая должна быть в правильном формате.
        password (str): Пароль пользователя, длина которого должна быть от 5 до 20 символов.

    """

    username: constr(min_length=3, max_length=20)
    email: EmailStr
    password: constr(min_length=5, max_length=20)

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    """
    Модель для ответа при запросе данных пользователя.

    Эта модель используется для возврата информации о пользователе, такой как
    имя, email и статус активности. Она не включает в себя конфиденциальную информацию,
    такую как пароль, и предоставляет только публичные данные.

    Атрибуты:
        username (str): Имя пользователя.
        email (str): Электронная почта пользователя.
        is_active (bool): Статус активности пользователя (активен или нет).

    """

    username: str
    email: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """
    Модель для обновления информации пользователя.

    Эта модель используется для обновления данных пользователя. Поля могут быть
    переданы как `None`, что означает отсутствие изменения в этом поле.

    Атрибуты:
        username (str | None): Новое имя пользователя. Если не передано, оно не изменяется.
        email (EmailStr | None): Новый email пользователя. Если не передан, он не изменяется.

    """

    username: str | None
    email: EmailStr | None
    model_config = ConfigDict(from_attributes=True)
