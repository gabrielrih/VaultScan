from typing import Dict, List
from dataclasses import dataclass
from pykeepass import PyKeePass

from vaultscan.engines.base import (
    FilterType,
    BaseVaultConfig,
    BaseVaultEngine,
    Secret
)
from vaultscan.util.output.logger import LoggerFactory


logger = LoggerFactory.get_logger(__name__)


KEEPASS = 'keepass'


@dataclass
class KeePassConfig(BaseVaultConfig):
    path: str
    password: str

    def __post_init__(self):
        self.type = KEEPASS
        return super().__post_init__()

    @classmethod
    def from_dict(cls, content: Dict) -> 'KeePassConfig':
        return KeePassConfig(
            alias = content['alias'],
            path = content['path'],
            password = content['password']
        )


class KeepassSecretEngine(BaseVaultEngine):
    def __init__(self, vault: KeePassConfig):
        super().__init__(vault)
        self.client = PyKeePass(filename = vault.path, password = vault.password)

    def find(self, filter: str, type: FilterType, is_value: bool = False) -> List[Secret]:
        response = list()
        entries = self._find(filter, type)
        for entry in entries:
            value = ''
            if is_value:
                value = entry.password
            secret_name = KeepassSecretEngine.\
                format_secret_name(
                    group = str(entry.group),
                    secret = str(entry.title)
                )
            response.append(
                Secret(
                    vault = self.vault.alias,
                    name = secret_name,
                    value = value
                )
            )
        logger.debug(f'{len(response)} secrets found on KV {self.vault.alias} mathing the regex {filter}')
        return response
    
    def _find(self, filter: str, type: FilterType):
        if type == FilterType.BY_MATCH:
            return self._find_by_match(filter)
        return self._find_by_regex(filter)
    
    def _find_by_regex(self, filter: str):
        # Case sensitive
        return self.client.find_entries(title = f'{filter}.*', recursive = True, regex=  True)

    def _find_by_match(self, filter: str):
        # Case sensitive
        return self.client.find_entries(title = filter, recursive = True)

    @staticmethod
    def format_secret_name(group: str, secret: str) -> str:
        if not group:
            return f'/{secret}'
        # Initial value: Group: "Group1/Group2"
        # Expected output: Group1/Group2
        group = group.replace('Group: ', '').replace('"', '')
        return f'{group}/{secret}'
