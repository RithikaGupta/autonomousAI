from crewai_tools import BaseTool
import os
import subprocess

import streamlit as st


class MyCustomTool(BaseTool):
    name: str = "Code Executor Tool"
    description: str = "This tool is used to execute a Python file, it returns the runtime execution output."

    def _run(self, argument: str) -> str:
        # Your tool's logic here
        current_dir = os.path.dirname(__file__)
        print(current_dir)
        parent_directory = os.path.abspath(os.path.join(current_dir, '..'))
        filename = os.path.join(parent_directory, 'code-generated.py')
        print(filename)
        with open(filename, 'r') as file:
            lines = file.readlines()

        if len(lines) > 2:
            # Remove the first and last lines
            modified_lines = lines[1:-1]
        else:
            modified_lines = []

        # Write the modified content to a temporary file
        temp_script_path = 'api-test.py'
        with open(temp_script_path, 'w') as temp_file:
            temp_file.writelines(modified_lines)

        # print(f"modified lines")
        print(temp_script_path)
        process = subprocess.run(['pytest', temp_script_path], capture_output=True, text=True)

        print(process)

        st.session_state.messages.append({"role": "assistant", "content": process.stdout})
        return process.stdout
