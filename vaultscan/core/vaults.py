from vaultscan.core.output.logger import LoggerFactory
from vaultscan.repositories.vault.factory import VaultRepositoryFactory

from typing import List, Dict


logger = LoggerFactory.get_logger(__name__)


def get_vaults(only_vault: str = '') -> List[Dict]:
    vault_repository = VaultRepositoryFactory.create()
    if only_vault:
        vault: Dict = vault_repository.get(alias = only_vault)
        logger.debug(f'Vault "{only_vault}" content: {vault}')
        if not vault:
            return list()
        return [ vault ]

    return vault_repository.get_all()
