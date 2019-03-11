#!/usr/bin/env python
import click
import os
import os.path
import sys

import version

from commands import family
from commands import export
from commands import imprt
from commands import publish
from commands import report

from lib.config import Config

# Main command group
@click.group()
@click.version_option(version=version.VERSION, message="%(version)s")
@click.pass_context
def cli(ctx):
    """
    CLI to manage the Plebians data file.
    """
    config_file = os.getenv('HOME') + "/.config/plebeians.yml"
    if os.path.isfile(config_file):
        config = Config(os.getenv('PLEBEIANS_ORG'), config_file)
        ctx.obj = {
            'config': config
        }
    else:
        print("Config file '%s' missing." % (config_file))
        sys.exit(1)

# ------------------------------------------------------------------------------
# Add commands to main group
cli.add_command(family.family)
cli.add_command(export.export)
cli.add_command(imprt.imprt)
cli.add_command(publish.publish)
cli.add_command(report.report)

# ------------------------------------------------------------------------------
# Allow execution as a script
if __name__ == '__main__':
    cli()
