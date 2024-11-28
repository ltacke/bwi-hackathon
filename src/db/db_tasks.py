import json

from fastapi import UploadFile

from db.db_connection import get_all_rows_query, get_row_query, store_data, store_timestamp_id, update_data_id

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
    
    return store_data(TABLE_JOBS, data)

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

def store_application(name, email, phone, birthdate, job_id, result):
    job_uuid = get_job_uuid(job_id)
    job_questions = get_job_questions(job_id)
    data = {
        'job_id': job_uuid,
        'name': name,
        'email': email,
        'phone': phone,
        'birthdate': birthdate,
        'q1': job_questions[0],
        'q2': job_questions[1],
        'q3': job_questions[2],
        'q4': result['questions'][0],
        'q5': result['questions'][1],
        'skills': result['skills'],
        'education': result['education'],
        'experience': result['experience'],
        'gaps': result['gaps'],
        'applicant_questions': "\n".join(result['questions']),
        'json': json.dumps(result)

        }
    
    store_data(TABLE_APPLICANTS, data)


def get_applicants_by_job_id(job_id: str):
    job_id = get_job_uuid(job_id)
    rows, columns = get_all_rows_query(TABLE_APPLICANTS, "job_id", job_id)
    print(rows)
    field_pos = get_field_position('id', columns)
    result = []
    for r in rows:
        result.append(r[field_pos])
    return result
    

def retrieve_question(user_id, n):
    row, columns = get_row_query(TABLE_APPLICANTS, "id", user_id)
    question = row[get_field_position(f'q{n}', columns)]
    return question.replace("\"", "")

def retrieve_answer(user_id, n):
    row, columns = get_row_query(TABLE_APPLICANTS, "id", user_id)
    answer = row[get_field_position(f'a{n}', columns)]
    return answer

def retrieve_analysis(user_id, n):
    row, columns = get_row_query(TABLE_APPLICANTS, "id", user_id)
    analysis = row[get_field_position(f'analysis{n}', columns)]
    return analysis



    
def set_question_timestamp(user_id, n):
    store_timestamp_id(TABLE_APPLICANTS, user_id, f"start_time_q{n}")

def store_answer(user_id, n, answer):

    update_data_id(TABLE_APPLICANTS, user_id, f"a{n}", answer)

def store_analysis(user_id, n, analysis):
    
    update_data_id(TABLE_APPLICANTS, user_id, f"analysis{n}", json.dumps(analysis).replace('\'', '\'\''))


def set_answer_timestamp(user_id, n):
    store_timestamp_id(TABLE_APPLICANTS, user_id, f"end_time_q{n}")

def get_field_position(field, columns):
    for i in range(len(columns)):
        if columns[i] == field:
            return i
    return -1

