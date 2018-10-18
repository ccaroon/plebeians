import json
import md5

from lib.person import Person
# ------------------------------------------------------------------------------
class Family:
    """ A Family is a family name, location and collection of Persons """

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.address = kwargs.get('address')
        self.city = kwargs.get('city')
        self.state = kwargs.get('state')
        self.zip = kwargs.get('zip')
        self.notes = kwargs.get('notes', [])

        self.__members = []
        for person_data in kwargs.get('members', []):
            name = person_data.get('name', None)
            if name:
                person = Person(
                    name = person_data.get('name'),
                    email = person_data.get('email', 'N/A'),
                    birthday = person_data.get('birthday'),
                    phone = person_data.get('phone', {}),
                    photo = person_data.get('photo'),
                    relationships = person_data.get('relationships', {})
                )
                self.__members.append(person)

    def members(self):
        """ Return a list of family members """
        return self.__members

    def get(self, name):
        """ Get a family member (Person) by name """

        member = None
        for person in self.members():
            if person.name == name:
                member = person
                break

        return member

    def add(self, person):
        self.__members.append(person)
        self.__sort_members()

    def delete(self, person):
        self.__members.remove(person)
        self.__sort_members()

    def to_json(self):
        data = {
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip': self.zip,
            'notes': self.notes,
            'members': []
        }

        self.__sort_members()
        for person in self.__members:
            data['members'].append(person.to_json())

        return data

    def __sort_members(self):
        self.__members.sort(key=lambda m: m.name)

    def __str__(self):
        return json.dumps(self.to_json(), indent=2)
