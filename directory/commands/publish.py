import click
import os.path
from ftplib import FTP

# ------------------------------------------------------------------------------
@click.group()
def publish():
    """ Publish ... """
    pass

# ------------------------------------------------------------------------------
@publish.command()
@click.pass_context
def data(ctx):
    """ Publish the data file, directory.json, to an FTP site """
    config = ctx.obj['config']
    __upload_file(config, 'directory.json', 'txt')

# ------------------------------------------------------------------------------
@publish.command()
@click.pass_context
def pdf(ctx):
    """ Publish the PDF version to an FTP site """
    config = ctx.obj['config']
    __upload_file(config, "%s.pdf" % (config.org), 'bin')

# ------------------------------------------------------------------------------
# file_type: txt | bin
def __upload_file(config, file_name, file_type):
    host = config.get('publish:host')
    user = config.get('publish:username')
    passwd = config.get('publish:password')

    local_file = config.path('data:path', file_name)

    if not os.path.exists(local_file):
        raise Exception("Local file does not exist: '%s" % (local_file))

    remote = config.path('publish:base_path', 'publish:file_map:%s' % (file_name))
    remote_file = os.path.basename(remote)
    remote_path = os.path.dirname(remote)

    ftp = FTP(host, user, passwd)
    ftp.cwd(remote_path)

    if file_type == 'txt':
        with open(local_file, "r") as fp:
            ftp.storlines('STOR %s' % (remote_file), fp)
    elif file_type == 'bin':
        with open(local_file, "rb") as fp:
            ftp.storbinary('STOR %s' % (remote_file), fp)
    
    ftp.quit()

    print "Successfully published '%s' to %s/%s/%s" % (local_file, host, remote_path, remote_file)
