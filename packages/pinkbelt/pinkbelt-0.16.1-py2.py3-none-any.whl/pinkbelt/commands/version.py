import click

from pinkbelt.version import VERSION

@click.group(invoke_without_command=True, help='Version')
def cli():
    print(VERSION)
