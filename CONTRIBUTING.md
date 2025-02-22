# Contributing

## Index
- [Project structure](#project-structure)
- [Component architecture](#component-architecture)
- [Setting up the development environment](#setting-up-the-development-environment)
- [Guidelines](#guidelines)
- [Testing](#testing)
- [Release process](#release-process)

## Project structure

```
vaultscan/
├── commands/                 # Individual CLI commands (e.g., vault, find, config)
├── core/                     # The higher level classes for the main features
│   ├── engines               # Vault engine implementations (e.g., Azure, KeePass)
│   ├── output                # Output messages (e.g., logger and printer)
├── repositories/             # Repository interfaces (persistent storage for vaults, configs and more)
├── util/                     # Utility classes and helper modules
├── pyproject.toml            # Poetry configuration file
```

## Component architecture
**Higher level**
- CLI Interface: The user-facing part of your tool. See [click](https://click.palletsprojects.com/en/stable/) library.
- Output: Classes to print out messages. See [logging](https://docs.python.org/3/library/logging.html).
- DataCipher: It allows to encrypt/decrypt data using a global key. See [cryptography.fernet](https://cryptography.io/en/latest/fernet/).
- Scanner: The main and more abstract class to search secrets on vaults.
- GlobalConfigs: For managing configuration values.

**Lower level**
- Vault Engines: To define the engine implementations and how to interact with that. See [azure-keyvault-secrets](https://pypi.org/project/azure-keyvault-secrets/) and [pykeepass](https://pypi.org/project/pykeepass/).
- Repositories: Persistent storage for vaults, configs, secure keys, etc. See [json](https://docs.python.org/3/library/json.html) and [keyring](https://pypi.org/project/keyring/).
- Os discovery: To find out the current OS and the user informations.
- File System/JSON file hander: For saving json files on disk.

## Setting up the development environment

To contribute with the development of this repo you could use [Poetry](https://python-poetry.org/) to manage the Python version and control the dependencies.

```ps1
poetry install
```

To use the cli just run:

```ps1
vaultscan --help
```

I also recommend the use of [pyenv](https://github.com/pyenv-win/pyenv-win) to allow you to install and manage multiple Python version in your machine.


## Guidelines

1. **Classes in lower level shouldn't know about classes in higher level**

E.g., a [vault repository](./vaultscan/repositories/vault/base.py) implementation can know nothing about the [GlobalConfig](./vaultscan/core/configs.py) class.

2. **We use *factories* on the *repositories* to be easy to add a new implementation**

E.g, in the *secure_key* repository we have the [keyring](./vaultscan/repositories/secure_key/keyring.py) implementation for real usage and [in_memory](./vaultscan/repositories/secure_key/in_memory.py) implementation for unit tests. But, we could easily create a new implementation if you wanted to.

3. **All the messages printed to the user should be defined on the [friendly_messages](./vaultscan/core/friendly_messages.py) file**

It makes it easy to manage and add new friendly user messages.

To print messages it uses the [logger](./vaultscan/core/output/logger.py) implementation. The *logger* allow us to customize the type of message by info, warning, error, success and debug.

> Note that the debug message is not consider a friendly message since it's not show by default to the user. So it does not make sense to put those messages on the [friendly_messages](./vaultscan/core/friendly_messages.py) class.

4. **When implementing a new engine you should:**

Code the real vault implementation: See [BaseVaultConfig](./vaultscan/repositories/vault/base.py), [BaseVaultEngine](./vaultscan/core/engines/base.py) and [AvailableEngines](./vaultscan/core/engines/engines.py).

Code the command to add the new vault engine: See the [vault commands](./vaultscan/commands/vault.py) file.

5. **When implementing a new configuration you should:**

Code the basics of the new config: See [AvailableConfigs](./vaultscan/core/configs.py). In that class you should add the config name, its type, its default value and its possible values.

Actually use the new configuration on code: As you can see in the example of the [vault.py](./vaultscan/commands/vault.py) file, when it defines a variable called *DEFAULT_OUTPUT_FORMAT* that stores the current value for the *AvailableConfigs.OUTPUT_FORMAT* config.

## Testing 

You're able to manually run the unit tests:

```
pytest .\test\vaultscan\unit
```

... or you could run the end to end tests:

```
pytest .\test\vaultscan\e2e
```

⚠️ **Work in progress!** We still don't have enought unit tests to consider it OK, so we're working on it.

## Release Process

A new release is generated automatically by the [ci pipeline](.github/workflows/ci.yml) everytime you changed the package version on the [pyproject.toml](./pyproject.toml) file.

```toml
[project]
name = "VaultScan"
version = "0.1.4"
```
