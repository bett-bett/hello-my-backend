import click
from app import app

@app.cli.command("ping")
def ping():
    """ping"""
    click.echo("Pong!")

@app.cli.command("hello")
@click.option("--name", default="World", help="Name to greet")
def greet_command(name):
    """Greets user by name. `flask greet --name=name`"""
    click.echo(f"Hello, {name}!")