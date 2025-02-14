from vaultscan.engines.base import BaseVaultConfig
from vaultscan.util.output.logger import LoggerFactory

from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Dict


logger = LoggerFactory.get_logger()


@dataclass
class Secret:
    vault_alias: str
    secret_name: str


class FindType(Enum):
    BY_REGEX = auto()
    EXACTLY_MATCH = auto()


class SecretScanner:
    def __init__(self, vaults: List[BaseVaultConfig]):
        self.vaults = vaults

    def find(self, secret_name: str, type: FindType = FindType.BY_REGEX) -> List[Dict]:
        logger.verbose(f'Finding secrets using type {type}')
        if type == FindType.BY_REGEX:
            return self.find_by_regex(secret_name)
        return self.find_exactly_match(secret_name)

    def find_by_regex(self, secret_name: str) -> List[Dict]:
        return get_fake_secrets()

    def find_exactly_match(self, secret_name: str) -> List[Dict]:
        return get_fake_secrets()



def get_fake_secrets() -> List[Dict]:
    secrets = list()
    secrets.append(
        Secret(
            vault_alias = 'vault1',
            secret_name = 'my_secret_1'
        ).__dict__)
    secrets.append(
        Secret(
            vault_alias = 'vault1',
            secret_name = 'other'
        ).__dict__)
    secrets.append(
        Secret(
            vault_alias = 'other_vault',
            secret_name = 'kkk'
        ).__dict__)
    return secrets
