"""Console script for podcust.

Useful documentation at:
https://click.palletsprojects.com/en/7.x/quickstart/#nesting-commands
https://click.palletsprojects.com/en/7.x/complex/
https://dev.to/drcloudycoder/develop-python-cli-with-subcommands-using-click-4892
"""

import click
from podcust.commands import demo, transmission
from podcust import __version__ as cver


@click.group()
def main(args=None):
    """Podcust commands provide a wrapper around lower level utilities
    from podman, the Operating System and the container you are managing."""
    click.echo("Welcome to Podman Custodian!")


@click.command()
def version():
    """Show podcust version."""
    print(f"Current podcust version is: {cver}")


main.add_command(demo.demo)
main.add_command(transmission.transmission)
main.add_command(version)
