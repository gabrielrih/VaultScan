# vaultscan
VaultScan is a CLI tool for searching objects across multiple vault engines, supporting regex and exact name searches for efficient retrieval.

# Index
- [Features](#features)
- [Installation](#installation)
    - [Via GitHub Releases](#via-github-releases)
- [Usage](#usage)
    - [Configuring the vaults](#configuring-the-vaults)
    - [Authentication & Engine Configuration](#authentication--engine-configuration)
    - [Searching secrets by its exact name](#searching-secrets-by-their-names)
    - [Searching secrets using regex](#searching-secrets-using-regex)
- [Supported Operating Systems & Limitations](#supported-operating-systems--limitations)
- [Contributing](#Contributing)

# Features

The main group commands available on this tool are:

- **Vault:** To configure a list of vaults used for searching objects
- **Find:** To find objects across vaults
- **Config:** To manage configurations

# Installation

## Via GitHub Releases
You can install this package by downloading the latest ```.whl``` file from GitHub Releases and using pip to install it.

- Go to the [Releases page](https://github.com/gabrielrih/VaultScan/releases/tag/latest).
- Find the latest version and download the ```.whl``` file (Example, ```vaultscan-0.1.5-py3-none-any.whl```).
Or you can download it from the terminal:

```ps1
wget -O "vaultscan-0.1.5-py3-none-any.whl" "https://github.com/gabrielrih/VaultScan/releases/download/latest/vaultscan-0.1.5-py3-none-any.whl"
```

- After downloading the .whl file, install it using pip:

```ps1
pip install --user vaultscan-0.1.5-py3-none-any.whl
```

By doing that a ```vaultscan.exe``` file will be created probably on the folder: ```C:\Users\user\AppData\Roaming\Python\Python312\Scripts```. So, you must add this folder on the user PATH.

To see the installed version you can run:

```ps1
pip show vaultscan
```

# Usage

After installation, run the CLI with:

```ps1
vaultscan --help
```

## Configuring the vaults
First of all you must configure the vaults you want to use in the tool. This is a required step.

### Configuring an Azure Key Vault

```ps1
vaultscan vault add kv --alias mykv --vault-name vault --resource-group-name rg --subscription-id id 
```

### Configuring a Keepass database

```ps1
vaultscan vault add keepass --alias my_keepass --path "C:\databases\passwords.kdbx"
```

To look at the configured vaults you can run:

```ps1
vaultscan vault list
```

## Authentication & Engine Configuration
Each vault engine has its own authentication method. Below is an overview of how authentication works for supported engines:

### Azure Key Vault

The [Azure Key Vault](https://azure.microsoft.com/en-us/) engine uses the [```DefaultAzureCredential```](https://learn.microsoft.com/en-us/dotnet/api/azure.identity.defaultazurecredential?view=azure-dotnet) class to authentication and authorization. This class can use environment variable, managed identity or even the ```az cli```.

The easiest and recommended way to authenticate is using az cli. By using service principal you should set the following environment variables:

On Windows:
```ps1
$Env:AZURE_CLIENT_ID="your-client-id"
$Env:AZURE_TENANT_ID="your-tenant-id"
$Env:AZURE_CLIENT_SECRET="your-client-secret"
```

On Linux:
```bash
export AZURE_CLIENT_ID="your-client-id"
export AZURE_TENANT_ID="your-tenant-id"
export AZURE_CLIENT_SECRET="your-client-secret"
```

[Click here for more information](https://microsoft.github.io/spring-cloud-azure/4.0.0-beta.3/4.0.0-beta.3/reference/html/authentication.html)

### Keepass

[Keepass](https://keepass.info/) is a free open source password manager, which helps you to manage your passwords in a secure way. You can store all your passwords in one database, which is locked with a master key. So you only have to remember one single master key to unlock the whole database.

It means the authentication of the keepass database is by using a master key provided by the user when configuring the vault.

```
vaultscan vault add keepass --help
```

> The password is securely encrypted and saved.


## Searching secrets by its exact name

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

## Searching secrets using regex

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


# Supported Operating Systems & Limitations

**Supported Operating Systems**
- Windows
- Linux

**Limitations**
- Keyring Support:
    - On Windows and WSL, secure keyring backends require additional configuration. Is common to have the following error on WSL:

```
keyring.errors.NoKeyringError: No recommended backend was available. Install a recommended 3rd party backend package; or, install the keyrings.alt package if you want to use the non-recommended backends.
```

- CLI Dependencies:
    - Some features (like colored output) may depend on terminal capabilities.
- Environment Variables:
    - Ensure your system’s PATH includes directories like ```~/.local/bin``` (Linux/macOS) or ```%APPDATA%\Python\Scripts``` (Windows) for proper command discovery.

# Contributing

For detailed contribution guidelines, see [CONTRIBUTING.md](./CONTRIBUTING.md).
