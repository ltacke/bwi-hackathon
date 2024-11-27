import os
from dotenv import load_dotenv

from crewai import Crew, LLM
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from watsonx.watson_ai_client import WatsonXClient

from crew.tasks.eval_tasks import EvalTasks
from crew.agents.eval_agents import EvalAgents


load_dotenv(override=True)


def run(question, answer):
    tasks = EvalTasks()
    agents = EvalAgents()

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

    bullet_point_agent = agents.bullet_point_summary_agent(llm)
    open_gaps_agent = agents.open_gaps_agent(llm)
    eval_agent = agents.eval_agent(llm)
    followup_questions_agent = agents.followup_questions_agent(llm)
    json_saver_agent = agents.json_saver_agent(llm)

    bullet_point_task = tasks.bullet_point_summary(bullet_point_agent, answer)
    open_gaps_task = tasks.open_gaps(open_gaps_agent, question, answer)
    fiteval_task = tasks.fit_eval(eval_agent, question, answer)
    followup_questions_task = tasks.followup_questions(followup_questions_agent, answer)
    json_saver_task = tasks.json_saver_task(json_saver_agent)

    followup_questions_task.context = [bullet_point_task, open_gaps_task]

    json_saver_task.context = [
        bullet_point_task,
        open_gaps_task,
        fiteval_task,
        followup_questions_task,
    ]

    crew = Crew(
        agents=[
            bullet_point_agent,
            open_gaps_agent,
            eval_agent,
            followup_questions_agent,
            json_saver_agent,
        ],
        tasks=[
            bullet_point_task,
            open_gaps_task,
            fiteval_task,
            followup_questions_task,
            json_saver_task,
        ],
    )
    result = crew.kickoff()

    return result
