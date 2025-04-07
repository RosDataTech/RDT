import requests
from time import sleep
API_ENDPOINT = "https://api.hh.ru/vacancies"
RESULTS_FILENAME = "junior_skills.txt"
REQUEST_DELAY = 0.5

def fetch_job_openings(search_term, exp_level="noExperience", items=100, offset=0):
    query_params = {
        "text": f"{search_term} Junior",
        "experience": exp_level,
        "per_page": items,
        "page": offset,
        "order_by": "publication_time"
    }
    
    try:
        response = requests.get(API_ENDPOINT, params=query_params)
        response.raise_for_status()
        sleep(REQUEST_DELAY)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {str(e)}")
        return None

def parse_skills(job_data):
    skill_descriptions = []
    
    for position in job_data.get("items", []):

        details = position.get("snippet") or {}
        
        raw_skills = details.get("requirement")
        skills_text = str(raw_skills) if raw_skills is not None else ""
        
        clean_skills = skills_text.replace("<highlighttext>", "").replace("</highlighttext>", "").strip()
        
        if clean_skills:
            skill_descriptions.append(clean_skills)
        else:
            print(f"Skipped position: {position.get('name') or 'UNKNOWN_TITLE'}")
    
    return skill_descriptions


def job_req_search(search_term, exp_level = 'noExperience'):

    job_results = fetch_job_openings(search_term = search_term, exp_level= exp_level)
    
    if not job_results or "items" not in job_results:
        print("No job listings found")
        return
    
    required_skills = parse_skills(job_results)
    
    if not required_skills:
        print("No skill requirements extracted")
        return
    
    return required_skills

if __name__ == "__main__":
    print(job_req_search('Python Dev'))