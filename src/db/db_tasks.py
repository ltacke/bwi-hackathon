import json

from fastapi import UploadFile

from db.db_connection import retrieve_data, store_data

TABLE_JOBS = "jobs"
TABLE_APPLICANTS = "applicants"

def store_job(id: str, url: str, job_description):

    data = {
        "title": id,
        "url": url,
        "job_role": job_description["job_role"],
        "job_level": job_description["job_level"],
        "pre_requirements_education":  job_description["pre_requirements"]['education'],
        "pre_requirements_experience": job_description["pre_requirements"]['experience'],
        "hard_skills": "\n".join(job_description["hard_skills"]),
        "soft_skills": "\n".join(job_description["soft_skills"]),
        "responsibilities": "\n".join(job_description["responsibilities"]),
        "others": "\n".join(job_description["others"]),
        "questions": "\n".join(job_description["questions"]),
        "job_json": json.dumps(job_description),
    }
    
    store_data(TABLE_JOBS, data)

def store_application(cv: UploadFile, job_id: str, result):
    #job_uuid = get_job_uuid(job_id)
    job_uuid = "asdf"
    data = {
        'job_id': job_uuid,
        'cv': cv.file

        }
    
    store_data(TABLE_APPLICANTS, data)

if __name__ == "__main__":
    store_job('Cloud-Engineer-57661', 'https://test.com', "{}")

