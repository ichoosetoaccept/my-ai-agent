import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        # build absolute working dir
        absolute_path_working_dir = os.path.abspath(working_directory)

        # build target_dir
        target_dir = os.path.normpath(os.path.join(absolute_path_working_dir, directory))

        # Is target dir within working dir?
        valid_target_dir = os.path.commonpath([absolute_path_working_dir, target_dir]) == absolute_path_working_dir

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        # If directory is not a dir
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        return f'Success: "{directory}" is within the working directory'

    except Exception as e:
        return f"Error: {e}"
