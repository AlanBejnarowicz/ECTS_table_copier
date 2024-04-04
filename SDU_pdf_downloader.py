import numpy as np
import pandas as pd
import os
import requests
#import fitz  # PyMuPDF


courses_filename = 'data.csv'
PDF_folder = 'PDFs'

def download_PDF(url,course_name):
    # get filename from url
    filename = url.split('/')[-1]
    print('Downloading: ', course_name, ' from: ', url)

    path = PDF_folder + '/' + course_name + '.pdf'

    # create file and write content
    with open(path, 'wb') as f:
        f.write(requests.get(url).content)



if __name__ == '__main__':
    print("SDU course decrtiption filler")

    # read csv
    df = pd.read_csv(courses_filename)
    # get all links
    links = df['Link']
    names = df['Name']

    print('Creating PDFs folder')
    # create folder for PDFs
    if not os.path.exists(PDF_folder):
        os.makedirs(PDF_folder)

    # delete all files in folder
    files = os.listdir(PDF_folder)
    for file in files:
        os.remove(PDF_folder + '/' + file)
        print ('Deleting: ', file)

    print('Downloading PDFs')

    # download 2 first PDFs
    for i in range(links.size):
        download_PDF(links[i], names[i])


