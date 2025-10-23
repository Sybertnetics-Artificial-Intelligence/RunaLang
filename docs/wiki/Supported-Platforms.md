# Supported Platforms

Runa is designed to be a truly cross-platform language, supporting a wide range of operating systems and architectures.

## Overview

Runa compiles to native code for maximum performance and portability. The compiler supports multiple platforms through platform-specific backends for code generation, syscalls, and calling conventions.

## Tier 1 Platforms (Fully Supported)

These platforms receive the highest level of support and testing:

### Linux
- **x86_64** (64-bit Intel/AMD)
  - Ubuntu 20.04+
  - Debian 10+
  - Fedora 35+
  - Arch Linux
  - CentOS/RHEL 8+

- **ARM64** (AArch64)
  - Raspberry Pi 4+
  - AWS Graviton
  - Apple Silicon via Rosetta (native macOS support available)

- **ARM32** (ARMv7)
  - Raspberry Pi 2/3
  - Embedded Linux systems

### macOS (Darwin)
- **x86_64** (Intel Macs)
  - macOS 10.15 Catalina or later

- **ARM64** (Apple Silicon)
  - macOS 11.0 Big Sur or later
  - M1, M2, M3 processors

### Windows
- **x86_64** (64-bit)
  - Windows 10 (version 1809 or later)
  - Windows 11
  - Windows Server 2019+

- **ARM64** (AArch64)
  - Windows 11 ARM64
  - Surface Pro X

## Tier 2 Platforms (Supported)

These platforms are supported but may receive less frequent testing:

### BSD Variants

#### FreeBSD
- **x64** (x86_64)
  - FreeBSD 12.0+
- **ARM64** (AArch64)
  - FreeBSD 13.0+

#### NetBSD
- **x64** (x86_64)
  - NetBSD 9.0+
- **ARM64** (AArch64)
  - NetBSD 9.0+

#### OpenBSD
- **x64** (x86_64)
  - OpenBSD 6.8+
- **ARM64** (AArch64)
  - OpenBSD 7.0+

## Tier 3 Platforms (Experimental)

These platforms have basic support but are still under development:

### RISC-V
- **RISC-V 64-bit** (RV64)
  - Linux distributions
  - Embedded systems

- **RISC-V 32-bit** (RV32)
  - Embedded systems
  - IoT devices

### MIPS
- **MIPS64**
  - Linux distributions
  - Legacy systems

- **MIPS32**
  - Embedded systems
  - Routers and network equipment

### PowerPC
- **PowerPC 64-bit**
  - Linux on POWER8/POWER9
  - Legacy systems

## Architecture Support Matrix

| OS/Architecture | x86_64 | ARM64 | ARM32 | RISC-V 64 | RISC-V 32 | MIPS64 | MIPS32 | PowerPC |
|-----------------|--------|-------|-------|-----------|-----------|--------|--------|---------|
| Linux           | ✅ T1  | ✅ T1 | ✅ T1 | ⚠️ T3    | ⚠️ T3    | ⚠️ T3  | ⚠️ T3  | ⚠️ T3  |
| macOS           | ✅ T1  | ✅ T1 | ❌    | ❌        | ❌        | ❌     | ❌     | ❌      |
| Windows         | ✅ T1  | ✅ T1 | ❌    | ❌        | ❌        | ❌     | ❌     | ❌      |
| FreeBSD         | ✅ T2  | ✅ T2 | ❌    | ❌        | ❌        | ❌     | ❌     | ❌      |
| NetBSD          | ✅ T2  | ✅ T2 | ❌    | ❌        | ❌        | ❌     | ❌     | ❌      |
| OpenBSD         | ✅ T2  | ✅ T2 | ❌    | ❌        | ❌        | ❌     | ❌     | ❌      |

**Legend:**
- ✅ = Fully supported
- ⚠️ = Experimental
- ❌ = Not supported
- T1/T2/T3 = Tier 1/2/3

## Platform-Specific Features

### Linux
- Full syscall support
- Native threading via pthreads
- Direct I/O and async I/O
- eBPF integration (planned)

### macOS
- Cocoa/AppKit bindings (planned)
- Metal GPU support (planned)
- Native app bundling

### Windows
- Win32 API support
- Windows Runtime (WinRT) support (planned)
- DirectX support (planned)
- Native .exe generation

### BSD Systems
- Native syscall support
- kqueue for async I/O
- Jails/containers support (planned)

## Calling Conventions

Runa supports platform-specific calling conventions:

| Platform | x86_64 Convention | ARM64 Convention |
|----------|-------------------|------------------|
| Linux | System V AMD64 ABI | AAPCS64 |
| macOS | System V AMD64 ABI | Apple ARM64 |
| Windows | Microsoft x64 | ARM64 Windows |
| BSD | System V AMD64 ABI | AAPCS64 |

## Syscall Support

Each platform has dedicated syscall implementations:

```
runa/bootstrap/v0.0.8.5/compiler/frontend/primitives/platform/
├── linux_x86_64/syscall.runa
├── linux_arm64/syscall.runa
├── darwin_x86_64/syscall.runa
├── darwin_arm64/syscall.runa
├── windows_x86_64/syscall.runa
├── freebsd_x64/syscall.runa
└── ... (more platforms)
```

## Testing Your Platform

To verify Runa works on your platform:

```bash
# Clone the repository
git clone https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang.git
cd RunaLang/bootstrap/v0.0.8.5

# Run platform detection
runac --detect-platform

# Run test suite
./tests/run_all_tests.sh
```

## Cross-Compilation

Runa supports cross-compilation to target different platforms:

```bash
# Compile for Linux ARM64 from x86_64
runac myapp.runa --target linux-arm64 -o myapp_arm64

# Compile for Windows from Linux
runac myapp.runa --target windows-x86_64 -o myapp.exe

# Compile for macOS ARM64 from x86_64
runac myapp.runa --target darwin-arm64 -o myapp_m1
```

See [Cross-Compilation](Cross-Compilation) for detailed instructions.

## Platform-Specific Code

You can write platform-specific code using conditional compilation:

```runa
Note: Platform-specific implementation
Process called "get home directory":
    When platform is "linux":
        Return environment variable "HOME"
    When platform is "darwin":
        Return environment variable "HOME"
    When platform is "windows":
        Return environment variable "USERPROFILE"
    Otherwise:
        Return "/tmp"
```

## Minimum Requirements

### All Platforms
- 64 MB RAM minimum (more recommended)
- 10 MB disk space for compiler
- C compiler or assembler (temporary, until self-hosting complete)

### Linux
- Kernel 4.15+ (for x86_64)
- Kernel 4.18+ (for ARM64)
- glibc 2.27+ or musl 1.1.20+

### macOS
- 10.15 Catalina or later
- Xcode Command Line Tools (for assembler)

### Windows
- Windows 10 version 1809 or later
- MSVC Build Tools or MinGW-w64 (temporary)

## Future Platform Support

Platforms under consideration for future support:

- **Android** (ARM64, x86_64)
- **iOS** (ARM64)
- **WebAssembly** (WASM)
- **Fuchsia** (x86_64, ARM64)
- **Haiku** (x86_64)
- **Solaris/Illumos** (x86_64)

## Contributing Platform Support

We welcome contributions for platform support! See areas we need help:

- Testing on Tier 2/3 platforms
- Implementing syscalls for new platforms
- Optimizing for specific architectures
- Adding platform-specific library bindings

See the [Contributing Guide](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang/blob/main/CONTRIBUTING.md) for details.

## Platform-Specific Notes

### Linux on ARM
- Tested on Raspberry Pi 4 (8GB)
- Works on AWS Graviton instances
- Full feature parity with x86_64

### Apple Silicon
- Native ARM64 support (no Rosetta required)
- Optimized for M1/M2/M3 processors
- Universal binary support planned

### Windows ARM64
- Tested on Surface Pro X
- Native ARM64 execution
- Win32 API compatibility

### BSD Systems
- Focused on recent versions
- kqueue async I/O support
- May require additional dependencies

## Troubleshooting

### Platform Not Detected

```bash
runac: error: unsupported platform
```

**Solution**: Check if your platform is supported in the matrix above. For experimental platforms, use the `--force-platform` flag.

### Missing Dependencies

```bash
runac: error: assembler not found
```

**Solution**: Install platform-specific build tools:
- Linux: `sudo apt install binutils` or equivalent
- macOS: `xcode-select --install`
- Windows: Install MSVC Build Tools or MinGW-w64

### Syscall Errors

```bash
runtime error: invalid syscall
```

**Solution**: Your platform may have a syscall ABI mismatch. Report this on [GitHub Issues](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang/issues).

## Related Pages

- [Platform-Specific Notes](Platform-Specific-Notes)
- [Cross-Compilation](Cross-Compilation)
- [Building from Source](Building-from-Source)
- [Troubleshooting](Troubleshooting)

---

**Questions?** Ask in [GitHub Discussions](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang/discussions) or [Discord](https://discord.gg/sybertnetics-runa).
