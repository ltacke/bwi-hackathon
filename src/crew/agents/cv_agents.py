from crewai import Agent


class CvAgents:
    def skills_agent(self, llm):
        return Agent(
            llm=llm,
            role="Skills Extractor Agent",
            goal="Extract all skills from the resume",
            tools=[],
            backstory="Backstory of the agent",
            verbose=True,
            max_iter=5,
        )
