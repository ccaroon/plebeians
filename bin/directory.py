#!/usr/bin/env python
from datetime import datetime
import json
import md5
import os.path
import sys
# ------------------------------------------------------------------------------
class Directory:
    """ A Directory is a collection of Families """

    def __init__(self, data_file):
        self.__data_file = data_file
        print data_file
        with open(data_file, 'r') as fh:
            self.__data = json.load(fh)

        self.__families = {}
        for name, fam_data in self.__data.iteritems():
            family = Family(
                name = fam_data['name'],
                address = fam_data['address'],
                city = fam_data['city'],
                state = fam_data['state'],
                zip = fam_data['zip'],
                members = fam_data['members']
            )
            self.__families[family.id] = family

    def families(self):
        families = self.__families.values()
        families.sort(key=lambda f: f.name)
        return families

    def get(self, name, address):
        id = Family.compute_id(name, address)
        return self.__families.get(id, None)

    def to_json(self):
        data = {}
        for id, family in self.__families.iteritems():
            data[id] = family.to_json()

        return data

    def stats(self):
        families = self.families()
        fam_count = len(families)
        total_peeps = 0
        for fam in families:
            members = fam.members()
            mem_count = len(members)
            total_peeps += mem_count
            print "%s -> %d" % (fam.name, mem_count)

        print "---------------------------------"
        print "Families: %d | Total Members: %d" % (fam_count, total_peeps)

    def save(self, use_version=True):
        output_file = self.__data_file

        if use_version:
            (path, ext) = os.path.splitext(self.__data_file)
            id = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            output_file = "%s-%s%s" % (path, id, ext)

        with open(output_file, 'w') as fh:
            json.dump(self.to_json(), fh)

    def __str__(self):
        return json.dumps(self.to_json(), indent=2)

# ------------------------------------------------------------------------------
class Family:
    """ A Family is a family name, location and collection of Persons """

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.address = kwargs.get('address')
        self.city = kwargs.get('city')
        self.state = kwargs.get('state')
        self.zip = kwargs.get('zip')

        self.__members = {}
        for name, per_data in kwargs.get('members', {}).iteritems():
            name = per_data.get('name', None)
            if name:
                person = Person(
                    name = per_data.get('name'),
                    email = per_data.get('email', 'N/A'),
                    birthday = per_data.get('birthday'),
                    phone = per_data.get('phone', {}),
                    photo = per_data.get('photo'),
                    relationships = per_data.get('relationships', {})
                )
                self.__members[name] = person

        self.id = Family.compute_id(self.name, self.address)

    @classmethod
    def compute_id(cls, name, address):
        id = md5.md5("%s|%s" % (name, address))
        return id.hexdigest()

    def members(self):
        """ Return a list of family members """

        members = self.__members.values()
        members.sort(key=lambda m: m.name)
        return members

    def get(self, name):
        """ Get a family member (Person) by name """
        return self.__members.get(name, None)

    def to_json(self):
        data = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip': self.zip,
            'members': {}
        }

        for name, person in self.__members.iteritems():
            data['members'][name] = person.to_json()

        return data

    def __str__(self):
        return json.dumps(self.to_json(), indent=2)

# ------------------------------------------------------------------------------
class Person:
    """ A Person is a collection of information about an individual """

    BDAY_FORMAT = "%Y-%m-%d"

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email', 'N/A')

        self.birthday = None
        if kwargs.get('birthday'):
            self.birthday = datetime.strptime(kwargs.get('birthday'), Person.BDAY_FORMAT)

        self.phone = kwargs.get('phone', {})
        self.photo = kwargs.get('photo')
        # TODO: store as reference to another Person
        self.relationships = kwargs.get('relationships', {})

        if isinstance(self.relationships, list):
            converted_relationships = {}
            for rel in self.relationships:
                type, name = rel.split(':')
                converted_relationships[type.lower()] = name.strip()

            self.relationships = converted_relationships

    def to_json(self):
        data = {
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'photo': self.photo,
            'relationships': self.relationships
        }

        if self.birthday:
            data['birthday'] = self.birthday.strftime(Person.BDAY_FORMAT)

        return data

    def __str__(self):
        return json.dumps(self.to_json(), indent=2)

# ------------------------------------------------------------------------------
# Todo:
# - command: Needs photo or photo too small
# - command: Stats
# - Combine Directory and PrintDirectory
def main():
    dir = Directory(sys.argv[1])

    # fam = dir.get("Caroon", "5520 Middleton Rd")
    # fam = dir.get("Adams", "403 Shetland Rd")
    # print fam.id, fam.name
    # d = dir.to_json()
    # print json.dumps(d)

    # print json.dumps(fam.to_json())

    # print dir
    # dir.stats()
    dir.save()

################################################################################
if __name__ == '__main__':
    main()
