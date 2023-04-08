# Dependencies
# ReportLab
from reportlab.pdfgen import canvas          # canvas
from reportlab.lib.units import cm           # measurements
from reportlab.lib.pagesizes import A4       # measurements
from reportlab.pdfbase import pdfmetrics     # custom font support
from reportlab.pdfbase.ttfonts import TTFont # custom font support

# Python Modules
import csv                      # data import
import re                       # filename processing
from datetime import date       # filename processing
from unidecode import unidecode # filename processing

def print_progress(i, total):
    progress = i / total * 100
    print(f"Progress: {progress:.1f}%", end="\r")

    return

def generate_strings(name, role, hours):
    return [
        {
            "string": "Certificamos que",
            "style": "italic"
        },
        {
            "string": name,
            "style": "bold"
        },
        {
            "string": "participou na 21ª Feira Brasileira de Ciência e Engenharia da",
            "style": "italic"
        },
        {
            "string": role,
            "style": "bold"
        },
        {
            "string": "dos prêmios",
            "style": "italic"
        },
        {
            "string": "Ciências Moleculares de Mérito Acadêmico e de Interdisciplinaridade",
            "style": "regular"
        },
        {
            "string": f"com carga horária de {hours} horas",
            "style": "italic"
        }
    ]

def generate_certificate(name, certificate_name, today, background_path, certificate_string):
    # canvas initialization
    clean_name = re.sub(r'[^0-9a-zA-Z]+', '', unidecode(name))
    filename = f'certificados/{today}_{certificate_name}_{clean_name}.pdf' # generates certificate filename 
    c = canvas.Canvas(filename, pagesize=[A4[1], A4[0]])         # initializes PDF canvas

    # custom font
    pdfmetrics.registerFont(TTFont('LibreCaslon',        'LibreCaslonText-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('LibreCaslon-Italic', 'LibreCaslonText-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('LibreCaslon-Bold',   'LibreCaslonText-Bold.ttf'))

    # draw certificate background
    c.drawImage(background_path, 0, 0, width=A4[1], height=A4[0])

    # certificate body
    c.setFillColorRGB(0.01, 0.01, 0.01) # set font color
    y = 16 * cm # initial y height
    for line in certificate_string:
        # set font style
        if   line["style"] == "regular": c.setFont('LibreCaslon', 14)
        elif line["style"] == "italic":  c.setFont('LibreCaslon-Italic', 14)
        elif line["style"] == "bold":    c.setFont('LibreCaslon-Bold', 18)

        # center string
        text_width = c.stringWidth(line["string"])
        x = (A4[1] - text_width) / 2
        
        c.drawString(x, y, line["string"]) # draw string
        y -= 1.275 * cm # decreases y height for next line

    # save as PDF file
    c.save()


if __name__ == "__main__":
    data = []
    with open('pessoas.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            data.append(row)

    today = date.today()
    total = len(data)
    for i, person in enumerate(data):
        print_progress(i, total)
        certificate_string = generate_strings(person['nome'], person['cargo'], person['horas'])
        generate_certificate(person['nome'], "FEBRACE", today, "background/background.png", certificate_string)
