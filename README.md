# vaultscan
Scanning and searching secrets in multiple Azure Key Vaults.

This tool can be useful to search in a fast way secrets by its name or via regex throughout multiple vaults.

# Index
- [Installing it](#installing-it)
- [Using it](#using-it)
    - [Configuring the vaults](#configuring-the-vaults)
    - [Searching secrets by their names](#searching-secrets-by-their-names)
    - [Searching secrets using regex](#searching-secrets-using-regex)
- [Contribute](#contribute)
    - [Environment variables](#environment-variables)
    - [Testing](#testing)

# Installing it 
TO DO

# Using it

## Configuring the vaults
First of all you must configure the vaults you want to use in the tool. This is a required step.

The current supported vaults are:
- Azure Key Vault
- KeePass

Configuring an Azure Key Vault:

```ps1
vaultscan config add kv --alias mykv --vault-name vault --resource-group-name rg --subscription-id id 
```

Configuring an Keepass:
```ps1
vaultscan config add keepass --alias my_keepass --path C:\databases\passwords.kdbx
```


To look at the configured vaults you can run:

```ps1
vaultscan config view
```

> Internally, the tool creates a ```vaults.json``` file on the user HOME folder ```C:\Users\user\.vaultscan```

## Searching secrets by their names
TO DO

## Searching secrets using regex
TO DO

# Contribute

To contribute with the development of this repo you could use poetry to control the dependencies.

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
VAULTSCAN_VERBOSE_ENABLED = True
```

> For more information just look at the [settings.py](./vaultscan/settings.py) file


## Testing 

```ps1
pytest
```
