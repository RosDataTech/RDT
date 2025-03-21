from bs4 import BeautifulSoup
import requests
import psycopg2
from urllib.parse import urljoin  
from urllib.parse import urlparse

url = urlparse('DB_URL')

conn = psycopg2.connect(
    host=url.hostname,
    port=url.port,
    database=url.path[1:], 
    user=url.username,
    password=url.password
)
cur = conn.cursor()

pedagogy_codes = [
    "44.03.02", "44.03.05", "42.03.01",
    "45.03.02", "44.03.03", "44.03.04",
    "44.03.01", "37.03.01", "39.03.02"
]

relevant_years = [2024, 2023, 2022, 2021, 2020]
relevant_years.sort(reverse=True)

url = "https://s.rgsu.net/sveden/education/eduop/"
response = requests.get(url, verify=False)
soup = BeautifulSoup(response.text, 'lxml')

pdf_counter = 0

eduOp_rows = soup.find_all('tr', itemprop='eduOp')

for row in eduOp_rows:
    code = row.find('td', itemprop='eduCode').text.strip()
    
    if code in pedagogy_codes:
        links = row.find_all('a', href=True)
        
        for year in relevant_years:
            found_link = None
            for link in links:
                if str(year) in link['href'] and link['href'].endswith('.pdf'):
                    found_link = link['href']
                    break
            
            if found_link and 'netcat' not in found_link:
                if not found_link.startswith('http'):
                    found_link = f"https://s.rgsu.net{found_link}"
                    cur.execute(f'''INSERT INTO Pedagogy (university,code,url,type)
                                    VALUES ('RGSU','{code}','{found_link}','.pdf')''')
                
                print(f"{code},{found_link}")
                pdf_counter += 1
                break

print(f"Всего найдено PDF-файлов: {pdf_counter}")

conn.commit()
cur.close()  
conn.close()
