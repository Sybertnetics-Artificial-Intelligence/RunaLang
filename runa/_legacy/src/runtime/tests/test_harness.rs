//! Runa Test Harness
// Recursively discovers and runs all .runa files in the tests/ directory.
// For each .runa file, runs it with runac.exe and compares output to .out file if present.

use std::fs;
use std::io::Read;
use std::path::{Path, PathBuf};
use std::process::Command;

/// Recursively find all .runa files in the given directory.
fn find_runa_files(dir: &Path, files: &mut Vec<PathBuf>) {
    if let Ok(entries) = fs::read_dir(dir) {
        for entry in entries.flatten() {
            let path = entry.path();
            if path.is_dir() {
                find_runa_files(&path, files);
            } else if let Some(ext) = path.extension() {
                if ext == "runa" {
                    files.push(path);
                }
            }
        }
    }
}

#[test]
fn run_all_runa_tests() {
    let mut files = Vec::new();
    let test_dir = Path::new("tests");
    find_runa_files(test_dir, &mut files);
    assert!(!files.is_empty(), "No .runa test files found in tests/ directory");

    let runac_path = Path::new("target/debug/runac.exe");
    assert!(runac_path.exists(), "runac.exe not found at {:?}", runac_path);

    let mut failures = Vec::new();

    for file in files {
        let output = Command::new(runac_path)
            .arg(&file)
            .output()
            .expect("Failed to execute runac.exe");
        let stdout = String::from_utf8_lossy(&output.stdout);
        let stderr = String::from_utf8_lossy(&output.stderr);
        let combined_output = format!("{}{}", stdout, stderr);

        // Check for .out file
        let out_path = file.with_extension("out");
        if out_path.exists() {
            let mut expected = String::new();
            fs::File::open(&out_path)
                .and_then(|mut f| f.read_to_string(&mut expected))
                .expect(&format!("Failed to read expected output file: {:?}", out_path));
            if combined_output.trim() != expected.trim() {
                failures.push((file.clone(), expected, combined_output.to_string()));
            }
        } else if !output.status.success() {
            failures.push((file.clone(), String::from("<no .out file, expected success>"), combined_output.to_string()));
        }
    }

    if !failures.is_empty() {
        for (file, expected, actual) in &failures {
            eprintln!("\nTest failed: {}", file.display());
            eprintln!("Expected:\n{}\n---\nActual:\n{}\n", expected, actual);
        }
        panic!("{} test(s) failed", failures.len());
    }
} 