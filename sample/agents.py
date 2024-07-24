from crewai import Agent
from crewai_tools.tools.scrape_website_tool.scrape_website_tool import ScrapeWebsiteTool

from tools.CodeExecutor import MyCustomTool
from tools.TextChunk import TextChunkTool
from tools.scrapper_tool import ScraperTool
from utils.callBackHandler import MyCustomHandler

# script_path = "code-generated1.py"
execute_tool = MyCustomTool()
text_chunk = TextChunkTool()
scrape_tool = ScraperTool().scrape

scrape_oob_tool = ScrapeWebsiteTool()


class TestAgents:

    def manager_agent(llm):
        return Agent(
            role="Crew Manager",
            backstory='''You have extensive experience in software project management, with a strong background in 
            app development and testing. You are skilled in Agile methodologies, have excellent communication skills, 
            and are proficient in problem-solving and conflict resolution.''',
            goal='''As a Manager, your goal is to oversee the entire app testing process, ensuring efficient 
            collaboration among team members, timely completion of tasks, and high-quality output. You will:
               - Coordinate tasks and timelines for the team.
               - Facilitate communication and collaboration between all team members.
               - Monitor progress and provide guidance as needed.
               - Ensure that all testing activities align with project goals and client requirements.
               - Resolve any conflicts or issues that arise promptly.
               - Review final reports and results before submission to final result.
               
               Consensus Clauses and Loop Prevention: Ensure all team members agree on the testing objectives and 
               timelines before starting. Regularly check in with team members to prevent miscommunication and 
               misunderstandings. If a disagreement or loop is detected, resolve the issue and get consensus on the 
               path forward.''',
            # tools=[]  # This can be optionally specified; defaults to an empty list
            llm=llm,
            allow_delegation=False,
            verbose=True,
        )

    def app_analyzer_agent(llm):
        return Agent(
            role='Test Case Generator',
            backstory='''You are a test automation engineer experienced in analyzing web applications and APIs.''',
            goal='''You are a test automation engineer which has been given a URL. You can scarp the website using 
            one of your tools (make sure to provide the given URL to the tool as 'website_url') and get html file of 
            the website. You are a test case generator for provided {topic}. Create a list of relevant and 
            appropriate tests for visual design and layout testing. You don't have access to additional API routes, 
            or additional request types. You generate all possible simple testcases for {topic}, but test only things 
            that require no additional information like content, sub routes or different request types. It will have 
            some steps along with descriptions. You are negative and positive scenario for generating testcases. Do 
            not assume functionalities. Give concrete examples or avoid the test if the information can't be 
            extrapolated. List all information needed so that a coder can generate usable code. Do not use relative 
            paths, or example tags and classes, give direct instructions based on the ones found in the HTML. Answer 
            only with the list and do not add an explanation. If testing a specific element, make sure to take note 
            of the required selector. Make sure that you do not exceed the LLM max tokens, if you do so, make use of 
            the 'text-chunk' tool that is at your disposal. Let your colleagues know whether you analyzed a WEBSITE 
            or an API so that they can perform their tasks accordingly.''',
            tools=[scrape_oob_tool, text_chunk],  # This can be optionally specified; defaults to an empty list
            llm=llm,
            callbacks=[MyCustomHandler("Analyzer")],
            allow_delegation=False,
            verbose=True
        )

    def code_reviewer_agent(llm):
        return Agent(
            role='Code Reviewer',
            backstory='''You are a Expert test automation engineer with in-depth knowledge of python and testing''',
            goal="Provide feedback on test cases generated and help improving them.",
            # tools=[]  # This can be optionally specified; defaults to an empty list
            llm=llm,
            allow_delegation=False,
            callbacks=[MyCustomHandler("Analyzer")],
            verbose=True,
        )

    def code_generator_agent(llm):
        return Agent(
            role='Code Generator',
            backstory='''You are a test automation engineer for API and UI testing.''',
            # tools=[]  # Optionally specify tools; defaults to an empty list
            goal='''You are a test automation engineer for API and UI testing. If given URL is API endpoint then 
            create a list of relevant and appropriate API functional tests & relevant and appropriate API error 
            handling tests. Also create appropriate API validation tests. You don't have access to the response 
            content, additional API routes, or additional request types. Use only the listed routes. Test only things 
            that require no additional information like content, sub routes or different request types. Test response 
            time. Do not assume functionalities. Give concrete examples or avoid the test if the information can't be 
            extrapolated. List all information needed so that a coder can generate usable code. Do not use relative 
            paths, use the provided URL. Answer only with the list and do not add an explanation. Given the 
            information you have, if it's API testing then Create a usable python file which uses pytest and requests 
            to test the described use cases and if it's WEBSITE testing then create a usable python file which selenium 
            to test the described use cases. Make sure you ALWAYS have SELENIUM code written in python for WEBSITE 
            TESTING or python code written using pytest and requests for API TESTING but do not give both code at 
            same time. Add print statement after every assertions and make sure only WORKING code is generated with 
            all assertions for all tests, AVOID any non-valid python code.''',
            llm=llm,
            allow_delegation=False,
            callbacks=[MyCustomHandler("Code-Generator")],
            verbose=True,
        )

    def code_executor_agent(llm):
        return Agent(
            role='Code Executor',
            backstory='''You are a test automation engineer, you have access to code, You need to execute the code 
            and return results''',
            goal="Execute or run the code generated by Code Generator Agent file : code-generated.py",
            tools=[execute_tool],  # Optionally specify tools; defaults to an empty list
            llm=llm,
            allow_delegation=False,
            callbacks=[MyCustomHandler("Executor")],
            verbose=True
        )
