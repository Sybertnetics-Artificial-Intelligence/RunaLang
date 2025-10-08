# Runa CI/CD Pipeline Specification

**Version:** 1.0
**Status:** Canonical
**Last Updated:** 2025-10-08

---

## Overview

**Runa replaces all CI/CD configuration formats:**
- ❌ GitHub Actions (`.github/workflows/*.yml`)
- ❌ GitLab CI (`.gitlab-ci.yml`)
- ❌ Jenkins (Jenkinsfile)
- ❌ CircleCI (`.circleci/config.yml`)
- ❌ Travis CI (`.travis.yml`)
- ❌ Azure Pipelines (`azure-pipelines.yml`)

**With a single unified approach:** `.runa` pipeline files that are executable, type-safe, and portable across all CI platforms.

---

## Basic Pipeline Structure

### Standard CI Pipeline

**File:** `.runa/ci/pipeline.runa`

```runa
Note: CI/CD Pipeline for MyProject
Note: This file replaces .github/workflows, .gitlab-ci.yml, Jenkinsfile, etc.

Import "runa/ci" as CI

@Reasoning:
  Unified CI/CD pipeline that runs on any platform.
  Defines stages: build → test → deploy.
@End Reasoning

Type called "PipelineConfig":
    name as String
    triggers as List[String]
    stages as List[Stage]
End Type

Type called "Stage":
    name as String
    jobs as List[Job]
End Type

Type called "Job":
    name as String
    steps as List[Step]
    environment as Dictionary[String, String]
End Type

Type called "Step":
    name as String
    action as Process
End Type

Note: ============================================
Note: PIPELINE TRIGGERS
Note: ============================================

Process called "define_triggers" returns List[String]:
    Return a list containing:
        "push:main",
        "push:develop",
        "pull_request:*",
        "schedule:daily"
End Process

Note: ============================================
Note: BUILD STAGE
Note: ============================================

Process called "step_setup_environment":
    Call CI.display("Setting up build environment...")

    Call CI.install_dependency("runa-compiler", "1.0.0")
    Call CI.install_dependency("runa-stdlib", "1.0.0")

    Call CI.display("✓ Environment ready")
End Process

Process called "step_compile":
    Call CI.display("Compiling source code...")

    Call CI.run_command("runa build.runa compile")

    Call CI.display("✓ Compilation successful")
End Process

Process called "step_lint":
    Call CI.display("Running linter...")

    Call CI.run_command("runa lint src/")

    Call CI.display("✓ Linting passed")
End Process

Process called "build_job" returns Job:
    Return a value of type Job with
        name as "build",
        steps as a list containing:
            step("Setup Environment", step_setup_environment),
            step("Compile", step_compile),
            step("Lint", step_lint)
        End,
        environment as a dictionary containing:
            "RUNA_ENV" as "ci",
            "BUILD_MODE" as "release"
        End Dictionary
End Process

Note: ============================================
Note: TEST STAGE
Note: ============================================

Process called "step_unit_tests":
    Call CI.display("Running unit tests...")

    Call CI.run_command("runa build.runa test")

    Call CI.display("✓ Unit tests passed")
End Process

Process called "step_integration_tests":
    Call CI.display("Running integration tests...")

    Call CI.run_command("runa test.runa integration")

    Call CI.display("✓ Integration tests passed")
End Process

Process called "step_coverage_report":
    Call CI.display("Generating coverage report...")

    Call CI.run_command("runa coverage.runa report")
    Call CI.upload_artifact("coverage-report.html")

    Call CI.display("✓ Coverage report generated")
End Process

Process called "test_job" returns Job:
    Return a value of type Job with
        name as "test",
        steps as a list containing:
            step("Unit Tests", step_unit_tests),
            step("Integration Tests", step_integration_tests),
            step("Coverage Report", step_coverage_report)
        End,
        environment as a dictionary containing:
            "TEST_MODE" as "ci"
        End Dictionary
End Process

Note: ============================================
Note: DEPLOY STAGE
Note: ============================================

Process called "step_package":
    Call CI.display("Creating deployment package...")

    Call CI.run_command("runa build.runa package")
    Call CI.upload_artifact("build/myapp-1.0.0.tar.gz")

    Call CI.display("✓ Package created")
End Process

Process called "step_deploy_staging":
    Call CI.display("Deploying to staging...")

    Call CI.run_command("runa deploy.runa staging")

    Call CI.display("✓ Deployed to staging")
End Process

Process called "step_deploy_production":
    Note: Only deploy to production on main branch
    Let branch be CI.get_current_branch()

    If branch is not "main":
        Call CI.display("Skipping production deployment (not on main branch)")
        Return
    End If

    Call CI.display("Deploying to production...")

    Call CI.run_command("runa deploy.runa production")

    Call CI.display("✓ Deployed to production")
End Process

Process called "deploy_job" returns Job:
    Return a value of type Job with
        name as "deploy",
        steps as a list containing:
            step("Package", step_package),
            step("Deploy to Staging", step_deploy_staging),
            step("Deploy to Production", step_deploy_production)
        End,
        environment as a dictionary containing:
            "DEPLOY_ENV" as "ci"
        End Dictionary
End Process

Note: ============================================
Note: PIPELINE DEFINITION
Note: ============================================

Process called "define_pipeline" returns PipelineConfig:
    Return a value of type PipelineConfig with
        name as "MyProject CI/CD Pipeline",
        triggers as define_triggers(),
        stages as a list containing:
            stage("Build", a list containing build_job()),
            stage("Test", a list containing test_job()),
            stage("Deploy", a list containing deploy_job())
        End
End Process

Note: ============================================
Note: EXECUTE PIPELINE
Note: ============================================

Process called "main":
    Let pipeline be define_pipeline()

    Call CI.display("=== Starting Pipeline: " + pipeline.name + " ===")

    For Each stage in pipeline.stages:
        Call CI.display("Stage: " + stage.name)

        For Each job in stage.jobs:
            Call CI.display("  Job: " + job.name)

            Note: Set environment variables
            For Each key, value in job.environment:
                Call CI.set_environment_variable(key, value)
            End For

            Note: Execute steps
            For Each step in job.steps:
                Call CI.display("    Step: " + step.name)
                Call step.action()
            End For
        End For
    End For

    Call CI.display("=== Pipeline Complete ===")
End Process
```

**Usage:**
```bash
# Run locally (for testing)
runa .runa/ci/pipeline.runa

# On CI platform (auto-detected)
# GitHub Actions: runs on push/PR
# GitLab CI: runs on push/PR
# Jenkins: runs on schedule
```

---

## Platform-Specific Examples

### GitHub Actions Replacement

**Before (`.github/workflows/ci.yml`):**
```yaml
name: CI Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node
        uses: actions/setup-node@v3
      - run: npm install
      - run: npm run build

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: npm test
```

**After (`.runa/ci/pipeline.runa`):**
```runa
Import "runa/ci" as CI

Process called "build_stage":
    Call CI.checkout_repository()
    Call CI.run_command("runa build.runa")
End Process

Process called "test_stage":
    Call CI.run_command("runa test.runa")
End Process

Process called "main":
    Let triggers be a list containing "push:main", "push:develop", "pull_request"

    If CI.should_run(triggers):
        Call build_stage()
        Call test_stage()
    End If
End Process
```

### GitLab CI Replacement

**Before (`.gitlab-ci.yml`):**
```yaml
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - make build

test:
  stage: test
  script:
    - make test

deploy:
  stage: deploy
  script:
    - ./deploy.sh production
  only:
    - main
```

**After (`.runa/ci/pipeline.runa`):**
```runa
Process called "pipeline":
    Call stage_build()
    Call stage_test()

    Let branch be CI.get_current_branch()
    If branch is "main":
        Call stage_deploy()
    End If
End Process
```

### Jenkins Pipeline Replacement

**Before (Jenkinsfile):**
```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'make build'
            }
        }
        stage('Test') {
            steps {
                sh 'make test'
            }
        }
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh './deploy.sh'
            }
        }
    }
}
```

**After (`.runa/ci/pipeline.runa`):**
```runa
Note: Same Runa pipeline works on Jenkins, GitHub Actions, GitLab CI, etc.

Process called "main":
    Call build_stage()
    Call test_stage()

    If CI.get_current_branch() is "main":
        Call deploy_stage()
    End If
End Process
```

---

## Advanced Features

### Parallel Jobs

```runa
Process called "parallel_tests":
    Let test_suites be a list containing:
        "unit_tests",
        "integration_tests",
        "e2e_tests"

    Let jobs be an empty list

    For Each suite in test_suites:
        Let job be CI.create_async_job(run_test_suite, suite)
        Add job to jobs
    End For

    For Each job in jobs:
        Call CI.wait_for_job(job)
    End For
End Process
```

### Conditional Execution

```runa
Process called "conditional_deployment":
    Let branch be CI.get_current_branch()
    Let commit_message be CI.get_commit_message()

    If branch is "main" and commit_message contains "[deploy]":
        Call deploy_to_production()
    Otherwise if branch starts with "hotfix/":
        Call deploy_to_staging()
    Otherwise:
        Call CI.display("Skipping deployment")
    End If
End Process
```

### Matrix Builds

```runa
Process called "matrix_build":
    Let platforms be a list containing "linux", "windows", "macos"
    Let versions be a list containing "1.0", "1.1", "1.2"

    For Each platform in platforms:
        For Each version in versions:
            Call CI.display("Building for " + platform + " v" + version)
            Call build_for_platform(platform, version)
        End For
    End For
End Process
```

### Caching

```runa
Process called "build_with_cache":
    Note: Check for cached dependencies
    Let cache_key be "dependencies-" + hash_file("dependencies.runa")

    If CI.cache_exists(cache_key):
        Call CI.restore_cache(cache_key)
        Call CI.display("✓ Dependencies restored from cache")
    Otherwise:
        Call CI.run_command("runa install-dependencies")
        Call CI.save_cache(cache_key, "runa_modules/")
        Call CI.display("✓ Dependencies installed and cached")
    End If

    Call CI.run_command("runa build.runa")
End Process
```

### Secrets Management

```runa
Process called "deploy_with_secrets":
    Note: Get secrets from CI platform
    Let api_key be CI.get_secret("API_KEY")
    Let db_password be CI.get_secret("DB_PASSWORD")

    Note: Set as environment variables
    Call CI.set_environment_variable("API_KEY", api_key)
    Call CI.set_environment_variable("DB_PASSWORD", db_password)

    Call CI.run_command("runa deploy.runa production")
End Process
```

---

## Complete Example

**File:** `.runa/ci/complete_pipeline.runa`

```runa
Note: Production-grade CI/CD pipeline

Import "runa/ci" as CI

Type called "BuildResult":
    success as Boolean
    artifacts as List[String]
    duration_ms as Integer
End Type

Type called "TestResult":
    passed as Integer
    failed as Integer
    coverage_percent as Float
End Type

Note: ============================================
Note: BUILD STAGE
Note: ============================================

@Implementation:
  Comprehensive build with caching and artifacts.
@End Implementation

Process called "build_stage" returns BuildResult:
    Let start_time be CI.current_time_milliseconds()

    Call CI.display("=== Build Stage ===")

    Note: Restore dependency cache
    Let cache_key be "deps-" + CI.hash_file("dependencies.runa")
    If CI.cache_exists(cache_key):
        Call CI.restore_cache(cache_key)
    Otherwise:
        Call CI.run_command("runa install-dependencies")
        Call CI.save_cache(cache_key, "runa_modules/")
    End If

    Note: Compile
    Call CI.run_command("runa build.runa compile")

    Note: Package
    Call CI.run_command("runa build.runa package")

    Let artifacts be a list containing:
        "build/myapp",
        "build/myapp-1.0.0.tar.gz"

    For Each artifact in artifacts:
        Call CI.upload_artifact(artifact)
    End For

    Let end_time be CI.current_time_milliseconds()

    Return a value of type BuildResult with
        success as true,
        artifacts as artifacts,
        duration_ms as end_time - start_time
End Process

Note: ============================================
Note: TEST STAGE
Note: ============================================

@Implementation:
  Run tests in parallel with coverage reporting.
@End Implementation

Process called "test_stage" returns TestResult:
    Call CI.display("=== Test Stage ===")

    Note: Run unit tests
    Call CI.run_command("runa test.runa unit")

    Note: Run integration tests
    Call CI.run_command("runa test.runa integration")

    Note: Generate coverage
    Call CI.run_command("runa coverage.runa report")
    Call CI.upload_artifact("coverage-report.html")

    Note: Parse results
    Let results be CI.parse_test_results("test-results.json")

    Return a value of type TestResult with
        passed as results.passed,
        failed as results.failed,
        coverage_percent as results.coverage
End Process

Note: ============================================
Note: SECURITY STAGE
Note: ============================================

Process called "security_stage":
    Call CI.display("=== Security Stage ===")

    Note: Run security scanner
    Call CI.run_command("runa security.runa scan")

    Note: Check for vulnerabilities
    Call CI.run_command("runa security.runa audit-dependencies")

    Call CI.display("✓ Security checks passed")
End Process

Note: ============================================
Note: DEPLOY STAGE
Note: ============================================

@Implementation:
  Deploy to staging, then production (with approval).
@End Implementation

Process called "deploy_stage":
    Call CI.display("=== Deploy Stage ===")

    Let branch be CI.get_current_branch()

    Note: Deploy to staging
    Call CI.display("Deploying to staging...")
    Call CI.run_command("runa deploy.runa staging")
    Call CI.display("✓ Deployed to staging: https://staging.myapp.com")

    Note: Deploy to production (main branch only)
    If branch is "main":
        Call CI.display("Waiting for production approval...")

        Note: Manual approval gate
        Call CI.wait_for_approval("production-deployment")

        Call CI.display("Deploying to production...")
        Call CI.run_command("runa deploy.runa production")
        Call CI.display("✓ Deployed to production: https://myapp.com")
    End If
End Process

Note: ============================================
Note: NOTIFICATION STAGE
Note: ============================================

Process called "notify_success" that takes build_result as BuildResult, test_result as TestResult:
    Let message be "✓ Pipeline SUCCESS\n"
    Set message to message + "Build: " + string_from(build_result.duration_ms) + "ms\n"
    Set message to message + "Tests: " + string_from(test_result.passed) + " passed\n"
    Set message to message + "Coverage: " + string_from(test_result.coverage_percent) + "%"

    Call CI.send_notification("slack", message)
    Call CI.send_notification("email", message)
End Process

Process called "notify_failure" that takes error as String:
    Let message be "✗ Pipeline FAILED\n"
    Set message to message + "Error: " + error

    Call CI.send_notification("slack", message)
    Call CI.send_notification("email", message)
End Process

Note: ============================================
Note: MAIN PIPELINE
Note: ============================================

Process called "main":
    Let start_time be CI.current_time_milliseconds()

    Call CI.display("=== Starting CI/CD Pipeline ===")
    Call CI.display("Branch: " + CI.get_current_branch())
    Call CI.display("Commit: " + CI.get_commit_hash())

    Note: Execute pipeline stages
    Let build_result be build_stage()

    If not build_result.success:
        Call notify_failure("Build failed")
        Call CI.exit_with_code(1)
    End If

    Let test_result be test_stage()

    If test_result.failed > 0:
        Call notify_failure("Tests failed")
        Call CI.exit_with_code(1)
    End If

    Call security_stage()
    Call deploy_stage()

    Let end_time be CI.current_time_milliseconds()
    Let total_duration be end_time - start_time

    Call CI.display("=== Pipeline Complete ===")
    Call CI.display("Total Duration: " + string_from(total_duration) + "ms")

    Call notify_success(build_result, test_result)
End Process
```

---

## Summary

**Runa replaces all CI/CD formats with:**
- ✅ Platform-independent pipeline definitions
- ✅ Type-safe job and step configuration
- ✅ Executable, testable pipelines
- ✅ Built-in caching, artifacts, secrets
- ✅ Parallel execution support
- ✅ One syntax for GitHub Actions, GitLab CI, Jenkins, etc.

**Stop using:** YAML/Groovy CI configs

**Start using:** `.runa/ci/pipeline.runa`

---

## See Also

- [Runa Build System](./runa_build_system.md)
- [Runa Container Specification](./runa_container_specification.md)
- [Runa Dependency Management](./runa_dependency_management.md)

---

**End of Document**
