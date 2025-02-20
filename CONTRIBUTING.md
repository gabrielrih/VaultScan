# Contributing

To contribute with the development of this repo you could use [Poetry](https://python-poetry.org/) to manage the Python version and control the dependencies.

```ps1
poetry install
```

To use the cli just run:

```ps1
vaultscan --help
```

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
