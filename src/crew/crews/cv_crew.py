import os
import json
from dotenv import load_dotenv

from crewai import Crew, LLM
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from src.watsonx.watson_ai_client import WatsonXClient

from crew.tasks.cv_tasks import CvTasks
from crew.agents.cv_agents import CvAgents


load_dotenv(override=True)


def run(
    cv,
):
    tasks = CvTasks()
    agents = CvAgents()

    API_KEY = os.environ["WAI_API_KEY"]
    URL = os.environ["WAI_URL"]
    PROJECT_ID = os.environ["WAI_PROJECT_ID"]
    os.environ["WX_URL"] = URL
    os.environ["WX_TOKEN"] = WatsonXClient.get_access_token(API_KEY)

    parameters = {
        GenParams.TOP_K: 1,
        GenParams.TOP_P: 0,
        GenParams.RANDOM_SEED: 42,
        GenParams.REPETITION_PENALTY: 1.05,
        GenParams.MAX_NEW_TOKENS: 600,
    }

    llm = LLM(
        model="watsonx/meta-llama/llama-3-70b-instruct",
        base_url=URL,
        project_id=PROJECT_ID,
        params=parameters,
    )

    with open("output/test-description.json", "r") as f:
        job_description = json.load(f)
        print(job_description)

    skills_agent = agents.skills_agent(llm)
    experience_agent = agents.experience_agent(llm)
    gap_agent = agents.gap_identifier_agent(llm)
    question_agent = agents.question_agent(llm)

    skills_task = tasks.extract_skills(skills_agent, cv)
    experience_task = tasks.extract_experience(experience_agent, cv)
    gap_task = tasks.identify_gaps(gap_agent, job_description)
    question_task = tasks.question_task(question_agent, 1342, job_description)

    gap_task.context = [experience_task, skills_task]
    question_task.context = [experience_task, skills_task, gap_task]

    crew = Crew(
        agents=[skills_agent, experience_agent, gap_agent, question_agent],
        tasks=[skills_task, experience_task, gap_task, question_task],
        verbose=True,
    )
    result = crew.kickoff()

    return result
