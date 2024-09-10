# To install required packages:
# pip install crewai==0.22.5 streamlit==1.32.2
import streamlit as st
from crewai import Crew, Process
from langchain_openai import AzureChatOpenAI

from agents import TestAgents
from tasks import Tasks
from utils.htmlHelper import addHtmlHeader

llm = AzureChatOpenAI(openai_api_type="azure", openai_api_version="2024-02-01",
                      azure_endpoint="https://chat-fast-86510d1a.openai.azure.com",
                      openai_api_key="", deployment_name="gpt-35-turbo-1106",
                      model="gpt-35-turbo")

topic = ""

addHtmlHeader(st)
manager_agent = TestAgents.manager_agent(llm)
app_analyzer_agent = TestAgents.app_analyzer_agent(llm)
code_generator_agent = TestAgents.code_generator_agent(llm)
code_reviewer_agent = TestAgents.code_reviewer_agent(llm)
code_executor_agent = TestAgents.code_executor_agent(llm)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "What story or website testcase you want to generate and execute?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    topic = prompt

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    app_analyzer_task = Tasks.app_analyzer_task(app_analyzer_agent, topic)
    code_generate_task = Tasks.test_generator_task(code_generator_agent, topic)
    code_review_task = Tasks.test_reviewer_task(code_reviewer_agent)
    code_execute_task = Tasks.test_execution_task(code_executor_agent)

    # Create Agents
    project_crew = Crew(
        tasks=[app_analyzer_task, code_generate_task, code_review_task, code_execute_task],
        agents=[app_analyzer_agent, code_generator_agent, code_reviewer_agent, code_executor_agent],
        #manager_agent=manager_agent,
        # manager_llm=llm,
        process=Process.sequential
        #process=Process.hierarchical
    )

    final = project_crew.kickoff()

    result = f"## Here is the Final Result \n\n {final}"
    st.session_state.messages.append({"role": "assistant", "content": result})
    st.chat_message("assistant").write(result)
