from typing import List, Dict

from vaultscan.repositories.config.base import ConfigRepository, Config


class InMemoryConfigRepository(ConfigRepository):
    def __init__(self):
        self.configs = list()

    def initialize(self): pass

    def set(self, new_config: Config) -> None:
        content = {
            'name': new_config.name,
            'value': new_config.value
        }
        self.configs.append(content)
        return None

    def unset(self, name: str) -> None:
        for config in self.configs:
            if config['name'] == name:
                self.configs.remove(config)
        return None

    def get(self, name: str) -> Dict:
        if not self.configs:
            return {}
        for config in self.configs:
            if config['name'] == name:
                return config
        return {}

    def get_all(self) -> List[Dict]:
        return self.configs
