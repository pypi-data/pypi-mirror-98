from redis import Redis
from typing import Optional, Any

from arsene.schemas.redis import RedisModel
from arsene.connection.base import Base


class RedisConnection(Base):
    def __init__(
        self, *, schema: RedisModel,
        **base_kwargs: Any
    ) -> None:
        self.schema = schema
        self.status = False
        self.client = self.create_client()
        super().__init__(**base_kwargs)

    def create_client(self):
        return Redis(
            **self.schema.dict()
        )

    def test_connection(self) -> None:
        self.client.ping()
        self.status = True

    def set(self, *, key: str, expire: Optional[int] = None, data) -> None:
        data_convert = self.set_data(
            data, serializable=self.json_serial
        )
        self.client.set(key, data_convert, ex=expire)

    def get(self, *, key: str):
        if not self.client.get(key):
            return None

        data_convert = self.client.get(key).decode('utf-8')
        return self.resolve_data(
            data_convert, object_hook=self.object_hook
        )

    def delete(self, *, key: str) -> None:
        self.client.delete(key)
