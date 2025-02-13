import os
import getpass

from vaultscan.util.os import SupportedOS


class CurrentUser:
    def __init__(self):
        self.current_os: SupportedOS = SupportedOS.detect()

    @property
    def username(self) -> str:
        return getpass.getuser()

    @property
    def home_path(self) -> str:
        env_var = self.current_os.home_env_var
        path = os.getenv(env_var)
        if not path:
            raise EnvironmentError('Unable to determine the user home directory')
        return path
