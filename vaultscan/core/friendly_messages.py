from enum import Enum

''' 
    All messages that will be printed out to user should be here
    It guarantees its reuse and makes it easy to change the message for better understanding
    IMPORTANT: DEBUG and RAISE EXCEPTION messages SHOULDN'T BE HERE. That is because there is no need to those messages be user friendly.
'''
class VaultMessages(Enum):
    VAULT_ADDED = 'The vault "{alias}" was added!'
    VAULT_REMOVED = 'The vault "{alias}" was removed!'
    VAULT_RENAMED = 'The vault "{old_alias}" has been renamed to "{new_alias}"!'
    VAULT_NOT_FOUND = 'The vault "{alias}" was not found!'
    VAULT_STATUS_CHANGED = 'The status of vault "{alias}" has been changed to "{status}"!'
    VAULT_ALREADY_EXISTS = 'The alias "{alias}" already exists!'
    VAULT_DISABLED = 'Ignoring vault "{alias}" because it is disabled'
    ALL_VAULTS_REMOVED = 'All the vaults has been removed from the configuration!'
    NO_VAULTS = 'No vault found!'
    NUMBER_OF_VAULTS_FOUND = '{quantity} vault(s) found!'
    SEARCHING_ON_VAULT = 'Searching on vault "{alias}" of type "{type}"'
    WARNING_WHEN_FILTER_USED_WITH_ONLY_VAULT = 'filter value is ignored when --only-vault is provided'


class ConfigMessages(Enum):
    CONFIG_SET = 'The config "{config}" was set using the given value!'
    CONFIG_RESET = 'The config "{config}" has been reverted to its original value!'
    INVALID_VALUE = 'The value "{value}" is not valid for the "{config}" configuration. The possible values are: {possible_values}'
    NUMBER_OF_CONFIGS_FOUND = '{quantity} config(s) found!'


class VersionMessages(Enum):
    PACKAGE_NOT_INSTALLED = '{package_name} is not installed via pip!'
    INSTALLED_VERSION = '{package_name} installed version: {version}'


class SecretMessages(Enum):
    NUMBER_OF_SECRETS_FOUND = '{quantity} secret(s) found!'
    WARNING_WHEN_EXACT_FLAG_USED_WITH_NO_FILTER = '--exact flag is ignored when no filter is provided'
    WARNING_WHEN_SEARCHING_ALL_SECRETS = 'No filter provided. Searching for all secrets across all vaults. This may take a while...'


class CacheMessages(Enum):
    CACHE_CLEARED = 'The cache has been successfully cleared!'
