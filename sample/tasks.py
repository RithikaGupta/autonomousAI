from crewai import Task


class Tasks():
    def app_analyzer_task(agent, prompt):
        return Task(
            description=f"""Read html content and Write Test Cases with Steps {prompt}. """,
            agent=agent,
            expected_output="Generate testcases with steps bullet points."
        )

    def app_analyzer_task(agent, prompt):
        return Task(
            description=f"""You have a strong background in software analysis and quality assurance, with extensive 
            experience in defining and managing test cases. You are familiar with various testing methodologies and 
            tools. You MUST first identify on whether the given {prompt} is a website or an API endpoint.
            You have the ability of reading/scraping websites html content. Given the input {prompt}, identify if 
            it refers to a website or an API endpoint, then write detailed test case for the give input {prompt}. 
            If the full HTML content is not available, analyze the website or the API and generate positive and 
            negative possible scenarios.""",
            agent=agent,
            expected_output="Definition of the given input, whether it is an API or a website. Testcases generations "
                            "with detailed steps listed in bullet points.",
        )

    def test_generator_task(agent, prompt):
        return Task(
            description=f"""Identify if its UI testing or API testing and then write detailed test case for the give 
            input {prompt}. """,
            agent=agent,
            expected_output='''Generate automated test cases in code-generated.py file, remove first and last line 
                            after code is added.''',
            output_file="code-generated.py"
        )

    def test_reviewer_task(agent):
        return Task(
            description=f"""Review Test cases generated and improve it by providing feedback. """,
            agent=agent,
            expected_output="Review automated test cases and provide feedback"
        )

    def test_execution_task(agent):
        return Task(
            description="""Execute the given python file using python shell and show testcase result as passed failed""",
            agent=agent,
            expected_output='Generate test case result in table with two columns, one column for test case name and '
                            'other for result. Add appropriate details with test case name and its result only based '
                            'on result.',
        )
