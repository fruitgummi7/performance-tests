from clients.grpc.gateway.locust import GatewayGRPCSequentialTaskSet
from locust import User, between, task
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserResponse
from contracts.services.gateway.accounts.rpc_open_savings_account_pb2 import OpenSavingsAccountResponse


class GetDocumentsSequentialTaskSet(GatewayGRPCSequentialTaskSet):
    """
    Нагрузочный сценарий, который последовательно:
    1. Создаёт нового пользователя.
    2. Открывает сберегательный счёт.
    3. Получает документы по счёту (тариф и контракт).

    Использует базовый GatewayGRPCSequentialTaskSet и уже созданных в нём API клиентов.
    """
    create_user_response: CreateUserResponse | None = None
    open_savings_account_response: OpenSavingsAccountResponse | None = None

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


class GetDocumentsUser(User):
    """
    Пользователь Locust, исполняющий последовательный сценарий получения документов.
    """
    host = "localhost"
    tasks = [GetDocumentsSequentialTaskSet]
    wait_time = between(1, 3)