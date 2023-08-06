import importlib
from typing import Any, List

import dataclasses
from polyswarmdconfig.artifactclient import AbstractArtifactServiceClient
from polyswarmdconfig.config import Config


DEFAULT_FALLBACK_SIZE = 10 * 1024 * 1024


class ClassModuleLoader:
    module_name: str
    class_name: str

    def __init__(self, module_name: str, class_name: str):
        self.module_name = module_name
        self.class_name = class_name

    def load(self):
        client_module = importlib.import_module(self.module_name)
        return getattr(client_module, self.class_name)


@dataclasses.dataclass
class Library(Config):
    module: str
    class_name: str
    args: List[Any] = dataclasses.field(default_factory=list)
    client: AbstractArtifactServiceClient = dataclasses.field(init=False)

    def __post_init__(self):
        self.client = ClassModuleLoader(self.module, self.class_name).load()(*self.args)


@dataclasses.dataclass
class Artifact(Config):
    library: Library
    limit: int = 256
    fallback_max_size: int = DEFAULT_FALLBACK_SIZE
    max_size: int = DEFAULT_FALLBACK_SIZE
    download_as_url: bool = True

    def __post_init__(self):
        if self.limit < 1 or self.limit > 256:
            raise ValueError(
                'Artifact limit must be greater than 0 and cannot exceed contract limit of 256'
            )

        if self.fallback_max_size < 1:
            raise ValueError('Fall back max artifact size must be above 0')

    @property
    def client(self):
        return self.library.client
