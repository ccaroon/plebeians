import click
import re

from lib.directory import Directory
from lib.family import Family
from lib.person import Person

@click.group()
def family():
    pass

@family.command()
@click.argument("name")
@click.pass_context
def view(ctx, name):
    directory = Directory(ctx.obj['directory_file'])
    family = directory.get(name)

    if isinstance(family, list):
        family = __choose_family(family)

    print family

# @click.command()
# @click.argument("thing")
# @click.pass_context
# def data_fix(ctx, thing):
#     directory = Directory(ctx.obj['directory_file'])
#
#     # Fix relationships structure
#     if thing == "relationships":
#         for fam in directory.families():
#             for person in fam.members():
#                 new_rels = []
#                 for rel in person.relationships:
#                     new_rels.append({'type': rel['type'].capitalize(), 'name': rel['name']})
#
#                 person.relationships = new_rels
#         directory.save()
#     # Fix email addr -- set to None if none
#     elif thing == "email":
#         for fam in directory.families():
#             for person in fam.members():
#                 if person.email == "N/A":
#                     person.email = None
#         directory.save()
#     else:
#         print "data_fix: Unknown 'thing': %s" % (thing)
#
# @click.command()
# @click.argument("name")
# @click.argument("address")
# @click.pass_context
# def edit(ctx, name, address):
#     directory = Directory(ctx.obj['directory_file'])
#
#     family = directory.get(name, address)
#
#     need_to_save = False
#     fields = family.to_json()
#     for name,value in fields.iteritems():
#         if name in ('id', 'members'):
#             continue
#
#         new_value = raw_input("%s (%s): " % (name, value))
#         if new_value:
#             need_to_save = True
#             setattr(family, name, new_value)
#
#     if need_to_save:
#         directory.save()
#
@family.command()
@click.argument("name")
@click.pass_context
def add(ctx, name):
    directory = Directory(ctx.obj['directory_file'])

    family_data = Family(name=name).to_json()
    fields = family_data.keys()
    fields.sort()
    print "----- Adding the '%s' Family -----" % (family_data['name'])
    for name in fields:
        if name in ('id', 'name', 'members'):
            continue

        new_value = raw_input("%s: " % (name))
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
                member_data['relationships'] = []
                add_rels = True
                while add_rels:
                    print "----- Add Relationship -----"
                    rel_type = raw_input("%s type: " % (name))
                    rel_name = raw_input("%s name: " % (name))

                    if rel_type and rel_name:
                        member_data['relationships'].append({
                            'type': rel_type,
                            'name': rel_name
                        })

                    add_rels = __prompt_to_continue(msg="Add More Relations")
            elif name == 'phone':
                member_data['phone'] = {}
                add_phone = True
                while add_phone:
                    print "----- Add Phone -----"
                    phone_type = raw_input("%s type: " % (name)).upper()
                    phone_num = raw_input("%s number: " % (name))

                    # Format Number
                    number = re.sub("\D", "", phone_num)
                    match = re.search("(?P<exchange>\d\d\d)(?P<prefix>\d\d\d)(?P<last_four>\d\d\d\d)", number)
                    parts = match.groupdict()
                    number = "(%s) %s-%s" % (parts['exchange'], parts['prefix'], parts['last_four'])
                    member_data['phone'][phone_type] = number

                    add_phone = __prompt_to_continue(msg="Add More Phones")
            else:
                new_value = raw_input("%s: " % (name))
                member_data[name] = new_value if new_value else ""

        member_data['birthday'] = raw_input("birthday (YYYY-MM-DD)? ")
        member_data['photo'] = re.sub('\W','-', member_data['name'].lower()) + ".jpeg"

        new_member = Person(**member_data)
        new_family.add(new_member)

        add_members = __prompt_to_continue(msg="Add More Members")

    # print new_family
    directory.save()

@family.command()
@click.argument("name")
@click.pass_context
def delete(ctx, name):
    directory = Directory(ctx.obj['directory_file'])
    family = directory.get(name)

    if isinstance(family, list):
        family = __choose_family(family)

    choice = raw_input("Confirm Delete: %s - %s (yes|no)? " % (family.name, family.address))
    if choice == 'yes':
        directory.delete(family)
        directory.save()
    else:
        print "Not Deleting Family: %s - %s" % (family.name, family.address)


# ------------------------------------------------------------------------------
def __prompt_to_continue(**kwargs):
    accepted_choice = kwargs.get('accept', 'y')
    choice = raw_input("%s? (%s|n)" % (kwargs.get("msg", "Continue"), accepted_choice))
    return True if choice == accepted_choice else False

# ------------------------------------------------------------------------------
def __choose_family(family_list):
    family = None

    num = 1
    for fam in family_list:
        print "%d) %s - %s" % (num, fam.name, fam.address)
        num += 1

    choice = raw_input("Which Family? ")
    choice = int(choice) if choice else 0

    if choice in range(1, len(family_list)+1):
        family = family_list[choice-1]

    return family
