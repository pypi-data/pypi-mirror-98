import dataclasses

from redis import Redis as RedisClient
from typing import Optional

from polyswarmdconfig.config import Config


@dataclasses.dataclass
class Redis(Config):
    uri: Optional[str] = None
    client: Optional[RedisClient] = dataclasses.field(init=False, default=None)

    def __post_init__(self):

        if self.uri:
            self.client = RedisClient.from_url(self.uri)
