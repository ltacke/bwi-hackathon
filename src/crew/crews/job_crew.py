from dotenv import load_dotenv

from crewai import Crew
from watsonx.llm import standard_llm

from crew.tasks.job_tasks import JobTasks
from crew.agents.job_agents import JobAgents



load_dotenv(override=True)


def run(
    url: str,
    job_id: str,
):
    tasks = JobTasks()
    agents = JobAgents()

    llm = standard_llm()

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
    
