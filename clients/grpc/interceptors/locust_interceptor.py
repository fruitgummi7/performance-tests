from grpc import UnaryUnaryClientInterceptor, RpcError
import time
from locust.env import Environment

class LocustInterceptor(UnaryUnaryClientInterceptor):
    """
    gRPC-интерцептор для сбора метрик Locust.
    Используется для измерения времени выполнения вызовов и регистрации успехов/ошибок.
    """
    def __init__(self, environment: Environment):
        """
        :param environment: Экземпляр среды Locust, содержащий события сбора метрик.
        """
        self.environment = environment

    def intercept_unary_unary(self, continuation, client_call_details, request):
        """
        Метод-перехватчик для unary-unary gRPC вызовов.

        :param continuation: Функция, вызывающая фактический gRPC метод.
        :param client_call_details: Детали запроса (метод, метаданные, таймаут и т.д.).
        :param request: Объект запроса, отправляемый на сервер.
        :return: gRPC response (future объект).
        """
        response = None
        exception: RpcError | None = None
        start_time = time.perf_counter()
        response_length = 0


        try:
            response = continuation(client_call_details, request)
            response_length = response.result().ByteSize()
        except RpcError as error:
            exception = error

        self.environment.events.request.fire(
            name=client_call_details.method,
            context=None,
            response=response,
            exception=exception,
            request_type="gRPC",
            response_time=(time.perf_counter() - start_time) * 1000,
            response_length=response_length
        )

        return response