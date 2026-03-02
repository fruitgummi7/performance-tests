from pydantic import BaseModel, Field, EmailStr, ConfigDict
from tools.fakers import fake
class UserSchema(BaseModel):
    """
    Описание структуры пользователя.
    """
    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")
    phone_number: str = Field(alias="phoneNumber")

class GetUserResponseSchema(BaseModel):
    """
    Описание структуры ответа получения пользователя.
    """
    user: UserSchema

class CreateUserRequestSchema(BaseModel):
    """
    Структура данных для создания нового пользователя.
    """
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    email: str = Field(default_factory=fake.email)
    last_name: str = Field(alias="lastName", default_factory=fake.last_name)
    first_name: str = Field(alias="firstName", default_factory=fake.first_name)
    middle_name: str = Field(alias="middleName", default_factory=fake.middle_name)
    phone_number: str = Field(alias="phoneNumber", default_factory=fake.phone_number)

class CreateUserResponseSchema(BaseModel):
    """
    Описание структуры ответа создания пользователя.
    """
    user: UserSchema
