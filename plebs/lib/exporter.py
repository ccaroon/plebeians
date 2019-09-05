from datetime import datetime
from lib.directory import Directory

class Exporter:

    def __init__(self, data_path):
        # Read Directory Data
        self.__data_path = data_path
        self.__directory = Directory(F"{data_path}/directory.json")

    def export_markdown(self, filename):
        with open(F"{self.__data_path}/{filename}.md", "w") as output:

            output.write("# Massey's Chapel UMC - Member Directory\n\n")

            # Family -> Members -> Person
            for family in self.__directory.families():
                output.write(F"## {family.name}\n")
                output.write(F"""{family.address}
{family.city}, {family.state} {family.zip}
\n""")

                for member in family.members():
                    bday = "N/A" if member.birthday == None else datetime.strftime(member.birthday, "%b %d")
                    email = "N/A" if member.email == None else member.email

                    phone = "N/A"
                    if len(member.phone) > 0:
                        phones = []
                        for type, num in member.phone.items():
                            phones.append(F"{type}: {num}")
                        phone = " | ".join(phones)

                    person = "* %-25s\t%s\t%-25s\t%s\n" % (member.name, bday, email, phone)
                    output.write(person)

                output.write("\n")
