import click
import json

from lib.family import Family
from lib.person import Person
from lib.prompt import Prompt
from lib.directory import Directory
from lib.vcf_parser import VCFParser
# ------------------------------------------------------------------------------
@click.group()
def imprt():
    """ Import data into the Directory from various other formats. """
    pass
# ------------------------------------------------------------------------------
@imprt.command()
@click.argument("vcf_file")
@click.pass_context
def vcf(ctx, vcf_file):
    """Import VCF Card"""

    config = ctx.obj['config']
    directory = Directory(config.path('data:path', 'directory.json'))

    vcf = VCFParser(photo_dir=config.path('data:path', 'photos'))
    data = vcf.parse(vcf_file)

    print "----- %s - %s -----" % (data['last_name'], data['address'])

    family = directory.get(data['last_name'])
    family = Prompt.choose_from_list(family, "Which Family")
    if family:
        person = family.get(data['name'])
        if person:
            print "%s already exists." % (data['name'])
        else:
            new_person = Person(**data)
            family.add(new_person)
            directory.save()
    else:
        new_family = Family(
            name=data['last_name'],
            address=data['address'],
            city=data['city'],
            state=data['state'],
            zip=data['zip'],
            members=[data]
        )
        directory.add(new_family)
        directory.save()






# 
