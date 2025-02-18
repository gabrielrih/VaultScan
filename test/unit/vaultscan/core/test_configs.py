import pytest

from unittest import TestCase
from unittest.mock import patch

from vaultscan.core.configs import AvailableConfigs, OutputFormatConfig


'''
    We must mock here the repository because the test must be performed simulating when the 
    config are using the default value and when it's using a value configured on the repository
'''
@pytest.mark.usefixtures("mock_repository")
class TestAvailableConfigs(TestCase):
    @pytest.fixture(autouse = True)
    def mock_repository(self):
        with patch("vaultscan.core.configs.repository") as mock_repository:
            self.mock_repository = mock_repository
            yield mock_repository

    def test_verbose_config_when_default(self):
        # Given
        self.mock_repository.get.return_value = {}
        
        # When
        is_verbose = AvailableConfigs.VERBOSE.value

        # Then
        self.mock_repository.is_called_once()
        self.assertIsInstance(is_verbose, bool)
        self.assertFalse(
            is_verbose,
            msg = 'The expected default value should be False. See default_value on AvailableConfigs class.'
        )

    def test_verbose_config_when_custom(self): 
        # Given
        self.mock_repository.get.return_value = {
            'name': AvailableConfigs.VERBOSE.config_name,
            'value': 'true'
        }
        
        # When
        is_verbose = AvailableConfigs.VERBOSE.value

        # Then
        self.mock_repository.is_called_once()
        self.assertIsInstance(is_verbose, bool)
        self.assertTrue(
            is_verbose,
            msg = "The expected default value should be True. It''s getting the 'verbose' config from a mock repository"
        )

    def test_output_format_config_when_default(self):
        # Given
        self.mock_repository.get.return_value = {}
        expected_default_value = OutputFormatConfig.JSON

        # When
        output_format = AvailableConfigs.OUTPUT_FORMAT.value

        # Then
        self.assertIsInstance(output_format, OutputFormatConfig)
        self.assertEqual(output_format, expected_default_value)

    def test_output_format_config_when_custom(self):
        # Given
        self.mock_repository.get.return_value = {
            'name': AvailableConfigs.OUTPUT_FORMAT.config_name,
            'value': str(OutputFormatConfig.TABLE.value)
        }
        expected_default_value = OutputFormatConfig.TABLE

        # When
        output_format = AvailableConfigs.OUTPUT_FORMAT.value

        # Then
        self.assertIsInstance(output_format, OutputFormatConfig)
        self.assertEqual(output_format, expected_default_value)
