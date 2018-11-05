import datetime
import os.path
import re

# -----------------------------------------------------------------------------
class VCFParser:

    TAG_BEGIN = "^BEGIN:VCARD"
    TAG_END   = "^END:VCARD"

    # -----------------------------------------------------------------------------
    TAG_MAP = [
        {
            'fields': ('name', 'first_name', 'last_name', 'misc'),
            # N:LAST;FIRST;;;
            'token': "^N:(?P<last_name>.*?);(?P<first_name>.*?);(?P<suffix>.*?);(?P<misc>.*)$",
            'handler': 'process_name'
        },
        {
            'fields': 'email',
            # EMAIL;type=INTERNET;type=HOME;type=pref:foobar@example.com
            'token': "^EMAIL;.*:(?P<email_addr>.*)$",
            'handler': 'process_email'
        },
        {
            'fields': 'phone',
            # TEL;type=CELL;type=VOICE;type=pref:919-641-6341
            'token': "^TEL;type=(?P<type>.*?);.*:(?P<number>.*)$",
            'handler': 'process_phone'
        },
        {
            'fields': ('address', 'city', 'state', 'zip'),
            # ADR;type=HOME;type=pref:;;4003 Sheetland Rd;Redgemont;NC;27572;
            'token': "item\d\.ADR;type=HOME:;;(?P<address>.*?);(?P<city>.*?);(?P<state>.*?);(?P<zip>.*);",
            'handler': 'process_address'
        },
        {
            'fields': ('address', 'city', 'state', 'zip'),
            # ADR;type=HOME;type=pref:;;4003 Sheetland Rd;Redgemont;NC;27572;
            'token': "ADR;type=HOME;.*:;;(?P<address>.*?);(?P<city>.*?);(?P<state>.*?);(?P<zip>.*);",
            'handler': 'process_address'
        },
        {
            'fields': 'birthday',
            # BDAY:1800-12-17
            'token': "^BDAY.*:(?P<bday>.*)",
            'handler': 'process_bday'
        },
        {
            'fields': 'relationships',
            # item2.X-ABRELATEDNAMES;type=pref:Ken
            'token': "X-ABRELATEDNAMES;?(.*):(?P<name>.*)",
            'handler': 'process_relationships'
        }
    ]
    # -----------------------------------------------------------------------------

    def __init__(self, **kwargs):
        self.__record = {}
        self.__photo_dir = kwargs.get('photo_dir')

    def is_begin(self, line):
        return (True if re.search(VCFParser.TAG_BEGIN, line) else False)

    def is_end(self, line):
        return (True if re.search(VCFParser.TAG_END, line) else False)

    def process_name(self, data):
        full_name = "%s %s" % (data['first_name'], data['last_name'])

        if data['suffix']:
            full_name += ", %s" % (data['suffix'])

        values = (full_name, data['first_name'], data['last_name'], data['misc'])
        return values

    def process_address(self, data):
        address = re.sub("\\\\,", ",", data['address'])
        address = re.sub("\\\\n", "", data['address'])
        return (address, data['city'], data['state'], data['zip'])

    def process_email(self, data):
        return data['email_addr']

    def process_phone(self, data):
        type = data['type']
        number = re.sub("\D", "", data['number'])

        match = re.search("(?P<exchange>\d\d\d)(?P<prefix>\d\d\d)(?P<last_four>\d\d\d\d)", number)
        parts = match.groupdict()
        number = "(%s) %s-%s" % (parts['exchange'], parts['prefix'], parts['last_four'])

        phone = self.__record.get('phone', {})
        phone[type] = number

        return phone

    def process_bday(self, data):
        bday = data['bday'].split('-')
        dt = datetime.date(1900, int(bday[1]), int(bday[2]))
        return (datetime.date.strftime(dt, "%Y-%m-%d"))

    def process_note(self, data):
        return (re.sub("\\\\,", ",", data['notes']))

    def process_relationships(self, data):
        rel_name = data['name']

        line = self.__fh.readline().rstrip("\n\r")

        # item2.X-ABLabel:_$!<Spouse>!$_
        match = re.search("<(?P<rel_type>.*)>", line)
        if not match:
            # item3.X-ABLabel:mother-in-law
            match = re.search("X-ABLabel:(?P<rel_type>.*)", line)

        d2 = match.groupdict()
        rel_type = d2['rel_type'].title()
        rels = self.__record.get('relationships', [])

        # entry = "%s: %s" % (rel_type, rel_name)
        entry = {'type': rel_type, 'name': rel_name}
        if not entry in rels:
            rels.append(entry)

        return(rels)

    def verify_photo(self):
        photo_name = self.__record['name'].lower()
        photo_name = re.sub('\W','-', photo_name) + ".jpeg"

        self.__record['photo'] = None

        photo_path = "%s/%s" % (self.__photo_dir, photo_name)
        if os.path.isfile(photo_path):
            self.__record['photo'] = photo_name

    def __set_fields(self, fields, value):
        if isinstance(fields, tuple):
            index = 0
            for f in fields:
                self.__set_field(f, value[index])
                index+=1
        else:
            self.__set_field(fields, value)

    def __set_field(self, field, value):
        nodes = field.split('.')
        leaf = nodes.pop()

        for name in nodes:
            if not self.__record.has_key(name):
                self.__record[name] = {}

            self.__record = self.__record[name]

        self.__record[leaf] = value

    def parse(self, filename):
        self.__record = {}

        found_start = False
        with open(filename, "r") as f:
            self.__fh = f
            line = "nothing"
            while (line):
                line = f.readline().rstrip("\n\r")

                if (self.is_begin(line)):
                    found_start = True
                elif (self.is_end(line)):
                    self.verify_photo()
                    break
                else:
                    for tag in VCFParser.TAG_MAP:
                        match = re.search(tag['token'], line)
                        if match:
                            handler = getattr(self, tag['handler'])
                            value = handler(match.groupdict())
                            self.__set_fields(tag['fields'], value)

        return self.__record









# 
