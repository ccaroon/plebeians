import re

class Prompt:
    """ Collection of Class Methods to prompt for various kinds in input """

    @classmethod
    def input(cls, msg):
        value = input(msg)
        return (value)

    # --------------------------------------------------------------------------
    @classmethod
    def notes(cls):
        new_data = []
        add_more = True
        while add_more:
            print("----- Add Note -----")
            title = Prompt.input("Note Title: ")
            text  = Prompt.input("Note Text: ")

            if title and text:
                new_data.append({
                    'title': title,
                    'text': text
                })

            add_more = Prompt.more(msg="Add More Notes")

        return (new_data)
    # --------------------------------------------------------------------------
    @classmethod
    def phone(cls):
        new_data = {}
        add_more = True
        while add_more:
            print("----- Add Phone -----")
            phone_type = Prompt.input("Phone Type: ")
            phone_num = Prompt.input("Phone Number: ")

            if phone_type and phone_num:
                # Format Number
                number = re.sub("\D", "", phone_num)
                match = re.search("(?P<exchange>\d\d\d)(?P<prefix>\d\d\d)(?P<last_four>\d\d\d\d)", number)
                parts = match.groupdict()
                number = "(%s) %s-%s" % (parts['exchange'], parts['prefix'], parts['last_four'])

                # Add to new data
                new_data[phone_type.upper()] = number

            add_more = Prompt.more(msg="Add More Phones")

        return new_data
    # --------------------------------------------------------------------------
    @classmethod
    def relationships(cls):
        new_data = []
        add_more = True
        while add_more:
            print("----- Add Relationship -----")
            rel_type = Prompt.input("Relation Type: ")
            rel_name = Prompt.input("Relation Name: ")

            if rel_type and rel_name:
                new_data.append({
                    'type': rel_type.capitalize(),
                    'name': rel_name
                })

            add_more = Prompt.more(msg="Add More Relations")

        return new_data
    # --------------------------------------------------------------------------
    @classmethod
    def more(cls, **kwargs):
        accepted_choice = kwargs.get('accept', 'y')
        choice = Prompt.input("%s? (%s|n)" % (kwargs.get("msg", "Continue"), accepted_choice))
        return True if choice == accepted_choice else False

    # --------------------------------------------------------------------------
    @classmethod
    def choose_from_list(cls, object_list, msg):
        value = None

        if isinstance(object_list, (list, tuple)):
            num = 1
            for obj in object_list:
                print("%d) %s" % (num, obj))
                num += 1

            choice = Prompt.input(msg)
            choice = int(choice) if choice else 0

            if choice in range(1, len(object_list)+1):
                value = object_list[choice-1]
        else:
            value = object_list

        return value
    # --------------------------------------------------------------------------
