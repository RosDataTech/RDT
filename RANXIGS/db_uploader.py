from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import psycopg2
from urllib.parse import urlparse

url = urlparse('DB_URL')

conn = psycopg2.connect(
    host=url.hostname,
    port=url.port,
    database=url.path[1:], 
    user=url.username,
    password=url.password
)
cur= conn.cursor()

k = 0
codes = [
    "38.03.04", "40.03.01", "40.03.02", "41.03.01",
    "41.03.02", "38.04.04", "40.04.01", "41.04.01",
    "40.05.01", "40.05.04"
]
driver = webdriver.Chrome()
driver.get("https://www.ranepa.ru/sveden/education/obrazovatelnye-programmy-nabora-2023-2024")
time.sleep(5)
rows = driver.find_elements(By.XPATH, "//tr[@itemprop='eduOp']")
for row in rows:
    edu_code = row.find_element(By.XPATH, ".//span[@itemprop='eduCode']").text.strip()
    if str(edu_code) in codes:
        popup_content = row.find_element(By.CLASS_NAME, "popupFileWindow__content")
        link = popup_content.find_elements(By.TAG_NAME, "a")[-1]
        k+=1
        href = link.get_attribute("href")
        cur.execute(f'''INSERT INTO Jurisprudence (university,code,url,type)
                    VALUES ('RANH','{str(edu_code)}','{href}','.pdf')''')
        print(edu_code,href)
print(k)
driver.quit()


conn.commit()
cur.close()  
conn.close()


