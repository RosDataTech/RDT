import requests
import time
import os

def download_file(url, download_dir):
    local_filename = url.split('/')[-1]
    local_path = os.path.join(download_dir, local_filename)
    with requests.get(url, stream=True) as r:
        if r.status_code == 200:  
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Файл {local_filename} успешно загружен.")
        else:
            print(f"Ошибка {r.status_code}: Не удалось загрузить файл {url}.")




def wait_for_download_complete(download_dir, timeout=30):
    """
    Ожидает завершения загрузки файла в указанной папке.
    """
    end_time = time.time() + timeout
    while time.time() < end_time:
        if not any(fname.endswith('.crdownload') for fname in os.listdir(download_dir)):
            return True
        time.sleep(1)
    return False
