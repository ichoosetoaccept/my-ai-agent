import os

from openai.types.chat import ChatCompletionFunctionToolParam

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        # build absolute working dir
        absolute_path_working_dir = os.path.abspath(working_directory)

        # build target_dir
        target_file = os.path.normpath(os.path.join(absolute_path_working_dir, file_path))

        # Is target dir within working dir?
        valid_target_file = os.path.commonpath([absolute_path_working_dir, target_file]) == absolute_path_working_dir

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        # If directory is not a dir
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file) as f:
            content = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {e}"

schema_get_file_content: ChatCompletionFunctionToolParam = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Gets content of a file in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}
