# vaultscan
VaultScan is a CLI tool for searching objects across multiple vault engines, supporting regex and exact name searches for efficient retrieval.

# Index
- [Features](#features)
- [Installation](#installation)
    - [Requirements](#requirements)
    - [Via GitHub Releases](#via-github-releases)
- [Usage](#usage)
    - [Configuring the vaults](#configuring-the-vaults)
    - [Authentication & Engine configuration](#authentication--engine-configuration)
    - [Searching secrets by its exact name](#searching-secrets-by-their-names)
    - [Searching secrets using regex](#searching-secrets-using-regex)
- [Supported OS & Limitations](#supported-os--limitations)
- [Contributing](#Contributing)

# Features

The main group commands available on this tool are:

- **Vault:** To configure a list of vaults used for searching objects
- **Find:** To find objects across vaults
- **Config:** To manage configurations

# Installation

## Requirements

- [Python](https://www.python.org/downloads/): >= 3.11

## Via GitHub Releases
You can install this tool by downloading the latest ```.whl``` file from GitHub Releases and using pip.

- Go to the [Releases page](https://github.com/gabrielrih/VaultScan/releases/).
- Find the latest version and download the ```.whl``` file (Example, ```vaultscan-1.1.0-py3-none-any.whl```).

Or you can download it from the terminal:

```
wget -O "vaultscan-1.1.0-py3-none-any.whl" "https://github.com/gabrielrih/VaultScan/releases/download/v1.1.0/vaultscan-1.1.0-py3-none-any.whl"
```

- After downloading the .whl file, install it using pip:

```
pip install --user vaultscan-1.1.0-py3-none-any.whl
```

By doing that a ```vaultscan.exe``` file will be created probably on the folder: ```C:\Users\user\AppData\Roaming\Python\Python312\Scripts```. So, you must add this folder on the user PATH.

To see the installed version you can run:

```
pip show vaultscan
```

# Usage

After installation, run the CLI with:

```
vaultscan --help
```

## Configuring the vaults
First of all you must configure the vaults you want to use in the tool. This is a required step.

### Configuring an Azure Key Vault

```
vaultscan vault add keyvault --alias mykv --vault-name vault
```

> vault_name on Azure are unique, so you does not need more information than that.

### Configuring a Keepass database

```
vaultscan vault add keepass --alias my_keepass --path "C:\databases\passwords.kdbx"
```

Look at the configured vaults just running:

```
vaultscan vault list
```

## Authentication & Engine configuration
Each vault engine has its own authentication method. Below is an overview of how authentication works for supported engines:

### Azure Key Vault

The [Azure Key Vault](https://azure.microsoft.com/en-us/) engine uses the [```DefaultAzureCredential```](https://learn.microsoft.com/en-us/dotnet/api/azure.identity.defaultazurecredential?view=azure-dotnet) class for authentication and authorization. This class can uses environment variable, managed identity or even the ```az cli```.

The easiest and **recommended** way to authenticate is by using ```az cli```. 

But, you could also use a service principal by setting the following environment variables:

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

It means the authorization for the keepass database is through a password provided by the user when configuring the vault.

```
vaultscan vault add keepass --help
```

> The password is securely encrypted and saved on your local machine.

**Limitation**: It supports Keepass database when using master key. If you're using a [Key File](https://keepass.info/help/base/keys.html) to protect your secrets the cli won't work.

## Searching secrets by its exact name

Search for all secrets that match an exact name:

```
vaultscan find secrets my_secret_name --exact
```

Search for all secrets that match an exact name showing its values:

```
vaultscan find secrets my_secret_name --exact --show-values
```

Search for all secrets that match an exact name in an specific vault:

```
vaultscan find secrets my_secret_name --only-vault key_vault --exact
```

## Searching secrets using regex

Search for all secrets that match a given regex:
```
vaultscan find secrets host
```

Search for all secrets that match a given regex with its corresponding value:
```
vaultscan find secrets host --show-values
```

Search for all secrets that match a given regex in an specific vault:

```
vaultscan find secrets host --only-vault key_vault
```

## Searching all secrets

Search for all secrets in all vaults:

```
vaultscan find secrets
```

> This command can take a while if you are using a lot of vaults

Search for all secrets in an specific vault:

```
vaultscan find secrets --only-vault key_vault
```

## Counting secrets

Count for secrets that match a given regex in all vaults:

```
vaultscan find secrets my_secret_name --count-only
```

Count for secrets that match a given regex in an specific vault:

```
vaultscan find secrets my_secret --only-vault key_vault --count-only
```

Count for all secrets in an specific vault:

```
vaultscan find secrets --only-vault key_vault --count-only
```

# Supported OS & Limitations

**Supported Operating Systems**
- Windows
- Linux

**Limitations**
- Keyring Support:
    - On Windows and WSL, secure keyring backends require additional configuration. It's common to have the following error on WSL:

```
keyring.errors.NoKeyringError: No recommended backend was available. Install a recommended 3rd party backend package; or, install the keyrings.alt package if you want to use the non-recommended backends.
```

- CLI Dependencies:
    - Some features (like colored output) may depend on terminal capabilities.
- Environment Variables:
    - Ensure your system’s PATH includes directories like ```~/.local/bin``` (Linux/macOS) or ```%APPDATA%\Python\Scripts``` (Windows) for proper command discovery.
    - This is important so that you can run the ```vaultscan``` tool anywhere on the terminal.

# Contributing

For detailed contribution guidelines, see [CONTRIBUTING.md](./CONTRIBUTING.md).
