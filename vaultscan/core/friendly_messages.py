from enum import Enum


class VaultFriendlyMessages(Enum):
    VAULT_ADDED = 'The vault "{alias}" was added on the configuration!'
    VAULT_REMOVED = 'The alias "{alias}" was removed from the configuration!'
    VAULT_RENAMED = 'The alias "{old_alias}" has been renamed to "{new_alias}"!'
    VAULT_NOT_FOUND = 'The alias "{alias}" was not found on the configuration!'
    VAULT_STATUS_CHANGED = 'The status of alias "{alias}" has been changed to "{status}"!'
    VAULT_ALREADY_EXISTS = 'The alias "{alias}" already exists!'
    ALL_VAULTS_REMOVED = 'All the vaults has been removed from the configuration!'
    NO_VAULTS = 'No vaults found!'
    X_VAULTS_FOUND = '{quantity} vaults found!'


class ConfigFriendlyMessages(Enum):
    CONFIG_SET = 'The config "{1}" was set using the given value!'
    CONFIG_RESET = 'The config "{1}" has been reverted to its original value!'
    INVALID_VALUE = 'The value "{1}" is not valid for the "{2}" configuration. The possible values are: {3}'


class VersionFriendlyMessages(Enum):
    PACKAGE_NOT_INSTALLED = '{1} is not installed via pip!'

