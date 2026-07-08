import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    print(f"Result for current directory:")
    try:
        
        absworking_directory = os.path.abspath(working_directory)
        full_directory = os.path.normpath(os.path.join(absworking_directory, directory))
        valid_target_directory = os.path.commonpath([absworking_directory, full_directory]) == absworking_directory
        if not valid_target_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(full_directory):
            return f'Error: "{directory}" is not a valid directory'

        files_data = ""
        for item in os.listdir(full_directory):
            name = item
            file_size = os.path.getsize(os.path.join(full_directory, item))
            is_dir = os.path.isdir(os.path.join(full_directory, item)) 

            files_data += f' - {name}: file_size={file_size} bytes, is_dir={is_dir}\n'
        return files_data
    
    except Exception as e:
        return f'Error: {str(e )}'
 
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "required": ["directory"],
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}