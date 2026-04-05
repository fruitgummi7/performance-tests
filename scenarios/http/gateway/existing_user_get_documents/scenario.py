from locust import task, events
from locust.env import Environment

from clients.http.gateway.locust import GatewayHTTPTaskSet
from seeds.scenarios.existing_user_get_documents import ExistingUserGetDocumentsSeedsScenario
from seeds.schema.result import SeedUserResult
from tools.locust.user import LocustBaseUser


@events.init.add_listener
def init(environment: Environment, **kwargs):
    seeds_scenario = ExistingUserGetDocumentsSeedsScenario()
    seeds_scenario.build()
    environment.seeds = seeds_scenario.load()

class GetDocumentsTaskSet(GatewayHTTPTaskSet):
    seed_user: SeedUserResult

    def on_start(self) -> None:
        super().on_start()
        self.seed_user = self.user.environment.seeds.get_next_user()

    @task(1)
    def get_accounts(self):
        self.accounts_gateway_client.get_accounts(user_id=self.seed_user.user_id)

    @task(2)
    def get_tariff_document(self):
        self.documents_gateway_client.get_tariff_document(
            account_id=self.seed_user.savings_accounts[0].account_id
        )

    @task(2)
    def get_contract_document(self):
        self.documents_gateway_client.get_contract_document(
            account_id=self.seed_user.debit_card_accounts[0].account_id
        )


class GetDocumentsScenarioUser(LocustBaseUser):
    tasks = [GetDocumentsTaskSet]
