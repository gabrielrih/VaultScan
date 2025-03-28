from typing import List, Dict

from vaultscan.repositories.config.base import ConfigRepository, Config
from vaultscan.repositories.file_handler import FileHandler


class ConfigRepositoryAsJson(ConfigRepository):
    ''' Repository implementation to persist the configurations on a file '''
    def __init__(self, file: FileHandler):
        self.file = file
        if not self.file.exists:
            self.initialize()

    def initialize(self):
        content: Dict = {
            'configs': list()
        }
        self.file.write(content)

    def set(self, new_config: Config) -> None:
        content: Dict = self.file.read()
        configs: List[Dict] = content['configs']
        for config in configs:
            if config['name'] == new_config.name:  # Changing the value
                config['value'] = new_config.value
                content['configs'] = configs
                self.file.write(content)
                return
        # Setting a new config on the file
        configs.append(new_config.to_dict())
        content['configs'] = configs
        self.file.write(content)
        return

    def unset(self, name: str) -> None:
        content: Dict = self.file.read()
        configs: List[Dict] = content['configs']
        for config in configs:
            if config['name'] == name:
                configs.remove(config)
                content['configs'] = configs
                self.file.write(content)
                return

    def get(self, name: str) -> Dict:
        content: Dict = self.file.read()
        configs: List[Dict] = content['configs']
        for config in configs:
            if config['name'] == name:
                return config
        return {}

    def get_all(self) -> List[Dict]:
        content: Dict = self.file.read()
        return content['configs']
