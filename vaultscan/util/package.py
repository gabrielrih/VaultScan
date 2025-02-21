def get_top_level_package(package: str) -> str:
    # Assuming your package structure is like "vaultscan.util" or "vaultscan.core", etc.
    return package.split('.')[0]


PACKAGE_NAME = get_top_level_package(__package__) if __package__ else "VaultScan"
