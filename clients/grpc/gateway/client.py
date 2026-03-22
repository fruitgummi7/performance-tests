from grpc import Channel, insecure_channel, intercept_channel
from clients.grpc.interceptors.locust_interceptor import LocustInterceptor
from locust.env import Environment


def build_gateway_grpc_client() -> Channel:
    """
    Фабричная функция (билдер) для создания gRPC-канала к сервису grpc-gateway.

    :return: gRPC-канал (Channel), настроенный на адрес localhost:9003.
    """
    return insecure_channel('localhost:9003')

def build_gateway_locust_grpc_client(environment: Environment) -> Channel:
    """
    Фабричная функция для создания gRPC-канала, адаптированного для Locust.
    В канал автоматически встраивается интерцептор LocustInterceptor,
    который регистрирует вызовы в системе метрик Locust.

    :param environment: Среда выполнения Locust (необходима для отправки событий).
    :return: gRPC-канал с интерцептором, пригодный для нагрузочного тестирования.
    """
    locust_interceptor = LocustInterceptor(environment=environment)

    channel = insecure_channel('localhost:9003')
    return intercept_channel(channel, locust_interceptor)
