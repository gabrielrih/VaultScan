from vaultscan.engines.base import Secret
from vaultscan.engines.key_vault import KeyVaultSecretEngine, KeyVaultConfig
from vaultscan.util.output.logger import LoggerFactory

from enum import Enum, auto
from typing import List, Dict


logger = LoggerFactory.get_logger()


class FindType(Enum):
    BY_REGEX = auto()
    EXACTLY_MATCH = auto()


class SecretScanner:
    # FIX IT: Aqui to usando só o KV, isso deveria ser dinâmico para identificar KeePass e outros caras também
    def __init__(self, vaults: List[Dict]):
        self.vaults: List[KeyVaultConfig] = KeyVaultConfig.from_list(vaults)
        logger.verbose(f'Using vaults: {self.vaults}')

    def find(self, secret_name: str, type: FindType = FindType.BY_REGEX) -> List[Dict]:
        logger.verbose(f'Filtering {type}')
        if type == FindType.BY_REGEX:
            return self.find_by_regex(secret_name)
        return self.find_exactly_match(secret_name)

    # FIX IT: Aqui fazer o tratamento pelo type do vault
    def find_by_regex(self, secret_name: str) -> List[Dict]:
        response = list()
        for vault in self.vaults:
            logger.verbose(f'Finding on vault {vault.alias} - {vault.type}')
            secrets: List[Secret] = KeyVaultSecretEngine(vault).find_by_regex(secret_name)
            for secret in secrets:
                response.append(secret.__dict__)
        return response

    # FIX IT: Aqui fazer o tratamento pelo type do vault
    def find_exactly_match(self, secret_name: str) -> List[Dict]:
        response = list()
        for vault in self.vaults:
            logger.verbose(f'Finding on vault {vault.alias} - {vault.type}')
            secrets: List[Secret] = KeyVaultSecretEngine(vault).find_by_name(secret_name)
            logger.verbose(f'{len(secrets)} secret(s) found on vault {vault.alias} - {vault.type}')
            for secret in secrets:
                response.append(secret.__dict__)
        return response
