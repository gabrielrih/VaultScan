import json
import click

from tabulate import tabulate
from enum import Enum
from typing import Any, List, Dict

from vaultscan.util.output.logger import LoggerFactory


logger = LoggerFactory.get_logger(__name__)


class OutputFormat(Enum):
    JSON = "json"
    TABLE = "table"
    STANDARD = "standard"

    def get_values() -> List[str]:
        values = list()
        for format in OutputFormat:
            values.append(format.value)
        return values


class OutputHandler:
    def __init__(self, format: OutputFormat = OutputFormat.JSON):
        self.format = format

    def print(self, data: Any):
        if not data:
            return
        logger.debug(f'Printing using {self.format} format')
        if self.format == OutputFormat.JSON:
            return self.print_as_json(data)
        if self.format == OutputFormat.TABLE:
            return self.print_as_table(data)
        self.print_as_string(data)

    def print_as_json(self, data: Any):
        click.secho(json.dumps(data, indent=4))

    def print_as_table(self, data: List[Dict[str, Any]]):
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            headers = data[0].keys() if data else []
            table = tabulate(
                [item.values() for item in data],
                headers = headers,
                tablefmt = "grid"
            )
            click.secho(table)
            return
        logger.error("Invalid data format for table output.")

    def print_as_string(self, data: Any):
        click.secho(str(data))
