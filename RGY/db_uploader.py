from selenium import webdriver
from selenium.webdriver.common.by import By
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
cur= conn.cursor()


from selenium import webdriver
from selenium.webdriver.common.by import By
import time


codes = ['05.03.01.01', '05.03.01.02',
         '05.03.06.01']

driver = webdriver.Chrome()

driver.get('https://www.gubkin.ru/programms/bachelor.php')
time.sleep(3)

table = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div/table/tbody/tr/td[2]/table[1]')
rows = table.find_elements(By.XPATH, ".//tr")

count = 0
for row in rows:
    cells = row.find_elements(By.XPATH, ".//td")
    row_data = [cell.text for cell in cells]
    if row_data[0] in codes:
        link = row.find_element(By.XPATH, f".//a[contains(@href, '.pdf')]")
        count+=1
        file_url = link.get_attribute("href")
        print(file_url,row_data[0])
        cur.execute(f'''INSERT INTO Geology (university,code,url,type)
                                    VALUES ('RGY','{row_data[0]}','{file_url}','.pdf')''')
driver.quit()
print(count)
conn.commit()
cur.close()  
conn.close()
