from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile
from PyPDF2 import PdfReader
import uvicorn

from model import job, eval

from crew.crews import job_crew, cv_crew, eval_crew

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/job_crew")
def run_job_crew(body: job):
    return job_crew.run(body.website_url, body.job_id)


@app.post("/cv_crew")
def run_cv_crew(pdf: UploadFile):
    reader = PdfReader(pdf.file)
    result = ""
    for pages in reader.pages:
        result += pages.extract_text()
    return cv_crew.run(result)


@app.post("/eval_crew")
def run_eval_crew(body: eval):
    return eval_crew.run(body.question, body.answer)
