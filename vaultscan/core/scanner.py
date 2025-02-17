from vaultscan.engines.engines import get_engine_from_type
from vaultscan.engines.base import Secret, FilterType
from vaultscan.util.output.logger import LoggerFactory

from abc import ABC, abstractmethod
from typing import List, Dict


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
            logger.info(f'Searching on vault {vault.alias} ({vault.type =})')
            secrets: List[Secret] = engine.engine(vault).find(
                filter = filter,
                type = self.filter_type,
                is_value = is_value
            )
            for secret in secrets:
                response.append(secret.__dict__)
        logger.info(f'{len(response)} secret(s) found!')
        return response
