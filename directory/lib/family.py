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

    def add(self, person):
        self.__members[person.name] = person

    def delete(self, person):
        self.__members.pop(person.name)

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
