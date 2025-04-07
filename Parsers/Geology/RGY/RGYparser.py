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

count = 1
for row in rows:
    cells = row.find_elements(By.XPATH, ".//td")
    row_data = [cell.text for cell in cells]
    if row_data[0] in codes:
        link = row.find_element(By.XPATH, f".//a[contains(@href, '.pdf')]")
        file_url = link.get_attribute("href")
        print(file_url)
driver.quit()
