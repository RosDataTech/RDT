import rdt_hhru as hh
import rdt_pdf as pdf
import rdt_database as db
import rdt_ml as ml
import numpy as np
db_url = ''


def main():
    hh_search_term = 'Python Developer'

    job_text = hh.job_req_search(hh_search_term)

    db_url = ''

    uni_data = db.dataToDict(db_url)['IT']

    edu_texts = []

    skill_mapping = {
    # Программирование и разработка ПО
    "программное обеспечение": ["python", "c++", "git", "docker", "sql", "rest api"],
    "алгоритмы": ["структуры данных", "алгоритмы сортировки", "оптимизация кода", "O(n) complexity"],
    "объектно-ориентированное программирование": ["design patterns", "solid", "uml", "java", "c#"],
    
    # Математическое моделирование
    "математические модели": ["numpy", "scipy", "matlab", "simulink", "оптимизация", "линейная алгебра"],
    "теория вероятностей": ["pandas", "статистика", "hypothesis testing", "scikit-learn"],
    
    # Информационные системы и базы данных
    "информационные системы": ["postgresql", "mongodb", "redis", "kafka", "etl", "apache spark"],
    "большие данные": ["hadoop", "hive", "airflow", "databricks", "pyspark", "tableau"],
    
    # Аппаратное обеспечение и сети
    "аппаратные средства": ["arduino", "raspberry pi", "iot", "embedded systems", "fpga"],
    "сетевое оборудование": ["cisco", "tcp/ip", "vpn", "firewalls", "osi model"],
    
    # Управление проектами
    "управление проектами": ["jira", "trello", "agile", "scrum", "kanban", "risk management"],
    "техническая документация": ["confluence", "markdown", "swagger", "latex", "draw.io"],
    
    # Специализированные области
    "системы управления полетами": ["matlab/simulink", "ros (robot os)", "aerospace simulation", "control theory"],
    "схемотехническая документация": ["altium designer", "autocad", "solidworks", "spice"],
    "машинное обучение": ["tensorflow", "pytorch", "opencv", "computer vision", "nlp"]
}


    result_metrics = []
    for uni_name, pdf_url in uni_data[5:]:
        try:
            edu_texts.append(pdf.uni_cutter(pdf_url, uni_name))
        except Exception as e:
            print(f"Не удалось обработать {uni_name}: {e}")
    

    metric = 'optimal'  # default_metric = 'optimal', ['optimal', 'cluster', 'semantic']

    analyzer = ml.Analyzer(skill_mapping)
    for edu_text in edu_texts:
        result_metrics.append(analyzer.main_analyze(edu_text, job_text, metric)[1])
        print('done')

    print("\nКоэффициент соответствия:")
    print(np.average(result_metrics))

if __name__ == "__main__":
    main()

    
