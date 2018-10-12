#!/usr/bin/env python
import click

import version

from commands import export
from commands import report

# Main command group
@click.group()
@click.version_option(version=version.VERSION, message="%(version)s")
@click.pass_context
def cli(ctx):
    """
    CLI to manager the Plebians data file.
    """
    data_path = "/Users/ccaroon/Dropbox/MCUMC/mcumc"
    ctx.obj = {
        'data_path': data_path,
        'directory_file': "%s/directory.json" % (data_path)
    }

# ------------------------------------------------------------------------------
# Add commands to main group
cli.add_command(export.export)
cli.add_command(report.report)

# ------------------------------------------------------------------------------
# Allow execution as a script
if __name__ == '__main__':
    cli()
