from crewai import Agent


class EvalAgents:
    def agent(self, llm):
        return Agent(
            llm=llm,
            role="Role Desription",
            goal="Whats the goal of the agent",
            tools=[],
            backstory="Backstory of the agent",
            verbose=True,
            max_iter=5,
        )
