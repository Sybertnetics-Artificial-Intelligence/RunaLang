use std::env;
use std::fs;
use std::process;
use std::path::{Path, PathBuf};
use std::collections::HashSet;

mod lexer;
mod parser;
mod codegen;
mod typechecker;

use lexer::Lexer;
use parser::Parser;
use codegen::CodeGenerator;
use typechecker::TypeChecker;
use parser::AstNode;

fn find_function_calls(ast: &AstNode, calls: &mut HashSet<String>) {
    match ast {
        AstNode::Program(statements) => {
            for stmt in statements {
                find_function_calls(stmt, calls);
            }
        }
        AstNode::FunctionCall { name, arguments } => {
            calls.insert(name.clone());
            for arg in arguments {
                find_function_calls(arg, calls);
            }
        }
        AstNode::BinaryExpression { left, right, .. } => {
            find_function_calls(left, calls);
            find_function_calls(right, calls);
        }
        AstNode::LetStatement { value, .. } => {
            find_function_calls(value, calls);
        }
        AstNode::SetStatement { value, .. } => {
            find_function_calls(value, calls);
        }
        AstNode::DisplayStatement { value } => {
            find_function_calls(value, calls);
        }
        AstNode::ReturnStatement { value: Some(value) } => {
            find_function_calls(value, calls);
        }
        AstNode::IfStatement { condition, then_block, else_block } => {
            find_function_calls(condition, calls);
            for stmt in then_block {
                find_function_calls(stmt, calls);
            }
            if let Some(else_stmts) = else_block {
                for stmt in else_stmts {
                    find_function_calls(stmt, calls);
                }
            }
        }
        AstNode::WhileStatement { condition, body } => {
            find_function_calls(condition, calls);
            for stmt in body {
                find_function_calls(stmt, calls);
            }
        }
        AstNode::ProcessDefinition { body, .. } => {
            for stmt in body {
                find_function_calls(stmt, calls);
            }
        }
        _ => {} // Other nodes don't contain function calls
    }
}

fn find_defined_functions(ast: &AstNode, functions: &mut HashSet<String>) {
    match ast {
        AstNode::Program(statements) => {
            for stmt in statements {
                find_defined_functions(stmt, functions);
            }
        }
        AstNode::ProcessDefinition { name, .. } => {
            functions.insert(name.clone());
        }
        _ => {} // Other nodes don't define functions
    }
}

fn compile_with_dependencies(input_file: &str, output_file: &str) -> Result<(), String> {
    let main_source = fs::read_to_string(input_file)
        .map_err(|e| format!("Error reading file {}: {}", input_file, e))?;

    // Parse main file to find function calls
    let mut lexer = Lexer::new(&main_source);
    let tokens = lexer.tokenize()
        .map_err(|e| format!("Lexer error in {}: {}", input_file, e))?;

    let mut parser = Parser::new(tokens);
    let main_ast = parser.parse()
        .map_err(|e| format!("Parser error in {}: {}", input_file, e))?;

    // Options from CLI/env
    let mut no_dir_scan = env::var("RUNA_NO_DIR_SCAN").ok().map(|v| v == "1" || v.eq_ignore_ascii_case("true")).unwrap_or(false);
    let mut emit_asm_only = env::var("RUNA_EMIT_ASM_ONLY").ok().map(|v| v == "1" || v.eq_ignore_ascii_case("true")).unwrap_or(false);
    let mut preferred_linker = env::var("RUNA_LINKER").ok();
    let mut source_roots: Vec<PathBuf> = env::var("RUNA_SOURCE_ROOTS").ok()
        .map(|v| v.split(';').filter(|s| !s.is_empty()).map(|s| PathBuf::from(s)).collect())
        .unwrap_or_else(|| Vec::new());

    // Also parse extra CLI flags beyond <input> <output>
    let args: Vec<String> = env::args().collect();
    if args.len() > 3 {
        for flag in &args[3..] {
            if flag == "--no-dir-scan" { no_dir_scan = true; }
            else if flag == "--emit-asm-only" { emit_asm_only = true; }
            else if let Some(rest) = flag.strip_prefix("--linker=") { preferred_linker = Some(rest.to_string()); }
            else if let Some(rest) = flag.strip_prefix("--source-root=") { source_roots.push(PathBuf::from(rest)); }
        }
    }

    // Always process dependencies first, then check for missing functions
    // Import-driven module loading with directory-scan fallback
    fn collect_import_paths(ast: &AstNode, acc: &mut Vec<String>) {
        match ast {
            AstNode::Program(stmts) => { for s in stmts { collect_import_paths(s, acc); } }
            AstNode::ImportStatement { module_path, .. } => { acc.push(module_path.clone()); }
            AstNode::ProcessDefinition { body, .. } => { for s in body { collect_import_paths(s, acc); } }
            AstNode::IfStatement { then_block, else_block, .. } => {
                for s in then_block { collect_import_paths(s, acc); }
                if let Some(else_stmts) = else_block { for s in else_stmts { collect_import_paths(s, acc); } }
            }
            AstNode::WhileStatement { body, .. } => { for s in body { collect_import_paths(s, acc); } }
            _ => {}
        }
    }

    // Resolve a module path to a file on disk using entry dir then source roots
    fn resolve_module(input_dir: &Path, module: &str, roots: &[PathBuf]) -> Option<PathBuf> {
        let candidates = [input_dir.to_path_buf()].into_iter().chain(roots.iter().cloned());
        for base in candidates {
            let mut p = base.join(module);
            if p.extension().and_then(|s| s.to_str()) != Some("runa") {
                p.set_extension("runa");
            }
            if p.exists() { return Some(p); }
        }
        None
    }

    let input_dir = Path::new(input_file).parent().unwrap_or(Path::new("."));
    let mut to_visit: Vec<PathBuf> = Vec::new();
    let mut visited: HashSet<PathBuf> = HashSet::new();
    let mut dependency_asts = Vec::new();

    // Seed imports from main AST
    let mut initial_imports = Vec::new();
    collect_import_paths(&main_ast, &mut initial_imports);
    for m in initial_imports {
        if let Some(resolved) = resolve_module(input_dir, &m, &source_roots) {
            to_visit.push(resolved);
        } else {
            return Err(format!("Import not found: {}", m));
        }
    }

    // BFS load imports
    while let Some(path) = to_visit.pop() {
        let can = match fs::canonicalize(&path) { Ok(p) => p, Err(_) => path.clone() };
        if visited.contains(&can) { continue; }
        visited.insert(can.clone());

        let dep_source = fs::read_to_string(&path)
            .map_err(|e| format!("Error reading dependency {}: {}", path.display(), e))?;
        let mut dep_lexer = Lexer::new(&dep_source);
        let dep_tokens = dep_lexer.tokenize()
            .map_err(|e| format!("Lexer error in {}: {}", path.display(), e))?;
        let mut dep_parser = Parser::new(dep_tokens);
        let dep_ast = dep_parser.parse()
            .map_err(|e| format!("Parser error in {}: {}", path.display(), e))?;

        // Collect transitive imports
        let mut more = Vec::new();
        collect_import_paths(&dep_ast, &mut more);
        for m in more {
            if let Some(resolved) = resolve_module(input_dir, &m, &source_roots) {
                to_visit.push(resolved);
            } else {
                return Err(format!("Import not found: {}", m));
            }
        }

        dependency_asts.push(dep_ast);
    }

    // Fallback to directory scan when no imports and scanning allowed
    if dependency_asts.is_empty() && !no_dir_scan {
        for entry in fs::read_dir(input_dir).map_err(|e| format!("Error reading directory: {}", e))? {
            let entry = entry.map_err(|e| format!("Error reading directory entry: {}", e))?;
            let path = entry.path();
            if path.extension().and_then(|s| s.to_str()) == Some("runa") && path != Path::new(input_file) {
                let dep_source = fs::read_to_string(&path)
                    .map_err(|e| format!("Error reading dependency {}: {}", path.display(), e))?;
                let mut dep_lexer = Lexer::new(&dep_source);
                let dep_tokens = dep_lexer.tokenize()
                    .map_err(|e| format!("Lexer error in {}: {}", path.display(), e))?;
                let mut dep_parser = Parser::new(dep_tokens);
                let dep_ast = dep_parser.parse()
                    .map_err(|e| format!("Parser error in {}: {}", path.display(), e))?;
                dependency_asts.push(dep_ast);
            }
        }
    }

    // Now find all function calls and definitions (including dependencies)
    let mut called_functions = HashSet::new();
    let mut defined_functions = HashSet::new();

    find_function_calls(&main_ast, &mut called_functions);
    find_defined_functions(&main_ast, &mut defined_functions);

    // Also find defined functions in all dependencies
    for dep_ast in &dependency_asts {
        find_defined_functions(dep_ast, &mut defined_functions);
    }

    // Filter out built-in functions from called_functions
    let builtin_functions: HashSet<String> = [
        "length_of", "read_file", "write_file", "concat", "substring", "to_string", "char_at"
    ].iter().map(|s| s.to_string()).collect();

    let user_called_functions: HashSet<String> = called_functions
        .difference(&builtin_functions)
        .cloned()
        .collect();

    // Find missing functions that need to be imported (excluding built-ins)
    let missing_functions: Vec<String> = user_called_functions
        .difference(&defined_functions)
        .cloned()
        .collect();

    // println!("Missing functions: {:?}", missing_functions);
    // println!("Called functions: {:?}", called_functions);
    // println!("Defined functions: {:?}", defined_functions);
    // println!("User called functions: {:?}", user_called_functions);

    if missing_functions.is_empty() && dependency_asts.is_empty() {
        // No dependencies, compile normally
        compile_single_file(input_file, output_file)
    } else {
        // Combine ASTs with dependencies (dependencies already processed above)
        // FIXED: Combine ASTs in correct order - ALL globals first, then functions, then execution
        let mut combined_statements = Vec::new();
        let mut seen_functions = HashSet::new();
        let mut all_functions = Vec::new();
        let mut main_execution_statements = Vec::new();
        let mut all_globals = Vec::new();

        // Step 1: Collect dependency globals FIRST (must be processed before any function bodies)
        for dep_ast in &dependency_asts {
            match dep_ast {
                AstNode::Program(dep_statements) => {
                    for stmt in dep_statements {
                        match &stmt {
                            // Collect global variable declarations from dependencies
                            AstNode::GlobalLetStatement { .. } => {
                                all_globals.push(stmt.clone());
                            }
                            _ => {}
                        }
                    }
                }
                _ => {}
            }
        }

        // Step 2: Collect functions from main and dependencies, and collect main-file globals
        match main_ast {
            AstNode::Program(main_statements) => {
                for stmt in main_statements {
                    match &stmt {
                        AstNode::ProcessDefinition { name, .. } => {
                            seen_functions.insert(name.clone());
                            all_functions.push(stmt);
                        }
                        // Collect top-level globals from main file
                        AstNode::GlobalLetStatement { .. } => {
                            all_globals.push(stmt);
                        }
                        // All other main execution statements (Display, If, While, etc.)
                        _ => {
                            main_execution_statements.push(stmt);
                        }
                    }
                }
            }
            other => main_execution_statements.push(other),
        }

        // Add dependency functions (avoiding duplicates)
        for dep_ast in dependency_asts {
            match dep_ast {
                AstNode::Program(dep_statements) => {
                    for stmt in dep_statements {
                        match &stmt {
                            AstNode::ProcessDefinition { name, .. } => {
                                if !seen_functions.contains(name) {
                                    seen_functions.insert(name.clone());
                                    all_functions.push(stmt);
                                }
                            }
                            _ => {} // Globals already collected, skip other statements
                        }
                    }
                }
                _ => {}
            }
        }

        // Step 3: Combine in CORRECT order - globals first, then functions, then execution
        // 1. ALL globals first (ensures type checker state is initialized)
        for global in all_globals {
            combined_statements.push(global);
        }
        // 2. ALL functions second (can reference globals safely)
        for function in all_functions {
            combined_statements.push(function);
        }
        // 3. Main execution statements last (can reference both globals and functions)
        for exec_stmt in main_execution_statements {
            combined_statements.push(exec_stmt);
        }

        let combined_ast = AstNode::Program(combined_statements);

        // Type check combined AST
        let mut typechecker = TypeChecker::new();
        typechecker.check(&combined_ast)
            .map_err(|e| format!("Type error: {}", e))?;

        // Generate code for combined AST
        // Multi-module pipeline: emit .s/.o per module and link
        let temp_dir = Path::new(output_file).parent().unwrap_or(Path::new(".")).join(".runa_build");
        if !temp_dir.exists() { fs::create_dir_all(&temp_dir).map_err(|e| format!("Error creating temp dir: {}", e))?; }

        // Collect modules: per-source plan (first pass approximation)
        // 1) Library objects: functions only
        let mut codegen_lib = CodeGenerator::new();
        let lib_asm = codegen_lib.generate_lib(&combined_ast)
            .map_err(|e| format!("Code generation error (lib): {}", e))?;
        let lib_s = temp_dir.join("module_lib.s");
        fs::write(&lib_s, lib_asm).map_err(|e| format!("Write asm failed: {}", e))?;
        let lib_o = temp_dir.join("module_lib.o");
        assemble_to_object(&lib_s, &lib_o, preferred_linker.as_deref())?;

        // 2) Main object: real main from AST
        let mut codegen_main = CodeGenerator::new();
        let main_asm = codegen_main.generate_main_only(&combined_ast)
            .map_err(|e| format!("Code generation error (main): {}", e))?;
        let main_s = temp_dir.join("__main.s");
        fs::write(&main_s, main_asm).map_err(|e| format!("Write main asm failed: {}", e))?;
        let main_o = temp_dir.join("__main.o");
        assemble_to_object(&main_s, &main_o, preferred_linker.as_deref())?;

        // Link all objects with runtime
        link_objects(&[lib_o.as_path(), main_o.as_path()], output_file, preferred_linker.as_deref())
    }
}

fn compile_single_file(input_file: &str, output_file: &str) -> Result<(), String> {
    let source = fs::read_to_string(input_file)
        .map_err(|e| format!("Error reading file {}: {}", input_file, e))?;

    let mut lexer = Lexer::new(&source);
    let tokens = lexer.tokenize()
        .map_err(|e| format!("Lexer error: {}", e))?;

    let mut parser = Parser::new(tokens);
    let ast = parser.parse()
        .map_err(|e| format!("Parser error: {}", e))?;

    let mut typechecker = TypeChecker::new();
    typechecker.check(&ast)
        .map_err(|e| format!("Type error: {}", e))?;

    let mut codegen = CodeGenerator::new();
    let assembly = codegen.generate(&ast)
        .map_err(|e| format!("Code generation error: {}", e))?;

    // Honor options from env (emit-asm-only, linker)
    let emit_asm_only = env::var("RUNA_EMIT_ASM_ONLY").ok().map(|v| v == "1" || v.eq_ignore_ascii_case("true")).unwrap_or(false);
    let preferred_linker = env::var("RUNA_LINKER").ok();
    write_and_assemble_with_options(&assembly, output_file, preferred_linker.as_deref(), emit_asm_only)
}

fn which(prog: &str) -> Option<String> {
    // Very simple PATH scan
    if let Ok(path) = env::var("PATH") {
        for dir in path.split(if cfg!(windows) { ';' } else { ':' }) {
            let p = Path::new(dir).join(prog);
            if p.exists() { return Some(p.to_string_lossy().to_string()); }
            // On Windows, also try .exe
            if cfg!(windows) {
                let pe = Path::new(dir).join(format!("{}.exe", prog));
                if pe.exists() { return Some(pe.to_string_lossy().to_string()); }
            }
        }
    }
    None
}

fn to_wsl_path<P: AsRef<Path>>(p: P) -> Result<String, String> {
    let p = p.as_ref();
    if p.exists() {
        let abs = fs::canonicalize(p).map_err(|e| format!("Path canonicalize failed for {}: {}", p.display(), e))?;
        return windows_abs_to_wsl(&abs);
    }
    // If path doesn't exist (e.g., output), canonicalize parent and append file name
    if let Some(parent) = p.parent() {
        let abs_parent = fs::canonicalize(parent)
            .map_err(|e| format!("Parent canonicalize failed for {}: {}", parent.display(), e))?;
        let joined = abs_parent.join(p.file_name().unwrap_or_default());
        return windows_abs_to_wsl(&joined);
    }
    // Fallback: best-effort string conversion
    windows_abs_to_wsl(p)
}

fn windows_abs_to_wsl<P: AsRef<Path>>(p: P) -> Result<String, String> {
    let mut s = p.as_ref().to_string_lossy().replace('\\', "/");
    // Normalize Windows extended path prefix (//?/) if present
    if s.starts_with("//?/") {
        s = s[4..].to_string();
    }
    if s.len() > 2 && s.as_bytes()[1] == b':' {
        let drive = s.chars().next().unwrap().to_ascii_lowercase();
        let rest = &s[2..];
        Ok(format!("/mnt/{}/{}", drive, rest.trim_start_matches('/')))
    } else {
        Ok(s)
    }
}

fn write_and_assemble_with_options(assembly: &str, output_file: &str, linker_opt: Option<&str>, emit_asm_only: bool) -> Result<(), String> {
    let asm_file = format!("{}.s", output_file);
    fs::write(&asm_file, assembly)
        .map_err(|e| format!("Error writing assembly file: {}", e))?;

    if emit_asm_only {
        println!("Emitted assembly to {} (linking skipped by --emit-asm-only)", asm_file);
        return Ok(());
    }

    // Path to the v0.1 runtime library - try multiple locations
    let runtime_paths = [
        "../v0.1_microruna-compiler/runtime/libruna_runtime.a",
        "../../v0.1_microruna-compiler/runtime/libruna_runtime.a",
        "./runa/bootstrap/v0.1_microruna-compiler/runtime/libruna_runtime.a",
        "/mnt/d/SybertneticsUmbrella/SybertneticsAISolutions/MonoRepo/runa/bootstrap/v0.1_microruna-compiler/runtime/libruna_runtime.a"
    ];

    let runtime_lib_path = runtime_paths.iter()
        .find(|path| Path::new(path).exists())
        .ok_or("Runtime library not found in any expected location")?;

    // Choose linker: prefer explicit, then clang, then gcc
    let chosen = if let Some(l) = linker_opt { l.to_string() }
                 else if which("clang").is_some() { "clang".to_string() }
                 else { "gcc".to_string() };

    // If using WSL linker, run through "wsl" and convert paths
    let status = if chosen == "wsl-clang" || chosen == "wsl-gcc" {
        let tool = if chosen == "wsl-clang" { "clang" } else { "gcc" };
        let asm_wsl = to_wsl_path(&asm_file)?;
        let out_wsl = to_wsl_path(output_file)?;
        // Convert runtime path to WSL if needed
        let rt_wsl = if runtime_lib_path.starts_with("/mnt/") { runtime_lib_path.to_string() } else { to_wsl_path(runtime_lib_path)? };
        // Prefer dynamic link on WSL to avoid static glibc issues
        process::Command::new("wsl")
            .args(&[tool, "-o", &out_wsl, &asm_wsl, &rt_wsl, "-fuse-ld=lld"])
            .status()
            .map_err(|e| format!("Error invoking WSL {}: {}. Ensure WSL and {} are installed, or use --emit-asm-only.", tool, e, tool))?
    } else {
        // Native Windows or Unix toolchain on PATH
        // Keep static on native Unix; on Windows this path is unlikely to work
        process::Command::new(&chosen)
            .args(&["-o", output_file, &asm_file, runtime_lib_path, "-static"]) // static link
            .status()
            .map_err(|e| format!("Error invoking {}: {}. Use --emit-asm-only or set RUNA_EMIT_ASM_ONLY=1 to skip linking.", chosen, e))?
    };

    if status.success() {
        println!("Successfully compiled to {} (with v0.1 runtime) using {}", output_file, chosen);
        Ok(())
    } else {
        Err("Assembly/linking failed".to_string())
    }
}

fn assemble_to_object(asm_path: &Path, obj_path: &Path, linker_opt: Option<&str>) -> Result<(), String> {
    // Prefer clang -c; if RUNA_LINKER or explicit linker is wsl-*, use WSL clang
    let linker = linker_opt.map(|s| s.to_string()).or_else(|| env::var("RUNA_LINKER").ok());
    if matches!(linker.as_deref(), Some("wsl-clang") | Some("wsl-gcc")) {
        let asm_wsl = to_wsl_path(asm_path)?;
        let obj_wsl = to_wsl_path(obj_path)?;
        let tool = if linker.as_deref() == Some("wsl-gcc") { "gcc" } else { "clang" };
        let status = process::Command::new("wsl")
            .args(&[tool, "-c", &asm_wsl, "-o", &obj_wsl])
            .status()
            .map_err(|e| format!("WSL assemble failed: {}", e))?;
        if status.success() { Ok(()) } else { Err("WSL assemble failed".to_string()) }
    } else {
        let tool = which("clang").or_else(|| which("gcc")).ok_or("No assembler (clang/gcc) found in PATH")?;
        let status = process::Command::new(tool)
            .args(&["-c", &asm_path.to_string_lossy(), "-o", &obj_path.to_string_lossy()])
            .status()
            .map_err(|e| format!("Assemble failed: {}", e))?;
        if status.success() { Ok(()) } else { Err("Assemble failed".to_string()) }
    }
}

fn link_objects(objs: &[&Path], output_file: &str, linker_opt: Option<&str>) -> Result<(), String> {
    // Runtime library resolution
    let runtime_paths = [
        "../v0.1_microruna-compiler/runtime/libruna_runtime.a",
        "../../v0.1_microruna-compiler/runtime/libruna_runtime.a",
        "./runa/bootstrap/v0.1_microruna-compiler/runtime/libruna_runtime.a",
        "/mnt/d/SybertneticsUmbrella/SybertneticsAISolutions/MonoRepo/runa/bootstrap/v0.1_microruna-compiler/runtime/libruna_runtime.a"
    ];
    let runtime_lib_path = runtime_paths.iter()
        .find(|path| Path::new(path).exists())
        .ok_or("Runtime library not found in any expected location")?;

    let linker = linker_opt.unwrap_or("clang");
    if linker == "wsl-clang" || linker == "wsl-gcc" {
        let tool = if linker == "wsl-gcc" { "gcc" } else { "clang" };
        let mut args: Vec<String> = Vec::new();
        args.push("-o".into()); args.push(to_wsl_path(output_file)?.into());
        for o in objs { args.push(to_wsl_path(o)?) }
        let rt = if runtime_lib_path.starts_with("/mnt/") { runtime_lib_path.to_string() } else { to_wsl_path(runtime_lib_path)? };
        args.push(rt);
        args.push("-fuse-ld=lld".into());
        let status = process::Command::new("wsl")
            .args([tool].iter().map(|s| s.to_string()).chain(args.into_iter()).collect::<Vec<String>>())
            .status()
            .map_err(|e| format!("WSL link failed: {}", e))?;
        if status.success() { Ok(()) } else { Err("WSL link failed".to_string()) }
    } else {
        let tool = which(linker).unwrap_or("clang".into());
        let mut cmd = process::Command::new(&tool);
        cmd.arg("-o").arg(output_file);
        for o in objs { cmd.arg(o); }
        cmd.arg(runtime_lib_path).arg("-static");
        let status = cmd.status().map_err(|e| format!("Link failed: {}", e))?;
        if status.success() { Ok(()) } else { Err("Link failed".to_string()) }
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 {
        eprintln!("Usage: {} <input.runa> <output> [--no-dir-scan] [--source-root=<dir>] [--emit-asm-only] [--linker=clang|gcc]", args[0]);
        process::exit(1);
    }

    let input_file = &args[1];
    let output_file = &args[2];

    // Debug mode: print tokens
    if output_file == "debug" {
        let source = match fs::read_to_string(input_file) {
            Ok(content) => content,
            Err(err) => {
                eprintln!("Error reading file {}: {}", input_file, err);
                process::exit(1);
            }
        };

        let mut lexer = Lexer::new(&source);
        let tokens = match lexer.tokenize() {
            Ok(tokens) => tokens,
            Err(err) => {
                eprintln!("Lexer error: {}", err);
                process::exit(1);
            }
        };

        for token in &tokens {
            println!("{:?}", token);
        }
        process::exit(0);
    }

    // Compile with dependency resolution
    if let Err(err) = compile_with_dependencies(input_file, output_file) {
        eprintln!("{}", err);
        process::exit(1);
    }
}
