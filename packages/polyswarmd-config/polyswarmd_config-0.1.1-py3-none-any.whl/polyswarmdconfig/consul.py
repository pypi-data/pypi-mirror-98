import dataclasses

from urllib.parse import urlparse
from consul import Consul as ConsulClient
from typing import Optional

from polyswarmdconfig.config import Config


@dataclasses.dataclass
class Consul(Config):
    uri: str
    token: Optional[str] = None
    client: ConsulClient = dataclasses.field(init=False)

    def __post_init__(self):
        u = urlparse(self.uri)
        self.client = ConsulClient(host=u.hostname, port=u.port, scheme=u.scheme, token=self.token)
