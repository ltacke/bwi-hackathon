import json
from typing import Optional
from fastapi import FastAPI, UploadFile, BackgroundTasks, Form
from PyPDF2 import PdfReader

from db.db_tasks import get_applicant_description, get_applicants_by_job_id, retrieve_analyses, retrieve_analysis, retrieve_answer, retrieve_applicants, retrieve_applicants_for_manager, retrieve_question, set_answer_timestamp, set_question_timestamp, store_analysis, store_answer, store_application, store_flag, store_job
from model import job, eval, save_answer_body

from crew.crews import job_crew, cv_crew, eval_crew

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/job_crew")
def run_job_crew(body: job):
    result = job_crew.run(body.website_url, body.job_id)

    store_job(body.job_id, body.website_url, json.loads(result.raw))
   
    return result


@app.post("/cv_crew")
def run_cv_crew(
    cv: UploadFile, 
    name: str = Form(),
    email: str = Form(),
    phone: str = Form(),
    birthdate: str = Form(),
    job_id: str= Form()
    ):
    reader = PdfReader(cv.file)
    result = ""
    for pages in reader.pages:
        result += pages.extract_text()

    result = cv_crew.run(result, job_id)

    store_application(name, email, phone, birthdate, job_id, json.loads(result.raw))

    return result


@app.post("/eval_crew")
def run_eval_crew(body: eval):
    result = eval_crew.run(body.question, body.answer)
    
    return result


@app.get("/get_question")
def get_question(user_id: str, n: int):
    # get question
    question = retrieve_question(user_id, n)

    # set timestamp
    set_question_timestamp(user_id, n)
    return question



@app.post("/save_answer")
def save_answer(body: save_answer_body, background_tasks: BackgroundTasks):
    store_answer(body.user_id, body.n, body.answer)
    set_answer_timestamp(body.user_id, body.n)
    background_tasks.add_task(analyze_background, body.user_id, body.n)

@app.get("/get_analysis")
def get_analysis(user_id: str, n: int):
    # get question
    question = retrieve_question(user_id, n)
    answer = retrieve_answer(user_id, n)
    analysis = retrieve_analysis(user_id, n)
    analysis['question'] = question
    analysis['answer'] = answer
    return analysis


@app.get("/get_all_analyses")
def get_analysis(user_id: str):
    # get question
    analyses = retrieve_analyses(user_id)
    return analyses


@app.get("/get_applicants_for_job")
def get_applicants_for_job(job_id: str):
   return get_applicants_by_job_id(job_id)

@app.get("/get_applicants")
def get_applicants(include_job_title:bool):
   return retrieve_applicants(include_job_title)


@app.get("/get_applicants_for_manager")
def get_applicants_for_manager():
   return retrieve_applicants_for_manager()


@app.get("/get_applicant_profile")
def get_applicant_profile(user_id: str):
   return get_applicant_description(user_id)


@app.post("/set_applicant_flag")
def set_applicant_flag(user_id, flag):
   return store_flag(user_id, flag)

def analyze_background(user_id, n):
    q = retrieve_question(user_id, n)
    a = retrieve_answer(user_id, n)
    
    result = eval_crew.run(q, a)
    
    store_analysis(user_id, n, json.loads(result.raw))
    return(result.raw)
    