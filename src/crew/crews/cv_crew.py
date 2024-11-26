import os
from dotenv import load_dotenv

from crewai import Crew, LLM
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from src.watsonx.watson_ai_client import WatsonXClient

from crew.tasks.cv_tasks import CvTasks
from crew.agents.cv_agents import CvAgents


load_dotenv(override=True)


def run(
    context,
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

    crew = Crew(
        agents=[],
        tasks=[],
    )
    result = crew.kickoff()

    return result
