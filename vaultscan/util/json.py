from json import load, dump, dumps
from typing import Dict


INDENT = 4


class JsonFileManager:
    @staticmethod
    def load(path: str) -> Dict:
        with open(path, "r") as file:
            return load(file)

    @staticmethod
    def write(content: Dict, path: str) -> None:
        with open(path, 'w') as f:
            dump(content, f, indent=INDENT)



class JsonHandler:
    @staticmethod
    def beatifull_print(content: Dict) -> str:
        return dumps(content, indent=INDENT)
