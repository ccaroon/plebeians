import click

from lib.print_directory import PrintDirectory

@click.group()
def export():
    pass

@export.command()
@click.pass_context
def pdf(ctx):
    """Export Directory Data to a Pretty PDF"""
    pdir = PrintDirectory(ctx.obj['data_path'])
    pdir.render()
