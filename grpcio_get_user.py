import grpc
from contracts.services.gateway.users.rpc_get_user_pb2 import GetUserRequest, GetUserResponse
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserRequest, CreateUserResponse
from contracts.services.gateway.users.users_gateway_service_pb2_grpc import UsersGatewayServiceStub
from tools.fakers import fake


channel = grpc.insecure_channel('localhost:9003')
users_gateway_service = UsersGatewayServiceStub(channel)


create_user_request = CreateUserRequest(
    email=fake.email(),
    first_name=fake.first_name(),
    last_name=fake.last_name(),
    middle_name=fake.middle_name(),
    phone_number=fake.phone_number(),
)
create_user_response: CreateUserResponse = users_gateway_service.CreateUser(create_user_request)
print("Create user response:", create_user_response)

get_user_request = GetUserRequest(id=create_user_response.user.id)
get_user_response: GetUserResponse = users_gateway_service.GetUser(get_user_request)
print("Get user response:", get_user_response)

