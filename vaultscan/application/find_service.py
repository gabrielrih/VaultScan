from typing import List, Dict

from vaultscan.application.result import ServiceResult
from vaultscan.core.searcher import MultiVaultSearcherFactory
from vaultscan.core.friendly_messages import VaultMessages, SecretMessages
from vaultscan.repositories.vault.factory import VaultRepositoryFactory


class FindSecretService:
    def __init__(self, only_vault: str = None) -> ServiceResult:
        self.only_vault = only_vault
        
    def find(self, filter: str = None, exact: bool = False, show_values: bool = False, only_count: bool = False) -> ServiceResult:
        vaults = self.get_vaults()
        if not vaults:
            return ServiceResult(
                success = False,
                message = VaultMessages.NO_VAULTS.value
            )
        
        warnings = []
        if exact and not filter:
            warnings.append(SecretMessages.WARNING_WHEN_EXACT_FLAG_USED_WITH_NO_FILTER.value)

        if not filter and not self.only_vault:
            warnings.append(SecretMessages.WARNING_WHEN_SEARCHING_ALL_SECRETS.value)

        ignore_disabled = not bool(self.only_vault)
        scanner = MultiVaultSearcherFactory.create(
            vaults = vaults,
            exact_match = exact,
            ignore_disabled = ignore_disabled
        )

        # When we just want to count the secrets, there is no need to get their values
        should_fetch_values: bool = show_values and not only_count
        secrets: List[Dict] = scanner.find(
            filter = filter if filter else '',  # guarantees that filter is never None
            is_value = should_fetch_values
        )

        message = SecretMessages.NUMBER_OF_SECRETS_FOUND.value.format(quantity = len(secrets))
        if only_count:    
            return ServiceResult(
                success = True,
                message = message,
                warnings = warnings
            )

        return ServiceResult(
            success = True,
            message = message,
            data = secrets,
            warnings = warnings
        )

    def get_vaults(self) -> List[Dict]:
        vault_repository = VaultRepositoryFactory.create()
        if self.only_vault:
            vault: Dict = vault_repository.get(alias = self.only_vault)
            if not vault:
                return list()
            return [ vault ]
        return vault_repository.get_all()
