from json import load, dump, dumps
from typing import Dict


INDENT = 4


def load_json_from_file(path: str) -> Dict:
    with open(path, "r") as file:
        return load(file)


def write_json_on_file(content: Dict, path: str) -> None:
    with open(path, 'w') as f:
        dump(content, f, indent=INDENT)


def beatifull_print(content: Dict) -> str:
    return dumps(content, indent=INDENT)
