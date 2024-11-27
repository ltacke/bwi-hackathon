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

    def question_task(self, agent, applicant_id, job_description):
        return Task(
            description=f"""Formulate a collection of questions based on the job description, the identified gaps and the extracted skills and experience. 
            Find questions that proof skills and experience of the applicant, qualify or disqualify the already identified gaps.
            Output all the questions into a folder called output and name the file like: {applicant_id}-personal-questions.json.
            The job description is: {job_description}""",
            expected_output="""A well structured JSON file with the collection of five questions that a applicant should be able to answer. {"questions": ["", "", "", "", ""]}""",
            agent=agent,
        )
