import rdt_hhru as hh
import rdt_pdf as pdf
import rdt_database as db
import rdt_ml as ml

def main():
    # Ввод запроса от пользователя
    hh_search_term = str(input("Введите название профессии: ").strip())

    # Получение требований из hh.ru
    print(f"\nПолучение требований по вакансии '{hh_search_term}'...")
    job_texts = hh.job_req_search(hh_search_term, exp_level)

    # Загрузка образовательных программ из базы
    db_url = 'Your database url here'
    uni_data = db.dataToDict(db_url)

    # Извлечение текстов программ обучения
    edu_texts = ""
    for uni_name, pdf_url in uni_data.items():
        try:
            edu_texts += "\n" + pdf.uni_cutter(pdf_url, uni_name)
        except Exception as e:
            print(f"Не удалось обработать {uni_name}: {e}")

    # Выбор метрики сравнения
    metrics = ['optimal', 'cluster', 'semantic']
    default_metric = 'optimal'

    while True:
        metric = input(
            f"Выберите метрику сравнения из доступного списка:\n"
            f" - optimal (по умолчанию)\n"
            f" - cluster\n"
            f" - semantic\n"
            f"Нажмите Enter для выбора default_metric = optimal\n"
            f"Ваш выбор: "
        ).strip().lower()

        if not metric:
            metric = default_metric
            print(f"\nИспользуется метрика по умолчанию: '{metric}'\n")
            break

        if metric not in metrics:
            print("\nОшибка: такого значения нет в списке. Попробуйте ещё раз.\n")
        else:
            print(f"\nИспользуется метрика: '{metric}'\n")
            break


    # Анализ соответствия
    analyzer = ml.Analyzer()
    result = analyzer.main_analyze(edu_texts, job_texts, metric)

    print("\nКоэффициент соответствия:")
    print(result)

if __name__ == "__main__":
    main()
