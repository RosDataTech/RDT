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

pedagogy_codes = ["44.03.02", "44.03.05", "49.03.02", "45.03.02", "44.03.03", "44.03.04"]

relevant_years = [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017]
relevant_years.sort(reverse=True)

base_url = "https://omgpu.ru"

url = "https://omgpu.ru/sveden/education3#bakalavriat"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

pdf_counter = 0

max_year_links = {}

eduOp = soup.find_all(itemprop='eduOp')
for spec in eduOp:
    code = spec.find(itemprop='eduCode').text.strip()
    
    name = spec.find(itemprop='eduName').text.strip()
    
    edu_prof = spec.find(itemprop='eduProf')
    profile = edu_prof.text.strip() if edu_prof else "Общий профиль"
    
    if code in pedagogy_codes:
        edu_form = spec.find(itemprop='eduForm').text.strip()
        year = None
        if "год набора" in edu_form:
            year = int(edu_form.split("год набора")[1].strip().split(")")[0])
        
        if year and year in relevant_years:
            pdf_link = spec.find(itemprop='opMain').find('a')['href']
            full_url = base_url + pdf_link
            
            key = f"{code} - {name} - {profile}"
            
            if key not in max_year_links:
                max_year_links[key] = {'year': year, 'url': full_url}
            else:
                if year > max_year_links[key]['year']:
                    max_year_links[key] = {'year': year, 'url': full_url}

for key, data in max_year_links.items():
    print(f"{key[:8]} {data['url']}")
    pdf_counter += 1
    cur.execute(f'''INSERT INTO Pedagogy (university,code,url,type)
                                    VALUES ('OMPGU','{key[:8]}','{data['url']}','.pdf')''')
print('pdf_counter =', pdf_counter)

conn.commit()
cur.close()  
conn.close()
