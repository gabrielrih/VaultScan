from unittest import TestCase
from unittest.mock import patch


from vaultscan.util.os import SupportedOS


class TestSupportedOS(TestCase):
    def test_os_name_property_when_windows(self):
        expected_os_name = 'windows'
        os_name = SupportedOS.WINDOWS.os_name
        self.assertEqual(
            os_name,
            expected_os_name,
            msg = f'The value for the WINDOWS enum should be {expected_os_name}'
        )

    def test_os_name_property_when_linux(self):
        expected_os_name = 'linux'
        os_name = SupportedOS.LINUX.os_name
        self.assertEqual(
            os_name,
            expected_os_name,
            msg = f'The value for the LINUX enum should be {expected_os_name}'
        )

    def test_home_env_var_property_when_windows(self):
        expected_home_env_var = 'USERPROFILE'
        home_env_var = SupportedOS.WINDOWS.home_env_var
        self.assertEqual(
            home_env_var,
            expected_home_env_var,
            msg = f'The env var used to get the user home directory for WINDOWS should be {expected_home_env_var}'
        )

    def test_home_env_var_property_when_linux(self):
        expected_home_env_var = 'HOME'
        home_env_var = SupportedOS.LINUX.home_env_var
        self.assertEqual(
            home_env_var,
            expected_home_env_var,
            msg = f'The env var used to get the user home directory for LINUX should be {expected_home_env_var}'
        )

    @patch('os.name', 'nt')
    def test_detect_when_windows(self):
        os = SupportedOS.detect()
        self.assertEqual(
            os,
            SupportedOS.WINDOWS,
            msg = f'The expected OS should be {SupportedOS.WINDOWS.name}'
        )

    @patch('os.name', 'posix')
    def test_detect_when_linux(self):
        os = SupportedOS.detect()
        self.assertEqual(
            os,
            SupportedOS.LINUX,
            msg = f'The expected OS should be {SupportedOS.LINUX.name}'
        )
