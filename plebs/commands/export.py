import click

from lib.exporter import Exporter
from lib.print_directory import PrintDirectory
# ------------------------------------------------------------------------------
@click.group()
def export():
    """ Export the Directory Data to various other formats """
    pass
# ------------------------------------------------------------------------------
@export.command()
@click.option("--bdays", is_flag=True, default=False, help="Only Render the BDay Page.")
@click.pass_context
def pdf(ctx, bdays):
    """Export Directory Data to a Pretty PDF"""
    config = ctx.obj['config']

    output_filename = config.org
    if bdays:
        output_filename += "-BDays"

    pdir = PrintDirectory(config.path('data:path'), output_filename)
    pdir.render(bdays_only=bdays)

# ------------------------------------------------------------------------------
@export.command()
@click.pass_context
def txt(ctx):
    """Export Directory Data to a Text file"""
    config = ctx.obj['config']

    exporter = Exporter(config.path('data:path'))
    exporter.export_markdown(config.org)
