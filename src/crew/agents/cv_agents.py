from crewai import Agent
from crewai_tools import FileWriterTool


class CvAgents:
    def skills_agent(self, llm):
        return Agent(
            llm=llm,
            role="Skills Extractor Agent",
            goal="Extract all skills from the resume",
            tools=[],
            backstory="You are a Skills Extractor Agent. You are an expert in extracting skills from resumes.",
            verbose=True,
            max_iter=2,
        )

    def experience_agent(self, llm):
        return Agent(
            llm=llm,
            role="Experience Extractor Agent",
            goal="Extract all experiences from the resume including education, work experience, and projects",
            tools=[],
            backstory="You are an Experience Extractor Agent. You are an expert in extracting experiences from resumes.",
            verbose=True,
            max_iter=2,
        )

    def gap_identifier_agent(self, llm):
        return Agent(
            llm=llm,
            role="Gap Identifier Agent",
            goal="Identify gaps in the resume based on the extracted skills and experiences",
            backstory="You are a Gap Identifier Agent. You are an expert in identifying gaps in resumes.",
            verbose=True,
            max_iter=2,
        )

    def question_agent(self, llm):
        return Agent(
            llm=llm,
            role="Personalized Question Agent",
            goal="""Formulate a collection of questions based on the job description, the identified gaps and the extracted skills and experience. Identify the five most relevant questions.""",
            backstory="You are a Personalized Question Agent. You are an expert in formulating personalized questions based on the job description, the identified gaps, and the extracted skills and experiences.",
            verbose=True,
            max_iter=2,
        )

    def json_saver_agent(self, llm):
        return Agent(
            llm=llm,
            role="JSON Saver Agent",
            goal="Save the extracted informations into a JSON file called application.json.",
            backstory="You are a JSON Saver Agent. You are an expert in saving informations into a JSON file.",
            tools=[FileWriterTool()],
            verbose=True,
            max_iter=3,
        )
