import json
from fastapi import FastAPI, UploadFile, File
from PyPDF2 import PdfReader
import uvicorn

from db.db_tasks import store_application, store_job
from model import job, eval

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
def run_cv_crew(cv: UploadFile, job_id: str):
    reader = PdfReader(cv.file)
    result = ""
    for pages in reader.pages:
        result += pages.extract_text()
    

    result = cv_crew.run(result, job_id)

    store_application(cv, job_id, json.loads(result.raw))

    return result


@app.post("/eval_crew")
def run_eval_crew(body: eval):
    return eval_crew.run(body.question, body.answer)


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="localhost", port=8000, reload=True)
