from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from langchain_openai import AzureChatOpenAI

from customTools import CodeExecutorTool

llm = AzureChatOpenAI(openai_api_type="azure", openai_api_version="2024-02-01",
                      azure_endpoint="https://chat-fast-86510d1a.openai.azure.com",
                      openai_api_key="c6e872e392a2457a9783efd73bf1b8ff", deployment_name="gpt-35-turbo-1106",
                      model="gpt-35-turbo")

topic = ""


@CrewBase
class TestingCrew:
    """TestingCrew crew"""
    agents_config = "./config/agents.yaml"
    tasks_config = "./config/tasks.yaml"

    @agent
    def analyzer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['analyzer'],
            llm=llm
        )

    @agent
    def code_writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['code_writer'],
            llm=llm
        )

    @agent
    def executor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['executor'],
            tools=[CodeExecutorTool.python_code_executor],
            llm=llm
        )

    @task
    def read_html_task(self) -> Task:
        return Task(
            config=self.tasks_config['read_html'],
            agent=self.analyzer_agent()
        )

    @task
    def write_python_code_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_python_code'],
            agent=self.code_writer_agent()
        )

    @task
    def execute_python_code_task(self) -> Task:
        return Task(
            config=self.tasks_config['execute_python_code'],
            agent=self.executor_agent()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the testing crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=2
        )
