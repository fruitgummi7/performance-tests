from locust import SequentialTaskSet, task

from clients.grpc.gateway.locust import GatewayGRPCSequentialTaskSet
from contracts.services.gateway.accounts.rpc_open_debit_card_account_pb2 import OpenDebitCardAccountResponse
from contracts.services.gateway.cards.rpc_issue_physical_card_pb2 import IssuePhysicalCardResponse
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserResponse
from tools.locust.user import LocustBaseUser

class IssuePhysicalCardSequentialTaskSet(GatewayGRPCSequentialTaskSet):
    create_user_response: CreateUserResponse | None = None
    open_debit_card_account_response: OpenDebitCardAccountResponse | None = None
    issue_physical_card_response: IssuePhysicalCardResponse | None = None

    @task
    def create_user(self):
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_debit_card_account(self):
        if not self.create_user_response:
            return

        self.open_debit_card_account_response = self.accounts_gateway_client.open_debit_card_account(
            user_id=self.create_user_response.user.id
        )

    @task
    def issue_physical_card(self):
        if (not self.create_user_response) or (not self.open_debit_card_account_response):
            return

        self.cards_gateway_client.issue_physical_card(
            user_id=self.create_user_response.user.id,
            account_id=self.open_debit_card_account_response.account.id
        )

class IssuePhysicalCardScenarioUser(LocustBaseUser):
    tasks = [IssuePhysicalCardSequentialTaskSet]