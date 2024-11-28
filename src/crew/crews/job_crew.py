import os
from dotenv import load_dotenv

from crewai import Crew, LLM
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from watsonx.watson_ai_client import WatsonXClient

from crew.tasks.job_tasks import JobTasks
from crew.agents.job_agents import JobAgents



load_dotenv(override=True)


def run(
    url: str,
    job_id: str,
):
    tasks = JobTasks()
    agents = JobAgents()

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
        GenParams.MAX_NEW_TOKENS: 1500,
    }

    llm = LLM(
        model="watsonx/meta-llama/llama-3-70b-instruct",
        base_url=URL,
        project_id=PROJECT_ID,
        params=parameters,
    )
    sraping_agent = agents.scraping_agent(llm)
    question_agent = agents.question_agent(llm)
    extraction_agent = agents.extraction_agent(llm)
    gap_agent = agents.gap_agent(llm)
    json_agent = agents.json_saver_agent(llm)

    scraping_task = tasks.scrape_site(sraping_agent, url)
    question_task = tasks.question_task(question_agent)
    extraction_task = tasks.extraction_task(extraction_agent)
    gap_task = tasks.gap_task(gap_agent)
    json_task = tasks.json_saver_task(json_agent)

    question_task.context = [scraping_task]
    extraction_task.context = [scraping_task]
    gap_task.context = [extraction_task]
    json_task.context = [question_task, extraction_task, gap_task]

    job_crew = Crew(
        agents=[sraping_agent, extraction_agent, question_agent, gap_agent, json_agent],
        tasks=[scraping_task, extraction_task, question_task, gap_task, json_task],
        verbose=True,
    )

    return(job_crew.kickoff())
    
