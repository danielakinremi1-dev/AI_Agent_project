import os

def write_file(working_directory: str, file_path: str, content: str) -> str:

    try:
        absolute_directory = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(os.path.join(absolute_directory, file_path))
        valid_file_path = os.path.commonpath([absolute_directory, absolute_file_path]) == absolute_directory

        if not valid_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(absolute_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(absolute_file_path), exist_ok=True)

        with open(absolute_file_path, 'w') as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {str(e)}'