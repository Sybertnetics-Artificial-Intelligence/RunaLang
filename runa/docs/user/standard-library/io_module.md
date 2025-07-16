# IO Module

The IO module provides comprehensive file input/output operations for Runa programs, including text and binary file handling, directory operations, file metadata, and advanced file utilities.

## Overview

The IO module offers a complete set of file system operations with natural language syntax for basic operations and helper functions for advanced use cases.

## Basic File Operations

### Reading and Writing Files

```runa
Note: Basic file operations use natural language syntax
:End Note

Let content be read file "data.txt"
Write "Hello, World!" to file "output.txt"
Append "New line" to file "log.txt"

Let lines be read lines from file "config.txt"
Write lines to file "backup.txt"
```

### File Existence and Size

```runa
If file "important.dat" exists:
    Let file_size be size of file "important.dat"
    Call print with message as "File size: " plus file_size
Otherwise:
    Call print with message as "File not found"
```

## Binary File Operations

### Reading and Writing Binary Data

```runa
Let binary_data be read binary file "image.png"
Write binary binary_data to file "copy.png"

Let bytes be [72, 101, 108, 108, 111]  Note: "Hello" in ASCII
Write binary bytes to file "hello.bin"
```

## Directory Operations

### Creating and Managing Directories

```runa
Create directory "new_folder"
Create directories "path/to/nested/directory"

Let files be list files in directory "docs"
Let subdirs be list subdirectories in directory "project"

For each file in files:
    Call print with message as "File: " plus file
```

### Directory Walking

```runa
Let all_files be walk directory "project"
For each path in all_files:
    Call print with message as "Found: " plus path
```

## File Metadata

### File Information

```runa
If is file at "document.txt":
    Let modified_time be last modified time of file "document.txt"
    Let permissions be file permissions of "document.txt"
    Let owner be owner of file "document.txt"
    
    Call print with message as "Modified: " plus modified_time
    Call print with message as "Permissions: " plus permissions
    Call print with message as "Owner: " plus owner
```

### File Types

```runa
If is file at "data.txt":
    Call print with message as "Regular file"
Otherwise if is directory at "data.txt":
    Call print with message as "Directory"
Otherwise if is symbolic link at "data.txt":
    Call print with message as "Symbolic link"
```

## Path Operations

### Path Manipulation

```runa
Let abs_path be absolute path of "relative/file.txt"
Let rel_path be relative path from "/base" to "/base/file.txt"
Let joined be join paths ["folder", "subfolder", "file.txt"]
Let parts be split path "/home/user/documents/file.txt"

Let ext be file extension of "document.pdf"
Let name be filename of "/path/to/file.txt"
Let dir be directory of "/path/to/file.txt"
```

## System Directories

### Working with System Paths

```runa
Let cwd be current working directory
Change directory to "/home/user"
Let temp_dir be system temporary directory
Let home_dir be user home directory

Call print with message as "Current: " plus cwd
Call print with message as "Temp: " plus temp_dir
Call print with message as "Home: " plus home_dir
```

## Temporary Files and Directories

### Creating Temporary Resources

```runa
Let temp_file be create temp file with prefix as "runa_" and suffix as ".tmp"
Let temp_dir be create temp directory with prefix as "runa_"

Write "Temporary data" to file temp_file
Call print with message as "Created: " plus temp_file
```

## File Management

### Copying and Moving Files

```runa
Copy file from "source.txt" to "backup.txt"
Move file from "old_name.txt" to "new_name.txt"
Delete file "unwanted.txt"
```

### File Comparison and Hashing

```runa
If compare files "file1.txt" and "file2.txt":
    Call print with message as "Files are identical"
Otherwise:
    Call print with message as "Files differ"

Let hash_value be hash of file "document.pdf" using "sha256"
Call print with message as "Hash: " plus hash_value
```

## Advanced File Operations

### File Locking

```runa
Lock file "shared.dat"
Note: Perform operations on locked file
:End Note
Unlock file "shared.dat"
```

### File Truncation and Touch

```runa
Truncate file "large.dat" to 1024 bytes
Touch file "timestamp.txt"  Note: Update access/modification times
:End Note
```

### File Compression

```runa
Compress file from "large.txt" to "large.txt.gz"
Decompress file from "compressed.gz" to "decompressed.txt"
```

## Helper Functions

### Advanced Usage

```runa
Note: For advanced/AI-generated code, use helper functions
:End Note

Let content be read with path as "config.json"
Let result be write with path as "output.log" and data as log_data
Let copied be copy with source as "src.dat" and destination as "dst.dat"
```

## Error Handling

### Robust File Operations

```runa
Try:
    Let content be read file "important.txt"
    Write content to file "backup.txt"
Catch Error as e:
    Call print with message as "File operation failed: " plus e
```

## Performance Considerations

### Efficient File Operations

```runa
Note: For large files, consider binary operations
:End Note

Let large_data be read binary file "large.dat"
Let chunk_size be 8192
Let processed be 0

While processed is less than length of large_data:
    Let chunk be slice of large_data from processed to processed plus chunk_size
    Note: Process chunk
    :End Note
    Set processed to processed plus chunk_size
```

## API Reference

### Core Functions

- `read(path: String) -> String`: Read text file
- `write(path: String, data: String) -> None`: Write text file
- `append(path: String, data: String) -> None`: Append to file
- `exists(path: String) -> Boolean`: Check file existence
- `size(path: String) -> Integer`: Get file size

### Binary Operations

- `read_binary(path: String) -> List[Integer]`: Read binary file
- `write_binary(path: String, data: List[Integer]) -> None`: Write binary file

### Directory Operations

- `create_directory(path: String) -> None`: Create directory
- `create_directories(path: String) -> None`: Create nested directories
- `list_directory(path: String) -> List[String]`: List files
- `list_directories(path: String) -> List[String]`: List subdirectories
- `walk_directory(path: String) -> List[List[String]]`: Recursive listing

### File Metadata

- `is_file(path: String) -> Boolean`: Check if regular file
- `is_directory(path: String) -> Boolean`: Check if directory
- `is_symlink(path: String) -> Boolean`: Check if symbolic link
- `get_modified_time(path: String) -> Number`: Get modification time
- `get_permissions(path: String) -> Integer`: Get file permissions
- `get_owner(path: String) -> String`: Get file owner

### Path Operations

- `get_absolute_path(path: String) -> String`: Get absolute path
- `join_paths(paths: List[String]) -> String`: Join path components
- `split_path(path: String) -> List[String]`: Split path
- `get_extension(path: String) -> String`: Get file extension
- `get_filename(path: String) -> String`: Get filename
- `get_directory(path: String) -> String`: Get directory

### System Operations

- `get_current_directory() -> String`: Get current directory
- `change_directory(path: String) -> None`: Change directory
- `get_temp_directory() -> String`: Get temp directory
- `get_home_directory() -> String`: Get home directory

### Advanced Operations

- `lock_file(path: String) -> None`: Acquire file lock
- `unlock_file(path: String) -> None`: Release file lock
- `truncate_file(path: String, size: Integer) -> None`: Truncate file
- `touch_file(path: String) -> None`: Update timestamps
- `compare_files(file1: String, file2: String) -> Boolean`: Compare files
- `get_file_hash(path: String, algorithm: String) -> String`: Get file hash
- `compress_file(source: String, destination: String) -> None`: Compress file
- `decompress_file(source: String, destination: String) -> None`: Decompress file

## Testing

The IO module includes comprehensive tests covering:

- Basic file read/write operations
- Binary file operations
- Directory creation and listing
- File metadata retrieval
- Path manipulation
- Error handling scenarios
- Performance with large files
- File locking and synchronization
- Compression and decompression

## Examples

See the `examples/basic/file_operations.runa` file for complete working examples of all IO module features. 