################################################################################
# http://www.devshed.com/c/a/Python/Python-for-PDF-Generation/
################################################################################
from datetime import datetime
import itertools
import json
import os.path as path
import sys

from lib.directory import Directory

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.lib.colors import black, white, lightgrey

class PrintDirectory:
    FONT = "Times-Roman"
    FONT_BOLD = "Times-Bold"

    SIDE_LEFT  = 0
    SIDE_RIGHT = 1
    MAX_MEMBERS_PER_SIDE = 3

    def __init__(self, data_path, file_name):
        self.__data_path = data_path

        # Create and Prep page
        self.__pdf = Canvas("%s/%s.pdf" % (data_path, file_name), pagesize=landscape(letter), pageCompression=0)

        # Read Directory Data
        self.__directory = Directory("%s/directory.json" % (data_path))

    def render(self, **kwargs):
        if kwargs.get("bdays_only", False):
            self.render_bdays()
        else:
            self.render_title()
            self.render_bdays()
            self.render_families()

        # Save PDF
        self.__pdf.save()

    def render_title(self):
        x = 4.0*inch
        y = 8.0*inch

        # Border
        self.__pdf.setStrokeColorRGB(0,0,0)
        self.__pdf.setFillColor(lightgrey)
        self.__pdf.roundRect(3.0*inch, 7.4 *inch, 5*inch, 1*inch, 10, fill=1)

        # Top Title
        self.__pdf.setFillColorRGB(0,0,0)
        self.__pdf.setFont(PrintDirectory.FONT, 32)
        self.__pdf.drawString(x, y, "Massey's Chapel")
        self.__pdf.drawString(x-(.75*inch), y-(.50*inch), "United Methodist Church")

        # Church Photo
        photo = "%s/photos/title_photo.jpg" % (self.__data_path)
        self.__pdf.drawImage(photo, 1.0*inch, 1.25*inch, width=650, height=434)

        # Bottom - Sub-title
        x = 4.25*inch
        y = .75*inch
        self.__pdf.setFont(PrintDirectory.FONT, 24)
        self.__pdf.drawString(x, y, "Member Directory")
        self.__pdf.drawString(x+(.15*inch), y-(.35*inch), datetime.strftime(datetime.now(), "%B %Y"))

        self.__pdf.showPage()

    def render_bdays(self):
        # Month placement adjustment
        placement = [0, 0, 0, 0, 0, 0, 0, 0, 0, .15*inch, 0, 0]
        bdays = [{},{},{},{},{},{},{},{},{},{},{},{},{}]

        for family in self.__directory.families():
            for person in family.members():
                if person.birthday:
                    month = person.birthday.month
                    day = person.birthday.day
                    name = person.name

                    bucket = bdays[month].get(day, [])
                    if not bucket:
                        bdays[month][day] = bucket
                    bucket.append(name)

        self.__pdf.setFillColorRGB(0,0,0)
        self.__pdf.setFont(PrintDirectory.FONT, 24)
        self.__pdf.drawString(4.85*inch, 8.2*inch, "Birthdays")

        # Vertical Line Down Center
        self.__pdf.setStrokeColorRGB(0,0,0)
        self.__pdf.line(5.5*inch, 0.10*inch, 5.5*inch, 8.0*inch)

        origin_x = 0.5*inch
        origin_y = 7.75*inch
        width = 2.25*inch
        height = 2.5*inch
        row = 1

        for num, month in enumerate(bdays):
            if not month:
                continue

            if num % 2 != 0:
                # ODD
                offset = row - 1
                pos_x = origin_x
                pos_y = (origin_y - (offset*height)) + placement[num-1]
                # print "ODD - %d] x:%d y:%d" % (num, pos_x,pos_y)
            else:
                # EVEN
                offset = row - 1
                row += 1
                if row > 3:
                    row = 1
                pos_x = origin_x + width
                pos_y = (origin_y - (offset*height)) + placement[num-1]
                # print "EVEN - %d] x:%d y:%d" % (num, pos_x,pos_y)

            if num > 6:
                pos_x += 5.5*inch

            self.__pdf.setFont(PrintDirectory.FONT_BOLD, 9)
            header = self.__pdf.beginText(pos_x, pos_y)
            header.textLine("~~~ %s ~~~" % (datetime(1900,num,1).strftime("%B").upper()))
            self.__pdf.drawText(header)

            self.__pdf.setFont(PrintDirectory.FONT, 9)
            info = self.__pdf.beginText(pos_x, pos_y - 0.15*inch)
            for day in sorted(month.keys()):
                names = month.get(day)
                for n in names:
                    info.textLine("%02d) %s" % (day,n))

            self.__pdf.drawText(info)

        self.__pdf.showPage()

    def render_families(self):
        side_it = itertools.cycle((PrintDirectory.SIDE_LEFT, PrintDirectory.SIDE_RIGHT))

        families = self.__directory.families()
        family_index = 0
        family_count = len(families)
        while family_index < family_count:
            # Vertical Line Down Center
            self.__pdf.setStrokeColorRGB(0,0,0)
            self.__pdf.line(5.5*inch,0.10*inch, 5.5*inch, 8.4*inch)

            # Render the Family
            family1 = families[family_index]
            family_index += 1
            family1_args = {}
            family1_side = next(side_it)

            family2_args = {}
            family2_side = next(side_it)
            if len(family1.members()) > PrintDirectory.MAX_MEMBERS_PER_SIDE:
                family1_args = {
                    'm_start': 0,
                    'm_end': PrintDirectory.MAX_MEMBERS_PER_SIDE
                }
                family2 = family1
                family2_args = {
                    'm_start': PrintDirectory.MAX_MEMBERS_PER_SIDE + 1,
                    'm_end': PrintDirectory.MAX_MEMBERS_PER_SIDE * 2,
                    'family_cont': True
                }
            else:
                if family_index < family_count:
                    family2 = families[family_index]
                    # Don't start rendering a 2 page side family on the LEFT
                    if len(family2.members()) > PrintDirectory.MAX_MEMBERS_PER_SIDE:
                        family2 = None
                    else:
                        family_index += 1
                else:
                    family2 = None

            self.render_family(family1, family1_side, **family1_args)
            if family2:
                self.render_family(family2, family2_side, **family2_args)

            # End the Page
            self.__pdf.showPage()

    def render_family(self, family, side, **kwargs):
        left_margin  = 0
        right_margin = 0
        if side == PrintDirectory.SIDE_LEFT:
            left_margin  = .25*inch
            right_margin = 5.5*inch
        elif side == PrintDirectory.SIDE_RIGHT:
            left_margin  = 5.5*inch + .25*inch
            right_margin = 11*inch
        else:
            raise ValueError("Invalid value [%s] for 'side' parameter." % (side))

        # Family Name
        self.__pdf.setFont(PrintDirectory.FONT, 18)
        draw_pos = {'x': left_margin, 'y': 8.125*inch}
        self.__pdf.drawString(draw_pos['x'], draw_pos['y'], family.name)

        # Family Address
        if not kwargs.get('family_cont', False):
            self.__pdf.setFont(PrintDirectory.FONT, 16)
            draw_pos['y'] -= .20*inch
            addr = self.__pdf.beginText(draw_pos['x'], draw_pos['y'])
            addr.setLeading(15)
            addr.textLine(family.address)
            addr.textLine("%s, %s %s" % (family.city, family.state, family.zip))
            self.__pdf.drawText(addr)

        # Family Name/Address Divider
        self.__pdf.setStrokeColorRGB(.5, .5, .5)
        self.__pdf.line(left_margin, 7.5*inch, right_margin-(0.25*inch), 7.5*inch)

        # Member Photo, Info
        photo_dir = "%s/photos" % (self.__data_path)
        pos_x = left_margin
        pos_y = 5.35*inch

        all_members = family.members()
        m_start = kwargs.get('m_start', 0)
        m_end   = kwargs.get('m_end', len(all_members))

        members = all_members[m_start:m_end+1]
        for person in members:
            self.render_person(person, pos_x, pos_y, photo_dir)
            pos_x += 2.80*inch
            if pos_x >= right_margin:
                pos_x = left_margin
                pos_y = 1.90*inch

    def render_person(self, person, pos_x, pos_y, photo_dir):
            # Photo
            photo_name = person.photo if person.photo else 'unknown.jpeg'
            photo = "%s/%s" % (photo_dir, photo_name)
            self.__pdf.drawImage(photo, pos_x, pos_y, width=150,height=150)

            # Info
            info = self.__pdf.beginText(pos_x, pos_y - .25*inch)

            # Name
            info.setFont(PrintDirectory.FONT, 16)
            info.textLine(person.name)

            info.setFont(PrintDirectory.FONT, 12)

            # Bday
            date_str = "N/A"
            if person.birthday:
                date_str = datetime.strftime(person.birthday, "%b %d")
            info.textLine("Birthday: %s" % date_str)

            # Email
            email_addr = person.email if person.email else "N/A"
            info.textLine("Email: %s" % email_addr)

            # Phones
            if person.phone:
                for type, number in person.phone.items():
                    info.textLine("%s: %s" % (type.capitalize(), number))

            # Relationships
            if person.relationships:
                if len(person.relationships) > 2:
                    spouse = None
                    children = []
                    for rel in person.relationships:
                        if rel['type'] == 'Spouse':
                            spouse = rel['name']
                        elif rel['type'] == 'Child':
                            children.append(rel['name'])

                    text_lines = []
                    if spouse:
                        text_lines.append("Spouse: %s" % (spouse))
                    if children:
                        batch1 = children[:2]
                        batch2 = children[2:]

                        text_lines.append("Children: %s" % (", ".join(batch1)))
                        if batch2:
                            text_lines.append("                %s" % (", ".join(batch2)))

                    if text_lines:
                        info.textLine("_________________________")
                        for line in text_lines:
                            info.textLine(line)
                else:
                    info.textLine("_________________________")
                    for rel in person.relationships:
                        info.textLine("%s: %s" % (rel['type'], rel['name']))

            self.__pdf.drawText(info)





















#
