#!/usr/bin/env python
import base64
import datetime
import json
import os.path
import pprint
import re
import sys

DIRECTORY = {}

TAG_BEGIN = "^BEGIN:VCARD"
TAG_END   = "^END:VCARD"
################################################################################
def is_begin(line):
    return (True if re.search(TAG_BEGIN, line) else False)

def is_end(line):
    return (True if re.search(TAG_END, line) else False)

def process_name(record, data, fh):
    values = ("%s %s" % (data['first_name'], data['last_name']), data['last_name'])
    return values

def process_address(record, data, fh):
    return (data['address'], data['city'], data['state'], data['zip'])

def process_email(record, data, fh):
    return data['email_addr']

def process_phone(record, data, fh):
    return data['phone']

def process_bday(record, data, fh):
    bday = data['bday'].split('-')
    dt = datetime.date(1900, int(bday[1]), int(bday[2]))
    return (datetime.date.strftime(dt, "%Y-%m-%d"))

def process_note(record, data, fh):
    return (data['notes'])

def process_photo(record, data, fh):
    type = data['type'].lower()
    filename = record['member']['name'].lower()
    filename = re.sub('\W','-', filename) + "." + type
    b64_data = data['data_start']

    while True:
        line = f.readline().rstrip("\n\r")
        if not re.search("^\s+", line):
            break;
        else:
            b64_data += line

    img_data = base64.b64decode(b64_data)
    with open(filename, "w+b") as img:
        img.write(img_data)

    return (filename)

#################### Example Household #########################################
# {
#     "name": "Anderson",
#     "address1": "375 Mcintosh Road Apt. 821",
#     "address2": "",
#     "city": "New Derrickmouth",
#     "state": "SD",
#     "zip": "08562",
#     "members": [
#         {
#             "name": "James Anderson",
#             "position": "Husband/Father",
#             "phone": "(718) 916-9309",
#             "email": "James-Anderson@yahoo.com"
#             "birthday": "2003-06-19",
#         }
#     ]
# }
################################################################################
def process_household(record):

    # pprint.pprint(record)
    if not record['household'].get('name') and not record['household'].get('address'):
        raise Exception("No Household Found.")

    household_key = "%s%s" % (record['household']['name'], re.sub('\W+', '', record['household']['address']))

    household = DIRECTORY.get(household_key, None)

    if household:
        household['members'].append(record['member'])
        household['notes'].append(record['household']['notes'])
    else:
        household = {
            'name': record['household']['name'],
            'address1': record['household']['address'],
            'address2': "",
            'city': record['household']['city'],
            'state': record['household']['state'],
            'zip': record['household']['zip'],
            'notes': [record['household']['notes']],
            'members': [record['member']]
        }

        DIRECTORY[household_key] = household
################################################################################
TAG_MAP = [
    {
        'fields': ('member.name', 'household.name'),
        # N:LAST;FIRST;;;
        'token': "^N:(?P<last_name>.*?);(?P<first_name>.*?);(?P<misc>.*)$",
        'handler': process_name
    },
    {
        'fields': 'member.email',
        # EMAIL;type=INTERNET;type=HOME;type=pref:foobar@example.com
        'token': "^EMAIL;.*:(?P<email_addr>.*)$",
        'handler': process_email
    },
    {
        'fields': 'member.phone',
        # TEL;type=CELL;type=VOICE;type=pref:919-641-6341
        'token': "^TEL;.*:(?P<phone>.*)$",
        'handler': process_phone
    },
    {
        'fields': ('household.address', 'household.city', 'household.state', 'household.zip'),
        # ADR;type=HOME;type=pref:;;403 Shetland Rd;Rougemont;NC;27572;
        'token': "ADR;.*:;;(?P<address>.*?);(?P<city>.*?);(?P<state>.*?);(?P<zip>.*);",
        'handler': process_address
    },
    {
        'fields': 'member.birthday',
        # BDAY:1800-12-17
        'token': "^BDAY:(?P<bday>.*)",
        'handler': process_bday
    },
    {
        'fields': 'member.photo',
        # PHOTO;ENCODING=b;TYPE=JPEG:/9j/4AAQSkZJRgABAQEASABIAAD/4QBARXhpZgAATU0AKgAA
        'token': "^PHOTO;.*;TYPE=(?P<type>.*):(?P<data_start>.*)$",
        'handler': process_photo
    },
    {
        'fields': 'household.notes',
        # NOTE:Birthday: \nKen's birthday 10/6\nRiley's birthday 1/23\nJamie's birthday 9/14\n
        'token': "^NOTE:(?P<notes>.*)",
        'handler': process_note
    },
]
################################################################################
def set_fields(record, fields, value):
    if isinstance(fields, tuple):
        index = 0
        for f in fields:
            set_field(record, f, value[index])
            index+=1
    else:
        set_field(record, fields, value)

def set_field(record, field, value):
    nodes = field.split('.')
    leaf = nodes.pop()

    for name in nodes:
        if not record.has_key(name):
            record[name] = {}

        record = record[name]

    if record.has_key(leaf):
        record[leaf] += value
    else:
        record[leaf] = value
################################################################################
# filename = "MCUMC_Directory.vcf"
# filename = "example.vcf"

if len(sys.argv) < 2:
    raise Exception("Usage: %s <filename.vcf>" % sys.argv[0])
else:
    filename = sys.argv.pop(1)

with open(filename, "r") as f:

    record = {}
    line = "nothing"
    while (line):
        line = f.readline().rstrip("\n\r")

        if (is_begin(line)):
            record = {}
        elif (is_end(line)):
            try:
                process_household(record)
            except Exception as e:
                pass
        else:
            for tag in TAG_MAP:
                match = re.search(tag['token'], line)
                if match:
                    value = tag['handler'](record, match.groupdict(), f)
                    set_fields(record, tag['fields'], value)


def cmp(a,b):
    if a['name'] > b['name']:
        return 1
    elif a['name'] == b['name']:
        return 0
    else:
        return -1

entries = DIRECTORY.values()
entries.sort(cmp=cmp)
print json.dumps(entries)








#
