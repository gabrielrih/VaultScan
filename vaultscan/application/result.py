from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class ServiceResult():
    success: bool
    message: Optional[str] = None
    data: Optional[List[Dict]] = field(default_factory=list)
    warnings: Optional[List[str]] = field(default_factory=list)
