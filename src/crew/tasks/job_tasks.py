from crewai import Task


class JobTasks:
    def scrape_site(self, agent, website_url):
        return Task(
            description=f"""Scrape the BWI site {website_url}""",
            expected_output="Job desription from the website.",
            agent=agent,
        )

    def extraction_task(self, agent):
        return Task(
            description="""Extract the relevant informations from the crawled job description. Make sure to extract: Job Role, Job Level, Pre Requirements (Education, Experience), Hard Skills, Soft Skills, Responsibilities, Others.""",
            expected_output="""Extracted informations from the job description.""",
            agent=agent,
            async_execution=True,
        )
    def gap_task(self, agent):
        return Task(
            description="""Verify the requirements in the job description. Which possible other requirements are missing for the job role? Consider: Job Role, Job Level, Pre Requirements (Education, Experience), Hard Skills, Soft Skills and Responsibilities""",
            expected_output="""A list of five missing requirements from the job description.""",
            agent=agent,
            async_execution=False,
        )

    def question_task(self, agent):
        return Task(
            description="""Formulate a collection of five questions that a applicant should be able to answer.""",
            expected_output="""Formulated five questions that a applicant should be able to answer.""",
            agent=agent,
            async_execution=True,
        )

    def json_saver_task(self, agent):
        return Task(
            description="""Save the informations into a JSON file. Output all the infos into a folder called output and make sure to use job.json as file name.""",
            expected_output="""A well structured JSON file with the extracted informations. Make sure to use .json as file extension when saving the file.
            The JSON has to look exactly like this:
            {   
                "job_role": "", 
                "job_level": "", 
                "pre_requirements": {
                    "education": "", "experience": ""
                    }, 
                "hard_skills": ["", ""], 
                "soft_skills": ["", ""], 
                "responsibilities": ["", "",], 
                "others": ["", ""], 
                "questions": ["", "", "", "", ""],
                "missing_requirements": ["", "", "", "", ""]
            }""",
            agent=agent,
        )
