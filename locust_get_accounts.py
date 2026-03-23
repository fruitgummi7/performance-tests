from clients.http.gateway.locust import GatewayHTTPTaskSet
from locust import User, between, task
from clients.http.gateway.users.schema import CreateUserResponseSchema

class GetAccountsTaskSet(GatewayHTTPTaskSet):
    create_user_response: CreateUserResponseSchema | None = None

    @task(2)
    def create_user(self):
        self.create_user_response = self.users_gateway_client.create_user()

    @task(2)
    def open_deposit_account(self):
        if not self.create_user_response:
            return
        self.accounts_gateway_client.open_deposit_account(
            user_id=self.create_user_response.user.id,
        )

    @task(6)
    def get_accounts(self):
        if not self.create_user_response:
            return
        self.accounts_gateway_client.get_accounts(
            user_id=self.create_user_response.user.id,
        )



class GetAccountsUser(User):
    host = "localhost"
    tasks = [GetAccountsTaskSet]
    wait_time = between(1, 2)