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


driver = webdriver.Chrome()

driver.get('https://geol.msu.ru/obrazovatelnye-programmy/')
time.sleep(3)

table = driver.find_element(By.XPATH, '//*[@id="about-dep"]/ul[2]')
rows = table.find_elements(By.XPATH, ".//li")

count = 1
for row in rows:
    link = driver.find_element(By.XPATH, f'//*[@id="about-dep"]/ul[2]/li[{count}]/a')
    link.click()
    for _ in range(2):
        link = driver.find_element(By.XPATH, '//*[@id="about-dep"]/p[2]/a')
        link.click()
    file_link = link.get_attribute("href")
    print(file_link)
    cur.execute(f'''INSERT INTO Geology (university,code,url,type)
                                    VALUES ('MGY','*','{file_link}','.pdf')''')
    driver.execute_script("window.history.go(-2)")
    count += 1

print(count)
driver.quit()
conn.commit()
cur.close()  
conn.close()
