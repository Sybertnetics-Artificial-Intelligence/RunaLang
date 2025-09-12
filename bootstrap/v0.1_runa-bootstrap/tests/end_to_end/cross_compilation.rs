// End-to-end tests for cross-compilation functionality

use runa_bootstrap::compiler::CompilerDriver;
use runa_bootstrap::utils::diagnostics::DiagnosticEngine;
use runa_bootstrap::runtime::platform::Platform;
use std::fs;
use tempfile::TempDir;

#[test]
fn test_cross_compile_to_different_targets() {
    let temp_dir = TempDir::new().expect("Failed to create temp directory");
    let input_file = temp_dir.path().join("cross_test.runa");
    
    let program = r#"
Process called "main" returns Integer:
    Let result be 123
    Return result
End Process
    "#;
    
    fs::write(&input_file, program).expect("Failed to write test file");
    
    let targets = vec![
        "linux_x64",
        "linux_arm64", 
        "windows_x64",
        "macos_x64",
        "macos_arm64",
        "freebsd_x64",
    ];
    
    for target in targets {
        let output_file = temp_dir.path().join(format!("cross_test_{}", target));
        let mut diagnostic_engine = DiagnosticEngine::new();
        let mut compiler = CompilerDriver::new(&mut diagnostic_engine);
        
        // Cross-compilation should not produce compile errors
        // (linking may fail without proper target libraries, but that's expected)
        let result = compiler.compile_file(&input_file, &output_file, target, 2);
        
        if diagnostic_engine.has_errors() {
            panic!("Cross-compilation to {} failed with errors: {:?}", 
                   target, diagnostic_engine.diagnostics());
        }
        
        if let Err(e) = result {
            // Linking errors are expected in test environment
            println!("Note: Linking may fail for target {} in test environment: {}", target, e);
        }
    }
}

#[test]
fn test_platform_detection() {
    let current_platform = Platform::current();
    
    // Should detect some valid platform
    assert!(matches!(current_platform, 
        Platform::LinuxX64 | Platform::LinuxArm64 |
        Platform::WindowsX64 | Platform::WindowsArm64 |
        Platform::MacOsX64 | Platform::MacOsArm64 |
        Platform::FreeBsdX64 | Platform::OpenBsdX64 | Platform::NetBsdX64
    ));
}

#[test]
fn test_target_string_parsing() {
    let test_cases = vec![
        ("linux_x64", Some(Platform::LinuxX64)),
        ("windows_arm64", Some(Platform::WindowsArm64)),
        ("macos_x64", Some(Platform::MacOsX64)),
        ("freebsd_x64", Some(Platform::FreeBsdX64)),
        ("invalid_target", None),
        ("host", Some(Platform::current())),
    ];
    
    for (target_str, expected) in test_cases {
        let result = Platform::from_target_string(target_str);
        assert_eq!(result, expected, "Failed for target: {}", target_str);
    }
}

#[test]
fn test_platform_properties() {
    let linux_x64 = Platform::LinuxX64;
    let windows_x64 = Platform::WindowsX64;
    let macos_arm64 = Platform::MacOsArm64;
    
    // Test file extensions
    assert_eq!(linux_x64.executable_extension(), "");
    assert_eq!(windows_x64.executable_extension(), ".exe");
    assert_eq!(macos_arm64.executable_extension(), "");
    
    // Test shared library extensions
    assert_eq!(linux_x64.shared_library_extension(), ".so");
    assert_eq!(windows_x64.shared_library_extension(), ".dll");
    assert_eq!(macos_arm64.shared_library_extension(), ".dylib");
    
    // Test Unix-like detection
    assert!(linux_x64.is_unix_like());
    assert!(!windows_x64.is_unix_like());
    assert!(macos_arm64.is_unix_like());
}