# vaultscan
Searching secrets in multiple vaults.

This tool can be useful to search in a fast way secrets throughout multiple vaults.

Supported vaults:
- [Azure Key Vault](https://azure.microsoft.com/en-us/)
- [Keepass](https://keepass.info/)

# Index
- [Installing it](#installing-it)
- [Using it](#using-it)
    - [Configuring the vaults](#configuring-the-vaults)
    - [Searching secrets using regex](#searching-secrets-using-regex)
    - [Searching secrets by its exact name](#searching-secrets-by-their-names)
- [Contribute](#contribute)
    - [Environment variables](#environment-variables)
    - [Testing](#testing)
    - [Release](#release)

# Installing it 
You can install this package by downloading the latest ```.whl``` file from GitHub Releases and using pip to install it.

- Go to the Releases page.
- Find the latest version and download the ```.whl``` file (e.g., ```vaultscan-0.1.4-py3-none-any.whl```).
- After downloading the .whl file, install it using pip:

```ps1
pip install --user vaultscan-0.1.4-py3-none-any.whl
```

By doing that a ```vaultscan.exe``` file will be created probably on the folder: ```C:\Users\user\AppData\Roaming\Python\Python312\Scripts```. So, you must add this folder on the user PATH.

Finally you can run this script anywhere on the Terminal: 

```ps1
vaultscan --help
```

To see the installed version you can run:

```ps1
pip show vaultscan
```


# Using it

## Configuring the vaults
First of all you must configure the vaults you want to use in the tool. This is a required step.

### Configuring an Azure Key Vault

```ps1
vaultscan vault add kv --alias mykv --vault-name vault --resource-group-name rg --subscription-id id 
```

### Configuring an Keepass

```ps1
vaultscan vault add keepass --alias my_keepass --path "C:\databases\passwords.kdbx"
```

To look at the configured vaults you can run:

```ps1
vaultscan vault list
```

> Internally, the tool creates a ```vaults.json``` file on the user HOME folder ```C:\Users\user\.vaultscan```

## Searching secrets using regex

It will search all the secrets that match this exact name:

```ps1
vaultscan find secrets my_secret_name --exact
```

You can also include the values

```ps1
vaultscan find secrets my_secret_name --exact --show-values
```

And you can also search in an specific vault:

```ps1
vaultscan find secrets my_secret_name --only-vault key_vault --exact --show-values
```

## Searching secrets by its exact name

It will search all the secrets looking for the ```host``` regex:

```ps1
vaultscan find secrets host
```

You can also include the values

```ps1
vaultscan find secrets host --show-values
```

And you can also search in an specific vault:

```ps1
vaultscan find secrets host --only-vault key_vault --show-values
```

# Contribute

To contribute with the development of this repo you could use [Poetry](https://python-poetry.org/) to manage the Python version and control the dependencies.

```ps1
poetry install
```

To use the cli just run:

```ps1
vaultscan --help
```

## Environment variables

To help you on the development process you can create a ```.env``` file on the root folder and set the current variables:

```
LOG_LEVEL = 'DEBUG'
```

> For more information just look at the [settings.py](./vaultscan/settings.py) file


## Testing 

```ps1
pytest
```

## Release

A new release is generated automatically by the [ci pipeline](.github/workflows/ci.yml) everytime you changed the package version on the [pyproject.toml](./pyproject.toml) file.

```toml
[project]
name = "VaultScan"
version = "0.1.4"
```