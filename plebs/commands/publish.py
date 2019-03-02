import click
import os
import os.path

from lib.publisher import Publisher
# ------------------------------------------------------------------------------
@click.group()
def publish():
    """ Publish Stuff """
    pass

# ------------------------------------------------------------------------------
@publish.command()
@click.pass_context
def data(ctx):
    """ Publish the data file, directory.json. """
    config = ctx.obj['config']

    local_file = config.path('data:path', 'directory.json')
    remote_file = config.path('publisher:remote_path', 'static/%s/directory.json' % (config.org.lower()))

    with Publisher(config.get('publisher')) as publish:
        publish.file(local_file, remote_file)

    print("Successfully published '%s' to '%s'" % (local_file, remote_file))

# ------------------------------------------------------------------------------
@publish.command()
@click.pass_context
def pdf(ctx):
    """ Publish the PDF version. """
    config = ctx.obj['config']

    local_file = config.path('data:path', '%s.pdf' % (config.org))
    remote_file = config.path('publisher:remote_path', 'MemberDirectory.pdf')

    with Publisher(config.get('publisher')) as publish:
        publish.file(local_file, remote_file, binmode=True)

    print("Successfully published '%s' to '%s'" % (local_file, remote_file))

# ------------------------------------------------------------------------------
@publish.command()
@click.argument('photo')
@click.pass_context
def photo(ctx, photo):
    """ Publish a photo. """
    config = ctx.obj['config']

    local_file = config.path('data:path', "photos/%s" % (photo))
    remote_file = config.path('publisher:remote_path', 'static/%s/photos/%s' % (config.org.lower(), photo))

    with Publisher(config.get('publisher')) as publish:
        publish.file(local_file, remote_file)

    print("Successfully published '%s' to '%s'" % (local_file, remote_file))

# ------------------------------------------------------------------------------
@publish.command()
@click.pass_context
def app(ctx):
    """ Publish the Plebeians Web App. """
    config = ctx.obj['config']

    # Organization data will NOT be published.
    org_path = "static/%s" % (config.org.lower())

    local_base_path = os.path.dirname(os.path.realpath(__file__+'../../..'))
    local_base_path += "/dist"

    remote_base_path = config.get('publisher:remote_path')

    count = 0
    with Publisher(config.get('publisher')) as publish:
        count = publish.directory(local_base_path, remote_base_path, [org_path])

    print("Successfully published %d files from '%s' to '%s'" % (count, local_base_path, remote_base_path))
