from vaultscan.engines.engines import get_engine_from_type
from vaultscan.engines.base import Secret, FilterType
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
            logger.error(f'No vault matching alias "{only_vault}"')
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
                return list()
            return [ vault ]
        return vault_repository.get_all()


class Scanner(ABC):
    def __init__(self, vaults: List[Dict], filter_type: FilterType):
        self.vaults = vaults
        self.filter_type = filter_type
        logger.debug(f'Vaults: {self.vaults}')

    @abstractmethod
    def find(self, filter: str, is_value: bool = False) -> List[Dict]: pass


class MultiVaultScanner(Scanner):
    def __init__(self, vaults: List[Dict], filter_type: FilterType):
        super().__init__(vaults, filter_type)

    def find(self, filter: str, is_value: bool = False) -> List[Dict]:
        response = list()
        for vault in self.vaults:
            engine = get_engine_from_type(type = vault['type'])
            vault = engine.config.from_dict(vault)
            logger.debug(f'Searching on vault {vault.alias} ({vault.type =})')
            secrets: List[Secret] = engine.engine(vault).find(
                filter = filter,
                type = self.filter_type,
                is_value = is_value
            )
            for secret in secrets:
                response.append(secret.__dict__)
        logger.info(f'{len(secrets)} secret(s) found!')
        return response
