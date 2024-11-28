from crewai import Agent
from crew.tools import ScrapeBWI
from crewai_tools import FileWriterTool


class JobAgents:
    def scraping_agent(self, llm):
        return Agent(
            llm=llm,
            role="Expert Scraping Agent",
            goal="Scrape the website of the job posting and formulate a detailed job description with all relevant informations that you can find",
            tools=[ScrapeBWI()],
            backstory="You are a expert in scraping a job website and extracting all the relevant informations from the job posting.",
            verbose=True,
            max_iter=2,
        )

    def question_agent(self, llm):
        return Agent(
            llm=llm,
            role="Expert Question Agent",
            goal="""Read the scraped job description and formulate a collection of questions that a applicant should be able to answer. Identify the five most relevant questions.""",
            backstory="You are a expert in formulating questions based on a job description.",
            max_iter=2,
        )

    def extraction_agent(self, llm):
        return Agent(
            llm=llm,
            role="Expert Extraction Agent",
            goal="""Extract the key job informations from the given job description. Make sure to extract: Job Role, Job Level, Pre Requirements (Education, Experience), Hard Skills, Soft Skills, Responsibilities, Others.""",
            backstory="You are a expert in extracting key informations out of a job posting.",
            max_iter=3,
        )

    def gap_agent(self, llm):
        return Agent(
            llm=llm,
            role="Expert Gap Identification Agent",
            goal="""Extract missing requirements that are usually relevant for the job not mentioned in the given job description. Consider: Job Role, Job Level, Pre Requirements (Education, Experience), Hard Skills, Soft Skills and Responsibilities. Identify the most significant gaps.""",
            backstory="You are a expert for jobs that can identify missing requirements in a job posting.",
            max_iter=3,
        )

    def json_saver_agent(self, llm):
        return Agent(
            llm=llm,
            role="JSON Saver Agent",
            goal="Save the extracted informations into a JSON file called job.json.",
            backstory="You are a JSON Saver Agent. You are an expert in saving informations into a JSON file.",
            tools=[FileWriterTool()],
            verbose=True,
            max_iter=3,
        )
