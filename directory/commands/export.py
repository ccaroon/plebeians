import click

from lib.print_directory import PrintDirectory
# ------------------------------------------------------------------------------
@click.group()
def export():
    """ Export the Directory Data to various other formats """
    pass
# ------------------------------------------------------------------------------
@export.command()
@click.pass_context
def pdf(ctx):
    """Export Directory Data to a Pretty PDF"""
    pdir = PrintDirectory(ctx.obj['data_path'])
    pdir.render()
