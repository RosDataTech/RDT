from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import psycopg2
from urllib.parse import urljoin  
from urllib.parse import urlparse


url = urlparse('postgresql://postgres:yZKEWJnGDIaiZK6V@meekly-enabled-brocket.data-1.use1.tembo.io:5432/postgres')

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

driver = webdriver.Chrome()

driver.get("https://stankin.ru/sveden/education/eduop/")
time.sleep(5)


table = driver.find_element(By.XPATH, '//*[@id="vikon-content"]/div[2]/div[3]/table')

rows = table.find_elements(By.XPATH, ".//tr")
for row in rows:
    cells = row.find_elements(By.XPATH, ".//td")
    row_data = [cell.text for cell in cells]
    try:
        if row_data[1] in it_codes:
            link = row.find_element(By.XPATH, f".//a[contains(@href, '.pdf')]")
            file_url = link.get_attribute("href")
            if 'OPVO' in file_url:
                print(file_url)
                cur.execute(f'''INSERT INTO IT (university,code,url,type)
                                    VALUES ('STANKIN','{row_data[1]}','{file_url}','.pdf')''')
    except IndexError: # заплатка(        
        pass

driver.quit()

conn.commit()
cur.close()  
conn.close()
    
