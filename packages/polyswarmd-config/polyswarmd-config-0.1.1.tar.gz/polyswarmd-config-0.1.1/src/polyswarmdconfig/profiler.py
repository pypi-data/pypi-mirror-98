import dataclasses

from typing import Optional

from polyswarmdconfig import Config


@dataclasses.dataclass
class Profiler(Config):
    enabled: bool = False
    db_uri: Optional[str] = None

    def __post_init__(self):
        if self.enabled and self.db_uri is None:
            raise ValueError('Profiler enabled, but no db uri set')
