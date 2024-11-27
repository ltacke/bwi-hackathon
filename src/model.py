from pydantic import BaseModel


class job(BaseModel):
    website_url: str
    job_id: str


class eval(BaseModel):
    question: str
    answer: str
