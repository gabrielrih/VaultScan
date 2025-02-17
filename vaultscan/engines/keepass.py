from typing import Dict, List
from dataclasses import dataclass, field, fields
from pykeepass import PyKeePass

from vaultscan.engines.base import (
    FilterType,
    BaseVaultConfig,
    BaseVaultEngine,
    Secret
)
from vaultscan.repositories.secure_key.factory import SecureKeyRepositoryFactory
from vaultscan.repositories.secure_key.cipher import DataCipher
from vaultscan.util.output.logger import LoggerFactory


logger = LoggerFactory.get_logger(__name__)
cipher = DataCipher(repository = SecureKeyRepositoryFactory.create())


KEEPASS = 'keepass'


@dataclass
class KeePassConfig(BaseVaultConfig):
    path: str
    password: str = field(metadata = { "encrypted": True })

    def __post_init__(self):
        self.type = KEEPASS
        return super().__post_init__()

    def to_dict(self) -> Dict:
        data = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if f.metadata.get("encrypted"):
                value = cipher.encrypt(value)
                data[f.name] = {"encrypted": True, "value": value}
            else:
                data[f.name] = value
        return data

    @classmethod
    def from_dict(cls, content: Dict) -> 'KeePassConfig':
        kwargs = {}
        for f in fields(cls):
            if f.name == 'type':  # skip 'type" to prevent TypeError
                continue
            value = content.get(f.name)
            if isinstance(value, Dict) and value.get("encrypted"):
                kwargs[f.name] = cipher.decrypt(encrypted_value = value['value'])
            else:
                kwargs[f.name] = value
        return cls(**kwargs)


class KeePassSecretEngine(BaseVaultEngine):
    def __init__(self, vault: KeePassConfig):
        super().__init__(vault)
        self.client = PyKeePass(filename = vault.path, password = vault.password)

    def find(self, filter: str, type: FilterType, is_value: bool = False) -> List[Secret]:
        response = list()
        entries = self._find_by_type(filter, type)
        for entry in entries:
            value = ''
            if is_value:
                value = entry.password
            secret_name = KeePassSecretEngine.\
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
    
    def _find_by_type(self, filter: str, type: FilterType):
        ''' Case sensitive '''
        if type == FilterType.BY_MATCH:
            return self.client.find_entries(title = filter, recursive = True)
        if type == FilterType.BY_REGEX:
            return self.client.find_entries(title = f'{filter}.*', recursive = True, regex=  True)
        raise ValueError(f'Invalid FilterType {str(type)}!')

    @staticmethod
    def format_secret_name(group: str, secret: str) -> str:
        if not group:
            return f'/{secret}'
        # Initial value: Group: "Group1/Group2"
        # Expected output: Group1/Group2
        group = group.replace('Group: ', '').replace('"', '')
        return f'{group}/{secret}'
