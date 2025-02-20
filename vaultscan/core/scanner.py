from abc import ABC, abstractmethod
from typing import List, Dict

from vaultscan.core.engines.engines import get_engine_from_type
from vaultscan.core.engines.base import Secret, FilterType
from vaultscan.core.friendly_messages import VaultFriendlyMessages, SecretFriendlyMessages
from vaultscan.core.output.logger import LoggerFactory
from vaultscan.repositories.vault.base import VaultStatus


logger = LoggerFactory.get_logger(__name__)


class MultiVaultScannerBuilder:
    @staticmethod
    def create(vaults: List[Dict], exact_match: bool = False) -> 'Scanner':
        filter_type = FilterType.BY_REGEX
        if exact_match:
            filter_type = FilterType.BY_MATCH
        return MultiVaultScanner(vaults, filter_type)



class Scanner(ABC):
    def __init__(self, vaults: List[Dict], filter_type: FilterType):
        self.vaults = vaults
        self.filter_type = filter_type
        logger.debug(f'All vaults: {self.vaults}')

    @abstractmethod
    def find(self, filter: str, is_value: bool = False) -> List[Dict]: pass


class MultiVaultScanner(Scanner):
    def __init__(self, vaults: List[Dict], filter_type: FilterType):
        super().__init__(vaults, filter_type)

    def find(self, filter: str, is_value: bool = False) -> List[Dict]:
        response = list()
        for vault in self.vaults:
            # Convert from dict to the appropriate classes
            engine = get_engine_from_type(type = vault['type'])
            vault = engine.config.from_dict(vault)
            # Ignoring disabled vault
            if vault.status == VaultStatus.DISABLED:
                message = VaultFriendlyMessages.VAULT_DISABLED.value.format(alias = vault.alias)
                logger.info(message)
                continue
            # Searching secrets
            message = VaultFriendlyMessages.SEARCHING_ON_VAULT.value.format(
                alias = vault.alias,
                type = vault.type
            )
            logger.info(message)
            secrets: List[Secret] = engine.engine(vault).find(
                filter = filter,
                type = self.filter_type,
                is_value = is_value
            )
            for secret in secrets:
                response.append(secret.__dict__)
        message = SecretFriendlyMessages.NUMBER_OF_SECRETS_FOUND.value.format(quantity = len(response))
        logger.info(message)
        return response
