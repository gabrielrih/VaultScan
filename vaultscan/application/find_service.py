from typing import List, Dict

from vaultscan.application.base import BaseService, ServiceResult
from vaultscan.application.vault_service import GetVaultsService
from vaultscan.core.searcher import MultiVaultSearcherFactory
from vaultscan.core.friendly_messages import SecretMessages


class FindSecretService(BaseService):
    def __init__(self):
        self.get_vaults_service = GetVaultsService()

    def execute(self,
                filter: str = None,
                exact: bool = False,
                only_vault: str = None,
                show_values: bool = False,
                only_count: bool = False) -> ServiceResult:
        
        vaults_result: ServiceResult = self.get_vaults_service.execute(only_vault = only_vault)
        if not vaults_result.success:
            return ServiceResult(
                success = False,
                message = vaults_result.message
            )
        
        warnings = []
        if exact and not filter:
            warnings.append(SecretMessages.WARNING_WHEN_EXACT_FLAG_USED_WITH_NO_FILTER.value)

        if not filter and not only_vault:
            warnings.append(SecretMessages.WARNING_WHEN_SEARCHING_ALL_SECRETS.value)

        ignore_disabled = not bool(only_vault)
        scanner = MultiVaultSearcherFactory.create(
            vaults = vaults_result.data,
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
