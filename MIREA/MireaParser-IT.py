from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import urljoin  
import download_func


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

# Папка для загрузки файлов
download_dir = r"YOUR DOWNLOAD FOLDER"
relevant_year = '2024'


# Настройки Chrome
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})


driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.mirea.ru/sveden/education/")
time.sleep(5)


search_box = driver.find_element(By.XPATH, "//*[@id='page-wrapper']/div[2]/div/div/div[1]/div/div/div[2]/ul[4]/li/a")
search_box.click()
time.sleep(5)

table = driver.find_element(By.XPATH, "//*[@id='page-wrapper']/div[2]/div/div/div[1]/div/div/div[2]/ul[4]/li/div/div[2]/table")

rows = table.find_elements(By.XPATH, ".//tr")
for row in rows:
    cells = row.find_elements(By.XPATH, ".//td")
    row_data = [cell.text for cell in cells]
    try:
        line = row_data[5]
        for code in it_codes:
            if code in line:
                splitted_line = [i for i in line.split()]
                for layer in splitted_line:
                    if '.pdf' in layer and relevant_year in layer:
                        link = row.find_element(By.XPATH, f".//a[contains(@href, {relevant_year}.pdf)]")
                        file_url = link.get_attribute("href")

                        if not file_url.startswith("http"):
                            file_url = urljoin("https://www.mirea.ru", file_url)  
                        download_func.download_file(file_url, download_dir)
                        
                        if download_func.wait_for_download_complete(download_dir):
                            print(f"Файл {file_url} успешно загружен.")
                        else:
                            print(f"Не удалось загрузить файл {file_url}.")
    except IndexError: # заплатка(        
        pass

driver.quit()
