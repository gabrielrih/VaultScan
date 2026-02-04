import subprocess

from vaultscan.util.package import PACKAGE_NAME


class TestCliVersionCommand():
    def test_show_version(self):
        # Given
        expected_output_message = f'{PACKAGE_NAME} installed version:'

        # When
        result = subprocess.run(
            ['vaultscan', 'version'],  # Simulating the CLI execution
            capture_output = True,  # Capture stdout and stderr
            text = True  # Decode output as text (instead of bytes)
        )

        # Then
        assert result.returncode == 0  # Ensure the command ran successfully
        output_message = result.stdout.strip()
        assert expected_output_message in output_message
