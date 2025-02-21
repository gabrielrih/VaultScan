import concurrent.futures

from abc import ABC, abstractmethod
from typing import List, Dict

from vaultscan.core.engines.engines import AvailableEngines
from vaultscan.core.engines.base import Secret, FilterType
from vaultscan.core.friendly_messages import VaultMessages, SecretMessages
from vaultscan.core.output.logger import LoggerFactory
from vaultscan.repositories.vault.base import VaultStatus


logger = LoggerFactory.get_logger(__name__)


class MultiVaultSearcherFactory:
    @staticmethod
    def create(vaults: List[Dict], exact_match: bool = False) -> 'Searcher':
        filter_type = FilterType.BY_REGEX
        if exact_match:
            filter_type = FilterType.BY_MATCH
        return MultiVaultSearcher(vaults, filter_type)


class Searcher(ABC):
    def __init__(self, vaults: List[Dict], filter_type: FilterType):
        self.vaults = vaults
        self.filter_type = filter_type
        logger.debug(f'All vaults: {self.vaults}')

    @abstractmethod
    def find(self, filter: str, is_value: bool = False) -> List[Dict]: pass


class MultiVaultSearcher(Searcher):
    def __init__(self, vaults: List[Dict], filter_type: FilterType):
        super().__init__(vaults, filter_type)

    def find(self, filter: str, is_value: bool = False) -> List[Dict]:
        secrets: List[Dict] = list()
        with concurrent.futures.ThreadPoolExecutor(max_workers = 5) as executor:
            futures = [
                executor.submit(self._find_on_vault, vault, filter, is_value)
                for vault in self.vaults
            ]
            for future in concurrent.futures.as_completed(futures):
                try:
                    secrets.extend(future.result())
                except Exception as e:
                    logger.error("Error searching vault: %s", e)
        message = SecretMessages.NUMBER_OF_SECRETS_FOUND.value.format(quantity = len(secrets))
        logger.info(message)
        return secrets
    
    def _find_on_vault(self, vault: Dict, filter: str, is_value: bool) -> List[Dict]:
        engine: AvailableEngines = AvailableEngines.from_type(type = vault['type'])
        vault = engine.config.from_dict(vault)
        if vault.status == VaultStatus.DISABLED:
            message = VaultMessages.VAULT_DISABLED.value.format(alias = vault.alias)
            logger.info(message)
            return []
        message = VaultMessages.SEARCHING_ON_VAULT.value.format(
            alias = vault.alias,
            type = vault.type
        )
        logger.info(message)
        secrets: List[Secret] = engine.engine(vault).find(
            filter = filter,
            type = self.filter_type,
            is_value = is_value
        )
        # Convert each secret to a dict
        return [ secret.__dict__ for secret in secrets]
