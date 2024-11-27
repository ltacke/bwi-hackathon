from crewai import Task


class EvalTasks:
    def bullet_point_summary(self, agent, answer):
        return Task(
            description=f"""
            Summarize a given answer text into a maximum of 4 bullet points. Be precice and only include the most important informations as short as possible.
            The answer was: '{answer}'""",
            expected_output="A precice list of 4 bullet points.",
            agent=agent,
            async_execution=True,
        )

    def open_gaps(self, agent, question, answer):
        return Task(
            description=f"""
            Based on the given question and answer, identify potential gaps in the answer. Be precice and formulate your answer into a maximum of 2 bullet points. Think about your answer and keep in mind that there don't have to be gaps necessarily. 
            The question was: '{question}'
            The answer was: '{answer}'""",
            expected_output="A precice list of max. 2 bullet points.",
            agent=agent,
            async_execution=True,
        )

    def fit_eval(self, agent, question, answer):
        return Task(
            description=f"""
            Evaluate the answer on a scale of 0 to 10 based on the question and give a reason for the evaluation. Be precice and give a detailed explanation for your evaluation.
            The question was: {question}
            The answer was: {answer}""",
            expected_output="A number between 0 and 10 and a detailed explanation.",
            agent=agent,
            async_execution=True,
        )

    def followup_questions(self, agent, answer):
        return Task(
            description=f"""
            Generate 2 follow-up questions based on the given answer. Be precice and formulate your questions in a way that they are related to the answer and the gaps you identified.
            The follow-up question can be used to reassure details from the given answer or to close potentially open gaps.
            The answer was: {answer}""",
            expected_output="Two follow-up questions.",
            agent=agent,
        )

    def json_saver_task(self, agent):
        return Task(
            description="""Save the informations into a JSON file. Output all the infos into a folder called output and make sure to use eval.json as file name.""",
            expected_output="""A well structured JSON file with the extracted informations. Make sure to use .json as file extension when saving the file.
            The JSON has to look like this:
            {   
                "summary": ["", "", "", ""], 
                "gaps": ["", ""], 
                "eval": { 
                    "score": <number>, 
                    "reason": ""
                    }, 
                "questions": ["", ""] 
            }""",
            agent=agent,
        )
