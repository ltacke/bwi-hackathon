from dotenv import load_dotenv
from crewai import Crew
from db.db_tasks import get_job_description
from watsonx.llm import standard_llm

from crew.tasks.cv_tasks import CvTasks
from crew.agents.cv_agents import CvAgents


load_dotenv(override=True)
FOLDER = "output"

def run(
    cv,
    job_id
):
    tasks = CvTasks()
    agents = CvAgents()

    llm = standard_llm()

    job_description = get_job_description(job_id)

    skills_agent = agents.skills_agent(llm)
    experience_agent = agents.experience_agent(llm)
    gap_agent = agents.gap_identifier_agent(llm)
    question_agent = agents.question_agent(llm)
    json_saver_agent = agents.json_saver_agent(llm)

    skills_task = tasks.extract_skills(skills_agent, cv)
    experience_task = tasks.extract_experience(experience_agent, cv)
    gap_task = tasks.identify_gaps(gap_agent, job_description)
    question_task = tasks.question_task(question_agent)
    json_saver_task = tasks.json_saver_task(json_saver_agent)

    gap_task.context = [experience_task, skills_task]
    question_task.context = [experience_task, skills_task, gap_task]
    json_saver_task.context = [question_task, experience_task, skills_task, gap_task]

    crew = Crew(
        agents=[
            skills_agent,
            experience_agent,
            gap_agent,
            question_agent,
            json_saver_agent,
        ],
        tasks=[skills_task, experience_task, gap_task, question_task, json_saver_task],
        verbose=True,
    )
    result = crew.kickoff()

    return result
