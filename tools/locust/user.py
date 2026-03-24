from locust import User, between


class LocustBaseUser(User):
    """
    Базовый виртуальный пользователь Locust, от которого наследуются все сценарии.
    Содержит общие настройки, которые могут быть переопределены при необходимости.
    """
    host = "localhost"
    abstract = True
    wait_time = between(1, 3)