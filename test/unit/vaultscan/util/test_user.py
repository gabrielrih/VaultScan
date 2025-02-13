import os

from unittest import TestCase
from unittest.mock import patch

from vaultscan.util.user import CurrentUser
from vaultscan.util.os import SupportedOS


class TestCurrentUser(TestCase):
    @patch('getpass.getuser', return_value = 'my_username')
    def test_username_property(self, mock_getuser):
        # Given
        expected_username = 'my_username'

        # When
        user = CurrentUser()
        username = user.username

        # Then
        mock_getuser.assert_called_once()
        self.assertIsInstance(username, str)
        self.assertEqual(
            username,
            expected_username,
            msg = f'The username should be {expected_username}'
        )

    @patch('os.name', 'nt')
    @patch.dict(os.environ, { SupportedOS.WINDOWS.home_env_var: 'C:\\Users\\username' })
    def test_home_path_property_when_windows(self):
        # Given
        expected_path = 'C:\\Users\\username'

        # When
        user = CurrentUser()
        path = user.home_path

        # Then
        self.assertIsInstance(path, str)
        self.assertEqual(
            path,
            expected_path,
            msg = f'The expected user home directory on {SupportedOS.WINDOWS.name} should be {expected_path}'
        )

    @patch('os.name', 'posix')
    @patch.dict(os.environ, { SupportedOS.LINUX.home_env_var: '/home/username' })
    def test_path_property_when_linux(self):
        # Given
        expected_path = '/home/username'

        # When
        user = CurrentUser()
        path = user.home_path

        # Then
        self.assertIsInstance(path, str)
        self.assertEqual(
            path,
            expected_path,
            msg = f'The expected user home directory on {SupportedOS.LINUX.name} should be {expected_path}'
        )
