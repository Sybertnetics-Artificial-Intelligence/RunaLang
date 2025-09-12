// Platform-specific functionality for the bootstrap compiler

use std::env;

#[derive(Debug, Clone, PartialEq)]
pub enum Platform {
    LinuxX64,
    LinuxArm64,
    WindowsX64,
    WindowsArm64,
    MacOsX64,
    MacOsArm64,
    FreeBsdX64,
    OpenBsdX64,
    NetBsdX64,
}

#[derive(Debug, Clone, PartialEq)]
pub enum Architecture {
    X86_64,
    Aarch64,
}

#[derive(Debug, Clone, PartialEq)]
pub enum OperatingSystem {
    Linux,
    Windows,
    MacOs,
    FreeBsd,
    OpenBsd,
    NetBsd,
}

impl Platform {
    pub fn current() -> Platform {
        match (env::consts::OS, env::consts::ARCH) {
            ("linux", "x86_64") => Platform::LinuxX64,
            ("linux", "aarch64") => Platform::LinuxArm64,
            ("windows", "x86_64") => Platform::WindowsX64,
            ("windows", "aarch64") => Platform::WindowsArm64,
            ("macos", "x86_64") => Platform::MacOsX64,
            ("macos", "aarch64") => Platform::MacOsArm64,
            ("freebsd", "x86_64") => Platform::FreeBsdX64,
            ("openbsd", "x86_64") => Platform::OpenBsdX64,
            ("netbsd", "x86_64") => Platform::NetBsdX64,
            _ => Platform::LinuxX64, // Default fallback
        }
    }
    
    pub fn from_target_string(target: &str) -> Option<Platform> {
        match target {
            "linux_x64" => Some(Platform::LinuxX64),
            "linux_arm64" => Some(Platform::LinuxArm64),
            "windows_x64" => Some(Platform::WindowsX64),
            "windows_arm64" => Some(Platform::WindowsArm64),
            "macos_x64" => Some(Platform::MacOsX64),
            "macos_arm64" => Some(Platform::MacOsArm64),
            "freebsd_x64" => Some(Platform::FreeBsdX64),
            "openbsd_x64" => Some(Platform::OpenBsdX64),
            "netbsd_x64" => Some(Platform::NetBsdX64),
            "host" => Some(Platform::current()),
            _ => None,
        }
    }
    
    pub fn operating_system(&self) -> OperatingSystem {
        match self {
            Platform::LinuxX64 | Platform::LinuxArm64 => OperatingSystem::Linux,
            Platform::WindowsX64 | Platform::WindowsArm64 => OperatingSystem::Windows,
            Platform::MacOsX64 | Platform::MacOsArm64 => OperatingSystem::MacOs,
            Platform::FreeBsdX64 => OperatingSystem::FreeBsd,
            Platform::OpenBsdX64 => OperatingSystem::OpenBsd,
            Platform::NetBsdX64 => OperatingSystem::NetBsd,
        }
    }
    
    pub fn architecture(&self) -> Architecture {
        match self {
            Platform::LinuxX64 | Platform::WindowsX64 | Platform::MacOsX64 
            | Platform::FreeBsdX64 | Platform::OpenBsdX64 | Platform::NetBsdX64 => {
                Architecture::X86_64
            }
            Platform::LinuxArm64 | Platform::WindowsArm64 | Platform::MacOsArm64 => {
                Architecture::Aarch64
            }
        }
    }
    
    pub fn executable_extension(&self) -> &'static str {
        match self.operating_system() {
            OperatingSystem::Windows => ".exe",
            _ => "",
        }
    }
    
    pub fn shared_library_extension(&self) -> &'static str {
        match self.operating_system() {
            OperatingSystem::Windows => ".dll",
            OperatingSystem::MacOs => ".dylib",
            _ => ".so",
        }
    }
    
    pub fn static_library_extension(&self) -> &'static str {
        match self.operating_system() {
            OperatingSystem::Windows => ".lib",
            _ => ".a",
        }
    }
    
    pub fn object_file_extension(&self) -> &'static str {
        match self.operating_system() {
            OperatingSystem::Windows => ".obj",
            _ => ".o",
        }
    }
    
    pub fn path_separator(&self) -> char {
        match self.operating_system() {
            OperatingSystem::Windows => '\\',
            _ => '/',
        }
    }
    
    pub fn path_delimiter(&self) -> char {
        match self.operating_system() {
            OperatingSystem::Windows => ';',
            _ => ':',
        }
    }
    
    pub fn is_unix_like(&self) -> bool {
        !matches!(self.operating_system(), OperatingSystem::Windows)
    }
    
    pub fn supports_position_independent_executables(&self) -> bool {
        // All modern platforms support PIE
        true
    }
    
    pub fn default_linker(&self) -> &'static str {
        match self.operating_system() {
            OperatingSystem::Windows => "link.exe",
            OperatingSystem::MacOs => "ld",
            _ => "ld",
        }
    }
    
    pub fn system_include_paths(&self) -> Vec<&'static str> {
        match self.operating_system() {
            OperatingSystem::Linux => vec![
                "/usr/include",
                "/usr/local/include",
                "/usr/include/x86_64-linux-gnu",
            ],
            OperatingSystem::MacOs => vec![
                "/usr/include",
                "/usr/local/include",
                "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include",
            ],
            OperatingSystem::FreeBsd => vec![
                "/usr/include",
                "/usr/local/include",
            ],
            OperatingSystem::OpenBsd => vec![
                "/usr/include",
                "/usr/local/include",
            ],
            OperatingSystem::NetBsd => vec![
                "/usr/include",
                "/usr/pkg/include",
            ],
            OperatingSystem::Windows => vec![
                // Windows SDK paths would go here
            ],
        }
    }
    
    pub fn system_library_paths(&self) -> Vec<&'static str> {
        match self.operating_system() {
            OperatingSystem::Linux => vec![
                "/lib",
                "/usr/lib",
                "/usr/local/lib",
                "/lib/x86_64-linux-gnu",
                "/usr/lib/x86_64-linux-gnu",
            ],
            OperatingSystem::MacOs => vec![
                "/usr/lib",
                "/usr/local/lib",
            ],
            OperatingSystem::FreeBsd => vec![
                "/lib",
                "/usr/lib",
                "/usr/local/lib",
            ],
            OperatingSystem::OpenBsd => vec![
                "/lib",
                "/usr/lib",
                "/usr/local/lib",
            ],
            OperatingSystem::NetBsd => vec![
                "/lib",
                "/usr/lib",
                "/usr/pkg/lib",
            ],
            OperatingSystem::Windows => vec![
                // Windows system library paths would go here
            ],
        }
    }
}