from dataclasses import dataclass, field

import yaml
from dataclass_factory import Factory

factory = Factory()


@dataclass
class Config:
    host: str
    port: int
    name: str
    user: str
    password: str
    storage_path: str
    database_url: str = field(init=False, repr=True)

    def __post_init__(self):
        self.database_url = (f"postgresql://"
                             f"{self.user}:{self.password}@{self.host}"
                             f":{self.port}/{self.name}")


config: Config = factory.load(yaml.safe_load(open("../config.yaml", "r")),
                              Config)
