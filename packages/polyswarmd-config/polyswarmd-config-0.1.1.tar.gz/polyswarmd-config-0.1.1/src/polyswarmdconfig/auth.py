import dataclasses

from typing import Optional

from polyswarmdconfig.config import Config


@dataclasses.dataclass
class Auth(Config):
    uri: Optional[str] = None

    @property
    def require_api_key(self):
        return self.uri is not None
