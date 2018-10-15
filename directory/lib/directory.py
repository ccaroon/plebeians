from datetime import datetime
import json
import os.path

from lib.family import Family

# ------------------------------------------------------------------------------
class Directory:
    """ A Directory is a collection of Families """

    def __init__(self, data_file):
        self.__data_file = data_file
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
            json.dump(self.to_json(), fh, indent=2)

    def __str__(self):
        return json.dumps(self.to_json(), indent=2)
