# Dependencies
# ReportLab
from reportlab.pdfgen import canvas          # canvas
from reportlab.lib.units import cm           # measurements
from reportlab.lib.pagesizes import A4       # measurements
from reportlab.pdfbase import pdfmetrics     # custom font support
from reportlab.pdfbase.ttfonts import TTFont # custom font support

# Python Modules
import argparse                 # argument parsing
import json                     # strings parsing
import sys                      # exception handling
import csv                      # data import
import re                       # filename processing
from datetime import date       # filename processing
from unidecode import unidecode # filename processing

def print_progress(i, total):
    progress = i / total * 100
    print(f"Progress: {progress:.1f}%", end="\r")

    return

def replace_json_variables(json_file_path, variables):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    # Recursively replace variables in the JSON data
    def replace_variables(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, str):
                    for var_key, var_value in variables.items():
                        value = value.replace(f'${var_key}', var_value)
                    obj[key] = value
                else:
                    replace_variables(value)
        elif isinstance(obj, list):
            for i in range(len(obj)):
                replace_variables(obj[i])

    replace_variables(json_data)

    return json_data

def generate_certificate(name, certificate_name, today, background_path, certificate_string, signatures):
    # canvas initialization
    clean_name = re.sub(r'[^0-9a-zA-Z]+', '', unidecode(name))
    filename = f'certificados/{today}_{certificate_name}_{clean_name}.pdf' # generates certificate filename 
    c = canvas.Canvas(filename, pagesize=[A4[1], A4[0]])         # initializes PDF canvas

    # custom font
    pdfmetrics.registerFont(TTFont('LibreCaslon',        'LibreCaslonText-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('LibreCaslon-Italic', 'LibreCaslonText-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('LibreCaslon-Bold',   'LibreCaslonText-Bold.ttf'))

    # draw certificate background
    try:
        if background_path: c.drawImage(background_path, 0, 0, width=A4[1], height=A4[0])
        else: print("Imagem de fundo não especificada")
    except OSError as e:
        print(f"Imagem de fundo não encontrada")
        sys.exit()

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

    # certificate signature
    c.setFont('LibreCaslon', 10)
    if(len(signatures) == 1):
        x = 13.83 * cm
        y = 3.63 * cm
        for key, string in signatures[0].items():
            c.drawString(x, y, string, charSpace=-0.25)
            y -= 0.46 * cm
    if(len(signatures) == 2):
        x = 2.795 * cm
        y = 3.63 * cm
        for key, string in signatures[0].items():
            c.drawString(x, y, string, charSpace=-0.25)
            y -= 0.46 * cm
        x = 18.425 * cm
        y = 3.63 * cm
        for key, string in signatures[1].items():
            c.drawString(x, y, string, charSpace=-0.25)
            y -= 0.46 * cm


    # save as PDF file
    c.save()

if __name__ == "__main__":
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("pessoas", help="[csv] Dados das pessoas que serão utilizados para geração dos certificados")
    parser.add_argument("-a", "--assinantes", help="[csv] Dados das pessoas que assinarão os certificados")
    parser.add_argument("-b", "--background", help="[image] Imagem de fundo do certificado")
    parser.add_argument("-s", "--strings", help="[json] Texto do certificado", default="febracm_vencedores")
    args = parser.parse_args()

    # data loading
    data = []
    with open(f'{args.pessoas}', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            data.append(row)

    signatures = []
    try:
        with open(f'{args.assinantes}', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                signatures.append(row)
    except OSError as e:
        print(f"Arquivo de assinantes não especificado")
    
    # generate certificates
    today = date.today() # filename
    total = len(data)    # progress
    for i, person in enumerate(data):
        print_progress(i, total)
        certificate_string = replace_json_variables(f"{args.strings}", person)
        generate_certificate(person['nome'], "FEBRACE", today, args.background, certificate_string, signatures)