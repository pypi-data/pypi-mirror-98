import dataclasses

from pykafka import KafkaClient
from typing import Optional

from polyswarmdconfig.config import Config


@dataclasses.dataclass
class Kafka(Config):
    brokers: str = ''
    broker_version: str = '1.1.1'
    use_greenlets: bool = True
    client: Optional[KafkaClient] = dataclasses.field(init=False, default=None)

    def __post_init__(self):
        if self.brokers:
            self.client = KafkaClient(hosts=self.brokers,
                                      use_greenlets=self.use_greenlets,
                                      broker_version=self.broker_version)
