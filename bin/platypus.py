#!/usr/bin/env python
# http://www.devshed.com/c/a/Python/Python-for-PDF-Generation/
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm, mm, inch, pica

style = getSampleStyleSheet()

pdf = SimpleDocTemplate("platypus-test.pdf", pagesize=letter)

story = []

# text = """
# This is the way the world ends.
# This is the way the world ends.
# This is the way the world ends.
# Not with a BANG!, but a whimper.
# """
# for x in xrange(25):
#     para = Paragraph(text, style["Normal"])
#     story.append(para)
#     story.append(Spacer(inch * .5, inch * .5))


for color in ["red","green","blue"]:
    para = Paragraph("<font color='%s'>This is <b>%s</b>.</font>" % (color, color), style["Normal"])
    story.append(para)
    story.append(Spacer(inch * .5, inch * .5))


pdf.build(story)
