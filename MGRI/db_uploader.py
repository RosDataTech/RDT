import psycopg2
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

url = urlparse('DB_URL')

conn = psycopg2.connect(
    host=url.hostname,
    port=url.port,
    database=url.path[1:], 
    user=url.username,
    password=url.password
)
cur= conn.cursor()




codes = ['21.02.20', '05.03.01',
         '21.05.01', '21.05.02',
         '21.05.03', '05.04.01',
         '21.06.01']

driver = webdriver.Chrome()

driver.get("https://www.mgri.ru/sveden/education/eduop/")
time.sleep(5)

pdf_counter = 0
table = driver.find_element(By.XPATH, '//*[@id="vikon-content"]/div[3]/div[4]/table')
rows = table.find_elements(By.XPATH, ".//tr")
for row in rows:
    cells = row.find_elements(By.XPATH, ".//td")
    row_data = [cell.text for cell in cells]
    try:
        if row_data[1] in codes:
            link = row.find_element(By.XPATH, f".//a[contains(@href, '.pdf')]")
            file_url = link.get_attribute("href")
            print(file_url)
            print(row_data[1])
            cur.execute(f'''INSERT INTO Geology (university,code,url,type)
                                    VALUES ('MGRI','{row_data[1]}','{file_url}','.pdf')''')
            pdf_counter+=1
    except IndexError:
        pass

driver.quit()

print(pdf_counter)

conn.commit()
cur.close()  
conn.close()