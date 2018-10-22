import click
import re

from lib.directory import Directory
from lib.family import Family
from lib.person import Person
from lib.prompt import Prompt
# ------------------------------------------------------------------------------
@click.group()
def family():
    """ Manage Family Data """
    pass
# ------------------------------------------------------------------------------
@family.command()
@click.argument("name")
@click.pass_context
def view(ctx, name):
    """ View a Family """
    directory = Directory(ctx.obj['directory_file'])
    family = directory.get(name)

    family = Prompt.choose_from_list(family, "Which Family? ")

    print repr(family)
# ------------------------------------------------------------------------------
@family.command()
@click.argument("name")
@click.pass_context
def edit(ctx, name):
    """ Edit a Family's Data """
    directory = Directory(ctx.obj['directory_file'])
    family = directory.get(name)

    family = Prompt.choose_from_list(family, "Which Family? ")

    need_to_save = False
    fam_data = family.to_json()
    fields = fam_data.keys()
    fields.sort()
    for name in fields:
        if name in ('id', 'name', 'members'):
            continue

        # TODO: what if notes already exist?
        if name == 'notes':
            new_value = Prompt.notes()
        else:
            old_value = fam_data[name]
            new_value = Prompt.input("%s (%s): " % (name, old_value))

        if new_value:
            need_to_save = True
            setattr(family, name, new_value)

    if need_to_save:
        directory.save()
# ------------------------------------------------------------------------------
@family.command()
@click.argument("name")
@click.option("--family-name", "-f", help="Specify Family Name")
@click.pass_context
def edit_member(ctx, name, family_name):
    """ Edit a Family Member """
    directory = Directory(ctx.obj['directory_file'])

    family, person = __find_member(directory, name, family_name)

    if person:
        need_to_save = False
        person_data = person.to_json()
        fields = person_data.keys()
        fields.sort()
        for field in fields:
            if field in ('name', 'photo'):
                continue

            if field == 'phone':
                new_value = Prompt.phone()
                if new_value:
                    person_data['phone'].update(new_value)
                    new_value = person_data['phone']
            elif field == 'relationships':
                new_value = Prompt.relationships()
            else:
                old_value = person_data[field]
                new_value = Prompt.input("%s (%s): " % (field, old_value))

            if new_value:
                need_to_save = True
                setattr(person, field, new_value)

        if need_to_save:
            directory.save()
    else:
        print "Member not found: '%s'" % (name)

# ------------------------------------------------------------------------------
@family.command()
@click.argument("name")
@click.pass_context
def add(ctx, name):
    """ Add a new Family to the Directory """
    directory = Directory(ctx.obj['directory_file'])

    family_data = Family(name=name).to_json()
    fields = family_data.keys()
    fields.sort()
    print "----- Adding the '%s' Family -----" % (family_data['name'])
    for name in fields:
        if name in ('id', 'name', 'members'):
            continue

        new_value = Prompt.input("%s: " % (name))
        family_data[name] = new_value if new_value else ""

    new_family = Family(**family_data)
    print new_family
    directory.add(new_family)

    add_members = True
    template = Person().to_json()
    fields = template.keys()
    fields.sort()
    while add_members:
        print "----- Add Family Member -----"
        member_data = template.copy()
        for name in fields:
            if name in ('photo'):
                continue

            if name == 'relationships':
                member_data['relationships'] = Prompt.relationships()
            elif name == 'phone':
                member_data['phone'] = Prompt.phone()
            else:
                new_value = Prompt.input("%s: " % (name))
                member_data[name] = new_value if new_value else ""

        member_data['birthday'] = Prompt.input("birthday (YYYY-MM-DD)? ")
        member_data['photo'] = re.sub('\W','-', member_data['name'].lower()) + ".jpeg"

        new_member = Person(**member_data)
        new_family.add(new_member)

        add_members = Prompt.more(msg="Add More Members")

    # print new_family
    directory.save()
# ------------------------------------------------------------------------------
@family.command()
@click.argument("name")
@click.pass_context
def delete(ctx, name):
    """ Delete a Family from the Directory """
    directory = Directory(ctx.obj['directory_file'])
    family = directory.get(name)

    family = Prompt.choose_from_list(family, "Which Family? ")

    choice = Prompt.input("Confirm Delete: %s - %s (yes|no)? " % (family.name, family.address))
    if choice == 'yes':
        directory.delete(family)
        directory.save()
    else:
        print "Not Deleting Family: %s - %s" % (family.name, family.address)
# ------------------------------------------------------------------------------
@family.command()
@click.argument("name")
@click.option("--family-name", "-f", help="Specify Family Name")
@click.pass_context
def del_member(ctx, name, family_name):
    """ Remove a Family Member from a Family """
    directory = Directory(ctx.obj['directory_file'])

    family, person = __find_member(directory, name, family_name)

    if person:
        family.delete(person)
        directory.delete_photo(person)

        directory.save()
        print "'%s' successfully deleted." % (name)
    else:
        print "Member not found: '%s'" % (name)
# ------------------------------------------------------------------------------
@family.command()
@click.argument("thing")
@click.pass_context
def fix(ctx, thing):
    """ Run bulk data fix commands """
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
    elif thing == "add_notes":
        directory.save()
    elif thing == "family_member_to_list":
        directory.save()
    elif thing == "directory_to_list":
        directory.save()
    else:
        print "I'm sorry Dave, I'm afraid I can't fix %s!" % (thing)
# ------------------------------------------------------------------------------
def __find_member(directory, name, family_name=None):
    person = None
    family = None
    lookup_name = None

    if family_name:
        lookup_name = family_name
    else:
        name_parts = name.split()
        lookup_name = name_parts.pop()

    family = directory.get(lookup_name)
    family = Prompt.choose_from_list(family, "Which Family? ")

    if family:
        person = family.get(name)

    return (family, person)
