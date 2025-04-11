import rdt_hhru as hh
import rdt_pdf as pdf
import rdt_database as db
import rdt_ml as ml

def main():
    hh_search_term = ''

    job_texts = hh.job_req_search(hh_search_term)

    db_url = 'Your database url here'
    uni_data = db.dataToDict(db_url)['IT']

    edu_texts = []
    for uni_name, pdf_url in uni_data.items():
        try:
            edu_texts.append(pdf.uni_cutter(pdf_url, uni_name))
        except Exception as e:
            print(f"Не удалось обработать {uni_name}: {e}")

    metric = ''  # default_metric = 'optimal', ['optimal', 'cluster', 'semantic']

    analyzer = ml.Analyzer()
    for edu_text, job_text in edu_texts, job_texts:
        result = analyzer.main_analyze(edu_text, job_text, metric) # не закончил

    print("\nКоэффициент соответствия:")
    print(result)

if __name__ == "__main__":
    main()
