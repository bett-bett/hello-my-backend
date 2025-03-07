import click
from flask import Blueprint
bp = Blueprint('cli', __name__, cli_group=None)

@bp.cli.command("ping")
def ping():
    """ping"""
    click.echo("Pong!")

@bp.cli.command("hello")
@click.option("--name", default="World", help="Name to greet")
def greet_command(name):
    """Greets user by name. `flask greet --name=name`"""
    click.echo(f"Hello, {name}!")