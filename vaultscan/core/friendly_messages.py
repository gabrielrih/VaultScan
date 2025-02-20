from enum import Enum

''' 
    All messages that will be printed for the user should be here
    It guarantee its reuse and make it easy to change the message for Better understanding
    DEBUG and RAISE EXCEPTION messages SHOULDN'T BE HERE. That is because those messages are just used by devs.
'''
class VaultMessages(Enum):
    VAULT_ADDED = 'The vault "{alias}" was added on the configuration!'
    VAULT_REMOVED = 'The vault "{alias}" was removed from the configuration!'
    VAULT_RENAMED = 'The vault "{old_alias}" has been renamed to "{new_alias}"!'
    VAULT_NOT_FOUND = 'The alias "{alias}" was not found on the configuration!'
    VAULT_STATUS_CHANGED = 'The status of vault "{alias}" has been changed to "{status}"!'
    VAULT_ALREADY_EXISTS = 'The alias "{alias}" already exists!'
    VAULT_DISABLED = 'Ignoring vault "{alias}" because it is disabled'
    ALL_VAULTS_REMOVED = 'All the vaults has been removed from the configuration!'
    NO_VAULTS = 'No vaults found!'
    NUMBER_OF_VAULTS_FOUND = '{quantity} vaults found!'
    SEARCHING_ON_VAULT = 'Searching on vault "{alias}" of type "{type}"'


class ConfigMessages(Enum):
    CONFIG_SET = 'The config "{config}" was set using the given value!'
    CONFIG_RESET = 'The config "{config}" has been reverted to its original value!'
    INVALID_VALUE = 'The value "{value}" is not valid for the "{config}" configuration. The possible values are: {possible_values}'
    NUMBER_OF_CONFIGS_FOUND = '{quantity} configs found!'


class VersionMessages(Enum):
    PACKAGE_NOT_INSTALLED = '{package_name} is not installed via pip!'
    INSTALLED_VERSION = '{package_name} version: {version}'


class SecretMessages(Enum):
    NUMBER_OF_SECRETS_FOUND = '{quantity} secrets found!'
