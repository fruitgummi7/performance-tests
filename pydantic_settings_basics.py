from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, EmailStr, SecretStr, HttpUrl


class TestUser(BaseModel):
    email: EmailStr
    password: SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.basics",
        env_file_encoding="utf-8",
        env_nested_delimiter="."
    )

    base_url: HttpUrl
    test_user: TestUser


print(Settings())