import subprocess
import random
import string


def generate_random_name() -> str:
    length = 8
    return ''.join(
        random.choice(string.ascii_lowercase) for _ in range(length)
    )


RANDOM_VAULT_NAME = generate_random_name()


class TestCliVaultCommand:
    def test_add_and_remove_kv(self):
        # Given
        vault_name = f'{RANDOM_VAULT_NAME}-kv'

        # Adding it
        result_add = subprocess.run(
            ['vaultscan', 'vault', 'add', 'keyvault',
             '--alias', vault_name,
             '--vault-name', vault_name,
             '--rg', 'fake-rg',
             '--subscription-id', 'fake-subscription-id'],  # Simulating the CLI execution
            capture_output = True,  # Capture stdout and stderr
            text = True  # Decode output as text (instead of bytes)
        )
        assert result_add.returncode == 0  # Ensure the command ran successfully

        # Removing it
        result_remove = subprocess.run(
            ['vaultscan', 'vault', 'remove', '--alias', vault_name],  # Simulating the CLI execution
            capture_output = True,  # Capture stdout and stderr
            text = True  # Decode output as text (instead of bytes)
        )
        assert result_remove.returncode == 0  # Ensure the command ran successfully
    
    def test_add_keepass(self):
       # TO DO
       # It's necessary to allow the possibility to pass the password has an argument
       pass

    def test_rename_vault(self):
        # Given
        old_vault_name = f'{RANDOM_VAULT_NAME}-kv'
        new_vault_name = f'{RANDOM_VAULT_NAME}-kv'

        # When
        # Add, rename and then remove the vault
        result_add = subprocess.run(
            ['vaultscan', 'vault', 'add', 'keyvault',
             '--alias', old_vault_name,
             '--vault-name', old_vault_name,
             '--rg', 'fake-rg',
             '--subscription-id', 'fake-subscription-id'],  # Simulating the CLI execution
            capture_output = True,  # Capture stdout and stderr
            text = True  # Decode output as text (instead of bytes)
        )
        result_rename = subprocess.run(
            ['vaultscan', 'vault', 'rename',
             '--old-alias', old_vault_name,
             '--new-alias', new_vault_name],  # Simulating the CLI execution
            capture_output = True,  # Capture stdout and stderr
            text = True  # Decode output as text (instead of bytes)
        )
        result_remove = subprocess.run(
            ['vaultscan', 'vault', 'remove', '--alias', old_vault_name],  # Simulating the CLI execution
            capture_output = True,  # Capture stdout and stderr
            text = True  # Decode output as text (instead of bytes)
        )

        # Then
        assert result_add.returncode == 0
        assert result_rename.returncode == 0
        assert result_remove.returncode == 0

    def test_list(self):
        # When
        result = subprocess.run(
            ['vaultscan', 'vault', 'list'],  # Simulating the CLI execution
            capture_output = True,  # Capture stdout and stderr
            text = True  # Decode output as text (instead of bytes)
        )
        # Then
        assert result.returncode == 0  # Ensure the command ran successfully
        output_message = result.stdout.strip()
        assert output_message is not None

