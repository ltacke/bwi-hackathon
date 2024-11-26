from crewai import Task


class JobTasks:
    def scrape_site(self, agent, website_url):
        return Task(
            description=f"""Scrape the BWI site {website_url}""",
            expected_output="Job desription from the website.",
            agent=agent,
        )

    def extraction_task(self, agent, job_id):
        return Task(
            description=f"""Extract the infos into a well JSON format. Output all the infos into a folder called output and name the file like: {job_id}.json. Stick to the given format.""",
            expected_output="""A well structured JSON file with the extracted informations.{"job_role": "", "job_level": "", "pre_requirements": [{"education": ""}, {"experience": ""}], "hard_skills": ["", ""], "soft_skills": ["", ""], "responsibilities": ["", "",], "others": ["", ""]}""",
            agent=agent,
        )

    def question_task(self, agent, job_id):
        return Task(
            description=f"""Formulate a collection of questions that a applicant should be able to answer. Output all the questions into a folder called output and name the file like: {job_id}.txt.""",
            expected_output="A collection of questions that a applicant should be able to answer.",
            agent=agent,
            async_execution=True,
        )
