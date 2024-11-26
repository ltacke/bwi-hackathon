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
            goal="Read the scraped job description and formulate a collection of questions that a applicant should be able to answer. Identify the five most relevant questions your questions into a JSON file, into the folder 'output' and name the file.",
            tools=[FileWriterTool()],
            backstory="You are a expert in formulating questions based on a job description.",
            verbose=True,
            max_iter=2,
        )

    def extraction_agent(self, llm):
        return Agent(
            llm=llm,
            role="Expert Extraction Agent",
            goal="Extract the key job informations (job_role, job_level, pre_requirements, hard_skills, soft_skills, responsibilities, others, possible questions) from the given job description. Extract the informations into a structured text format and stick to the given key values.",
            tools=[FileWriterTool()],
            backstory="You are a expert in extracting key job informations into a structured text format.",
            verbose=True,
            max_iter=2,
        )
