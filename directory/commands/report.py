import click

from lib.directory import Directory
# ------------------------------------------------------------------------------
@click.group()
def report():
    """ Generate reports on the Directory data. """
    pass
# ------------------------------------------------------------------------------
@report.command()
@click.pass_context
def stats(ctx):
    """ Show some directory stats """
    directory = Directory(ctx.obj['directory_file'])
    directory.stats()
