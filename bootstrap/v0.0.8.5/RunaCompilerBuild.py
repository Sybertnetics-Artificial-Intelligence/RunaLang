import os
import sys
import subprocess
import shutil

# --- Configuration ---
# The root directory of your project. The script searches for all '.runa' files within this directory.
# By default, it uses the directory where the script is run.
PROJECT_ROOT = "."

# The name or path of your Runa compiler executable.
# We create a platform-aware path. On Linux/WSL, it will be './Compiled/Build/runac'
# and on Windows, it will be 'Compiled\Build\runac'.
compiler_path = os.path.join("Compiled", "Build", "runac")
if os.name == 'posix': # posix is for Linux, macOS, WSL
    COMPILER_EXECUTABLE = f"./{compiler_path}"
else: # 'nt' is for Windows
    COMPILER_EXECUTABLE = compiler_path

# The system assembler. 'as' is standard on Linux/WSL.
ASSEMBLER = "as"
# The system linker. Using 'gcc' is often easier as it handles linking standard libraries.
LINKER = "gcc"

# The directory where all build artifacts (object files, executables) will be stored.
BUILD_DIR = "build"

# The name of the final linked executable.
OUTPUT_EXECUTABLE = "runac"

# --- Script Logic ---

def find_source_files(root_dir, extension):
    """
    Recursively finds all files with a given extension in a directory.
    """
    source_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(extension):
                # We want to ignore directories that aren't part of the source code to be compiled.
                if "dev_tools" not in dirpath and "testing" not in dirpath and "Compiled" not in dirpath:
                    source_files.append(os.path.join(dirpath, filename))
    return source_files

def handle_error(command, returncode, stdout, stderr):
    """
    Centralized function to print detailed error messages and exit.
    """
    print(f"Error executing command: {command}", file=sys.stderr)
    print(f"Return Code: {returncode}", file=sys.stderr)
    print("\n--- STDOUT ---", file=sys.stderr)
    print(stdout if stdout else "<No output>", file=sys.stderr)
    print("\n--- STDERR ---", file=sys.stderr)
    print(stderr if stderr else "<No output>", file=sys.stderr)
    
    # Add a specific hint for WSL/Linux users for 'command not found'.
    if os.name == 'posix' and returncode == 127:
        print("\n[Hint] On WSL/Linux, this error can happen if the compiler does not have execute permissions.", file=sys.stderr)
        print(f"Please try running the following command in your terminal and then run the build script again:", file=sys.stderr)
        print(f"  chmod +x {compiler_path}\n", file=sys.stderr)

    sys.exit(1) # Exit the script if a command fails

def run_command(command):
    """
    Executes a command in the shell and checks for errors, including '[ERROR]' in the output.
    """
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        
        # New check: Fail the build if '[ERROR]' is in the compiler's output, even if it exits cleanly.
        if '[ERROR]' in result.stdout or '[ERROR]' in result.stderr:
            print(f"Build failed: Compiler reported an error for command: {command}", file=sys.stderr)
            handle_error(command, result.returncode, result.stdout, result.stderr)
            
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
            
    except subprocess.CalledProcessError as e:
        # Handle cases where the command itself returns a non-zero exit code.
        handle_error(e.cmd, e.returncode, e.stdout, e.stderr)

def clean():
    """
    Removes the build directory and all its contents.
    """
    if os.path.exists(BUILD_DIR):
        print(f"--- Cleaning up build artifacts ---")
        print(f"Removing directory: {BUILD_DIR}")
        shutil.rmtree(BUILD_DIR)
        print("Cleanup complete.")
    else:
        print("Build directory not found. Nothing to clean.")

def build():
    """
    Main function to drive the compilation and linking process.
    """
    print("--- Runa Compiler Build Script ---")

    if not os.path.exists(BUILD_DIR):
        print(f"Creating build directory: {BUILD_DIR}")
        os.makedirs(BUILD_DIR)

    print(f"Searching for source files in: {os.path.abspath(PROJECT_ROOT)}...")
    runa_files = find_source_files(PROJECT_ROOT, ".runa")
    asm_files = find_source_files(PROJECT_ROOT, ".asm")
    
    if not runa_files and not asm_files:
        print("Error: No source files (.runa, .asm) found.", file=sys.stderr)
        sys.exit(1)
        
    print(f"Found {len(runa_files)} .runa files and {len(asm_files)} .asm files.")

    # --- Phase 1: Compile .runa files to .s assembly files ---
    print("\n--- Phase 1: Compiling .runa to Assembly (.s) ---")
    generated_s_files = []
    for runa_file in runa_files:
        relative_path = os.path.relpath(runa_file, PROJECT_ROOT)
        base_name = relative_path.replace(os.sep, '_').replace('.runa', '.s')
        output_s_path = os.path.join(BUILD_DIR, base_name)
        generated_s_files.append(output_s_path)
        
        compile_command = f'"{COMPILER_EXECUTABLE}" "{runa_file}" "{output_s_path}"'
        print(f"Compiling: {runa_file}")
        print(f"  > {compile_command}")
        run_command(compile_command)
        
    # --- Phase 2: Assemble all .s and .asm files into .o object files ---
    print("\n--- Phase 2: Assembling to Object (.o) files ---")
    all_assembly_files = asm_files + generated_s_files
    object_files = []
    for asm_file in all_assembly_files:
        # For files from the source tree, create a unique name.
        if asm_file.startswith(BUILD_DIR):
            base_name = os.path.basename(asm_file)
        else:
            relative_path = os.path.relpath(asm_file, PROJECT_ROOT)
            base_name = relative_path.replace(os.sep, '_')
        
        object_filename = base_name.replace('.s', '.o').replace('.asm', '.o')
        object_file_path = os.path.join(BUILD_DIR, object_filename)
        object_files.append(object_file_path)

        assemble_command = f'{ASSEMBLER} "{asm_file}" -o "{object_file_path}"'
        print(f"Assembling: {asm_file}")
        print(f"  > {assemble_command}")
        run_command(assemble_command)

    # --- Phase 3: Link all object files into a single executable ---
    print("\n--- Phase 3: Linking object files ---")
    object_files_str = " ".join([f'"{obj}"' for obj in object_files])
    output_executable_path = os.path.join(BUILD_DIR, OUTPUT_EXECUTABLE)
    
    link_command = f'{LINKER} {object_files_str} -o "{output_executable_path}"'
    print(f"Linking {len(object_files)} object files...")
    print(f"  > {link_command}")
    run_command(link_command)

    print("\n--- Build process finished ---")
    print(f"The final executable is located at: {os.path.abspath(output_executable_path)}")

if __name__ == "__main__":
    args = sys.argv[1:]
    action = "build" 
    if args and args[0] in ["clean", "build"]:
        action = args.pop(0)

    if args:
        PROJECT_ROOT = args[0]
        if not os.path.isdir(PROJECT_ROOT):
            print(f"Error: Provided path '{PROJECT_ROOT}' is not a valid directory.", file=sys.stderr)
            sys.exit(1)

    if action == "build":
        build()
    elif action == "clean":
        clean()

