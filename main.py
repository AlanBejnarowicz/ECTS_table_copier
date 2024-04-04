import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://ects.pg.edu.pl/en/courses/12925/subcourses/12929/subjects'

if __name__ == '__main__':
    print('Scrapping data from: ', url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    body = soup.body  # korzystając z tego skrótu można dostać się do konkretnego znacznika

    data = []

    #print(soup.prettify())

    div = body.find('div', {'class': 'cell-mobile'})  # szukamy div'ów klasy "md wiki"

    #print(div.prettify())

    for div in body.find_all('div', {'class': 'cell-mobile'}):

        # fint text in <a>
        name = div.find('a', {'class': 'cell-mobile__link collapsed'}).get_text().strip()
        #print(name)

        card_link = div.find('a', {'class': 'btn btn--submit wide'}).get('href').strip()
        #print(card_link)

        ECTS = div.find('div', {'class': 'collapse'})
        ECTS = ECTS.find('div', {'class': ''}).get_text().strip()

        #remove all white spaces
        ECTS = ECTS.replace(' ', '')
        #split by new line
        ECTS = ECTS.split('\n')
        #print(ECTS[1])

        #print data in table
        print(name, '   ', ECTS[1], '   ', card_link)
        data.append([name, ECTS[1], card_link])


    #create dataframe
    df = pd.DataFrame(data, columns=['Name', 'ECTS', 'Link'])

    #save to csv
    df.to_csv('data.csv', index=False)




