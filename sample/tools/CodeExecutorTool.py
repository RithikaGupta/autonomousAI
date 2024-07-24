import os
import subprocess
import streamlit as st

# class CodeExecutorTool():
#     def run():
#         """This tool is used to execute a Python file, it has the Python file name as an argument 'file_name' and it returns the runtime execution result."""

#         dir = os.path.dirname(__file__)
#         parent_directory = os.path.abspath(os.path.join(dir, '..'))
#         filename = os.path.join(parent_directory, 'code-generated1.py')
#         print(filename)
#         process = subprocess.run(['python3', filename])
#         if process.returncode == 0:
#             return process
#         else:
#             return "[Execution finished] - The script encountered an error. Check"

from langchain.tools import tool


@tool("ExecuteTestCases")
def _run(argument: str) -> str:
    """Tool description for clarity."""
    print(f"running the test cases")
    # Your tool's logic here
    current_dir = os.path.dirname(__file__)
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
    temp_script_path = filename + '.temp.py'
    with open(temp_script_path, 'w') as temp_file:
        temp_file.writelines(modified_lines)
    print(f"modified lines")
    print(modified_lines)
    process = subprocess.run(['python3', filename], capture_output=True, text=True)
    if process.returncode == 0:
        st.session_state.messages.append({"role": "assistant", "content": process.stdout})
        return process.stdout
    else:
        return "[Execution finished] - The script encountered an error. Check"
