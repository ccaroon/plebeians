#!/usr/bin/env python
# http://www.devshed.com/c/a/Python/Python-for-PDF-Generation/
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm, mm, inch, pica

pdf = Canvas("canvas-test.pdf", pagesize = letter)

# ONE
# pdf.setFont("Courier", 12)
# pdf.setStrokeColorRGB(1, 0, 0)
# pdf.drawString(300, 300, "CLASSIFIED")
# pdf.drawString(2 * inch, inch, "For Your Eyes Only")

# TWO
# pdf.setFont("Courier", 60)
# pdf.setFillColorRGB(1, 0, 0)
# pdf.drawCentredString(letter[0] / 2, inch * 6, "CLASSIFIED")
# pdf.setFont("Courier", 30)
# pdf.drawCentredString(letter[0] / 2, inch * 5, "For Your Eyes")

# THREE
# rhyme = pdf.beginText(inch * 1, inch * 10)
# rhyme.textLine("This is the way the world ends.")
# rhyme.textLine("This is the way the world ends.")
# rhyme.textLine("This is the way the world ends.")
# rhyme.textLine("Not with a bang, but a whimper!")
# pdf.drawText(rhyme)

# FOUR - Images
pdf.line(inch, inch * 10, inch * 7.5, inch * 10)
pdf.drawImage("craig.jpg", inch, inch)

# ----------------------------
pdf.showPage()
pdf.save()
