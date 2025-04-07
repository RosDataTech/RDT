from bs4 import BeautifulSoup
import requests
import psycopg2
from urllib.parse import urljoin  
from urllib.parse import urlparse

url = urlparse('DB_url')

conn = psycopg2.connect(
    host=url.hostname,
    port=url.port,
    database=url.path[1:], 
    user=url.username,
    password=url.password
)
cur= conn.cursor()

it_codes = [
    "09.00.00", "09.03.01", "09.03.02", "09.03.03", "09.03.04", 
    "09.04.01", "09.04.02", "09.04.03", "09.04.04", "09.05.01", 
    "09.06.01", "10.00.00", "10.03.01", "10.04.01", "10.05.01", 
    "10.05.02", "10.05.03", "10.05.04", "10.05.05", "10.06.01", 
    "11.00.00", "11.03.02", "11.03.03", "11.04.02", "11.04.03", 
    "11.05.01", "11.06.01", "27.00.00", "27.03.03", "27.03.04", 
    "27.04.03", "27.04.04", "27.06.01", "38.00.00", "38.03.05", 
    "38.04.05", "01.00.00", "01.03.02", "01.04.02", "01.06.01", 
    "02.00.00", "02.03.01", "02.03.02", "02.03.03", "02.04.01", 
    "02.04.02", "02.04.03", "02.06.01", "45.00.00", "45.03.04", 
    "45.04.04", "54.00.00", "54.03.01", "54.04.01"
]

relevant_years = ['2024','2023']
relevant_years.sort(reverse=True)


url = "https://mf.bmstu.ru/sveden/education/eduop/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

pdf_counter = 0

eduOp = soup.find_all(itemprop = 'eduOp')
for spec in eduOp:
    eduCode = spec.find_all(itemprop = 'eduCode')[0].text.strip()
    if eduCode in it_codes:
        link_counter = 0
        for link in spec.find_all('a'):
            if relevant_years[0] in link['href'] and 'OPOP' in link['href']:
                print('https://mf.bmstu.ru/' + link['href'])
                cur.execute(f'''INSERT INTO IT (university,code,url,type)
                                    VALUES ('MGTU','{eduCode}','{'https://mf.bmstu.ru/' + link['href']}','.pdf')''')
                pdf_counter+=1
                link_counter+=1
        if link_counter == 0:
            for link in spec.find_all('a'):
                if relevant_years[1] in link['href'] and 'OPOP' in link['href']:
                    print('https://mf.bmstu.ru/' + link['href'])
                    cur.execute(f'''INSERT INTO IT (university,code,url,type)
                                    VALUES ('MGTU','{eduCode}','{'https://mf.bmstu.ru/' + link['href']}','.pdf')''')
                    pdf_counter+=1


print('pdf_counter = ', pdf_counter)



conn.commit()
cur.close()  
conn.close()
    