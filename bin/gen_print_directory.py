#!/usr/bin/env python
# http://www.devshed.com/c/a/Python/Python-for-PDF-Generation/
# ------------------------------------------------------------------------------
################################################################################
from datetime import datetime
import itertools
import json
import os.path as path
import sys

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import cm, mm, inch, pica

class Directory:
    FONT = "Times-Roman"

    SIDE_LEFT  = 0
    SIDE_RIGHT = 1

    def __init__(self, data_path):
        self.__data_path = data_path

        # Create and Prep page
        output_name = path.basename(data_path)
        self.__pdf = Canvas("%s.pdf" % (output_name), pagesize=landscape(letter), pageCompression=0)

        # Read Directory Data
        self.__member_data = None
        member_data_file = "%s/directory.json" % (data_path)
        with open(member_data_file, "r") as fh:
            self.__member_data = json.load(fh)

    def render(self):
        side_it = itertools.cycle((Directory.SIDE_LEFT, Directory.SIDE_RIGHT))

        fi = 0
        num_members = len(self.__member_data)
        while fi < num_members:
            # Vertical Line Down Center
            self.__pdf.setStrokeColorRGB(0,0,0)
            self.__pdf.line(5.5*inch,0*inch, 5.5*inch, 8.5*inch)

            # Render the Family
            family1 = self.__member_data[fi]
            fi += 1
            family1_args = {}
            family2_args = {}
            if len(family1['members']) > 3:
                family1_args = {
                    'm_start': 0,
                    'm_end': 3
                }
                family2 = family1
                family2_args = {
                    'm_start': 4,
                    'm_end': 6,
                    'family_cont': True
                }
            else:
                family2 = self.__member_data[fi]
                fi += 1

            self.render_family(family1, side_it.next(), **family1_args)
            self.render_family(family2, side_it.next(), **family2_args)

            # End the Page
            self.__pdf.showPage()

        # Save PDF
        self.__pdf.save()

    def render_family(self, family, side, **kwargs):
        left_margin  = 0
        right_margin = 0
        if side == Directory.SIDE_LEFT:
            left_margin  = .25*inch
            right_margin = 5.5*inch
        elif side == Directory.SIDE_RIGHT:
            left_margin  = 5.5*inch + .25*inch
            right_margin = 11*inch
        else:
            raise ValueError("Invalid value [%s] for 'side' parameter." % (side))

        # Family Name
        self.__pdf.setFont(Directory.FONT, 18)
        draw_pos = {'x': left_margin, 'y': 8.125*inch}
        self.__pdf.drawString(draw_pos['x'], draw_pos['y'], family['name'])

        # Family Address
        if not kwargs.get('family_cont', False):
            self.__pdf.setFont(Directory.FONT, 16)
            draw_pos['y'] -= .20*inch
            addr = self.__pdf.beginText(draw_pos['x'], draw_pos['y'])
            addr.setLeading(15)
            addr.textLine(family['address1'])
            addr.textLine("%s, %s %s" % (family['city'], family['state'], family['zip']))
            self.__pdf.drawText(addr)

        # Family Name/Address Divider
        self.__pdf.setStrokeColorRGB(.5, .5, .5)
        self.__pdf.line(left_margin, 7.5*inch, right_margin-(0.25*inch), 7.5*inch)

        # Member Photo, Info
        photo_dir = "%s/photos" % (self.__data_path)
        pos_x = left_margin
        pos_y = 5.25*inch

        m_start = kwargs.get('m_start', 0)
        m_end   = kwargs.get('m_end', len(family['members']))
        members = family['members'][m_start:m_end+1]

        for person in members:
            self.render_person(person, pos_x, pos_y, photo_dir)
            pos_x += 2.70*inch
            if pos_x >= right_margin:
                pos_x = left_margin
                pos_y = 1.90*inch

    def render_person(self, person, pos_x, pos_y, photo_dir):
            # print "%s - %s" % (person['name'], pos_x)
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
