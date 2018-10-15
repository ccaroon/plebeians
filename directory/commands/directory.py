import click

from lib.directory import Directory

@click.command()
@click.argument("name")
@click.argument("address")
@click.pass_context
def view(ctx, name, address):
    directory = Directory(ctx.obj['directory_file'])
    family = directory.get(name, address)
    print family

@click.command()
@click.pass_context
def dump(ctx):
    directory = Directory(ctx.obj['directory_file'])
    print directory

@click.command()
@click.argument("name")
@click.argument("address")
@click.pass_context
def edit(ctx, name, address):
    directory = Directory(ctx.obj['directory_file'])

    family = directory.get(name, address)

    need_to_save = False
    fields = family.to_json()
    for name,value in fields.iteritems():
        if name in ('id', 'members'):
            continue

        new_value = raw_input("%s (%s): " % (name, value))
        if new_value:
            need_to_save = True
            setattr(family, name, new_value)

    if need_to_save:
        directory.save()
