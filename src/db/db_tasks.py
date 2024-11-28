import json

from fastapi import UploadFile

from db.db_connection import get_row_query, retrieve_data, store_data

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
        "missing_requirements": "\n".join(job_description["missing_requirements"])
    }
    
    store_data(TABLE_JOBS, data)

def get_job_description(job_id: str):
    row, columns  = get_row_query(TABLE_JOBS, "title", job_id)
    job_description = row[get_field_position('job_json', columns)]
    del job_description['missing_requirements']
    return job_description

def get_job_uuid(job_id):
    row, columns  = get_row_query(TABLE_JOBS, "title", job_id)
    return row[get_field_position('id', columns)]

def get_job_questions(job_id):
    row, columns  = get_row_query(TABLE_JOBS, "title", job_id)
    return row[get_field_position('questions', columns)].split('\n')

def store_application(cv: UploadFile, job_id: str, result):
    job_uuid = get_job_uuid(job_id)
    job_questions = get_job_questions(job_id)
    data = {
        'job_id': job_uuid,
        'cv': cv.file,
        'q1': job_questions[0],
        'q2': job_questions[1],
        'q3': job_questions[2],
        'q4': result['questions'][0],
        'q5': result['questions'][1],
        

        }
    
    store_data(TABLE_APPLICANTS, data)

def get_field_position(field, columns):
    for i in range(len(columns)):
        if columns[i] == field:
            return i
    return -1

