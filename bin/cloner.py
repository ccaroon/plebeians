#!/usr/bin/env python
import json
from faker import Faker
import random
import string

fake = Faker()

HOUSEHOLD_COUNT = 75

households = []
for i in range(0, HOUSEHOLD_COUNT):
    household = {
        'name': fake.last_name(),
        'address1': fake.street_address(),
        'address2': "",
        'city': fake.city(),
        'state': fake.state_abbr(),
        'zip': fake.zipcode(),
        'members': []
    }


    member_count = random.randint(1,5)
    for num in range(0, member_count):
        name = ""
        position = ""
        # One Person - Random Gender
        if (member_count == 1):
            name = fake.first_name() + " " + household['name']
        # Two People - 1 Man, 1 Woman
        elif (member_count == 2):
            if (num == 0):
                name = fake.first_name_male() + " " + household['name']
                position = "Husband"
            elif (num == 1):
                name = fake.first_name_female() + " " + household['name']
                position = "Wife"
        # Three+ People - 1 Man, 1 Woman, Rest Children
        elif (member_count >= 3):
            if (num == 0):
                name = fake.first_name_male() + " " + household['name']
                position = "Husband/Father"
            elif (num == 1):
                name = fake.first_name_female() + " " + household['name']
                position = "Wife/Mother"
            else:
                name = fake.first_name() + " " + household['name']
                position = "Child"

        person = {
            'name': name,
            'phone': fake.numerify(text="(###) ###-####"),
            'email': string.replace(name, ' ', '-') + "@" + fake.free_email_domain(),
            'birthday': fake.date(pattern="%Y-%m-%d"),
            'position': position
        }
        household['members'].append(person)

    households.append(household)

def cmp(a,b):
    if a['name'] > b['name']:
        return 1
    elif a['name'] == b['name']:
        return 0
    else:
        return -1

households.sort(cmp=cmp)

print json.dumps(households)
