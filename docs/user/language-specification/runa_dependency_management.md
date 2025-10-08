# Runa Dependency Management Specification

**Version:** 1.0
**Status:** Canonical
**Last Updated:** 2025-10-08

---

## Overview

**Runa replaces all package management files:**
- ❌ package.json, package-lock.json (npm)
- ❌ requirements.txt, Pipfile (Python)
- ❌ Cargo.toml, Cargo.lock (Rust)
- ❌ go.mod, go.sum (Go)
- ❌ Gemfile, Gemfile.lock (Ruby)
- ❌ build.gradle, pom.xml (Java)

---

## Basic Dependency File

**File:** `dependencies.runa`

```runa
Note: Project dependencies
Note: Replaces package.json, requirements.txt, Cargo.toml, etc.

Import "runa/package" as Package

Type called "Dependency":
    name as String
    version as String
    source as String  Note: "registry", "git", "path"
    url as String
End Type

Type called "ProjectDependencies":
    name as String
    version as String
    dependencies as List[Dependency]
    dev_dependencies as List[Dependency]
End Type

Process called "define_dependencies" returns ProjectDependencies:
    Return a value of type ProjectDependencies with
        name as "MyApp",
        version as "1.0.0",
        dependencies as a list containing:
            dep("runa-stdlib", "1.0.0", "registry"),
            dep("runa-http", "2.1.0", "registry"),
            dep("runa-database", "1.5.3", "registry")
        End,
        dev_dependencies as a list containing:
            dep("runa-test", "1.0.0", "registry"),
            dep("runa-lint", "0.9.0", "registry")
        End
End Process

Process called "dep" that takes name as String, version as String, source as String returns Dependency:
    Return a value of type Dependency with
        name as name,
        version as version,
        source as source,
        url as ""
End Process

Let PROJECT_DEPS be define_dependencies()
```

**Usage:**
```bash
# Install dependencies
runa install dependencies.runa

# Update dependencies
runa update dependencies.runa
```

---

## Version Constraints

```runa
Process called "define_with_constraints" returns List[Dependency]:
    Return a list containing:
        Note: Exact version
        dep("package-a", "1.0.0", "registry"),

        Note: Semantic versioning
        dep("package-b", "^2.1.0", "registry"),  Note: >= 2.1.0, < 3.0.0
        dep("package-c", "~1.5.0", "registry"),  Note: >= 1.5.0, < 1.6.0

        Note: Git repository
        dep_git("package-d", "main", "https://github.com/user/package-d"),

        Note: Local path
        dep_path("local-lib", "../local-lib")
    End
End Process

Process called "dep_git" that takes name as String, branch as String, url as String returns Dependency:
    Return a value of type Dependency with
        name as name,
        version as branch,
        source as "git",
        url as url
End Process

Process called "dep_path" that takes name as String, path as String returns Dependency:
    Return a value of type Dependency with
        name as name,
        version as "local",
        source as "path",
        url as path
End Process
```

---

## Lockfile Generation

**File:** `dependencies.lock.runa` (auto-generated)

```runa
Note: Dependency lockfile (auto-generated)
Note: Replaces package-lock.json, Cargo.lock, go.sum, etc.
Note: DO NOT EDIT MANUALLY

Type called "LockedDependency":
    name as String
    version as String
    resolved_url as String
    integrity_hash as String
    dependencies as List[String]
End Type

Let LOCKED_DEPENDENCIES be a list containing:
    locked("runa-stdlib", "1.0.0", "https://registry.runa.dev/stdlib-1.0.0.tar.gz", "sha256:abc123..."),
    locked("runa-http", "2.1.0", "https://registry.runa.dev/http-2.1.0.tar.gz", "sha256:def456..."),
    locked("runa-database", "1.5.3", "https://registry.runa.dev/database-1.5.3.tar.gz", "sha256:ghi789...")
End

Process called "locked" that takes name as String, version as String, url as String, hash as String returns LockedDependency:
    Return a value of type LockedDependency with
        name as name,
        version as version,
        resolved_url as url,
        integrity_hash as hash,
        dependencies as an empty list
End Process
```

---

## Comparison: package.json vs dependencies.runa

**Before (package.json):**
```json
{
  "name": "myapp",
  "version": "1.0.0",
  "dependencies": {
    "express": "^4.18.0",
    "mongoose": "^6.5.0"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  },
  "scripts": {
    "start": "node index.js",
    "test": "jest"
  }
}
```

**After (dependencies.runa):**
```runa
Type called "ProjectConfig":
    name as String
    version as String
    dependencies as List[Dependency]
    dev_dependencies as List[Dependency]
    scripts as Dictionary[String, String]
End Type

Process called "load_config" returns ProjectConfig:
    Return a value of type ProjectConfig with
        name as "myapp",
        version as "1.0.0",
        dependencies as a list containing:
            dep("runa-express", "^4.18.0", "registry"),
            dep("runa-mongoose", "^6.5.0", "registry")
        End,
        dev_dependencies as a list containing:
            dep("runa-jest", "^29.0.0", "registry")
        End,
        scripts as a dictionary containing:
            "start" as "runa index.runa",
            "test" as "runa test.runa"
        End Dictionary
End Process

Let CONFIG be load_config()
```

---

## Workspace/Monorepo Support

**File:** `workspace.runa`

```runa
Note: Workspace configuration for monorepo
Note: Replaces npm workspaces, Cargo workspace, etc.

Type called "WorkspaceConfig":
    name as String
    members as List[String]
    shared_dependencies as List[Dependency]
End Type

Process called "define_workspace" returns WorkspaceConfig:
    Return a value of type WorkspaceConfig with
        name as "MyMonorepo",
        members as a list containing:
            "packages/core",
            "packages/ui",
            "packages/api",
            "apps/web",
            "apps/mobile"
        End,
        shared_dependencies as a list containing:
            dep("runa-stdlib", "1.0.0", "registry")
        End
End Process

Let WORKSPACE be define_workspace()
```

---

## Dependency Scripts

```runa
Process called "install_dependencies":
    Let deps be PROJECT_DEPS

    Call display("Installing " + string_from(length of deps.dependencies) + " dependencies...")

    For Each dep in deps.dependencies:
        Call display("  Installing: " + dep.name + "@" + dep.version)
        Call Package.install(dep)
    End For

    Call display("✓ Dependencies installed")
End Process

Process called "update_dependencies":
    Let deps be PROJECT_DEPS

    For Each dep in deps.dependencies:
        Let latest_version be Package.get_latest_version(dep.name)

        If latest_version is not dep.version:
            Call display("Updating " + dep.name + ": " + dep.version + " → " + latest_version)
            Call Package.update(dep.name, latest_version)
        End If
    End For

    Call display("✓ Dependencies updated")
End Process

Process called "audit_dependencies":
    Call display("Auditing dependencies for vulnerabilities...")

    Let vulnerabilities be Package.audit()

    If length of vulnerabilities is 0:
        Call display("✓ No vulnerabilities found")
    Otherwise:
        For Each vuln in vulnerabilities:
            Call display("⚠ " + vuln.package + ": " + vuln.description)
        End For

        Call panic("Vulnerabilities found")
    End If
End Process
```

---

## Summary

**Runa replaces package management with:**
- ✅ Type-safe dependency declarations
- ✅ Unified syntax across all ecosystems
- ✅ Automatic lockfile generation
- ✅ Version constraint validation
- ✅ Workspace/monorepo support

**Stop using:** package.json, requirements.txt, Cargo.toml, etc.
**Start using:** `dependencies.runa`

---

**End of Document**
