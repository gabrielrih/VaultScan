import os
from enum import Enum


class SupportedOS(Enum):
    WINDOWS = ('windows', 'USERPROFILE')
    LINUX = ('linux', 'HOME')

    def __init__(self, os_name: str, home_env_var: str):
        self._os_name = os_name
        self._home_env_var = home_env_var

    @property
    def os_name(self) -> str:
        return self._os_name
    
    @property
    def home_env_var(self) -> str:
        return self._home_env_var
    
    @staticmethod
    def detect() -> 'SupportedOS':
        if SupportedOS.is_windows():
            return SupportedOS.WINDOWS
        if SupportedOS.is_linux():
            return SupportedOS.LINUX
        raise EnvironmentError('Unsupported OS')

    @staticmethod
    def is_windows() -> bool:
        return os.name == 'nt'

    @staticmethod
    def is_linux() -> bool:
        return os.name == 'posix'
