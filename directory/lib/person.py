from datetime import datetime
import json

# ------------------------------------------------------------------------------
class Person(object):
    """ A Person is a collection of information about an individual """

    BDAY_FORMAT = "%Y-%m-%d"

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email', 'N/A')

        self.birthday = kwargs.get('birthday', None)

        self.phone = kwargs.get('phone', {})
        self.photo = kwargs.get('photo')
        # TODO: store as reference to another Person??
        self.relationships = kwargs.get('relationships', [])

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, bday):
        if isinstance(bday, (str, unicode)):
            self.__birthday = datetime.strptime(bday, Person.BDAY_FORMAT)
        elif isinstance(bday, datetime):
            self.__birthday = bday
        elif bday == None:
            self.__birthday = None
        else:
            raise ValueError("'birthday **must** be a string (YYYY-MM-DD) or a datetime'")

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
        return self.name

    def __repr__(self):
        return json.dumps(self.to_json(), indent=2)
