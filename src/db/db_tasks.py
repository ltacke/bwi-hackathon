import json
import os

from fastapi import UploadFile

from db.db_connection import retrieve_data, store_data

FOLDER = ('output')
TABLE_JOBS = "jobs"
TABLE_APPLICANTS = "applicants"

def store_job(id: str, url: str, job_json):

    print(job_json.keys())
    # load output
    file = id + '-description.json'
    try:
        job_json = json.load(open(FOLDER + '/' + file))
    except:
        for f in os.listdir(FOLDER):
            if f.endswith('.json') and not f.endswith('processed.json'):
                job_json = json.load(open(FOLDER + '/' + f))
                file = f

    req_education = ""
    req_experience = ""

    for e in job_json["pre_requirements"]:
        print(e)
        if "education" in e:
            req_education = e["education"]
        if "experience" in e:
            req_experience = e["experience"]

    data = {
        "title": id,
        "url": url,
        "job_role": job_json["job_role"],
        "job_level": job_json["job_level"],
        "pre_requirements_education": req_education,
        "pre_requirements_experience": req_experience,
        "hard_skills": "\n".join(job_json["hard_skills"]),
        "soft_skills": "\n".join(job_json["soft_skills"]),
        "responsibilities": "\n".join(job_json["responsibilities"]),
        "others": "\n".join(job_json["others"]),
        "job_json": json.dumps(job_json),
    }


    file = id + '-questions.json'
    try:
        job_questions = json.load(open(FOLDER + '/' + file))
        data['questions'] = "\n".join(job_questions['questions'])
    except:
        print("could not load questions")
        
    
    store_data(TABLE_JOBS, data)
    #os.rename(FOLDER + '/' + file, FOLDER + '/' + file.replace('.json', '_processed.json'))

def store_application(cv: UploadFile, job_id: str, result):
    job_uuid = get_job_uuid(job_id)

    data = {
        'job_id': job_uuid,
        'cv': cv.file

        }
    
    store_data(TABLE_APPLICANTS, data)

if __name__ == "__main__":
    store_job('Cloud-Engineer-57661', 'https://test.com')

    # print(retrieve_data(TABLE_JOBS))

    # questions = '''What are the key considerations for designing and implementing scalable and highly available cloud architectures, and how would you approach this task?
    # How do you ensure security by design in DevSecOps projects, and what measures would you take to integrate and monitor security standards in the development process?
    # Can you explain your experience with containerization and orchestration of cloud mechanisms, such as Kubernetes, and how you would optimize container solutions for efficient application operation?
    # How do you approach mentoring and technical training of team members in cloud technologies, and what strategies would you use to support their development?
    # What is your experience with cloud-native technologies, such as SAP BTP, GIT, Spring, and Docker, and how would you leverage these technologies to support the development of software-as-a-service solutions?'''
    # data = {
    #     'questions': questions
    # }
    # print(data)
    #store_data('jobs', 'id', data)
