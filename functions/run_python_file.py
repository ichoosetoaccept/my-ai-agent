import os
import subprocess

from openai.types.chat import ChatCompletionFunctionToolParam


def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        # build absolute working dir
        absolute_path_working_dir = os.path.abspath(working_directory)

        # build target_file_path
        target_file_path = os.path.normpath(os.path.join(absolute_path_working_dir, file_path))

        # Is target file within working dir?
        valid_target_file = os.path.commonpath([absolute_path_working_dir, target_file_path]) == absolute_path_working_dir

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["uv", "run", target_file_path]

        # If any additional args were provided, add them to the command list
        if args:
            command.extend(args)

        completed_process = subprocess.run(args=command, cwd=absolute_path_working_dir, capture_output=True, text=True, timeout=30, check=False)

        output_string: list[str] = []

        if completed_process.returncode != 0:
            output_string.append(f"Process exited with code {completed_process.returncode}")
        if not completed_process.stdout and not completed_process.stderr:
            output_string.append("No output produced")
        else:
            if completed_process.stdout:
                output_string.append(f"STDOUT:\n{completed_process.stdout}")
            if completed_process.stderr:
                output_string.append(f"STDERR:\n{completed_process.stderr}")

        return "\n".join(output_string)

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file: ChatCompletionFunctionToolParam = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs or executes a Python file with the Python interpreter and returns its stdout and stderr. Use this whenever the user asks to run, execute, or launch a Python script.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "An optional list of arguments to be passed when executing the Python code",
                },
            },
            "required": ["file_path"],
        },
    },
}
