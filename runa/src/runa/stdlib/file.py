"""
Runa Standard Library - File Module

Provides file system operations for Runa programs.
"""

import os
import shutil
from pathlib import Path

def read_text_file(file_path, encoding="utf-8"):
    """Read the entire contents of a text file."""
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return file.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        raise Exception(f"Error reading file: {e}")

def write_text_file(file_path, content, encoding="utf-8"):
    """Write content to a text file."""
    try:
        with open(file_path, 'w', encoding=encoding) as file:
            file.write(content)
        return True
    except Exception as e:
        raise Exception(f"Error writing file: {e}")

def append_to_text_file(file_path, content, encoding="utf-8"):
    """Append content to a text file."""
    try:
        with open(file_path, 'a', encoding=encoding) as file:
            file.write(content)
        return True
    except Exception as e:
        raise Exception(f"Error appending to file: {e}")

def read_lines_from_file(file_path, encoding="utf-8"):
    """Read all lines from a text file as a list."""
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return file.readlines()
    except FileNotFoundError:
        return None
    except Exception as e:
        raise Exception(f"Error reading file lines: {e}")

def write_lines_to_file(file_path, lines, encoding="utf-8"):
    """Write a list of lines to a text file."""
    try:
        with open(file_path, 'w', encoding=encoding) as file:
            file.writelines(lines)
        return True
    except Exception as e:
        raise Exception(f"Error writing lines to file: {e}")

def file_exists(file_path):
    """Check if a file exists."""
    return os.path.isfile(file_path)

def directory_exists(directory_path):
    """Check if a directory exists."""
    return os.path.isdir(directory_path)

def path_exists(path):
    """Check if a path (file or directory) exists."""
    return os.path.exists(path)

def create_directory(directory_path):
    """Create a directory (and parent directories if needed)."""
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except Exception as e:
        raise Exception(f"Error creating directory: {e}")

def delete_file(file_path):
    """Delete a file."""
    try:
        os.remove(file_path)
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        raise Exception(f"Error deleting file: {e}")

def delete_directory(directory_path):
    """Delete a directory and all its contents."""
    try:
        shutil.rmtree(directory_path)
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        raise Exception(f"Error deleting directory: {e}")

def copy_file(source_path, destination_path):
    """Copy a file from source to destination."""
    try:
        shutil.copy2(source_path, destination_path)
        return True
    except Exception as e:
        raise Exception(f"Error copying file: {e}")

def move_file(source_path, destination_path):
    """Move (rename) a file from source to destination."""
    try:
        shutil.move(source_path, destination_path)
        return True
    except Exception as e:
        raise Exception(f"Error moving file: {e}")

def get_file_size(file_path):
    """Get the size of a file in bytes."""
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        raise Exception(f"Error getting file size: {e}")

def get_file_modification_time(file_path):
    """Get the last modification time of a file."""
    try:
        return os.path.getmtime(file_path)
    except Exception as e:
        raise Exception(f"Error getting file modification time: {e}")

def list_files_in_directory(directory_path):
    """List all files in a directory."""
    try:
        return [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    except Exception as e:
        raise Exception(f"Error listing files: {e}")

def list_directories_in_directory(directory_path):
    """List all subdirectories in a directory."""
    try:
        return [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]
    except Exception as e:
        raise Exception(f"Error listing directories: {e}")

def list_all_items_in_directory(directory_path):
    """List all items (files and directories) in a directory."""
    try:
        return os.listdir(directory_path)
    except Exception as e:
        raise Exception(f"Error listing directory contents: {e}")

def get_current_directory():
    """Get the current working directory."""
    return os.getcwd()

def change_directory(directory_path):
    """Change the current working directory."""
    try:
        os.chdir(directory_path)
        return True
    except Exception as e:
        raise Exception(f"Error changing directory: {e}")

def get_absolute_path(path):
    """Get the absolute path of a file or directory."""
    return os.path.abspath(path)

def get_parent_directory(path):
    """Get the parent directory of a path."""
    return os.path.dirname(path)

def get_file_name(path):
    """Get the file name from a path."""
    return os.path.basename(path)

def get_file_extension(path):
    """Get the file extension from a path."""
    return os.path.splitext(path)[1]

def join_paths(*paths):
    """Join multiple path components into a single path."""
    return os.path.join(*paths)

def normalize_path(path):
    """Normalize a path by resolving .. and . components."""
    return os.path.normpath(path)

def is_absolute_path(path):
    """Check if a path is absolute."""
    return os.path.isabs(path)

# Runa-style function names for natural language calling
read_file_contents = read_text_file
write_file_contents = write_text_file
add_to_file = append_to_text_file
read_file_lines = read_lines_from_file
write_file_lines = write_lines_to_file
check_if_file_exists = file_exists
check_if_directory_exists = directory_exists
check_if_path_exists = path_exists
make_directory = create_directory
remove_file = delete_file
remove_directory = delete_directory
copy_file_to = copy_file
move_file_to = move_file
get_size_of_file = get_file_size
get_modification_time = get_file_modification_time
list_files = list_files_in_directory
list_subdirectories = list_directories_in_directory
list_directory_contents = list_all_items_in_directory
get_working_directory = get_current_directory
set_working_directory = change_directory
get_full_path = get_absolute_path
get_parent_folder = get_parent_directory
get_filename = get_file_name
get_extension = get_file_extension
combine_paths = join_paths
clean_path = normalize_path
check_if_absolute = is_absolute_path