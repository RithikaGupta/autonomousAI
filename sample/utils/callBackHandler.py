from typing import Any, Dict

import streamlit as st
from langchain_core.callbacks import BaseCallbackHandler

avators = {"Writer": "https://cdn-icons-png.flaticon.com/512/320/320336.png",
           "Reviewer": "https://cdn-icons-png.freepik.com/512/9408/9408201.png"}


class MyCustomHandler(BaseCallbackHandler):
    def __init__(self, agent_name: str) -> None:
        print(f"__init__ started")
        self.agent_name = agent_name
        print(f"__init__ finished")

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> None:
        print(f"on_chain_start started")
        print(self.agent_name)
        """Print out that we are entering a chain."""
        st.session_state.messages.append({"role": "assistant", "content": inputs['input']})
        st.chat_message("assistant").write(inputs['input'])
        print(f"on_chain_start finished")

    # def on_chain_end(self, outputs) -> None:
    #     print(f"on_chain_end started")
    #     CodeExecutorTool.run();
    # print(self.agent_name)
    # if(self.agent_name == "Executor"):
    #     st.session_state.messages.append({"role": self.agent_name, "content": "code-generated.py start executing for validating testcases"})
    #     st.chat_message(self.agent_name, avatar=avators[self.agent_name]).write("code-generated.py start executing for validating testcases...")
    #     CodeExecutorTool.run()
    #     #subprocess.call("code-generated.py", shell=True)
    # st.session_state.messages.append({"role": self.agent_name, "content": outputs['output']})
    # st.chat_message(self.agent_name, avatar=avators[self.agent_name]).write(outputs['output'])
    # print(f"on_chain_end finished")
