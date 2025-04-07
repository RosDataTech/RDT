import requests
import PyPDF2
from io import BytesIO

uni_index = {"MIREA" : ["14. "], "MFTI" : ["4. ","5. "],
         "MGTU" : ["1.6.","1.7."], "INNOP" : ["4. РЕЗУЛЬТАТЫ","5. СТРУКТУРА"],"RANH" : ["2.2.","3."],"MFUA" : ["4.","5."],
         "VSHE" : ["Характеристика профессиональной деятельности:","Характеристика образовательных модулей:"],
         "VSPU" : ["2.5. ","2.6. "], "SURGPU" : ["РАЗДЕЛ 4. ","РАЗДЕЛ 5. "], "ALTSPU" : ["Раздел 4. ","Раздел 5. "],
         "ASU" : ["3. Требования к результатам","4. Требования к структуре"], "PAVL" : ["1.5 ","1.6 "], "NSMU" : ["РАЗДЕЛ 4. ","РАЗДЕЛ 5. "], "USMA" : ["3. ","4. "],
         "SECH" : ["3. РЕЗУЛЬТАТЫ ОСВОЕНИЯ ОБРАЗОВАТЕЛЬНОЙ ПРОГРАММЫ", "1. СТРУКТУРА И ОБЪЕМ ОБРАЗОВАТЕЛЬНОЙ ПРОГРАММЫ"],
         "ROSUNIMED" : ["2. ","2.2. "], "PIROG" : ["РАЗДЕЛ 4. ","РАЗДЕЛ 5. "], "TUMGMU" : ["Приложение 4","Приложение 5"],
         "MGRI" : ["РЕЗУЛЬТАТЫ ОСВОЕНИЯ","Матрица соответствия"], "MGY" : ["2. ","4. "], "RGY" : ["ОБУЧЕНИЕ","ПРАКТИКИ И СТАЖИРОВКИ"], "MIIGAIK" : ["2.3.","3."],
         "RUDN" : ["6.","7."]
        }

def extract_text_from_pdf(pdf_url):

    response = requests.get(pdf_url)
    response.raise_for_status()  

    with BytesIO(response.content) as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

def uni_cutter(pdf_url, uni_name):
    try:
        text = extract_text_from_pdf(pdf_url)[::-1]

        start_index = text.index(uni_index[f'{uni_name}'][0][::-1])
        end_index = 0
        if len(uni_index[f'{uni_name}'])>1:
            end_index = text.index(uni_index[f'{uni_name}'][1][::-1])

        return text[end_index:start_index][::-1]
    
    except:
        return ''