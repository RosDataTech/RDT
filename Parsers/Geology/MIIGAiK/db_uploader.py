from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import psycopg2
from urllib.parse import urlparse

url = urlparse('db_url')

conn = psycopg2.connect(
    host=url.hostname,
    port=url.port,
    database=url.path[1:],
    user=url.username,
    password=url.password
)
cur = conn.cursor()


codes = ['21.03.03', '05.03.03',
         '21.03.02']

driver = webdriver.Chrome()

driver.get('https://www.miigaik.ru/education/oop/')
time.sleep(3)

table = driver.find_element(By.XPATH, '//*[@id="js-main"]/div/div[1]/div[1]/div/div[1]/div')
rows = table.find_elements(By.XPATH, ".//p")

count = 0
for row in rows:
    cells1 = row.find_elements(By.XPATH, ".//small")
    cells2 = row.find_elements(By.XPATH, ".//b")
    row_data = [cell.text for cell in cells1]
    data_codes = [cell.text for cell in cells2]
    if data_codes[0][:8] in codes:
        try:
            link = row.find_element(By.XPATH, f".//small/a[contains(@href, '.pdf')]")
            count += 1
            file_url = link.get_attribute("href")
            print(file_url)
            cur.execute(f'''INSERT INTO Geology (university,code,url,type)
                                                VALUES ('MIIGAIK','{data_codes[0][:8]}','{file_url}','.pdf')''')
        except NoSuchElementException:
            pass

driver.quit()

print(count)
conn.commit()
cur.close()
conn.close()
