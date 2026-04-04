from clients.http.gateway.accounts.schema import OpenSavingsAccountResponseSchema
from clients.http.gateway.locust import GatewayHTTPSequentialTaskSet
from locust import task

from clients.http.gateway.users.schema import CreateUserResponseSchema
from tools.locust.user import LocustBaseUser


class GetDocumentsSequentialTaskSet(GatewayHTTPSequentialTaskSet):
    """
    Нагрузочный сценарий, который последовательно:
    1. Создаёт нового пользователя.
    2. Открывает сберегательный счёт.
    3. Получает документы по счёту (тариф и контракт).

    Использует базовый GatewayHTTPSequentialTaskSet и уже созданных в нём API клиентов.
    """
    create_user_response: CreateUserResponseSchema | None = None
    open_savings_account_response: OpenSavingsAccountResponseSchema | None = None

    @task
    def create_user(self):
        self.create_user_response = self.users_gateway_client.create_user()

    def open_savings_account(self):
        if not self.create_user_response:
            return

        self.open_savings_account_response = self.accounts_gateway_client.open_savings_account(
            user_id=self.create_user_response.user.id,
        )

    def get_documents(self):
        if not self.open_savings_account_response:
            return

        self.documents_gateway_client.get_tariff_document(
            account_id=self.open_savings_account_response.account.id
        )
        self.documents_gateway_client.get_contract_document(
            account_id=self.open_savings_account_response.account.id
        )


class GetDocumentsUser(LocustBaseUser):
    """
    Пользователь Locust, исполняющий последовательный сценарий получения документов.
    """
    tasks = [GetDocumentsSequentialTaskSet]