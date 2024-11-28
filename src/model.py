from pydantic import BaseModel


class job(BaseModel):
    website_url: str
    job_id: str

class cvrequest(BaseModel):
    user_id: str
    job_id: str

class eval(BaseModel):
    question: str
    answer: str

class save_answer_body(BaseModel):
    user_id: str
    n: int
    answer: str