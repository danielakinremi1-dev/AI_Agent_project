import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        absolute_directory = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(os.path.join(absolute_directory, file_path))
        valid_file_path = os.path.commonpath([absolute_directory, absolute_file_path]) == absolute_directory

        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", absolute_file_path] + (args if args else [])
        process = subprocess.run(command, text=True, capture_output=True)

        output_string = ""
        if process.returncode != 0:
            output_string += f'Process exited with return code {process.returncode}'
        if process.stderr == None and process.stdout == None:
            output_string += f'No output produced'
        else:
            output_string += f'STDOUT:{process.stdout}\nSTDERR:{process.stderr}'
        
        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"