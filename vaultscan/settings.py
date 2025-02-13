from vaultscan.util.converter import TypeConverter

import os

from dotenv import load_dotenv
load_dotenv() # loading .env file


class GlobalSettings:
    @property
    def verbose_enabled(self) -> bool:
        return TypeConverter.string_to_boolean(
            os.getenv('VAULTSCAN_VERBOSE_ENABLED', 'False')
        )
