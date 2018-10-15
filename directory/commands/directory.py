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
@click.argument("thing")
@click.pass_context
def data_fix(ctx, thing):
    directory = Directory(ctx.obj['directory_file'])

    # Fix relationships structure
    if thing == "relationships":
        for fam in directory.families():
            for person in fam.members():
                new_rels = []
                for rel in person.relationships:
                    new_rels.append({'type': rel['type'].capitalize(), 'name': rel['name']})

                person.relationships = new_rels
        directory.save()
    # Fix email addr -- set to None if none
    elif thing == "email":
        for fam in directory.families():
            for person in fam.members():
                if person.email == "N/A":
                    person.email = None
        directory.save()
    else:
        print "data_fix: Unknown 'thing': %s" % (thing)

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
