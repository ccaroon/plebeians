import click
from PIL import Image

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
    directory = Directory(ctx.obj['config'].path('data:path', 'directory.json'))
    directory.stats()

# ------------------------------------------------------------------------------
@report.command()
@click.pass_context
def photos(ctx):
    """ List members who either don't have a photo or their photo it too small. """
    config = ctx.obj['config']
    directory = Directory(config.path('data:path', 'directory.json'))

    missing = []
    too_small = []
    for family in directory.families():
        for member in family.members():
            if not member.photo or member.photo == 'unknown.jpeg':
                missing.append(member.name)
            else:
                # print config.path('data:path','photos',member.photo)
                img = Image.open(config.path('data:path','photos',member.photo))
                size = img.size
                if size[0] < 300 or size[1] < 300:
                    too_small.append(member.name)

    print("----- Missing Photo -----")
    for name in missing:
        print(name)

    print("\n")

    print("----- Photo Too Small -----")
    for name in too_small:
        print(name)
