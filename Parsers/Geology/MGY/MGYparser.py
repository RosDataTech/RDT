from selenium import webdriver
from selenium.webdriver.common.by import By
import time


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
    driver.execute_script("window.history.go(-2)")
    count += 1

driver.quit()
