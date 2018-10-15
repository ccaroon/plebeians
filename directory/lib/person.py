from datetime import datetime
import json

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
        # TODO: store as reference to another Person??
        self.relationships = kwargs.get('relationships', [])

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
