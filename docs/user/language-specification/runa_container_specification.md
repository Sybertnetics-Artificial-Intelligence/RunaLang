# Runa Container Specification

**Version:** 1.0
**Status:** Canonical
**Last Updated:** 2025-10-08

---

## Overview

**Runa replaces Dockerfiles and container configs with executable `.runa` files.**

**Replaces:**
- ❌ Dockerfile
- ❌ Containerfile
- ❌ docker-compose.yml
- ❌ podman build scripts

---

## Basic Container Definition

**File:** `container.runa`

```runa
Note: Container specification for MyApp
Note: Replaces Dockerfile

Import "runa/container" as Container

Type called "ContainerSpec":
    base_image as String
    working_dir as String
    environment as Dictionary[String, String]
    ports as List[Integer]
    volumes as List[String]
    commands as List[String]
End Type

Process called "define_container" returns ContainerSpec:
    Return a value of type ContainerSpec with
        base_image as "runa/runtime:1.0",
        working_dir as "/app",
        environment as a dictionary containing:
            "RUNA_ENV" as "production",
            "PORT" as "8080"
        End Dictionary,
        ports as a list containing 8080, 443,
        volumes as a list containing "/app/data", "/app/logs",
        commands as a list containing:
            "runa install-dependencies",
            "runa build.runa",
            "runa start-server"
        End
End Process

Process called "main":
    Let spec be define_container()
    Call Container.build(spec, "myapp:1.0")
    Call display("✓ Container image built: myapp:1.0")
End Process
```

**Usage:**
```bash
# Build container
runa container.runa

# Equivalent to: docker build -t myapp:1.0 .
```

---

## Dockerfile Comparison

**Before (Dockerfile):**
```dockerfile
FROM ubuntu:22.04
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y runa-compiler
RUN runa build.runa
EXPOSE 8080
CMD ["runa", "start-server"]
```

**After (container.runa):**
```runa
Process called "build_container":
    Let spec be a value of type ContainerSpec with
        base_image as "ubuntu:22.04",
        working_dir as "/app",
        commands as a list containing:
            "copy . /app",
            "apt-get update && apt-get install -y runa-compiler",
            "runa build.runa"
        End,
        ports as a list containing 8080,
        entrypoint as a list containing "runa", "start-server"

    Call Container.build(spec, "myapp:latest")
End Process
```

---

## Multi-Stage Builds

```runa
Process called "multi_stage_build":
    Note: Stage 1 - Build
    Let build_stage be a value of type ContainerSpec with
        base_image as "runa/compiler:1.0",
        working_dir as "/build",
        commands as a list containing:
            "copy src/ /build/src/",
            "runa build.runa compile"
        End

    Call Container.build_stage(build_stage, "builder")

    Note: Stage 2 - Runtime
    Let runtime_stage be a value of type ContainerSpec with
        base_image as "runa/runtime:1.0",
        working_dir as "/app",
        commands as a list containing:
            "copy --from=builder /build/bin/myapp /app/myapp"
        End,
        entrypoint as a list containing "/app/myapp"

    Call Container.build(runtime_stage, "myapp:1.0")
End Process
```

---

## Docker Compose Replacement

**File:** `compose.runa`

```runa
Note: Multi-container application
Note: Replaces docker-compose.yml

Type called "Service":
    name as String
    image as String
    ports as List[String]
    environment as Dictionary[String, String]
    depends_on as List[String]
End Type

Process called "define_services" returns List[Service]:
    Let web be a value of type Service with
        name as "web",
        image as "myapp:1.0",
        ports as a list containing "8080:80",
        environment as a dictionary containing:
            "DATABASE_URL" as "postgresql://db:5432/myapp"
        End Dictionary,
        depends_on as a list containing "database"

    Let database be a value of type Service with
        name as "database",
        image as "postgres:14",
        ports as a list containing "5432:5432",
        environment as a dictionary containing:
            "POSTGRES_PASSWORD" as "secret"
        End Dictionary,
        depends_on as an empty list

    Return a list containing web, database
End Process

Process called "main":
    Let services be define_services()
    Call Container.compose_up(services)
End Process
```

---

## Summary

**Runa replaces container configs with:**
- ✅ Type-safe container definitions
- ✅ Executable build scripts
- ✅ Multi-stage build support
- ✅ Compose orchestration

**Stop using:** Dockerfiles, docker-compose.yml
**Start using:** `container.runa`, `compose.runa`

---

**End of Document**
