import grpc.experimental.gevent as grpc_gevent
from grpc import Channel


grpc_gevent.init_gevent()

class GRPCClient:
    """
    Базовый класс gRPC-клиента.

    Этот класс хранит общий канал (Channel) для связи с gRPC-сервером.
    От него будут наследоваться все остальные специфические клиенты.
    """
    def __init__(self, channel: Channel):
        """
        Конструктор базового клиента.

        :param channel: gRPC-канал, через который происходит подключение к серверу.
        Обычно создаётся один раз и переиспользуется.
        """
        self.channel = channel