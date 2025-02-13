import os

from unittest import TestCase
from typing import Dict
from json import dump


from vaultscan.util.json import (
    load_json_from_file,
    write_json_on_file,
    beatifull_print
)


class TestJSON(TestCase):
    def setUp(self):
        self.utility = Utility()

    def test_load_json_from_file(self):
        # Given
        filename = 'example_for_read.json'
        self.utility.create_sample_json_file(filename)

        # When
        content: Dict = load_json_from_file(path = filename)

        # Then
        self.assertIsInstance(content, Dict)

    def test_write_json_on_file(self):
        # Given
        # Removing file if exists before trying to create it again
        filename = 'example_for_write.json'
        self.utility.remove_file(filename)
        
        # When
        content: Dict = self.utility.get_sample_json_content()
        write_json_on_file(content, filename)

        # Then
        self.assertTrue(
            Utility.is_file_exists(filename),
            msg = f'The file {filename} should exist on disk!')


    def test_beatifull_print(self):
        # Given
        raw_content: Dict = self.utility.get_sample_json_content()

        # When
        content: str = beatifull_print(raw_content)

        # Then
        self.assertIsInstance(content, str)
        self.assertIsNotNone(content)


class Utility:
    @staticmethod
    def create_sample_json_file(path: str):
        Utility.remove_file(path)
        content: Dict = Utility.get_sample_json_content()
        Utility.create_file(content, path)

    @staticmethod
    def get_sample_json_content() -> Dict:
        return {
            'values': ['one', 'two']
        }

    @staticmethod
    def remove_file(path: str) -> None:
        if Utility.is_file_exists(path):
            os.remove(path)

    @staticmethod
    def is_file_exists(path: str) -> bool:
        return os.path.exists(path)

    @staticmethod
    def create_file(content: Dict, path: str) -> None:
        with open(path, 'w') as f:
            dump(content, f, indent=4)
