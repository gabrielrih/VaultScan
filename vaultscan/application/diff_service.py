from typing import List, Dict, Set, Optional

from vaultscan.application.base import BaseService, ServiceResult
from vaultscan.application.find_service import FindSecretService


class CompareSecretOnVaults(BaseService):
    def __init__(self):
        self.find_secret = FindSecretService()

    def execute(self, source_vault: str, target_vault: str, compare_values: bool = False, show_details: bool = False) -> ServiceResult:
        source_result: ServiceResult = self.find_secret.execute(
            only_vault = source_vault,
            show_values = compare_values
        )
        target_result: ServiceResult = self.find_secret.execute(
            only_vault = target_vault,
            show_values = compare_values
        )
        
        errors = self._validate_results(source_result, target_result)
        if errors:
            return ServiceResult(success = False, message = ' '.join(errors))
        
        source_dict: Dict[str, str] = self._to_dict(secrets = source_result.data or [])
        target_dict: Dict[str, str] = self._to_dict(secrets = target_result.data or [])

        comparison: Dict = self._compare_names(source_dict, target_dict)

        value_comparison = None
        if compare_values:
            value_comparison = self._compare_values(source_dict, target_dict, comparison["in_both"])

        data = self._build_summary(source_vault, target_vault, comparison, value_comparison)

        if show_details:
            data["details"] = self._build_details(comparison,value_comparison)

        return ServiceResult(
            success = True,
            data = [ data ]
        )

    def _validate_results(self, *results: ServiceResult) -> List[str]:
        return [ r.message for r in results if not r.success ]

    def _to_dict(self, secrets: List[Dict]) -> Dict[str, str]:
        return {
            secret["name"]: secret.get("value")
            for secret in secrets
        }
    
    def _compare_names(self, source: Dict[str, str], target: Dict[str, str]) -> Dict[str, Set[str]]:
        source_names = set(source)
        target_names = set(target)
        return {
            "only_in_source": source_names - target_names,
            "only_in_target": target_names - source_names,
            "in_both": source_names & target_names,
        }
    
    def _compare_values(self, source: Dict[str, str], target: Dict[str, str], common_names: Set[str]) -> Dict[str, Set[str]]:
        equal = {
            name for name in common_names
            if source[name] == target[name]
        }

        return {
            "equal": equal,
            "different": common_names - equal
        }
    
    def _build_summary(self, source_vault: str, target_vault: str, comparison: Dict[str, Set[str]], value_comparison: Optional[Dict[str, Set[str]]]) -> Dict:
        summary = {
            "source": source_vault,
            "target": target_vault,
            "only_in_source": len(comparison["only_in_source"]),
            "only_in_target": len(comparison["only_in_target"]),
            "present_in_both": {
                "total": len(comparison["in_both"])
            }
        }

        if value_comparison:
            summary["present_in_both"].update({
                "with_equal_values": len(value_comparison["equal"]),
                "with_different_values": len(value_comparison["different"])
            })

        return summary

    def _build_details(self, comparison: Dict[str, Set[str]], value_comparison: Optional[Dict[str, Set[str]]]) -> Dict:
        details = {
            "only_in_source": sorted(comparison["only_in_source"]),
            "only_in_target": sorted(comparison["only_in_target"]),
        }

        if value_comparison:
            details["present_in_both"] = {
                "with_equal_values": sorted(value_comparison["equal"]),
                "with_different_values": sorted(value_comparison["different"]),
            }
        else:
            details["present_in_both"] = sorted(comparison["in_both"])

        return details
