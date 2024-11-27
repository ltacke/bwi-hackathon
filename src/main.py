from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from PyPDF2 import PdfReader
import uvicorn

from model import job_cew

from crew.crews import job_crew, cv_crew

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/job_crew")
def run_job_crew(body: job_cew):
    return job_crew.run(body.website_url, body.job_id)


@app.post("/cv_crew")
def run_cv_crew(cv: UploadFile):
    reader = PdfReader(cv.file)
    result = ""
    for pages in reader.pages:
        result += pages.extract_text()
    return cv_crew.run(result)
