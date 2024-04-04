import numpy as np
import pandas as pd
import os
import requests
import fitz
import tabula

from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.platypus import Spacer





courses_filename = 'data.csv'
PDF_folder = 'PDFs'

output_pdf_file = 'course_descriptions.pdf'

if __name__ == '__main__':
    print("SDU course decrtiption filler")

    pdfmetrics.registerFont(TTFont('DejaVuSans', 'fonts/DejaVuSans.ttf'))

    # get all pdfs from folder
    files = os.listdir(PDF_folder)
    print('Number of PDFs: ', len(files))

    courses_data = []


    for i in range(len(files)):
        PDF_file = PDF_folder + '/' + files[i]

        # Inicjalizacja słownika na potrzebne dane
        course_data = {
            "Course Title": None,
            "ECTS points/workload": None,
            "Level": None,
            "Form of Instruction": None,
            "Form of Examination": None,
            "Description": None,
            "Literature": None
        }

        pdf_document = fitz.open(PDF_file)

        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            text = page.get_text()

            # Szukanie danych na podstawie słów kluczowych
            if "Subject name and code" in text:
                start_idx = text.find("Subject name and code") + len("Subject name and code")
                end_idx = text.find("Field of study")
                course_data["Course Title"] = text[start_idx:end_idx].strip()

            # Uzupełnienie danych ECTS
            if "ECTS credits" in text:
                start_idx = text.find("ECTS credits") + len("ECTS credits")
                end_idx = text[start_idx:].find("Learning profile") + start_idx

                print (text[start_idx:end_idx].strip())
                course_data["ECTS points/workload"] = text[start_idx:end_idx].strip()

            if "Education level" in text:
                start_idx = text.find("Education level") + len("Education level")
                end_idx = text.find("Subject group")
                course_data["Level"] = text[start_idx:end_idx].strip()

            if "Lesson types and methods of instruction" in text:
                start_idx = text.find("Lesson type")
                end_idx = text.find("Learning activity and number of study hours")
                course_data["Form of Instruction"] = text[start_idx:end_idx].strip()

            if "Assessment form" in text:
                start_idx = text.find("Assessment form") + len("Assessment form")
                end_idx = text.find("Conducting unit")
                course_data["Form of Examination"] = text[start_idx:end_idx].strip()

            if "Subject objectives" in text:
                start_idx = text.find("Subject objectives") + len("Subject objectives")
                end_idx = text.find("Learning outcomes", start_idx)
                description = text[start_idx:end_idx].strip()

                # if there is no new line after 20 characters add it at first space
                charachters = 0
                for x in range(len(description)):
                    charachters += 1
                    if description[x] == '\n':
                        charachters = 0

                    if charachters > 80 and description[x] == ' ':
                        description = description[:x] + '\n' + description[x:]
                        charachters = 0


                course_data["Description"] = description

            if "Recommended reading" in text:
                start_idx = text.find("Basic literature") + len("Basic literature")
                end_idx = text.find("Supplementary literature")
                course_data["Literature"] = text[start_idx:end_idx].strip()



        # Zamknięcie dokumentu PDF
        pdf_document.close()

        course_data["Form of Instruction"] = "Lecture"

        if files[i].find("laboratory") != -1:
            course_data["Form of Instruction"] = "Laboratory"

        elif files[i].find("project") != -1:
            course_data["Form of Instruction"] = "Project"


        #print data in lines
        # for key, value in course_data.items():
        #     print(key, '   ', value)

        # Dodanie danych do listy
        courses_data.append(course_data)

    # Utworzenie dokumentu PDF
    pdf = SimpleDocTemplate(output_pdf_file, pagesize=A4)
    pdf.title = "Updated Course Data"

    # Lista elementów do dodania do dokumentu PDF
    elements = []

    # Dodawanie tabel dla każdego kursu
    for course in courses_data:
        # Konwersja danych kursu do formatu odpowiedniego dla tabeli ReportLab
        course_table_data = [[key, value] for key, value in course.items()]
        table = Table(course_table_data, colWidths=[100, 400], repeatRows=1, splitByRow=False)


        # Stylizacja tabeli
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Dodanie tabeli do listy elementów dokumentu
        elements.append(table)
        # Dodanie spacji po każdej tabeli
        elements.append(Spacer(1, 30))

    # Generowanie dokumentu PDF
    pdf.build(elements)



