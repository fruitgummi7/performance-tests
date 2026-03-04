import grpc
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserRequest, CreateUserResponse
from contracts.services.gateway.users.users_gateway_service_pb2_grpc import UsersGatewayServiceStub

from contracts.services.gateway.accounts.rpc_open_credit_card_account_pb2 import (
    OpenCreditCardAccountRequest,
    OpenCreditCardAccountResponse
)
from contracts.services.gateway.accounts.accounts_gateway_service_pb2_grpc import AccountsGatewayServiceStub

from contracts.services.gateway.operations.operations_gateway_service_pb2_grpc import OperationsGatewayServiceStub
from contracts.services.gateway.operations.rpc_make_purchase_operation_pb2 import (
    MakePurchaseOperationRequest, MakePurchaseOperationResponse
)
from contracts.services.operations.operation_pb2 import OperationStatus

from tools.fakers import fake

channel = grpc.insecure_channel('localhost:9003')

users_gateway_service = UsersGatewayServiceStub(channel)
accounts_gateway_service = AccountsGatewayServiceStub(channel)
operations_gateway_service = OperationsGatewayServiceStub(channel)

create_user_request = CreateUserRequest(
    email=fake.email(),
    first_name=fake.first_name(),
    last_name=fake.last_name(),
    middle_name=fake.middle_name(),
    phone_number=fake.phone_number()
)
create_user_response: CreateUserResponse = users_gateway_service.CreateUser(create_user_request)
print("Create user response:", create_user_response)

open_credit_card_account_request = OpenCreditCardAccountRequest(user_id=create_user_response.user.id)
open_credit_card_account_response: OpenCreditCardAccountResponse = (
    accounts_gateway_service.OpenCreditCardAccount(open_credit_card_account_request)
)
print("Open credit card account response:", open_credit_card_account_response)

make_purchase_operation_request = MakePurchaseOperationRequest(
    account_id=open_credit_card_account_response.account.id,
    amount=fake.amount(),
    card_id=open_credit_card_account_response.account.cards[0].id,
    category=fake.category(),
    status=OperationStatus.OPERATION_STATUS_IN_PROGRESS
)
make_purchase_operation_response: MakePurchaseOperationResponse = (
    operations_gateway_service.MakePurchaseOperation(make_purchase_operation_request)
)
print("Make purchase operation response:", make_purchase_operation_response)