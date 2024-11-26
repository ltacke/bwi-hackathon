from pydantic import BaseModel


class job_cew(BaseModel):
    website_url: str
    job_id: str
