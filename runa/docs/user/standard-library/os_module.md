# OS Module

The OS module provides comprehensive utilities for interacting with the operating system, including file operations, process management, environment variables, system information, and advanced OS operations.

## Overview

The OS module offers a complete set of operating system interaction functions with natural language syntax for basic operations and helper functions for advanced use cases.

## Basic File and Directory Operations

### Working with Directories

```runa
Note: Basic directory operations use natural language syntax
:End Note

Let cwd be get current working directory
Call print with message as "Current directory: " plus cwd

Let files be list directory at path cwd
For each file in files:
    Call print with message as "File: " plus file

Create directory "new_folder"
Create directories "path/to/nested/directory"
```

### File Operations

```runa
Copy file from "source.txt" to "destination.txt"
Move file from "old_name.txt" to "new_name.txt"
Remove file "unwanted.txt"
Remove directory "empty_folder"
Remove recursive "folder_with_contents"
```

### File Information

```runa
Let file_size be size of file "large.dat"
Let permissions be file permissions of "script.sh"
Let owner be owner of file "important.txt"
Let modified_time be last modified time of file "document.txt"

Call print with message as "File size: " plus file_size
Call print with message as "Owner: " plus owner
```

## File Type Checks

### Checking File Properties

```runa
If is file at "data.txt":
    Call print with message as "Regular file"
Otherwise if is directory at "data.txt":
    Call print with message as "Directory"
Otherwise if is symbolic link at "data.txt":
    Call print with message as "Symbolic link"

If is executable file at "script.sh":
    Call print with message as "Executable file"

If is readable file at "config.txt":
    Call print with message as "Readable file"

If is writable file at "log.txt":
    Call print with message as "Writable file"
```

## Path Operations

### Path Manipulation

```runa
Let abs_path be absolute path of "relative/file.txt"
Let real_path be real path of "symlink.txt"
Let joined_path be join paths ["folder", "subfolder", "file.txt"]
Let path_parts be split path "/home/user/documents/file.txt"

Let ext be file extension of "document.pdf"
Let filename be filename of "/path/to/file.txt"
Let dirname be directory of "/path/to/file.txt"

Call print with message as "Extension: " plus ext
Call print with message as "Filename: " plus filename
```

## System Directories

### Working with System Paths

```runa
Let temp_dir be system temporary directory
Let home_dir be user home directory
Let system_dir be system directory
Let user_dir be user directory

Call print with message as "Temp directory: " plus temp_dir
Call print with message as "Home directory: " plus home_dir
```

### Temporary Files and Directories

```runa
Let temp_file be create temp file with prefix as "runa_" and suffix as ".tmp"
Let temp_dir be create temp directory with prefix as "runa_"

Write "Temporary data" to file temp_file
Call print with message as "Created: " plus temp_file
```

## Environment Variables

### Managing Environment Variables

```runa
Let path_var be get environment variable "PATH"
Let home_var be get environment variable "HOME"

Set environment variable "CUSTOM_VAR" to "custom_value"
Unset environment variable "OLD_VAR"

Let all_env_vars be get all environment variables
For each key and value in all_env_vars:
    Call print with message as key plus " = " plus value
```

## Process Management

### Process Information

```runa
Let process_id be get current process id
Let parent_id be get parent process id
Let process_name be get process name
Let process_cwd be get process working directory

Call print with message as "Process ID: " plus process_id
Call print with message as "Process name: " plus process_name
```

### Command Execution

```runa
Let result be execute command "ls -la"
Call print with message as "Exit code: " plus result["exit_code"]
Call print with message as "Output: " plus result["output"]

Let result_with_args be execute command with args "echo" and ["Hello", "World"]
Call print with message as "Output: " plus result_with_args["output"]

Let result_with_input be execute command with input "grep pattern" and "input data"
Call print with message as "Output: " plus result_with_input["output"]
```

### Background Processes

```runa
Let bg_process_id be execute command background "long_running_script.sh"
Call print with message as "Background process ID: " plus bg_process_id

If is process running bg_process_id:
    Call print with message as "Process is still running"
    Kill process bg_process_id
    Let exit_code be wait for process bg_process_id
    Call print with message as "Process exited with code: " plus exit_code
```

### Process Information

```runa
Let process_info be get process info process_id
Call print with message as "Process info: " plus process_info

Let all_processes be get all processes
For each process in all_processes:
    Call print with message as "Process: " plus process["name"] plus " (PID: " plus process["pid"] plus ")"
```

## System Information

### Platform and Architecture

```runa
Let platform be get system platform
Let architecture be get system architecture
Let version be get system version
Let system_name be get system name

Call print with message as "Platform: " plus platform
Call print with message as "Architecture: " plus architecture
Call print with message as "Version: " plus version
```

### Comprehensive System Info

```runa
Let system_info be get system info
For each key and value in system_info:
    Call print with message as key plus ": " plus value
```

### Hardware Information

```runa
Let cpu_count be get cpu count
Let cpu_usage be get cpu usage
Let memory_info be get memory info
Let disk_info be get disk info "/"

Call print with message as "CPU cores: " plus cpu_count
Call print with message as "CPU usage: " plus cpu_usage plus "%"
Call print with message as "Total memory: " plus memory_info["total"]
Call print with message as "Available memory: " plus memory_info["available"]
Call print with message as "Disk free: " plus disk_info["free"]
```

### Network Information

```runa
Let interfaces be get network interfaces
For each interface in interfaces:
    Call print with message as "Interface: " plus interface["name"]
    Call print with message as "  IP: " plus interface["ip"]
    Call print with message as "  MAC: " plus interface["mac"]

Let hostname be get hostname
Call print with message as "Hostname: " plus hostname
```

## User and Group Management

### User Information

```runa
Let username be get username
Let user_id be get user id
Let group_id be get group id
Let user_groups be get user groups

Call print with message as "Username: " plus username
Call print with message as "User ID: " plus user_id
Call print with message as "Group ID: " plus group_id

For each group in user_groups:
    Call print with message as "Group: " plus group

If is admin:
    Call print with message as "User has admin privileges"
Otherwise:
    Call print with message as "User does not have admin privileges"
```

### System Users and Groups

```runa
Let system_users be get system users
For each user in system_users:
    Call print with message as "User: " plus user["name"] plus " (ID: " plus user["id"] plus ")"

Let system_groups be get system groups
For each group in system_groups:
    Call print with message as "Group: " plus group["name"] plus " (ID: " plus group["id"] plus ")"
```

### User and Group Operations

```runa
If create user "newuser" with password "password123":
    Call print with message as "User created successfully"
    If add user "newuser" to group "users":
        Call print with message as "User added to group"
    If change user password "newuser" to "newpassword456":
        Call print with message as "Password changed"
    If remove user "newuser" from group "users":
        Call print with message as "User removed from group"
    If delete user "newuser":
        Call print with message as "User deleted"

If create group "newgroup":
    Call print with message as "Group created successfully"
    If delete group "newgroup":
        Call print with message as "Group deleted"
```

## System Monitoring

### System Metrics

```runa
Let uptime be get system uptime
Let boot_time be get system boot time
Let load_averages be get system load

Call print with message as "Uptime: " plus uptime plus " seconds"
Call print with message as "Boot time: " plus boot_time
Call print with message as "Load averages: " plus load_averages
```

### System Health and Security

```runa
Let system_health be get system health
For each key and value in system_health:
    Call print with message as key plus ": " plus value

Let system_security be get system security
For each key and value in system_security:
    Call print with message as key plus ": " plus value
```

### System Metrics and Monitoring

```runa
Let metrics be get system metrics
For each key and value in metrics:
    Call print with message as key plus ": " plus value

Set system monitoring to true
Let monitoring_data be get system monitoring
Call print with message as "Monitoring data: " plus monitoring_data
```

## System Services

### Service Management

```runa
Let services be get system services
For each service in services:
    Call print with message as "Service: " plus service["name"] plus " - " plus service["status"]

If start service "apache2":
    Call print with message as "Apache service started"
    If is service running "apache2":
        Call print with message as "Apache is running"
        If stop service "apache2":
            Call print with message as "Apache service stopped"

Let service_status be get service status "mysql"
Call print with message as "MySQL status: " plus service_status
```

## System Logs and Events

### Log Management

```runa
Let system_logs be get system logs "system"
For each log in system_logs:
    Call print with message as "Log: " plus log

Write system log "Application started" with level as "info"
Write system log "Error occurred" with level as "error"
```

### System Events and Alerts

```runa
Let system_events be get system events
For each event in system_events:
    Call print with message as "Event: " plus event["type"] plus " - " plus event["message"]

Let alerts be get system alerts
For each alert in alerts:
    Call print with message as "Alert: " plus alert["type"] plus " - " plus alert["message"]

Set system alert for "cpu_usage" with threshold as 80
Set system alert for "memory_usage" with threshold as 90
```

### Notifications

```runa
Let notifications be get system notifications
For each notification in notifications:
    Call print with message as "Notification: " plus notification["title"] plus " - " plus notification["message"]

Send system notification with title as "System Update" and message as "Updates are available"
```

## System Updates and Packages

### Package Management

```runa
Let packages be get system packages
For each package in packages:
    Call print with message as "Package: " plus package["name"] plus " - " plus package["version"]

If install package "nginx":
    Call print with message as "Nginx installed successfully"
    If uninstall package "nginx":
        Call print with message as "Nginx uninstalled"
```

### System Updates

```runa
Let updates be get system updates
For each update in updates:
    Call print with message as "Update: " plus update["name"] plus " - " plus update["version"]

If install system update "security-patch-2023":
    Call print with message as "Security patch installed"
```

## System Drivers and Devices

### Hardware Management

```runa
Let drivers be get system drivers
For each driver in drivers:
    Call print with message as "Driver: " plus driver["name"] plus " - " plus driver["status"]

Let devices be get system devices
For each device in devices:
    Call print with message as "Device: " plus device["name"] plus " - " plus device["type"]
```

## Volume Management

### Disk Volumes

```runa
Let volumes be get system volumes
For each volume in volumes:
    Call print with message as "Volume: " plus volume["name"] plus " - " plus volume["mount_point"]

If mount volume "/dev/sdb1" at "/mnt/data":
    Call print with message as "Volume mounted successfully"
    If unmount volume "/mnt/data":
        Call print with message as "Volume unmounted"
```

## Scheduled Tasks

### Task Management

```runa
Let scheduled_tasks be get system scheduled tasks
For each task in scheduled_tasks:
    Call print with message as "Task: " plus task["name"] plus " - " plus task["schedule"]

If create scheduled task "backup" with command as "backup_script.sh" and schedule as "daily":
    Call print with message as "Backup task created"
    If delete scheduled task "backup":
        Call print with message as "Backup task deleted"
```

## System Backups

### Backup Management

```runa
Let backups be get system backups
For each backup in backups:
    Call print with message as "Backup: " plus backup["name"] plus " - " plus backup["date"]

If create system backup "full_backup_2023":
    Call print with message as "System backup created"
    If restore system backup "full_backup_2023":
        Call print with message as "System backup restored"
```

## Helper Functions

### Advanced Usage

```runa
Note: For advanced/AI-generated code, use helper functions
:End Note

Let result be execute with command as "ls" and args as ["-la", "/home"]
Let system_info be get system info with info_type as "platform"
```

## Error Handling

### Robust OS Operations

```runa
Try:
    Let result be execute command "nonexistent_command"
    Assert false  Note: Should not reach here
:End Note
Catch Error as e:
    Call print with message as "Command failed: " plus e

Try:
    Create directory "/invalid/path"
    Assert false  Note: Should not reach here
:End Note
Catch Error as e:
    Call print with message as "Directory creation failed: " plus e
```

## Performance Considerations

### Efficient OS Operations

```runa
Note: For large directory listings, consider filtering
:End Note

Let all_files be list directory at path "/large_directory"
Let filtered_files be list with

For each file in all_files:
    If file ends with ".txt":
        Add file to filtered_files

Call print with message as "Text files: " plus length of filtered_files
```

## API Reference

### File and Directory Operations

- `get_current_directory() -> String`: Get current working directory
- `change_directory(path: String) -> None`: Change current directory
- `list_directory(path: String) -> List[String]`: List directory contents
- `create_directory(path: String) -> None`: Create directory
- `create_directories(path: String) -> None`: Create nested directories
- `remove_file(path: String) -> None`: Remove file
- `remove_directory(path: String) -> None`: Remove directory
- `remove_recursive(path: String) -> None`: Remove recursively
- `copy_file(source: String, destination: String) -> None`: Copy file
- `move_file(source: String, destination: String) -> None`: Move file

### File Information

- `get_file_size(path: String) -> Integer`: Get file size
- `get_file_permissions(path: String) -> Integer`: Get file permissions
- `set_file_permissions(path: String, mode: Integer) -> None`: Set file permissions
- `get_file_owner(path: String) -> String`: Get file owner
- `get_file_group(path: String) -> String`: Get file group
- `get_file_modified_time(path: String) -> Number`: Get modification time
- `get_file_created_time(path: String) -> Number`: Get creation time
- `get_file_access_time(path: String) -> Number`: Get access time

### File Type Checks

- `is_file(path: String) -> Boolean`: Check if regular file
- `is_directory(path: String) -> Boolean`: Check if directory
- `is_symlink(path: String) -> Boolean`: Check if symbolic link
- `is_executable(path: String) -> Boolean`: Check if executable
- `is_readable(path: String) -> Boolean`: Check if readable
- `is_writable(path: String) -> Boolean`: Check if writable

### Path Operations

- `get_absolute_path(path: String) -> String`: Get absolute path
- `get_real_path(path: String) -> String`: Get real path
- `join_paths(paths: List[String]) -> String`: Join paths
- `split_path(path: String) -> List[String]`: Split path
- `get_extension(path: String) -> String`: Get file extension
- `get_filename(path: String) -> String`: Get filename
- `get_directory(path: String) -> String`: Get directory

### System Directories

- `get_temp_directory() -> String`: Get temp directory
- `get_home_directory() -> String`: Get home directory
- `get_system_directory() -> String`: Get system directory
- `get_user_directory() -> String`: Get user directory
- `create_temp_file(prefix: String, suffix: String) -> String`: Create temp file
- `create_temp_directory(prefix: String) -> String`: Create temp directory

### Environment Variables

- `get_environment_variable(name: String) -> String`: Get env var
- `set_environment_variable(name: String, value: String) -> None`: Set env var
- `unset_environment_variable(name: String) -> None`: Unset env var
- `get_all_environment_variables() -> Dictionary[String, String]`: Get all env vars

### Process Management

- `get_current_process_id() -> Integer`: Get current PID
- `get_parent_process_id() -> Integer`: Get parent PID
- `get_process_name() -> String`: Get process name
- `get_process_working_directory() -> String`: Get process CWD
- `execute_command(command: String) -> Dictionary[String, Any]`: Execute command
- `execute_command_with_args(command: String, args: List[String]) -> Dictionary[String, Any]`: Execute with args
- `execute_command_with_input(command: String, input_data: String) -> Dictionary[String, Any]`: Execute with input
- `execute_command_background(command: String) -> Integer`: Execute in background
- `kill_process(process_id: Integer) -> None`: Kill process
- `wait_for_process(process_id: Integer) -> Integer`: Wait for process
- `is_process_running(process_id: Integer) -> Boolean`: Check if running
- `get_process_info(process_id: Integer) -> Dictionary[String, Any]`: Get process info
- `get_all_processes() -> List[Dictionary[String, Any]]`: Get all processes

### System Information

- `get_system_platform() -> String`: Get platform
- `get_system_architecture() -> String`: Get architecture
- `get_system_version() -> String`: Get version
- `get_system_name() -> String`: Get system name
- `get_system_info() -> Dictionary[String, String]`: Get system info
- `get_cpu_count() -> Integer`: Get CPU count
- `get_cpu_usage() -> Number`: Get CPU usage
- `get_memory_info() -> Dictionary[String, Integer]`: Get memory info
- `get_disk_info(path: String) -> Dictionary[String, Integer]`: Get disk info
- `get_network_interfaces() -> List[Dictionary[String, String]]`: Get network interfaces
- `get_hostname() -> String`: Get hostname

### User and Group Management

- `get_username() -> String`: Get username
- `get_user_id() -> Integer`: Get user ID
- `get_group_id() -> Integer`: Get group ID
- `get_user_groups() -> List[String]`: Get user groups
- `is_admin() -> Boolean`: Check admin privileges
- `get_system_users() -> List[Dictionary[String, String]]`: Get system users
- `create_user(username: String, password: String) -> Boolean`: Create user
- `delete_user(username: String) -> Boolean`: Delete user
- `change_user_password(username: String, new_password: String) -> Boolean`: Change password
- `get_system_groups() -> List[Dictionary[String, String]]`: Get system groups
- `create_group(groupname: String) -> Boolean`: Create group
- `delete_group(groupname: String) -> Boolean`: Delete group
- `add_user_to_group(username: String, groupname: String) -> Boolean`: Add user to group
- `remove_user_from_group(username: String, groupname: String) -> Boolean`: Remove user from group

### System Monitoring

- `get_system_uptime() -> Number`: Get uptime
- `get_boot_time() -> Number`: Get boot time
- `get_system_load() -> List[Number]`: Get load averages
- `get_system_health() -> Dictionary[String, String]`: Get system health
- `get_system_security() -> Dictionary[String, String]`: Get security info
- `get_system_metrics() -> Dictionary[String, Number]`: Get metrics
- `set_system_monitoring(enabled: Boolean) -> None`: Set monitoring
- `get_system_monitoring() -> Dictionary[String, Number]`: Get monitoring data

### System Services

- `get_system_services() -> List[Dictionary[String, String]]`: Get services
- `start_service(service_name: String) -> Boolean`: Start service
- `stop_service(service_name: String) -> Boolean`: Stop service
- `restart_service(service_name: String) -> Boolean`: Restart service
- `is_service_running(service_name: String) -> Boolean`: Check service
- `get_service_status(service_name: String) -> String`: Get service status

### System Logs and Events

- `get_system_logs(log_type: String) -> List[String]`: Get logs
- `write_system_log(message: String, level: String) -> None`: Write log
- `get_system_events() -> List[Dictionary[String, Any]]`: Get events
- `get_system_alerts() -> List[Dictionary[String, String]]`: Get alerts
- `set_system_alert(alert_type: String, threshold: Number) -> None`: Set alert
- `get_system_notifications() -> List[Dictionary[String, String]]`: Get notifications
- `send_system_notification(title: String, message: String) -> None`: Send notification

### Package and Update Management

- `get_system_packages() -> List[Dictionary[String, String]]`: Get packages
- `install_package(package_name: String) -> Boolean`: Install package
- `uninstall_package(package_name: String) -> Boolean`: Uninstall package
- `get_system_updates() -> List[Dictionary[String, String]]`: Get updates
- `install_system_update(update_id: String) -> Boolean`: Install update

### Hardware Management

- `get_system_drivers() -> List[Dictionary[String, String]]`: Get drivers
- `get_system_devices() -> List[Dictionary[String, String]]`: Get devices
- `get_system_volumes() -> List[Dictionary[String, String]]`: Get volumes
- `mount_volume(device: String, mount_point: String) -> Boolean`: Mount volume
- `unmount_volume(mount_point: String) -> Boolean`: Unmount volume

### Scheduled Tasks and Backups

- `get_system_scheduled_tasks() -> List[Dictionary[String, String]]`: Get tasks
- `create_scheduled_task(name: String, command: String, schedule: String) -> Boolean`: Create task
- `delete_scheduled_task(name: String) -> Boolean`: Delete task
- `get_system_backups() -> List[Dictionary[String, String]]`: Get backups
- `create_system_backup(backup_name: String) -> Boolean`: Create backup
- `restore_system_backup(backup_name: String) -> Boolean`: Restore backup

## Testing

The OS module includes comprehensive tests covering:

- Basic file and directory operations
- File information and permissions
- Path manipulation and validation
- Environment variable management
- Process creation and management
- System information retrieval
- User and group operations
- System monitoring and metrics
- Service management
- Log and event handling
- Package and update management
- Error handling scenarios
- Cross-platform compatibility

## Examples

See the `examples/basic/os_operations.runa` file for complete working examples of all OS module features. 