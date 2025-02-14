from vaultscan.engines.base import Secret, FilterType
from vaultscan.engines.key_vault import KeyVaultSecretEngine, KeyVaultConfig
from vaultscan.repositories.factory import VaultRepositoryFactory
from vaultscan.util.output.logger import LoggerFactory

from abc import ABC, abstractmethod
from typing import List, Dict


vault_repository = VaultRepositoryFactory.create()

logger = LoggerFactory.get_logger(__name__)


class MultiVaultScannerBuilder:
    @staticmethod
    def create(only_vault: str = '', exact_match: bool = False) -> 'Scanner':
        vaults: List[Dict] = MultiVaultScannerBuilder.get_vaults(only_vault)
        if not vaults:
            logger.error('No vault(s) found!')
            return
        filter_type = FilterType.BY_REGEX
        if exact_match:
            filter_type = FilterType.BY_MATCH
        return MultiVaultScanner(vaults, filter_type)

    @staticmethod
    def get_vaults(only_vault: str = '') -> List[Dict]:
        if only_vault:
            vault: Dict = vault_repository.get(alias = only_vault)
            logger.debug(f'Vault "{only_vault}" content: {vault}')
            if not vault:
                logger.info(f'No vault matching alias "{only_vault}"')
                return list()
            return [ vault ]

        return vault_repository.get_all()


class Scanner(ABC):
    # FIX IT: Aqui to usando só o KV, isso deveria ser dinâmico para identificar KeePass e outros caras também
    def __init__(self, vaults: List[Dict], filter_type: FilterType):
        self.vaults: List[KeyVaultConfig] = KeyVaultConfig.from_list(vaults)
        self.filter_type = filter_type
        logger.debug(f'Vaults: {self.vaults}')

    @abstractmethod
    def find(self, filter: str, is_value: bool = False) -> List[Dict]: pass


class MultiVaultScanner(Scanner):
    def __init__(self, vaults, filter_type):
        super().__init__(vaults, filter_type)

    def find(self, filter: str, is_value: bool = False) -> List[Dict]:
        response = list()
        for vault in self.vaults:
            logger.debug(f'Searching on vault {vault.alias} ({vault.type =})')
            secrets: List[Secret] = KeyVaultSecretEngine(vault).find(
                filter = filter,
                type = self.filter_type,
                is_value = is_value
            )
            for secret in secrets:
                response.append(secret.__dict__)
        logger.info(f'{len(secrets)} secret(s) found!')
        return response
