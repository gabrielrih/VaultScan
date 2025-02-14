from json import load, dump
from typing import Dict


class JsonFileManager:
    @staticmethod
    def load(path: str) -> Dict:
        with open(path, "r") as file:
            return load(file)

    @staticmethod
    def write(content: Dict, path: str) -> None:
        with open(path, 'w') as f:
            dump(content, f, indent=4)