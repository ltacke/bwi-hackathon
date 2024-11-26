from crewai import Task


class QuizTasks:
    def task(self, agent, context):
        return Task(
            description=f"""Description {context}""",
            expected_output="Expected output of the task.",
            agent=agent,
        )
