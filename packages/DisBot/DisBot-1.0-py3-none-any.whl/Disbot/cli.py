import click
from Disbot.subcommands import commands as subcommands


@click.group()
def Main():
    pass


Main.add_command(subcommands.createbot)