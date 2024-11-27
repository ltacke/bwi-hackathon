from crewai import Agent
from crewai_tools import FileWriterTool


class EvalAgents:
    def bullet_point_summary_agent(self, llm):
        return Agent(
            llm=llm,
            role="Bullet Point Summary Agent",
            goal="Summarize a given answer text into a maximum of 4 bullet points.",
            backstory="You are a Bullet Point Summary Agent. You are an expert in summarizing text into bullet points.",
            max_iter=3,
        )

    def open_gaps_agent(self, llm):
        return Agent(
            llm=llm,
            role="Gap Identifier Agent",
            goal="Identify gaps in the answer based on the question",
            backstory="You are a Gap Identifier Agent. You are an expert in identifying gaps in answers.",
            max_iter=3,
        )

    def eval_agent(self, llm):
        return Agent(
            llm=llm,
            role="Evaluator Agent",
            goal="Evaluate the answer on a scale of 0 to 10 based on the question and give a reason for the evaluation",
            backstory="You are an Evaluator Agent. You are an expert in evaluating answers.",
            max_iter=3,
        )

    def followup_questions_agent(self, llm):
        return Agent(
            llm=llm,
            role="Follow-up Questions Agent",
            goal="Generate 2 follow-up questions based on the answer and to close the gaps",
            backstory="You are a Follow-up Questions Agent. You are an expert in generating follow-up questions.",
            max_iter=3,
        )

    def json_saver_agent(self, llm):
        return Agent(
            llm=llm,
            role="JSON Saver Agent",
            goal="Save the extracted informations into a JSON file called eval.json.",
            backstory="You are a JSON Saver Agent. You are an expert in saving informations into a JSON file.",
            tools=[FileWriterTool()],
            verbose=True,
            max_iter=3,
        )
