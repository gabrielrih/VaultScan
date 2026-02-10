from typing import List, Dict

from vaultscan.application.base import BaseService, ServiceResult
from vaultscan.repositories.vault.factory import VaultRepositoryFactory
from vaultscan.core.friendly_messages import VaultMessages


class GetVaultsService(BaseService):
    def __init__(self):
        self.vault_repository = VaultRepositoryFactory.create()

    def execute(self, only_vault: str = None, filter: str = '') -> ServiceResult:
        if only_vault:
            warnings = []
            if filter:
               warnings.append(VaultMessages.WARNING_WHEN_FILTER_USED_WITH_ONLY_VAULT.value)
            result: ServiceResult = self._execute_only_vault(only_vault = only_vault)
            result.warnings.extend(warnings)
            return result

        return self._execute_all_vaults(filter = filter)

    def _execute_only_vault(self, only_vault: str) -> ServiceResult:
        vault: Dict = self.vault_repository.get(alias = only_vault)
        if not vault:
            return ServiceResult(
                success = False,
                message = VaultMessages.VAULT_NOT_FOUND.value.format(alias = only_vault)
            )
        return ServiceResult(
            success = True,
            message = VaultMessages.NUMBER_OF_VAULTS_FOUND.value.format(quantity = 1),
            data = [ vault ]
        )

    def _execute_all_vaults(self, filter: str = '') -> ServiceResult:
        vaults: List[Dict] = self.vault_repository.get_all(filter = filter)
        if not vaults:
            return ServiceResult(
                success = False,
                message = VaultMessages.NO_VAULTS.value
            )
        return ServiceResult(
            success = True,
            message = VaultMessages.NUMBER_OF_VAULTS_FOUND.value.format(quantity = len(vaults)),
            data = vaults
        )
