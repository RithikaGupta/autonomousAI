# To install required packages:
# pip install crewai==0.22.5 streamlit==1.32.2
import streamlit as st
from langchain_openai import AzureChatOpenAI
from testingCrew.crew import TestingCrew

llm = AzureChatOpenAI(openai_api_type="azure", openai_api_version="2024-02-01",
                      azure_endpoint="https://chat-fast-86510d1a.openai.azure.com",
                      openai_api_key="c6e872e392a2457a9783efd73bf1b8ff", deployment_name="gpt-35-turbo-1106",
                      model="gpt-35-turbo")

topic = ""


avators = {"Writer": "https://cdn-icons-png.flaticon.com/512/320/320336.png",
           "Reviewer": "https://cdn-icons-png.freepik.com/512/9408/9408201.png"}


st.title("💬 AI Autonomous multi agent based testing...")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "What story or website testcase you want to generate and execute ?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    topic = prompt

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    final = TestingCrew().crew().kickoff()

    result = f"## Here is the Final Result \n\n {final}"
    st.session_state.messages.append({"role": "assistant", "content": result})
    st.chat_message("assistant").write(result)
