from datetime import datetime
import json
import os
import os.path

from lib.family import Family

# ------------------------------------------------------------------------------
class Directory:
    """ A Directory is a collection of Families """

    def __init__(self, data_file):
        self.__data_file = data_file
        with open(data_file, 'r') as fh:
            self.__data = json.load(fh)

        self.__families = []
        for fam_data in self.__data:
            family = Family(
                name = fam_data['name'],
                address = fam_data['address'],
                city = fam_data['city'],
                state = fam_data['state'],
                zip = fam_data['zip'],
                members = fam_data['members'],
                notes = fam_data.get('notes', [])
            )
            self.__families.append(family)

    def families(self):
        return self.__families

    def get(self, name):
        family = None

        found = []
        for fam in self.families():
            if fam.name == name:
                found.append(fam)

        if len(found) == 0:
            family = None
        elif len(found) == 1:
            family = found[0]
        else:
            family = found

        return family

    def to_json(self):
        self.__sort_families()

        data = []
        for family in self.families():
            data.append(family.to_json())

        return data

    def stats(self):
        families = self.families()
        fam_count = len(families)
        total_peeps = 0
        for fam in families:
            members = fam.members()
            mem_count = len(members)
            total_peeps += mem_count
            print("%s -> %d" % (fam.name, mem_count))

        print("---------------------------------")
        print("Families: %d | Total Members: %d" % (fam_count, total_peeps))

    def save(self, use_version=True):
        output_file = self.__data_file

        if use_version:
            (path, ext) = os.path.splitext(self.__data_file)
            id = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            output_file = "%s-%s%s" % (path, id, ext)

        with open(output_file, 'w') as fh:
            json.dump(self.to_json(), fh, indent=2, separators=(',', ': '))

    def add(self, family):
        self.__families.append(family)
        self.__sort_families()

    # NOTE: Currently moves the file instead of deleting it
    def delete_photo(self, person):
        if person.photo:
            data_dir = os.path.dirname(self.__data_file)

            src_file = "%s/photos/%s" % (data_dir, person.photo)
            dest_file = "%s/backup/%s" % (data_dir, person.photo)
            os.rename(src_file, dest_file)

    def delete(self, family):
        for person in family.members():
            self.delete_photo(person)

        self.__families.remove(family)
        self.__sort_families()

    def __sort_families(self):
        self.__families.sort(key=lambda f: f.name)

    def __str__(self):
        return self.__data_file

    def __repr__(self):
        return json.dumps(self.to_json(), indent=2)
