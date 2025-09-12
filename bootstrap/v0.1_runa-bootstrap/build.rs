use std::env;
use std::path::PathBuf;
use std::process::Command;

fn main() {
    // Check for LLVM installation
    if let Err(e) = check_llvm_installation() {
        panic!("LLVM installation check failed: {}", e);
    }
    
    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:rerun-if-env-changed=LLVM_SYS_170_PREFIX");
}

fn check_llvm_installation() -> Result<(), String> {
    // Check if llvm-config is available
    let llvm_config_commands = vec![
        "llvm-config-17",
        "llvm-config-170", 
        "llvm-config",
    ];
    
    for cmd in &llvm_config_commands {
        if let Ok(output) = Command::new(cmd).arg("--version").output() {
            if output.status.success() {
                let version = String::from_utf8_lossy(&output.stdout);
                println!("cargo:warning=Found LLVM version: {}", version.trim());
                
                // Set LLVM config command for the build
                println!("cargo:rustc-env=LLVM_CONFIG_CMD={}", cmd);
                
                return Ok(());
            }
        }
    }
    
    // Check if LLVM_SYS_170_PREFIX is set
    if let Ok(prefix) = env::var("LLVM_SYS_170_PREFIX") {
        let llvm_config = PathBuf::from(&prefix).join("bin").join("llvm-config");
        if llvm_config.exists() {
            println!("cargo:warning=Using LLVM from LLVM_SYS_170_PREFIX: {}", prefix);
            return Ok(());
        }
    }
    
    Err("LLVM 17 not found. Please install LLVM 17 or set LLVM_SYS_170_PREFIX environment variable.".to_string())
}