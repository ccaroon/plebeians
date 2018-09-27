#!/usr/bin/env python
import argparse
import base64
import datetime
import json
import os.path
import pprint
import re
import shutil
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
    full_name = "%s %s" % (data['first_name'], data['last_name'])

    if data['suffix']:
        full_name += ", %s" % (data['suffix'])

    values = (full_name, data['first_name'], data['last_name'])
    return values

def process_address(record, data, fh):
    address = re.sub("\\\\,", ",", data['address'])
    address = re.sub("\\\\n", "", data['address'])
    return (address, data['city'], data['state'], data['zip'])

def process_email(record, data, fh):
    return data['email_addr']

def process_phone(record, data, fh):
    type = data['type']
    number = re.sub("\D", "", data['number'])

    match = re.search("(?P<exchange>\d\d\d)(?P<prefix>\d\d\d)(?P<last_four>\d\d\d\d)", number)
    parts = match.groupdict()
    number = "(%s) %s-%s" % (parts['exchange'], parts['prefix'], parts['last_four'])

    phone = record['member'].get('phone', {})
    phone[type] = number

    return phone

def process_bday(record, data, fh):
    bday = data['bday'].split('-')
    dt = datetime.date(1900, int(bday[1]), int(bday[2]))
    return (datetime.date.strftime(dt, "%Y-%m-%d"))

def process_note(record, data, fh):
    return (re.sub("\\\\,", ",", data['notes']))

def process_relationships(record, data, fh):
    rel_name = data['name']

    line = fh.readline().rstrip("\n\r")

    # item2.X-ABLabel:_$!<Spouse>!$_
    match = re.search("<(?P<rel_type>.*)>", line)
    if not match:
        # item3.X-ABLabel:mother-in-law
        match = re.search("X-ABLabel:(?P<rel_type>.*)", line)

    d2 = match.groupdict()
    rel_type = d2['rel_type'].title()
    rels = record['member'].get('relationships', [])

    entry = "%s: %s" % (rel_type, rel_name)
    if not entry in rels:
        rels.append(entry)

    return(rels)

def process_photo(record, data, fh):
    type = data['type'].lower()
    filename = record['member']['name'].lower()
    filename = re.sub('\W','-', filename) + "." + type
    b64_data = data['data_start']

    while True:
        line = fh.readline().rstrip("\n\r")
        if not re.search("^\s+", line):
            # rewind file to "put" line back
            fh.seek(len(line) * -1, 1)
            break;
        else:
            b64_data += line

    img_data = base64.b64decode(b64_data)
    with open("%s/%s" % (OUTPUT_DIR, filename), "w+b") as img:
        img.write(img_data)

    return (filename)

def process_alt_photo(record):
    photo_path = "%s/%s, %s.jpg" % (PHOTO_DIR, record['household']['name'], record['_hidden']['first_name'])

    if os.path.isfile(photo_path):
        # print "Found Alt Photo: %s" % (photo_path)
        filename = record['member']['name'].lower()
        filename = re.sub('\W','-', filename) + ".jpeg"
        shutil.copy(photo_path, "%s/%s" % (OUTPUT_DIR, filename))

        record['member']['photo'] = filename

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
# TODO: moved phone and relationships aggregation to HERE
def process_household(record):

    # pprint.pprint(record)
    household_name = record['household'].get('name', None)
    household_addr = record['household'].get('address', None)
    if not household_name or not household_addr:
        raise Exception("No Household Found N[%s] A[%s]" % (household_name, household_addr))

    household_key = re.sub('\W+', '', household_addr)
    # household_key = "%s%s" % (household_name, re.sub('\W+', '', household_addr))

    household = DIRECTORY.get(household_key, None)

    if household:
        if record['household']['name'] != household['name']:
            household['name'] += "/%s" % (record['household']['name'])
        household['members'].append(record['member'])
        notes = record['household'].get('notes')
        if notes:
            household['notes'].append(notes)
    else:
        household = {
            'name': household_name,
            'address1': household_addr,
            # 'address2': "",
            'city': record['household']['city'],
            'state': record['household']['state'],
            'zip': record['household']['zip'],
            'notes': [],
            'members': [record['member']]
        }
        notes = record['household'].get('notes')
        if notes:
            household['notes'].append(notes)

        DIRECTORY[household_key] = household
################################################################################
TAG_MAP = [
    {
        'fields': ('member.name', '_hidden.first_name', 'household.name'),
        # N:LAST;FIRST;;;
        'token': "^N:(?P<last_name>.*?);(?P<first_name>.*?);(?P<suffix>.*?);(?P<misc>.*)$",
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
        'token': "^TEL;type=(?P<type>.*?);.*:(?P<number>.*)$",
        'handler': process_phone
    },
    {
        'fields': ('household.address', 'household.city', 'household.state', 'household.zip'),
        # ADR;type=HOME;type=pref:;;4003 Sheetland Rd;Redgemont;NC;27572;
        'token': "ADR;type=HOME;.*:;;(?P<address>.*?);(?P<city>.*?);(?P<state>.*?);(?P<zip>.*);",
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
        'fields': 'member.relationships',
        # item2.X-ABRELATEDNAMES;type=pref:Ken
        'token': "X-ABRELATEDNAMES;?(.*):(?P<name>.*)",
        'handler': process_relationships
    },
    # {
    #     'fields': 'household.notes',
    #     # NOTE:Birthday: \nBob's birthday 10/6\nFred's birthday 1/23\nJamie's birthday 9/14\n
    #     'token': "^NOTE:(?P<notes>.*)",
    #     'handler': process_note
    # },
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

    # if record.has_key(leaf):
    #     record[leaf] += value
    # else:
    #     record[leaf] = value
    record[leaf] = value
################################################################################
parser = argparse.ArgumentParser(
    description="Convert VCF (V-Card) format data for use with Plebeians."
)

parser.add_argument("vcard_file",
    help="VCard Input File"
)
parser.add_argument("output_dir",
    help="Directory to write output files (JSON and Photos)"
)
parser.add_argument("--alt-photo-dir",
    help="Look for an alternate photo in this directory."
)

args = parser.parse_args()

filename   = args.vcard_file
OUTPUT_DIR = args.output_dir
PHOTO_DIR  = args.alt_photo_dir

# if not filename or not output_dir:
    # raise Exception("Usage: %s <filename.vcf> <alt_photo_dir>" % sys.argv[0])
################################################################################
with open(filename, "r") as f:
    record = {}
    line = "nothing"
    while (line):
        line = f.readline().rstrip("\n\r")

        if (is_begin(line)):
            record = {}
        elif (is_end(line)):
            try:
                if PHOTO_DIR:
                    process_alt_photo(record)

                process_household(record)
            except Exception as e:
                sys.stderr.write(e.message + "\n")
                continue
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

with open("%s/directory.json" % OUTPUT_DIR, "w") as fp:
    json.dump(entries, fp)
