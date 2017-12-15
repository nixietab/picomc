import click

from picomc.globals import gconf


@click.group()
def config_cli():
    """Configure picomc."""
    pass


@config_cli.command()
def show():
    """Print the current config."""
    for k, v in gconf.items():
        print("{}: {}".format(k, v))


@config_cli.command()
@click.argument('key')
@click.argument('value')
def set(key, value):
    setattr(gconf, key, value)


@config_cli.command()
@click.argument('key')
def get(key):
    try:
        print(getattr(gconf, key))
    except AttributeError:
        print("No such attribute.")


@config_cli.command()
@click.argument('key')
def delete(key):
    delattr(gconf, key)