from flask import  g, current_app
from flask.cli import with_appcontext
import click

@click.command('print-g')
@with_appcontext
def test_print():
    click.echo(current_app)

test_print()