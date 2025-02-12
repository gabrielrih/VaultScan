import click


@click.group()
def main(): pass


@click.group()
def config() -> None:
    ''' Manage the configuration vaults '''
    pass


@config.command()
def create() -> None:
    ''' Register a new vault on the configuration '''
    pass


@config.command()
def remove() -> None:
    ''' Remove a vault from the configuration'''
    pass


@click.group()
def find() -> None:
    ''' Find objects on vaults  '''
    pass


@find.command()
def secrets() -> None:
    ''' Find secrets '''
    pass


@find.command()
def keys() -> None:
    ''' Find keys '''
    raise NotImplementedError()


@find.command()
def certificates() -> None:
    ''' Find certificates '''
    raise NotImplementedError()


main.add_command(config)
main.add_command(find)
if __name__ == '__main__':
    main()
