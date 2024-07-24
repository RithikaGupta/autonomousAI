import os
from crewai_tools import tool
import subprocess
from datetime import datetime


@tool("Python code executor")
def python_code_executor(file_name):
    """This tool is used to execute a Python file, it has the Python file name as an argument 'file_name' and it returns the runtime execution result."""

    now = datetime.now()

    now_str = now.strftime("%d_%m_%Y_%H_%M_%S")

    output_file = os.getenv("CODE_EXECUTOR_OUTPUT_DIRECTORY") + str.replace(file_name, "\"", "").replace(".py", "") + "_" + now_str + ".txt"

    file_path = os.getenv("CODE_EXECUTOR_FILES_DIRECTORY") + str.replace(file_name, "\"", "")

    if file_name.endswith(".py"):

        # Run the Python file and capture the output
        #with open(output_file, 'w') as file:
            #process = subprocess.run(['python', file_path], stdout=file, stderr=subprocess.STDOUT)
        process = subprocess.run(['python', file_path], stderr=subprocess.STDOUT)

        # Check the return code to ensure the script ran successfully
        if process.returncode == 0:
            return "[Execution finished] - The script " + file_path + " ran successfully. Output is saved in " + output_file + "."
        else:
            return "[Execution finished] - The script " + file_path + " encountered an error. Check  " + output_file + "for details."
