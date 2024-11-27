
import json

from db_connection import store_data

FOLDER = ('output')

def store_job(id: str, url: str):
    table_name = 'jobs'
    # load output
    job_json = json.load(open(FOLDER + '/' + id + '.json'))

    req_education = ""
    req_experience = ""

    for e in job_json['pre_requirements']:
        print(e)
        if "education" in e:
            req_education = e['education']
        if "experience" in e:
            req_experience = e['experience']

    data = {
        'title': id,
        'url': url,
        'job_role': job_json['job_role'],
        'job_level': job_json['job_level'],
        'pre_requirements_education': req_education,
        'pre_requirements_experience': req_experience,
        'hard_skills': "\n".join(job_json['hard_skills']),
        'soft_skills': "\n".join(job_json['soft_skills']),
        'responsibilities': "\n".join(job_json['responsibilities']),
        'others': "\n".join(job_json['others']),
        'job_json': json.dumps(job_json)
        }

    
    store_data(table_name, data)



if __name__ == "__main__":
    store_job('test', 'https://test.com')