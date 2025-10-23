# Runa Deployment and Infrastructure

**Version:** 1.0
**Status:** Canonical
**Last Updated:** 2024-10-18

---

## Table of Contents

1. [CI/CD Pipelines](#cicd-pipelines)
2. [Infrastructure as Code](#infrastructure-as-code)
3. [Kubernetes Deployment](#kubernetes-deployment)
4. [Container Specification](#container-specification)

---

# CI/CD Pipelines
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

// Developer Mode
```runa
Note: CI/CD Pipeline for MyProject
Note: This file replaces .github/workflows, .gitlab-ci.yml, Jenkinsfile, etc.

Import "runa/ci" as CI

@Reasoning:
  Unified CI/CD pipeline that runs on any platform.
  Defines stages: build → test → deploy.
@End Reasoning

Type called "PipelineConfig":
    name : String
    triggers : List[String]
    stages : List[Stage]
End Type

Type called "Stage":
    name : String
    jobs : List[Job]
End Type

Type called "Job":
    name : String
    steps : List[Step]
    environment : Dictionary[String, String]
End Type

Type called "Step":
    name : String
    action : Process
End Type

Note: ============================================
Note: PIPELINE TRIGGERS
Note: ============================================

Process called "define_triggers" returns List[String]:
    return [
        "push:main",
        "push:develop",
        "pull_request:*",
        "schedule:daily"
    ]
End Process

Note: ============================================
Note: BUILD STAGE
Note: ============================================

Process called "step_setup_environment":
    Display "Setting up build environment..."

    CI.install_dependency("runa-compiler", "1.0.0")
    CI.install_dependency("runa-stdlib", "1.0.0")

    Display "✓ Environment ready"
End Process

Process called "step_compile":
    Display "Compiling source code..."

    CI.run_command("runa build.runa compile")

    Display "✓ Compilation successful"
End Process

Process called "step_lint":
    Display "Running linter..."

    CI.run_command("runa lint src/")

    Display "✓ Linting passed"
End Process

Process called "build_job" returns Job:
    return Job(
        name: "build",
        steps: [
            step("Setup Environment", step_setup_environment),
            step("Compile", step_compile),
            step("Lint", step_lint)
        ],
        environment: {
            "RUNA_ENV": "ci",
            "BUILD_MODE": "release"
        }
    )
End Process

Note: ============================================
Note: TEST STAGE
Note: ============================================

Process called "step_unit_tests":
    Display "Running unit tests..."

    CI.run_command("runa build.runa test")

    Display "✓ Unit tests passed"
End Process

Process called "step_integration_tests":
    Display "Running integration tests..."

    CI.run_command("runa test.runa integration")

    Display "✓ Integration tests passed"
End Process

Process called "step_coverage_report":
    Display "Generating coverage report..."

    CI.run_command("runa coverage.runa report")
    CI.upload_artifact("coverage-report.html")

    Display "✓ Coverage report generated"
End Process

Process called "test_job" returns Job:
    return Job(
        name: "test",
        steps: [
            step("Unit Tests", step_unit_tests),
            step("Integration Tests", step_integration_tests),
            step("Coverage Report", step_coverage_report)
        ],
        environment: {
            "TEST_MODE": "ci"
        }
    )
End Process

Note: ============================================
Note: DEPLOY STAGE
Note: ============================================

Process called "step_package":
    Display "Creating deployment package..."

    CI.run_command("runa build.runa package")
    CI.upload_artifact("build/myapp-1.0.0.tar.gz")

    Display "✓ Package created"
End Process

Process called "step_deploy_staging":
    Display "Deploying to staging..."

    CI.run_command("runa deploy.runa staging")

    Display "✓ Deployed to staging"
End Process

Process called "step_deploy_production":
    Note: Only deploy to production on main branch
    Let branch be CI.get_current_branch()

    If branch is not "main":
        Display "Skipping production deployment (not on main branch)"
        Return
    End If

    Display "Deploying to production..."

    CI.run_command("runa deploy.runa production")

    Display "✓ Deployed to production"
End Process

Process called "deploy_job" returns Job:
    return Job(
        name: "deploy",
        steps: [
            step("Package", step_package),
            step("Deploy to Staging", step_deploy_staging),
            step("Deploy to Production", step_deploy_production)
        ],
        environment: {
            "DEPLOY_ENV": "ci"
        }
    )
End Process

Note: ============================================
Note: PIPELINE DEFINITION
Note: ============================================

Process called "define_pipeline" returns PipelineConfig:
    return PipelineConfig(
        name: "MyProject CI/CD Pipeline",
        triggers: define_triggers(),
        stages: [
            stage("Build", [build_job()]),
            stage("Test", [test_job()]),
            stage("Deploy", [deploy_job()])
        ]
    )
End Process

Note: ============================================
Note: EXECUTE PIPELINE
Note: ============================================

Process called "main":
    Let pipeline be define_pipeline()

    Display "=== Starting Pipeline: " + pipeline.name + " ==="

    For Each stage in pipeline.stages:
        Display "Stage: " + stage.name

        For Each job in stage.jobs:
            Display "  Job: " + job.name

            Note: Set environment variables
            For Each key, value in job.environment:
    CI.set_environment_variable(key, value)
            End For

            Note: Execute steps
            For Each step in job.steps:
                Display "    Step: " + step.name
                step.action()
            End For
        End For
    End For

    Display "=== Pipeline Complete ==="
End Process
```

**Usage:**
```bash
# Run locally (for testing
runa .runa/ci/pipeline.runa

# On CI platform (auto-detected
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
    CI.checkout_repository()
    CI.run_command("runa build.runa")
End Process

Process called "test_stage":
    CI.run_command("runa test.runa")
End Process

Process called "main":
    Let triggers be [ "push:main", "push:develop", "pull_request"]

    If CI.should_run(triggers):
        build_stage()
        test_stage()
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
    stage_build()
    stage_test()

    Let branch be CI.get_current_branch()
    If branch is "main":
        stage_deploy()
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
    build_stage()
    test_stage()

    If CI.get_current_branch() is "main":
        deploy_stage()
    End If
End Process
```

---

## Advanced Features

### Parallel Jobs

```runa
Process called "parallel_tests":
    Let test_suites be [
        "unit_tests",
        "integration_tests",
        "e2e_tests"]

    Let jobs be []

    For Each suite in test_suites:
        Let job be CI.create_async_job(run_test_suite, suite
        Add job to jobs
    End For

    For Each job in jobs:
    CI.wait_for_job(job)
    End For
End Process
```

### Conditional Execution

```runa
Process called "conditional_deployment":
    Let branch be CI.get_current_branch()
    Let commit_message be CI.get_commit_message()

    If branch is "main" and commit_message contains "[deploy]":
        deploy_to_production()
    Otherwise if branch starts with "hotfix/":
        deploy_to_staging()
    Otherwise:
        Display "Skipping deployment"
    End If
End Process
```

### Matrix Builds

```runa
Process called "matrix_build":
    Let platforms be [ "linux", "windows", "macos"]
    Let versions be [ "1.0", "1.1", "1.2"]

    For Each platform in platforms:
        For Each version in versions:
            Display "Building for " + platform + " v" + version
            build_for_platform(platform, version)
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
    CI.restore_cache(cache_key)
        Display "✓ Dependencies restored from cache"
    Otherwise:
    CI.run_command("runa install-dependencies")
    CI.save_cache(cache_key, "runa_modules/")
        Display "✓ Dependencies installed and cached"
    End If

    CI.run_command("runa build.runa")
End Process
```

### Secrets Management

```runa
Process called "deploy_with_secrets":
    Note: Get secrets from CI platform
    Let api_key be CI.get_secret("API_KEY")
    Let db_password be CI.get_secret("DB_PASSWORD")

    Note: Set as environment variables
    CI.set_environment_variable("API_KEY", api_key)
    CI.set_environment_variable("DB_PASSWORD", db_password)

    CI.run_command("runa deploy.runa production")
End Process
```

---

## Complete Example

**File:** `.runa/ci/complete_pipeline.runa`

```runa
Note: Production-grade CI/CD pipeline

Import "runa/ci" as CI

Type called "BuildResult":
    success : Boolean
    artifacts : List[String]
    duration_ms : Integer
End Type

Type called "TestResult":
    passed : Integer
    failed : Integer
    coverage_percent : Float
End Type

Note: ============================================
Note: BUILD STAGE
Note: ============================================

@Implementation:
  Comprehensive build with caching and artifacts.
@End Implementation

Process called "build_stage" returns BuildResult:
    Let start_time be CI.current_time_milliseconds()

    Display "=== Build Stage ==="

    Note: Restore dependency cache
    Let cache_key be "deps-" + CI.hash_file("dependencies.runa")
    If CI.cache_exists(cache_key):
    CI.restore_cache(cache_key)
    Otherwise:
    CI.run_command("runa install-dependencies")
    CI.save_cache(cache_key, "runa_modules/")
    End If

    Note: Compile
    CI.run_command("runa build.runa compile")

    Note: Package
    CI.run_command("runa build.runa package")

    Let artifacts be [
        "build/myapp",
        "build/myapp-1.0.0.tar.gz"]

    For Each artifact in artifacts:
    CI.upload_artifact(artifact)
    End For

    Let end_time be CI.current_time_milliseconds()

    return BuildResult(
        success: true,
        artifacts: artifacts,
        duration_ms: end_time - start_time)
End Process

Note: ============================================
Note: TEST STAGE
Note: ============================================

@Implementation:
  Run tests in parallel with coverage reporting.
@End Implementation

Process called "test_stage" returns TestResult:
    Display "=== Test Stage ==="

    Note: Run unit tests
    CI.run_command("runa test.runa unit")

    Note: Run integration tests
    CI.run_command("runa test.runa integration")

    Note: Generate coverage
    CI.run_command("runa coverage.runa report")
    CI.upload_artifact("coverage-report.html")

    Note: Parse results
    Let results be CI.parse_test_results("test-results.json")

    return TestResult(
        passed: results.passed,
        failed: results.failed,
        coverage_percent: results.coverage)
End Process

Note: ============================================
Note: SECURITY STAGE
Note: ============================================

Process called "security_stage":
    Display "=== Security Stage ==="

    Note: Run security scanner
    CI.run_command("runa security.runa scan")

    Note: Check for vulnerabilities
    CI.run_command("runa security.runa audit-dependencies")

    Display "✓ Security checks passed"
End Process

Note: ============================================
Note: DEPLOY STAGE
Note: ============================================

@Implementation:
  Deploy to staging, then production (with approval).
@End Implementation

Process called "deploy_stage":
    Display "=== Deploy Stage ==="

    Let branch be CI.get_current_branch()

    Note: Deploy to staging
    Display "Deploying to staging..."
    CI.run_command("runa deploy.runa staging")
    Display "✓ Deployed to staging: https://staging.myapp.com"

    Note: Deploy to production (main branch only)
    If branch is "main":
        Display "Waiting for production approval..."

        Note: Manual approval gate
    CI.wait_for_approval("production-deployment")

        Display "Deploying to production..."
    CI.run_command("runa deploy.runa production")
        Display "✓ Deployed to production: https://myapp.com"
    End If
End Process

Note: ============================================
Note: NOTIFICATION STAGE
Note: ============================================

Process called "notify_success"(build_result : BuildResult, test_result : TestResult):
    Let message be "✓ Pipeline SUCCESS\n"
    Set message to message + "Build: " + string_from(build_result.duration_ms) + "ms\n"
    Set message to message + "Tests: " + string_from(test_result.passed) + " passed\n"
    Set message to message + "Coverage: " + string_from(test_result.coverage_percent) + "%"

    CI.send_notification("slack", message)
    CI.send_notification("email", message)
End Process

Process called "notify_failure"(error : String):
    Let message be "✗ Pipeline FAILED\n"
    Set message to message + "Error: " + error

    CI.send_notification("slack", message)
    CI.send_notification("email", message)
End Process

Note: ============================================
Note: MAIN PIPELINE
Note: ============================================

Process called "main":
    Let start_time be CI.current_time_milliseconds()

    Display "=== Starting CI/CD Pipeline ==="
    Display "Branch: " + CI.get_current_branch()
    Display "Commit: " + CI.get_commit_hash()

    Note: Execute pipeline stages
    Let build_result be build_stage()

    If not build_result.success:
        notify_failure("Build failed")
    CI.exit_with_code(1)
    End If

    Let test_result be test_stage()

    If test_result.failed > 0:
        notify_failure("Tests failed")
    CI.exit_with_code(1)
    End If

    security_stage()
    deploy_stage()

    Let end_time be CI.current_time_milliseconds()
    Let total_duration be end_time - start_time

    Display "=== Pipeline Complete ==="
    Display "Total Duration: " + string_from(total_duration) + "ms"

    notify_success(build_result, test_result)
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

# Infrastructure as Code

---

## Overview

**Runa replaces infrastructure config languages:**
- ❌ Terraform HCL
- ❌ AWS CloudFormation (YAML/JSON)
- ❌ Pulumi (multi-language)
- ❌ Ansible playbooks (YAML)

---

## Basic Infrastructure Definition

**File:** `infrastructure.runa`

```runa
Note: Infrastructure as Code
Note: Replaces Terraform HCL, CloudFormation, etc.

Import "runa/cloud" as Cloud

Type called "VirtualMachine":
    name : String
    instance_type : String
    ami : String
    region : String
    tags : Dictionary[String, String]
End Type

Type called "Database":
    name : String
    engine : String
    instance_class : String
    storage_gb : Integer
End Type

Type called "Infrastructure":
    vms : List[VirtualMachine]
    databases : List[Database]
    networks : List[Network]
End Type

Process called "define_infrastructure" returns Infrastructure:
    Let web_vm be VirtualMachine()
        name: "web-server",
        instance_type: "t3.medium",
        ami: "ami-12345",
        region: "us-east-1",
        tags: {
            "Environment": "production",
            "Role": "web"
        }

    Let db be Database(
        name: "prod-db",
        engine: "postgresql",
        instance_class: "db.t3.large",
        storage_gb: 100
    )

    return Infrastructure(
        vms: [web_vm],
        databases: [db],
        networks: []
    )
End Process

Process called "main":
    Let infra be define_infrastructure()

    Cloud.apply(infra)
    Display "✓ Infrastructure provisioned"
End Process
```

---

## Terraform HCL Comparison

**Before (main.tf):**
```hcl
resource "aws_instance" "web" {
  ami           = "ami-12345"
  instance_type = "t3.medium"

  tags = {
    Name = "web-server"
    Environment = "production"
  }
}

resource "aws_db_instance" "main" {
  engine         = "postgresql"
  instance_class = "db.t3.large"
  allocated_storage = 100
}
```

**After (infrastructure.runa):**
```runa
Process called "provision_aws":
    Let web_instance be vm()
        "web-server",
        "t3.medium",
        "ami-12345",
        tags("Environment", "production")
    

    Let database be db()
        "prod-db",
        "postgresql",
        "db.t3.large",
        100
    

    Cloud.provision(web_instance)
    Cloud.provision(database)
End Process
```

---

## Multi-Cloud Infrastructure

```runa
Process called "multi_cloud_deployment":
    Note: AWS Resources
    Let aws_vm be Cloud.aws_instance()
        "web-server-aws",
        "t3.medium",
        "us-east-1"
    

    Note: Azure Resources
    Let azure_vm be Cloud.azure_vm()
        "web-server-azure",
        "Standard_B2s",
        "eastus"
    

    Note: GCP Resources
    Let gcp_vm be Cloud.gcp_instance()
        "web-server-gcp",
        "n1-standard-2",
        "us-central1"
    

    Cloud.provision_all([ aws_vm, azure_vm, gcp_vm])
End Process
```

---

## State Management

```runa
Process called "manage_state":
    Note: Load current infrastructure state
    Let current_state be Cloud.load_state("production")

    Note: Define desired state
    Let desired_state be define_infrastructure()

    Note: Calculate diff
    Let diff be Cloud.plan(current_state, desired_state

    Display "Changes to apply:"
    For Each change in diff.changes:
        Display "  " + change.action + ": " + change.resource
    End For

    Note: Apply changes
    Cloud.apply_diff(diff)

    Note: Save new state
    Cloud.save_state("production"), desired_state
End Process
```

---

## CloudFormation Comparison

**Before (template.yaml):**
```yaml
Resources:
  WebServer:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t3.medium
      ImageId: ami-12345
      Tags:
        - Key: Name
          Value: web-server
```

**After (infrastructure.runa):**
```runa
Let web_server be Cloud.resource("AWS::EC2::Instance", {
    "InstanceType": "t3.medium",
    "ImageId": "ami-12345",
    "Tags": [tag("Name", "web-server")]
})
```

---

## Kubernetes Infrastructure

```runa
Process called "provision_k8s_cluster":
    Let cluster be Cloud.kubernetes_cluster()
        "prod-cluster",
        "1.27",
        3  Note: node count
    

    Let node_pool be Cloud.node_pool()
        cluster,
        "default-pool",
        "n1-standard-4",
        5
    

    Cloud.provision(cluster)
    Cloud.provision(node_pool)
End Process
```

---

## Summary

**Runa replaces IaC languages with:**
- ✅ Type-safe resource definitions
- ✅ Multi-cloud support
- ✅ State management
- ✅ Executable infrastructure code

**Stop using:** Terraform HCL, CloudFormation
**Start using:** `infrastructure.runa`

---

**End of Document**

---

# Kubernetes Deployment

---

## Overview

**Runa replaces Kubernetes YAML manifests with executable `.runa` files.**

**Replaces:**
- ❌ Deployment YAML
- ❌ Service YAML
- ❌ ConfigMap/Secret YAML
- ❌ Helm charts
- ❌ Kustomize overlays

---

## Basic Deployment

**File:** `k8s_deployment.runa`

```runa
Note: Kubernetes deployment specification
Note: Replaces deployment.yaml

Import "runa/kubernetes" as K8s

Type called "PodSpec":
    image : String
    replicas : Integer
    ports : List[Integer]
    env : Dictionary[String, String]
End Type

Type called "ServiceSpec":
    name : String
    type : String
    ports : List[Integer]
    selector : Dictionary[String, String]
End Type

Process called "define_deployment" returns PodSpec:
    return PodSpec(
        image: "myapp:1.0",
        replicas: 3,
        ports: [8080],
        env: {
            "DATABASE_URL": "postgresql://db:5432/myapp",
            "REDIS_URL": "redis://redis:6379"
        }
    )
End Process

Process called "define_service" returns ServiceSpec:
    return ServiceSpec(
        name: "myapp-service",
        type: "LoadBalancer",
        ports: [80],
        selector: {
            "app": "myapp"
        }
    )
End Process

Process called "main":
    Let deployment be define_deployment()
    Let service be define_service()

    K8s.apply_deployment("myapp", deployment
    K8s.apply_service(service

    Display "✓ Kubernetes resources applied"
End Process
```

---

## Kubernetes YAML Comparison

**Before (deployment.yaml):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:1.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          value: postgresql://db:5432/myapp
```

**After (k8s_deployment.runa):**
```runa
Let deployment be K8s.deployment("myapp", {
    "image": "myapp:1.0",
    "replicas": 3,
    "port": 8080,
    "env": {
        "DATABASE_URL": "postgresql://db:5432/myapp"
    }
})

K8s.apply(deployment)
```

---

## ConfigMap and Secrets

```runa
Process called "create_config":
    Let config_map be K8s.configmap("app-config", {
        "API_URL": "https://api.example.com",
        "MAX_CONNECTIONS": "100",
        "LOG_LEVEL": "INFO"
    })

    Let secret be K8s.secret("app-secrets", {
        "DATABASE_PASSWORD": "supersecret",
        "API_KEY": "abc123xyz789"
    })

    K8s.apply(config_map)
    K8s.apply(secret)
End Process
```

---

## Helm Chart Replacement

**File:** `helm_app.runa`

```runa
Note: Replaces Helm chart with values

Type called "HelmValues":
    release_name : String
    namespace : String
    replicas : Integer
    image_tag : String
    service_type : String
End Type

Process called "install_helm_chart"(values : HelmValues):
    Let deployment be K8s.deployment(values.release_name), {
        "image": "myapp:" + values.image_tag,
        "replicas": values.replicas
    }

    Let service be K8s.service(values.release_name + "-service", {
        "type": values.service_type
    }

    K8s.create_namespace(values.namespace
    K8s.apply_in_namespace(values.namespace, deployment
    K8s.apply_in_namespace(values.namespace, service
End Process

Process called "main":
    Let prod_values be HelmValues()
        release_name: "myapp-prod",
        namespace: "production",
        replicas: 5,
        image_tag: "1.0.0",
        service_type: "LoadBalancer"
    

    install_helm_chart(prod_values
End Process
```

---

## StatefulSet for Databases

```runa
Process called "deploy_database":
    Let statefulset be K8s.statefulset("postgres", {
        "image": "postgres:14",
        "replicas": 3,
        "volume_claim_template": {
            "storage": "10Gi",
            "storage_class": "fast-ssd"
        },
        "env": {
            "POSTGRES_PASSWORD": "secret"
        }
    })

    K8s.apply(statefulset)
End Process
```

---

## Ingress Configuration

```runa
Process called "configure_ingress":
    Let ingress be K8s.ingress("myapp-ingress", {
        "host": "myapp.example.com",
        "tls_enabled": true,
        "cert_secret": "myapp-tls-cert",
        "rules": [
            route("/", "myapp-service", 80),
            route("/api", "api-service", 8080)
        ]
    })

    K8s.apply(ingress)
End Process

Process called "route"(path : String, service : String, port : Integer) returns Dictionary[String, Any]:
    return {
        "path": path,
        "service": service,
        "port": port
    }
End Process
```

---

## Multi-Environment Deployment

```runa
Process called "deploy_to_environment"(env : String):
    Let config be match env:
        When "development":
            env_config(1, "dev", "NodePort"
        When "staging":
            env_config(3, "staging", "LoadBalancer"
        When "production":
            env_config(5, "prod", "LoadBalancer"
        Otherwise:
            panic("Unknown environment: " + env
    End Match

    deploy_with_config(config
End Process

Process called "env_config"(replicas : Integer, namespace : String, service_type : String) returns Dictionary[String, Any]:
    return {
        "replicas": replicas,
        "namespace": namespace,
        "service_type": service_type
    }
End Process
```

---

## Summary

**Runa replaces Kubernetes YAML with:**
- ✅ Type-safe resource definitions
- ✅ Executable deployment logic
- ✅ Multi-environment support
- ✅ Replaces Helm and Kustomize

**Stop using:** YAML manifests, Helm charts
**Start using:** `k8s_deployment.runa`

---

**End of Document**

---

# Container Specification

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
    base_image : String
    working_dir : String
    environment : Dictionary[String, String]
    ports : List[Integer]
    volumes : List[String]
    commands : List[String]
End Type

Process called "define_container" returns ContainerSpec:
    return ContainerSpec(
        base_image: "runa/runtime:1.0",
        working_dir: "/app",
        environment: {
            "RUNA_ENV": "production",
            "PORT": "8080"
        },
        ports: [8080, 443],
        volumes: ["/app/data", "/app/logs"],
        commands: [
            "runa install-dependencies",
            "runa build.runa",
            "runa start-server"
        ]
    )
End Process

Process called "main":
    Let spec be define_container()
    Container.build(spec, "myapp:1.0")
    Display "✓ Container image built: myapp:1.0"
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
    Let spec be ContainerSpec()
        base_image: "ubuntu:22.04",
        working_dir: "/app",
        commands: [
            "copy . /app",
            "apt-get update && apt-get install -y runa-compiler",
            "runa build.runa"
        ],
        ports: [8080],
        entrypoint: ["runa", "start-server"]
    )

    Container.build(spec, "myapp:latest")
End Process
```

---

## Multi-Stage Builds

```runa
Process called "multi_stage_build":
    Note: Stage 1 - Build
    Let build_stage be ContainerSpec(
        base_image: "runa/compiler:1.0",
        working_dir: "/build",
        commands: [
            "copy src/ /build/src/",
            "runa build.runa compile"
        ]
    )

    Container.build_stage(build_stage, "builder")

    Note: Stage 2 - Runtime
    Let runtime_stage be ContainerSpec(
        base_image: "runa/runtime:1.0",
        working_dir: "/app",
        commands: [
            "copy --from=builder /build/bin/myapp /app/myapp"
        ],
        entrypoint: ["/app/myapp"]
    )

    Container.build(runtime_stage, "myapp:1.0")
End Process
```

---

## Docker Compose Replacement

**File:** `compose.runa`

```runa
Note: Multi-container application
Note: Replaces docker-compose.yml

Type called "Service":
    name : String
    image : String
    ports : List[String]
    environment : Dictionary[String, String]
    depends_on : List[String]
End Type

Process called "define_services" returns List[Service]:
    Let web be Service(
        name: "web",
        image: "myapp:1.0",
        ports: ["8080:80"],
        environment: {
            "DATABASE_URL": "postgresql://db:5432/myapp"
        },
        depends_on: ["database"]
    )

    Let database be Service(
        name: "database",
        image: "postgres:14",
        ports: ["5432:5432"],
        environment: {
            "POSTGRES_PASSWORD": "secret"
        },
        depends_on: []
    )

    return [web, database]
End Process

Process called "main":
    Let services be define_services()
    Container.compose_up(services)
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

## Related Documentation

For more information on Runa language features used in deployment:

- [Runa Language Specification](./runa_language_specification.md) - Core language syntax and semantics
- [Runa Type System](./runa_type_system.md) - Type definitions and generic types
- [Runa Annotation System](./runa_annotation_system.md) - AI annotations for reasoning and implementation
- [Runa Standard Library](./runa_standard_library.md) - Built-in modules and functions
- [Runa Tools and Ecosystem](./runa_tools_and_ecosystem.md) - Compiler, tooling, and integrations

---