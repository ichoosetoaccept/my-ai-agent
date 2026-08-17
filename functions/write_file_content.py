import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        # build absolute working dir
        absolute_path_working_dir = os.path.abspath(working_directory)

        # build target_file_path
        target_file_path = os.path.normpath(os.path.join(absolute_path_working_dir, file_path))

        # Is target file within working dir?
        valid_target_file = os.path.commonpath([absolute_path_working_dir, target_file_path]) == absolute_path_working_dir

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        # If target is a folder instead of a file
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Create missing parent directories, if any
        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        with open(target_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
