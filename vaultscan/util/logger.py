import click

from vaultscan.settings import GlobalSettings


settings = GlobalSettings()


class LoggerFactory:
    @staticmethod
    def get_logger():
        return ClickLogger()


class ClickLogger:
    @staticmethod
    def success(message: str):
        message = f'SUCCESS: {message}' 
        click.secho(message, fg='green')

    @staticmethod
    def warning(message: str):
        message = f'WARNING: {message}' 
        click.secho(message, fg='yellow')

    @staticmethod
    def error(message: str):
        message = f'ERROR: {message}' 
        click.secho(message, fg='red')

    @staticmethod
    def verbose(message: str):
        ''' Just printing verbose message when the config is enabled '''
        if not settings.verbose_enabled:
            return
        message = f'VERBOSE: {message}'
        click.secho(message, fg='cyan')
