from pydantic import BaseModel, HttpUrl


class HTTPClientConfig(BaseModel):
    url: HttpUrl
    timeout: float = 100.0

    @property
    def client_url(self) -> str:
        return str(self.url)