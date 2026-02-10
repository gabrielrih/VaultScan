from typing import List, Dict, Set, Optional, Any
from dataclasses import dataclass, field

from vaultscan.application.base import BaseService, ServiceResult
from vaultscan.application.find_service import FindSecretService


class CompareSecretOnVaults(BaseService):
    def __init__(self):
        self.find_secret = FindSecretService()
        self.comparator = SecretComparator()

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
        name_comparison: Dict = self.comparator.compare_names(source = source_dict, target = target_dict)

        data = SecretDiffResult(
            source = source_vault,
            target = target_vault,
            only_in_source = name_comparison['only_in_source'],
            only_in_target = name_comparison['only_in_target'],
            in_both = name_comparison['in_both']
        )

        if compare_values:
            value_comparison: Dict = self.comparator.compare_values(
                source = source_dict,
                target = target_dict,
                common = name_comparison['in_both']
            )
            data.equal_values = value_comparison['equal']
            data.different_values = value_comparison['different']

        return ServiceResult(
            success = True,
            data = [ data.to_dict(show_details = show_details) ]
        )

    def _validate_results(self, *results: ServiceResult) -> List[str]:
        return [ r.message for r in results if not r.success ]

    def _to_dict(self, secrets: List[Dict]) -> Dict[str, str]:
        return {
            secret["name"]: secret.get("value")
            for secret in secrets
        }


class SecretComparator:
    @staticmethod
    def compare_names(source: Dict[str, str], target: Dict[str, str]) -> Dict:
        source_names = set(source)
        target_names = set(target)

        return {
            "only_in_source": source_names - target_names,
            "only_in_target": target_names - source_names,
            "in_both": source_names & target_names,
        }

    @staticmethod
    def compare_values(source: Dict[str, str], target: Dict[str, str], common: Set) -> Dict:
        equal = { n for n in common if source[n] == target[n] }
        return {
            "equal": equal,
            "different": common - equal
        }


@dataclass
class SecretDiffResult:
    source: str
    target: str
    only_in_source: Set[str] = field(default_factory=set)
    only_in_target: Set[str] = field(default_factory=set)
    in_both: Set[str] = field(default_factory=set)
    equal_values: Optional[Set[str]] = None
    different_values: Optional[Set[str]] = None

    def to_dict(self, show_details: bool = False) -> Dict[str, Any]:
        data = {
            "source": self.source,
            "target": self.target,
            "only_in_source": len(self.only_in_source),
            "only_in_target": len(self.only_in_target),
            "present_in_both": {
                "total": len(self.in_both)
            }
        }

        if self.equal_values is not None:
            data["present_in_both"].update({
                "with_equal_values": len(self.equal_values),
                "with_different_values": len(self.different_values),
            })

        if show_details:
            data["details"] = self._details()

        return data

    def _details(self) -> Dict[str, Any]:
        if self.equal_values is not None:
            return {
                "only_in_source": sorted(self.only_in_source),
                "only_in_target": sorted(self.only_in_target),
                "present_in_both": {
                    "with_equal_values": sorted(self.equal_values),
                    "with_different_values": sorted(self.different_values),
                }
            }

        return {
            "only_in_source": sorted(self.only_in_source),
            "only_in_target": sorted(self.only_in_target),
            "present_in_both": sorted(self.in_both),
        }
