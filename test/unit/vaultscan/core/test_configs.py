from unittest import TestCase

from vaultscan.repositories.config.base import Config
from vaultscan.repositories.config.in_memory import InMemoryConfigRepository
from vaultscan.core.configs import (
    AvailableConfigs,
    OutputFormatConfig,
    ConfigManager,
    ConfigValidator
)



class TestAvailableConfigs(TestCase):
    def test_check_type_when_verbose_config(self):
        config = AvailableConfigs.VERBOSE
        self.assertTrue(
            issubclass(config.value_type, bool),
            msg = f'The value type of the config {config} should be BOOL'
        )

    def test_check_type_when_output_format_config(self):
        config = AvailableConfigs.OUTPUT_FORMAT
        self.assertTrue(
            issubclass(config.value_type, OutputFormatConfig),
            msg = f'The value type of the config {config} should de {OutputFormatConfig.__name__}'
        )

    def test_get_values(self):
        expected_available_configs = ['verbose', 'output_format']
        values = AvailableConfigs.get_values()
        self.assertEqual(values, expected_available_configs)

    def test_from_config_name(self):
        expected_config_name = 'verbose'
        config: AvailableConfigs = AvailableConfigs.from_config_name(expected_config_name)
        self.assertIsInstance(config, AvailableConfigs)
        self.assertEqual(config.config_name, expected_config_name)


'''
    We must mock here the repository because the test must be performed simulating when the 
    config are using the default value and when it's using a value configured on the repository
'''
class TestConfigManager(TestCase):
    def setUp(self):
        self.repository = InMemoryConfigRepository()

    def test_get_value_when_default(self):
        # Given
        config = AvailableConfigs.VERBOSE
        expected_default_value = False
        
        # When
        manager = ConfigManager(config = config, repository = self.repository)
        value = manager.get_value()
        
        # Then
        self.assertEqual(value, expected_default_value)
    
    def test_get_value_when_custom_config(self):
        # Given
        repository = InMemoryConfigRepository()
        available_config = AvailableConfigs.VERBOSE
        expected_value = True
        
        # When
        # Setting a custom value for the verbose config
        new_config = Config(
            name = available_config.config_name,
            value = str(expected_value)
        )
        repository.set(new_config = new_config)
        manager = ConfigManager(config = AvailableConfigs.VERBOSE, repository = repository)
        value = manager.get_value()

        # Then
        self.assertEqual(value, expected_value)


    def test_get_value_as_string_when_default(self):
        # Given
        config = AvailableConfigs.VERBOSE
        expected_default_value = 'False'

        # When
        manager = ConfigManager(config = config, repository = self.repository)
        value: str = manager.get_value_as_string()

        # Then
        self.assertEqual(value, expected_default_value)

    def test_get_value_as_string_when_custom_config(self):
        # Given
        repository = InMemoryConfigRepository()
        available_config = AvailableConfigs.VERBOSE
        expected_value_as_string = 'True'
        
        # When
        # Setting a custom value for the verbose config
        new_config = Config(
            name = available_config.config_name,
            value = expected_value_as_string
        )
        repository.set(new_config = new_config)
        manager = ConfigManager(config = AvailableConfigs.VERBOSE, repository = repository)
        value = manager.get_value_as_string()

        # Then
        self.assertEqual(value, expected_value_as_string)



class TestConfigValidator(TestCase):
    def test_is_a_valid_value_when_true(self):
        # Given
        config: AvailableConfigs = AvailableConfigs.OUTPUT_FORMAT

        # When
        valid_value = 'json'
        is_valid = ConfigValidator.is_a_valid_value(
            config = config,
            value = valid_value
        )
        
        # Then
        self.assertTrue(
            is_valid,
            msg = f'The value "{valid_value}" should be valid for the {config} config'
        )

    def test_is_a_valid_value_when_false(self):
        # Given
        config: AvailableConfigs = AvailableConfigs.OUTPUT_FORMAT

        # When
        invalid_value = 'invalid_value'
        is_valid = ConfigValidator.is_a_valid_value(
            config = config,
            value = invalid_value
        )
        
        # Then
        self.assertFalse(
            is_valid,
            msg = f'The value "{invalid_value}" should not be valid for the {config} config'
        )
