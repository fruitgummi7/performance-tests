from locust import User, between, task

from tools.fakers import fake
from clients.http.gateway.users.client import build_users_gateway_locust_http_client, UsersGatewayHTTPClient
from clients.http.gateway.users.schema import CreateUserResponseSchema


class GetUserScenarioUser(User):
    host = "localhost"
    wait_time = between(1, 3)

    users_gateway_client: UsersGatewayHTTPClient
    create_user_response: CreateUserResponseSchema


    def on_start(self) -> None:
        self.users_gateway_client = build_users_gateway_locust_http_client(self.environment)

        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def get_user(self):
        self.users_gateway_client.get_user(self.create_user_response.user.id)

