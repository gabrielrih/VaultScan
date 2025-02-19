import json
import click

from enum import Enum
from abc import ABC, abstractmethod
from tabulate import tabulate
from typing import Any, List, Dict


class OutputFormat(Enum):
    JSON = "json"
    TABLE = "table"
    STANDARD = "standard"

    @classmethod
    def get_values(cls) -> List[str]:
        return [ e.value for e in cls ]


class OutputHandler:
    def __init__(self, format: OutputFormat):
        self.format = format

    def print(self, data: Any):
        if not data:
            return
        if self.format == OutputFormat.JSON:
            PrintAsJson.print(data)
            return
        if self.format == OutputFormat.TABLE:
            PrintAsTable.print(data)
            return
        if self.format == OutputFormat.STANDARD:
            PrintAsString.print(data)
            return
        raise NotImplementedOutputFormat(f'The format {self.format} are not implemented in {OutputHandler.__class__}!')


class NotImplementedOutputFormat(Exception):
    pass


class Print(ABC):
    @staticmethod
    @abstractmethod
    def print(data: Any) -> None: pass


class PrintAsJson(Print):
    @staticmethod
    def print(data: Any) -> None:
        click.secho(json.dumps(data, indent=4))


class PrintAsString(Print):
    @staticmethod
    def print(data: Any) -> None:
        click.secho(str(data))


class PrintAsTable(Print):
    @staticmethod
    def print(data: List[Dict[str, Any]]) -> None:
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            headers = data[0].keys() if data else []
            table = tabulate(
                [item.values() for item in data],
                headers = headers,
                tablefmt = "grid"
            )
            click.secho(table)
            return
        raise InvalidDataFormatForTableOutput(f'Invalid data format for table output. Try another format: {OutputFormat.get_values()}')


class InvalidDataFormatForTableOutput(Exception):
    pass
