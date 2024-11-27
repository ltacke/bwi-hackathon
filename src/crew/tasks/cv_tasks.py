from crewai import Task


class CvTasks:
    def extract_skills(self, agent, cv):
        return Task(
            description=f"""Extract skills from the CV.
            {cv} 
            Split them into soft skills and hard skills.""",
            expected_output="Soft skills and hard skills extracted from the given CV.",
            agent=agent,
            async_execution=True,
        )

    def extract_experience(self, agent, cv):
        return Task(
            description=f"""Extract experience from the CV.
            {cv}
            Split them into education and work experience.""",
            expected_output="Education and work experience extracted from the CV.",
            agent=agent,
            async_execution=True,
        )

    def identify_gaps(self, agent, job_description):
        return Task(
            description=f"""Identify gaps in the applicants extracted skills and experience in comparison to the requirements from the job_description:
            {job_description}""",
            expected_output="Potential Gaps identified in the applicants skills and experience.",
            agent=agent,
        )

    def question_task(self, agent):
        return Task(
            description="""Formulate a collection of questions based on the job description, the identified gaps and the extracted skills and experience. 
            Find questions that proof skills and experience of the applicant, qualify or disqualify the already identified gaps.""",
            expected_output="""A collection of five questions that a applicant should be able to answer.""",
            agent=agent,
        )

    def json_saver_task(self, agent):
        return Task(
            description="""Save the informations into a JSON file. Output all the infos into a folder called output and make sure to use personal-questions.json as file name.""",
            expected_output="""A well structured JSON file with the extracted informations. Make sure to use .json as file extension when saving the file.
            The JSON has to look like this:
            {   
                "questions": ["", "", "", "", ""] 
            }
            """,
            agent=agent,
        )
