#!/usr/bin/env python
# http://www.devshed.com/c/a/Python/Python-for-PDF-Generation/
# ------------------------------------------------------------------------------
################################################################################
from datetime import datetime
import json
import os.path as path
import sys

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import cm, mm, inch, pica

class Directory:
    FONT = "Times-Roman"

    def __init__(self, data_path):
        self.__data_path = data_path

        # Create and Prep page
        output_name = path.basename(data_path)
        self.__pdf = Canvas("%s.pdf" % (output_name), pagesize=landscape(letter))

        # Read Directory Data
        self.__member_data = None
        member_data_file = "%s/directory.json" % (data_path)
        with open(member_data_file, "r") as fh:
            self.__member_data = json.load(fh)

    def render(self):
        # Render a TEST family
        self.render_family(self.__member_data[54])

        # Save PDF
        self.__pdf.save()

    def render_family(self, family):
        # Vertical Line Down Center
        self.__pdf.setStrokeColorRGB(0,0,0)
        self.__pdf.line(5.5*inch,0*inch, 5.5*inch, 8.5*inch)

        # Family Name - Left
        self.__pdf.setFont(Directory.FONT, 18)
        draw_pos = {'x': .25*inch, 'y': 8.125*inch}
        self.__pdf.drawString(draw_pos['x'], draw_pos['y'], family['name'])

        # Family Address - Left
        self.__pdf.setFont(Directory.FONT, 16)
        draw_pos['y'] -= .20*inch
        addr = self.__pdf.beginText(draw_pos['x'], draw_pos['y'])
        addr.setLeading(12)
        addr.textLine(family['address1'])
        addr.textLine("%s, %s %s" % (family['city'], family['state'], family['zip']))
        self.__pdf.drawText(addr)

        # Family Name/Address Divider - Left
        self.__pdf.setStrokeColorRGB(.5, .5, .5)
        self.__pdf.line(0.25*inch, 7.5*inch, 5.25*inch, 7.5*inch)

        # Member Photo, Info
        photo_dir = "%s/photos" % (self.__data_path)
        pos_x = 0.25*inch
        pos_y = 5.25*inch
        for person in family['members']:
            print "%s - %s" % (person['name'], pos_x)
            # Photo
            photo = "%s/%s" % (photo_dir, person.get('photo', 'unknown.jpeg'))
            self.__pdf.drawImage(photo, pos_x, pos_y, width=150,height=150)

            # Info
            info = self.__pdf.beginText(pos_x, pos_y - .25*inch)

            # Name
            info.setFont(Directory.FONT, 16)
            info.textLine(person['name'])

            info.setFont(Directory.FONT, 12)

            # Bday
            date = "N/A"
            date_str = person.get('birthday', None)
            if date_str:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                date = datetime.strftime(date, "%b %d")
            info.textLine("Birthday: %s" % date)

            # Email
            info.textLine("Email: %s" % person.get('email', "N/A"))

            # Phones
            if person.has_key('phone'):
                for type, number in person['phone'].iteritems():
                    # info.textLine("Phone: %s (%s)" % (number, type))
                    info.textLine("%s: %s" % (type.capitalize(), number))

            # Relationships
            # TODO: Make smaller
            # info.textLine("_________________________")
            # for rel in person['relationships']:
            #     info.textLine(rel)

            self.__pdf.drawText(info)

            pos_x += 2.70*inch
            if pos_x >= 5.5*inch:
                pos_x = 0.25*inch
                pos_y = 1.90*inch

        self.__pdf.showPage()

# ------------------------------------------------------------------------------
def main():
    data_path = None
    if len(sys.argv) < 2:
        print "Usage: %s <data_dir>" % (sys.argv[0])
        sys.exit(1)
    else:
        data_path = sys.argv[1]
        if not path.exists(data_path):
            raise Exception("Path '%s' does not exist." % (data_path))

    directory = Directory(data_path)
    directory.render()

if __name__ == '__main__':
    main()
