import click

from lib.directory import Directory

@click.group()
def report():
    pass

@report.command()
@click.pass_context
def stats(ctx):
    directory = Directory(ctx.obj['directory_file'])
    directory.stats()
