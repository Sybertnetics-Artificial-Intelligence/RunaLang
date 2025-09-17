# Runa Bootstrap Build Strategy

## Current Status

- **v0.1**: Rust + LLVM (bootstrap compiler)
- **v0.2**: Runa generating syscall-only assembly (zero dependencies)

## Cross-Compilation Reality

### What Works
- ✅ Linux native build: `cargo build --release`
- ✅ v0.2 generates pure syscall assembly (no libc)

### What Doesn't Work Easily
- ❌ Cross-compiling v0.1 from Linux to Windows (LLVM dependency issues)
- ❌ Cross-compiling v0.1 from Linux to macOS (needs osxcross)

## Practical Solution

### Option 1: Native Builds (Recommended)
Build v0.1 on each platform natively:
```bash
# On Linux
cargo build --release
cp target/release/runac runac-linux-x64

# On Windows (in PowerShell or WSL)
cargo build --release
copy target\release\runac.exe runac-windows-x64.exe

# On macOS
cargo build --release
cp target/release/runac runac-macos-x64
```

### Option 2: Use GitHub Actions
Create CI/CD pipeline that builds on each platform:
```yaml
# .github/workflows/build.yml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
runs-on: ${{ matrix.os }}
steps:
  - cargo build --release
```

### Option 3: Docker/Containers
Use Windows containers for Windows builds, etc.

## Why This Is Fine

1. **v0.1 is temporary** - Only needed for initial bootstrap
2. **v0.2+ is pure assembly** - No external dependencies
3. **Build once per platform** - v0.1 only needs to be built once per OS
4. **Future versions are self-hosted** - v0.3+ will be written in Runa

## Current Working Setup

On Linux (WSL):
```bash
# Build Linux version of v0.1
cargo build --release

# Use v0.1 to compile v0.2
./target/release/runac v0.2_micro-runa/compiler.runa

# v0.2 generates pure assembly with syscalls
# No libc, no external dependencies!
```

## Next Steps

1. Build v0.1 natively on each target platform
2. Use each platform's v0.1 to bootstrap v0.2
3. v0.2 generates platform-specific syscall assembly
4. v0.3+ implements full cross-compilation in pure Runa