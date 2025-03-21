#!/bin/bash
# Building the package using Poetry
# Here we assume that the new version is already configured on the __version__ file
PACKAGE_VERSION=$(python -c "from vaultscan import __version__; print(__version__)")
if [ ! $? -eq 0 ]; then echo "Error on getting package version"; exit 1; fi;
if [ ! -n "$PACKAGE_VERSION" ]; then echo "Error: The PACKAGE_VERSION variable shoud not be empty"; fi
echo "PACKAGE_VERSION: $PACKAGE_VERSION"

echo "🔹Using the 'poetry version' command to inject the new version on the pyproject.toml file. It would be used by poetry install and poetry build"
poetry version $PACKAGE_VERSION
cat pyproject.toml

poetry install --no-interaction
if [ ! $? -eq 0 ]; then echo "Error installing package"; exit 1; fi;
poetry build
if [ ! $? -eq 0 ]; then echo "Error building package"; exit 1; fi;

echo "🔹Here we have the package files"
ls ./dist/
