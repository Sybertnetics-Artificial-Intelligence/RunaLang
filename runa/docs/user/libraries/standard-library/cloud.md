# Runa Cloud Infrastructure Module Guide

The Runa Cloud module provides comprehensive cloud infrastructure integration, container orchestration, and infrastructure-as-code capabilities. This module enables seamless interaction with major cloud providers and containerization platforms using Runa's natural language syntax.

## Overview

The cloud module consists of seven main components:

- **docker.runa**: Docker container and image management
- **kubernetes.runa**: Kubernetes cluster orchestration and resource management
- **aws.runa**: Amazon Web Services integration and service management
- **azure.runa**: Microsoft Azure cloud services integration
- **gcp.runa**: Google Cloud Platform services integration
- **serverless.runa**: Universal serverless computing abstractions
- **terraform.runa**: Infrastructure as code management and deployment

## Docker Container Management (`docker.runa`)

### Container Lifecycle Operations

```runa
Note: Create and manage Docker containers
Let container_config be empty Dictionary[String, Any]
Set container_config at "image" to "nginx:latest"
Set container_config at "name" to "web-server"
Set container_config at "ports" to list containing "80:8080", "443:8443"
Set container_config at "environment" to list containing "ENV=production", "DEBUG=false"
Set container_config at "volumes" to list containing "/data:/app/data", "/logs:/app/logs"

Let create_result be create_docker_container with container_config

If create_result at "success" is true:
    Let container_id be create_result at "container_id" as String
    Display "Container created with ID: " with message container_id
    
    Note: Start the container
    Let start_result be start_docker_container with container_id
    
    If start_result at "success" is true:
        Display "Container started successfully"
    Otherwise:
        Display "Failed to start container: " with message start_result at "error"
```

### Image Operations and Registry Management

```runa
Note: Build custom Docker images
Let build_config be empty Dictionary[String, Any]
Set build_config at "dockerfile_path" to "./Dockerfile"
Set build_config at "context" to "."
Set build_config at "tag" to "myapp:v1.0.0"
Set build_config at "build_args" to empty Dictionary[String, String]
Set build_config at "build_args" at "VERSION" to "1.0.0"
Set build_config at "build_args" at "ENVIRONMENT" to "production"

Let build_result be build_docker_image with build_config

If build_result at "success" is true:
    Display "Image built successfully"
    
    Note: Push to registry
    Let push_result be push_docker_image with "myapp:v1.0.0"
    
    If push_result at "success" is true:
        Display "Image pushed to registry"

Note: Pull images from registry
Let pull_result be pull_docker_image with "redis:alpine"
Let images_list be list_docker_images

Display "Available images:"
For each image in images_list at "images" as List[Dictionary[String, Any]]:
    Display "- " with message image at "repository" as String with message ":" with message image at "tag" as String
```

### Docker Compose Orchestration

```runa
Note: Deploy multi-container applications
Let compose_config be empty Dictionary[String, Any]
Set compose_config at "compose_file" to "docker-compose.yml"
Set compose_config at "project_name" to "web-application"
Set compose_config at "detached" to true
Set compose_config at "build" to true
Set compose_config at "environment_file" to ".env.production"

Let deploy_result be docker_compose_up with compose_config

If deploy_result at "success" is true:
    Display "Application deployed successfully"
    
    Note: Check service status
    Let status_result be docker_compose_status with "web-application"
    
    For each service in status_result at "services" as List[Dictionary[String, Any]]:
        Let service_name be service at "name" as String
        Let service_status be service at "status" as String
        Display service_name with message " is " with message service_status
```

### Container Monitoring and Logging

```runa
Note: Monitor container performance
Let stats_config be empty Dictionary[String, Any]
Set stats_config at "container" to "web-server"
Set stats_config at "stream" to false

Let stats_result be get_docker_container_stats with stats_config

If stats_result at "success" is true:
    Let stats_data be stats_result at "stats" as Dictionary[String, Any]
    Display "CPU Usage: " with message stats_data at "cpu_percent" as Float
    Display "Memory Usage: " with message stats_data at "memory_usage" as Integer with message " MB"
    Display "Network I/O: " with message stats_data at "network_io" as String

Note: Retrieve container logs
Let log_config be empty Dictionary[String, Any]
Set log_config at "container" to "web-server"
Set log_config at "tail" to 100
Set log_config at "follow" to false
Set log_config at "timestamps" to true

Let logs_result be get_docker_container_logs with log_config
Display "Recent logs:"
Display logs_result at "logs" as String
```

## Kubernetes Cluster Management (`kubernetes.runa`)

### Application Deployment and Management

```runa
Note: Deploy applications to Kubernetes cluster
Let deployment_config be empty Dictionary[String, Any]
Set deployment_config at "name" to "web-app-deployment"
Set deployment_config at "namespace" to "production"
Set deployment_config at "image" to "myapp:v1.0.0"
Set deployment_config at "replicas" to 3
Set deployment_config at "ports" to list containing 8080
Set deployment_config at "environment" to empty Dictionary[String, String]
Set deployment_config at "environment" at "DATABASE_URL" to "postgresql://db:5432/appdb"
Set deployment_config at "environment" at "REDIS_URL" to "redis://cache:6379"

Let deployment_result be create_kubernetes_deployment with deployment_config

If deployment_result at "success" is true:
    Display "Deployment created successfully"
    
    Note: Create service to expose the deployment
    Let service_config be empty Dictionary[String, Any]
    Set service_config at "name" to "web-app-service"
    Set service_config at "namespace" to "production"
    Set service_config at "selector" to empty Dictionary[String, String]
    Set service_config at "selector" at "app" to "web-app-deployment"
    Set service_config at "ports" to list containing empty Dictionary[String, Integer]
    Set service_config at "ports" at 0 at "port" to 80
    Set service_config at "ports" at 0 at "targetPort" to 8080
    Set service_config at "type" to "LoadBalancer"
    
    Let service_result be create_kubernetes_service with service_config
```

### Resource Management and Configuration

```runa
Note: Create ConfigMaps for application configuration
Let configmap_config be empty Dictionary[String, Any]
Set configmap_config at "name" to "app-config"
Set configmap_config at "namespace" to "production"
Set configmap_config at "data" to empty Dictionary[String, String]
Set configmap_config at "data" at "database.host" to "postgresql.production.local"
Set configmap_config at "data" at "cache.redis.url" to "redis://cache.production.local:6379"
Set configmap_config at "data" at "app.log.level" to "info"

Let configmap_result be create_kubernetes_configmap with configmap_config

Note: Create Secrets for sensitive data
Let secret_config be empty Dictionary[String, Any]
Set secret_config at "name" to "app-secrets"
Set secret_config at "namespace" to "production"
Set secret_config at "data" to empty Dictionary[String, String]
Set secret_config at "data" at "database.password" to "super-secure-password"
Set secret_config at "data" at "api.key" to "secret-api-key-12345"

Let secret_result be create_kubernetes_secret with secret_config

Note: Create persistent storage
Let pv_config be empty Dictionary[String, Any]
Set pv_config at "name" to "app-storage"
Set pv_config at "size" to "10Gi"
Set pv_config at "access_modes" to list containing "ReadWriteOnce"
Set pv_config at "storage_class" to "ssd"
Set pv_config at "mount_path" to "/app/data"

Let pv_result be create_kubernetes_persistent_volume with pv_config
```

### Cluster Monitoring and Scaling

```runa
Note: Monitor cluster resources
Let cluster_info be get_kubernetes_cluster_info

Display "Kubernetes Cluster Status:"
Display "Version: " with message cluster_info at "version" as String
Display "Nodes: " with message cluster_info at "node_count" as Integer
Display "Namespaces: " with message cluster_info at "namespace_count" as Integer

Note: Configure horizontal pod autoscaling
Let hpa_config be empty Dictionary[String, Any]
Set hpa_config at "name" to "web-app-hpa"
Set hpa_config at "namespace" to "production"
Set hpa_config at "target_deployment" to "web-app-deployment"
Set hpa_config at "min_replicas" to 2
Set hpa_config at "max_replicas" to 10
Set hpa_config at "cpu_threshold" to 70
Set hpa_config at "memory_threshold" to 80

Let hpa_result be create_kubernetes_hpa with hpa_config

If hpa_result at "success" is true:
    Display "Horizontal Pod Autoscaler configured"
```

## Amazon Web Services Integration (`aws.runa`)

### EC2 Instance Management

```runa
Note: Launch and manage EC2 instances
Let instance_config be empty Dictionary[String, Any]
Set instance_config at "image_id" to "ami-0abcdef1234567890"
Set instance_config at "instance_type" to "t3.medium"
Set instance_config at "key_name" to "production-keypair"
Set instance_config at "security_groups" to list containing "web-servers", "database-clients"
Set instance_config at "subnet_id" to "subnet-12345678"
Set instance_config at "user_data" to "#!/bin/bash\nyum update -y\nyum install -y httpd\nsystemctl start httpd"

Let instance_result be create_ec2_instance with instance_config

If instance_result at "success" is true:
    Let instance_id be instance_result at "instance_id" as String
    Display "Instance launched: " with message instance_id
    
    Note: Wait for instance to be running
    Let wait_result be wait_for_ec2_instance_state with instance_id and "running"
    
    If wait_result at "success" is true:
        Let instance_details be describe_ec2_instance with instance_id
        Let public_ip be instance_details at "public_ip" as String
        Display "Instance is running at: " with message public_ip
```

### S3 Storage Management

```runa
Note: Create and manage S3 buckets
Let bucket_name be "application-data-" concatenated with current_timestamp as String
Let bucket_region be "us-west-2"

Let create_bucket_result be create_s3_bucket with bucket_name and bucket_region

If create_bucket_result at "success" is true:
    Display "S3 bucket created: " with message bucket_name
    
    Note: Configure bucket policy for security
    Let policy_config be empty Dictionary[String, Any]
    Set policy_config at "bucket" to bucket_name
    Set policy_config at "policy" to s3_public_read_policy_json
    
    Let policy_result be set_s3_bucket_policy with policy_config
    
    Note: Upload files to bucket
    Let upload_config be empty Dictionary[String, Any]
    Set upload_config at "bucket" to bucket_name
    Set upload_config at "key" to "uploads/application.zip"
    Set upload_config at "file_path" to "./dist/application.zip"
    Set upload_config at "metadata" to empty Dictionary[String, String]
    Set upload_config at "metadata" at "Content-Type" to "application/zip"
    Set upload_config at "metadata" at "Cache-Control" to "max-age=3600"
    
    Let upload_result be upload_s3_object with upload_config
    
    If upload_result at "success" is true:
        Display "File uploaded successfully"
```

### Lambda Serverless Functions

```runa
Note: Deploy and manage Lambda functions
Let function_config be empty Dictionary[String, Any]
Set function_config at "function_name" to "data-processor"
Set function_config at "runtime" to "python3.9"
Set function_config at "handler" to "lambda_function.lambda_handler"
Set function_config at "role" to "arn:aws:iam::123456789012:role/lambda-execution-role"
Set function_config at "zip_file_path" to "./function.zip"
Set function_config at "memory_size" to 512
Set function_config at "timeout" to 30
Set function_config at "environment_variables" to empty Dictionary[String, String]
Set function_config at "environment_variables" at "DATABASE_URL" to "postgresql://rds-instance:5432/db"
Set function_config at "environment_variables" at "S3_BUCKET" to bucket_name

Let function_result be create_lambda_function with function_config

If function_result at "success" is true:
    Display "Lambda function deployed successfully"
    
    Note: Set up S3 trigger
    Let trigger_config be empty Dictionary[String, Any]
    Set trigger_config at "function_name" to "data-processor"
    Set trigger_config at "source_arn" to "arn:aws:s3:::" concatenated with bucket_name
    Set trigger_config at "events" to list containing "s3:ObjectCreated:*"
    
    Let trigger_result be add_lambda_trigger with trigger_config
    
    Note: Test function invocation
    Let invoke_config be empty Dictionary[String, Any]
    Set invoke_config at "function_name" to "data-processor"
    Set invoke_config at "payload" to "{\"test\": \"data\", \"bucket\": \"" concatenated with bucket_name concatenated with "\"}"
    Set invoke_config at "invocation_type" to "RequestResponse"
    
    Let invoke_result be invoke_lambda_function with invoke_config
    Display "Function response: " with message invoke_result at "response" as String
```

## Microsoft Azure Integration (`azure.runa`)

### Virtual Machine Management

```runa
Note: Create and manage Azure VMs
Let vm_config be empty Dictionary[String, Any]
Set vm_config at "vm_name" to "production-web-01"
Set vm_config at "resource_group" to "production-rg"
Set vm_config at "location" to "East US"
Set vm_config at "vm_size" to "Standard_B2s"
Set vm_config at "image" to empty Dictionary[String, String]
Set vm_config at "image" at "publisher" to "Canonical"
Set vm_config at "image" at "offer" to "0001-com-ubuntu-server-focal"
Set vm_config at "image" at "sku" to "20_04-lts-gen2"
Set vm_config at "admin_username" to "azureuser"
Set vm_config at "authentication_type" to "ssh"

Let vm_result be create_azure_vm with vm_config

If vm_result at "success" is true:
    Display "Azure VM created successfully"
    
    Note: Configure networking
    Let network_config be empty Dictionary[String, Any]
    Set network_config at "vm_name" to "production-web-01"
    Set network_config at "resource_group" to "production-rg"
    Set network_config at "network_security_group" to "web-nsg"
    Set network_config at "public_ip" to true
    Set network_config at "load_balancer" to "web-lb"
    
    Let network_result be configure_azure_vm_networking with network_config
```

### Azure Storage and Functions

```runa
Note: Create Azure Storage account
Let storage_config be empty Dictionary[String, Any]
Set storage_config at "account_name" to "productionstorage" concatenated with current_timestamp as String
Set storage_config at "resource_group" to "production-rg"
Set storage_config at "location" to "East US"
Set storage_config at "sku" to "Standard_LRS"
Set storage_config at "kind" to "StorageV2"

Let storage_result be create_azure_storage_account with storage_config

If storage_result at "success" is true:
    Let storage_account be storage_result at "account_name" as String
    Display "Storage account created: " with message storage_account
    
    Note: Deploy Azure Function
    Let function_config be empty Dictionary[String, Any]
    Set function_config at "function_app_name" to "data-processor-functions"
    Set function_config at "resource_group" to "production-rg"
    Set function_config at "location" to "East US"
    Set function_config at "runtime" to "python"
    Set function_config at "version" to "3.9"
    Set function_config at "storage_account" to storage_account
    Set function_config at "code_path" to "./azure-functions.zip"
    
    Let azure_function_result be deploy_azure_function with function_config
```

## Google Cloud Platform Integration (`gcp.runa`)

### Compute Engine Operations

```runa
Note: Create GCP VM instances
Let gce_config be empty Dictionary[String, Any]
Set gce_config at "instance_name" to "production-web-gcp"
Set gce_config at "zone" to "us-central1-a"
Set gce_config at "machine_type" to "e2-medium"
Set gce_config at "boot_disk_image" to "projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20240307"
Set gce_config at "network_tags" to list containing "http-server", "https-server"
Set gce_config at "metadata" to empty Dictionary[String, String]
Set gce_config at "metadata" at "startup-script" to "#!/bin/bash\napt-get update\napt-get install -y nginx"

Let gce_result be create_gce_instance with gce_config

If gce_result at "success" is true:
    Display "GCE instance created successfully"
    
    Note: Create instance group for load balancing
    Let group_config be empty Dictionary[String, Any]
    Set group_config at "group_name" to "web-servers-group"
    Set group_config at "zone" to "us-central1-a"
    Set group_config at "base_instance_name" to "web-server"
    Set group_config at "target_size" to 3
    Set group_config at "template" to "web-server-template"
    
    Let group_result be create_gce_instance_group with group_config
```

### Cloud Storage and Functions

```runa
Note: Create and manage GCS buckets
Let gcs_config be empty Dictionary[String, Any]
Set gcs_config at "bucket_name" to "production-app-storage-gcp"
Set gcs_config at "location" to "US-CENTRAL1"
Set gcs_config at "storage_class" to "STANDARD"
Set gcs_config at "versioning" to true

Let gcs_result be create_gcs_bucket with gcs_config

If gcs_result at "success" is true:
    Let bucket_name be gcs_result at "bucket_name" as String
    Display "GCS bucket created: " with message bucket_name
    
    Note: Deploy Cloud Function
    Let gcf_config be empty Dictionary[String, Any]
    Set gcf_config at "function_name" to "process-uploaded-data"
    Set gcf_config at "runtime" to "python39"
    Set gcf_config at "entry_point" to "main"
    Set gcf_config at "source_path" to "./cloud-functions/"
    Set gcf_config at "trigger" to empty Dictionary[String, String]
    Set gcf_config at "trigger" at "eventType" to "google.storage.object.finalize"
    Set gcf_config at "trigger" at "resource" to bucket_name
    
    Let gcf_result be deploy_gcp_cloud_function with gcf_config
```

## Universal Serverless Computing (`serverless.runa`)

### Cross-Platform Function Deployment

```runa
Note: Define serverless function configuration
Let serverless_function be empty ServerlessFunction
Set serverless_function.name to "universal-data-processor"
Set serverless_function.runtime to "python3.9"
Set serverless_function.handler to "main.handler"
Set serverless_function.memory_mb to 512
Set serverless_function.timeout_seconds to 30
Set serverless_function.source_code_path to "./functions/processor/"
Set serverless_function.environment_variables to empty Dictionary[String, String]
Set serverless_function.environment_variables at "DATABASE_URL" to "postgresql://db.example.com:5432/appdb"
Set serverless_function.environment_variables at "API_ENDPOINT" to "https://api.example.com/v1"

Note: Deploy to multiple cloud providers
Let aws_deployment_config be empty Dictionary[String, Any]
Set aws_deployment_config at "region" to "us-west-2"
Set aws_deployment_config at "iam_role" to "arn:aws:iam::123456789012:role/lambda-execution-role"

Let aws_deployment be deploy_serverless_function with serverless_function and "aws" and aws_deployment_config

Let azure_deployment_config be empty Dictionary[String, Any]
Set azure_deployment_config at "resource_group" to "serverless-functions-rg"
Set azure_deployment_config at "location" to "eastus"

Let azure_deployment be deploy_serverless_function with serverless_function and "azure" and azure_deployment_config

Let gcp_deployment_config be empty Dictionary[String, Any]
Set gcp_deployment_config at "region" to "us-central1"
Set gcp_deployment_config at "project_id" to "my-gcp-project"

Let gcp_deployment be deploy_serverless_function with serverless_function and "gcp" and gcp_deployment_config

Note: Monitor deployments across providers
Let deployments be list containing aws_deployment, azure_deployment, gcp_deployment
Let monitoring_result be monitor_serverless_functions with deployments

For each deployment in deployments:
    Let provider be deployment at "provider" as String
    Let status be deployment at "status" as String
    Let function_url be deployment at "function_url" as String
    Display provider with message " deployment: " with message status with message " at " with message function_url
```

### Event-Driven Serverless Workflows

```runa
Note: Configure serverless event handling
Let event_config be empty Dictionary[String, Any]
Set event_config at "function_name" to "universal-data-processor"
Set event_config at "event_sources" to list containing
    empty Dictionary[String, String],
    empty Dictionary[String, String],
    empty Dictionary[String, String]

Set event_config at "event_sources" at 0 at "type" to "http"
Set event_config at "event_sources" at 0 at "path" to "/webhook/data"
Set event_config at "event_sources" at 0 at "method" to "POST"

Set event_config at "event_sources" at 1 at "type" to "storage"
Set event_config at "event_sources" at 1 at "bucket" to "data-ingestion-bucket"
Set event_config at "event_sources" at 1 at "event" to "object.created"

Set event_config at "event_sources" at 2 at "type" to "queue"
Set event_config at "event_sources" at 2 at "queue_name" to "data-processing-queue"

Let event_setup_result be configure_serverless_events with event_config

Note: Create serverless workflow
Let workflow_config be empty Dictionary[String, Any]
Set workflow_config at "workflow_name" to "data-processing-pipeline"
Set workflow_config at "steps" to list containing
    empty Dictionary[String, String],
    empty Dictionary[String, String],
    empty Dictionary[String, String]

Set workflow_config at "steps" at 0 at "function" to "data-validator"
Set workflow_config at "steps" at 0 at "next" to "data-transformer"

Set workflow_config at "steps" at 1 at "function" to "data-transformer"
Set workflow_config at "steps" at 1 at "next" to "data-loader"

Set workflow_config at "steps" at 2 at "function" to "data-loader"
Set workflow_config at "steps" at 2 at "next" to "complete"

Let workflow_result be create_serverless_workflow with workflow_config
```

## Infrastructure as Code with Terraform (`terraform.runa`)

### Terraform Project Management

```runa
Note: Initialize and configure Terraform project
Let terraform_project_path be "./infrastructure"
Let tf_config be empty Dictionary[String, Any]
Set tf_config at "working_directory" to terraform_project_path
Set tf_config at "backend_config" to empty Dictionary[String, String]
Set tf_config at "backend_config" at "bucket" to "terraform-state-production"
Set tf_config at "backend_config" at "key" to "production/terraform.tfstate"
Set tf_config at "backend_config" at "region" to "us-west-2"
Set tf_config at "backend_config" at "dynamodb_table" to "terraform-state-lock"

Let init_result be terraform_init with tf_config

If init_result at "success" is true:
    Display "Terraform initialized successfully"
    
    Note: Plan infrastructure changes
    Let plan_config be empty Dictionary[String, Any]
    Set plan_config at "working_directory" to terraform_project_path
    Set plan_config at "var_file" to "production.tfvars"
    Set plan_config at "out" to "production.tfplan"
    Set plan_config at "variables" to empty Dictionary[String, String]
    Set plan_config at "variables" at "environment" to "production"
    Set plan_config at "variables" at "instance_count" to "3"
    
    Let plan_result be terraform_plan with plan_config
    
    If plan_result at "success" is true:
        Display "Terraform plan generated successfully"
        Display "Planned changes:"
        Display plan_result at "output" as String
        
        Note: Apply infrastructure changes
        Let apply_result be terraform_apply with terraform_project_path and "production.tfplan"
        
        If apply_result at "success" is true:
            Display "Infrastructure deployed successfully"
            
            Note: Get output values
            Let outputs_result be terraform_output with terraform_project_path
            Let load_balancer_dns be outputs_result at "load_balancer_dns_name" as String
            Let database_endpoint be outputs_result at "database_endpoint" as String
            
            Display "Application URL: " with message load_balancer_dns
            Display "Database endpoint: " with message database_endpoint
```

### Terraform Workspace and State Management

```runa
Note: Manage multiple environments with workspaces
Let staging_workspace_result be terraform_create_workspace with terraform_project_path and "staging"

If staging_workspace_result at "success" is true:
    Display "Staging workspace created"
    
    Let switch_result be terraform_select_workspace with terraform_project_path and "staging"
    
    If switch_result at "success" is true:
        Display "Switched to staging workspace"
        
        Note: Deploy staging environment
        Let staging_plan_config be empty Dictionary[String, Any]
        Set staging_plan_config at "working_directory" to terraform_project_path
        Set staging_plan_config at "var_file" to "staging.tfvars"
        Set staging_plan_config at "out" to "staging.tfplan"
        
        Let staging_plan_result be terraform_plan with staging_plan_config
        
        If staging_plan_result at "success" is true:
            Let staging_apply_result be terraform_apply with terraform_project_path and "staging.tfplan"

Note: Import existing resources
Let import_config be empty Dictionary[String, Any]
Set import_config at "working_directory" to terraform_project_path
Set import_config at "resource_address" to "aws_instance.web_server"
Set import_config at "resource_id" to "i-1234567890abcdef0"

Let import_result be terraform_import with import_config

Note: Manage Terraform state
Let state_list_result be terraform_state_list with terraform_project_path
Display "Resources in state:"
For each resource in state_list_result at "resources" as List[String]:
    Display "- " with message resource

Let state_show_result be terraform_state_show with terraform_project_path and "aws_instance.web_server"
Display "Resource details:"
Display state_show_result at "resource_details" as String
```

### Terraform Module Management

```runa
Note: Create and use Terraform modules
Let module_config be empty Dictionary[String, Any]
Set module_config at "module_name" to "vpc"
Set module_config at "module_path" to "./modules/vpc"
Set module_config at "variables" to empty Dictionary[String, String]
Set module_config at "variables" at "cidr_block" to "10.0.0.0/16"
Set module_config at "variables" at "availability_zones" to "us-west-2a,us-west-2b,us-west-2c"

Let module_result be create_terraform_module with module_config

Note: Validate Terraform configuration
Let validate_result be terraform_validate with terraform_project_path

If validate_result at "success" is true:
    Display "Terraform configuration is valid"
Otherwise:
    Display "Configuration errors:"
    Display validate_result at "errors" as String

Note: Format Terraform code
Let format_result be terraform_format with terraform_project_path and true  # Write changes

If format_result at "success" is true:
    Display "Terraform code formatted successfully"
```

## Integration Examples

### Complete Multi-Cloud Deployment

```runa
Note: Deploy application across multiple cloud providers
Process called "deploy_multi_cloud_application" that takes app_config as Dictionary[String, Any] returns Dictionary[String, Any]:
    Let deployment_results be empty Dictionary[String, Any]
    
    Note: Deploy to AWS
    Let aws_config be empty Dictionary[String, Any]
    Set aws_config at "region" to app_config at "aws_region" as String
    Set aws_config at "instance_type" to app_config at "instance_type" as String
    
    Let aws_result be deploy_to_aws with app_config and aws_config
    Set deployment_results at "aws" to aws_result
    
    Note: Deploy to Azure
    Let azure_config be empty Dictionary[String, Any]
    Set azure_config at "location" to app_config at "azure_location" as String
    Set azure_config at "vm_size" to app_config at "vm_size" as String
    
    Let azure_result be deploy_to_azure with app_config and azure_config
    Set deployment_results at "azure" to azure_result
    
    Note: Deploy to GCP
    Let gcp_config be empty Dictionary[String, Any]
    Set gcp_config at "zone" to app_config at "gcp_zone" as String
    Set gcp_config at "machine_type" to app_config at "machine_type" as String
    
    Let gcp_result be deploy_to_gcp with app_config and gcp_config
    Set deployment_results at "gcp" to gcp_result
    
    Return deployment_results

Let application_config be empty Dictionary[String, Any]
Set application_config at "app_name" to "web-application"
Set application_config at "image" to "myapp:v1.0.0"
Set application_config at "aws_region" to "us-west-2"
Set application_config at "azure_location" to "East US"
Set application_config at "gcp_zone" to "us-central1-a"
Set application_config at "instance_type" to "t3.medium"
Set application_config at "vm_size" to "Standard_B2s"
Set application_config at "machine_type" to "e2-medium"

Let multi_cloud_result be deploy_multi_cloud_application with application_config

For each provider in keys of multi_cloud_result:
    Let result be multi_cloud_result at provider as Dictionary[String, Any]
    Display provider with message " deployment: " with message result at "status" as String
```

### Disaster Recovery and Backup

```runa
Note: Implement disaster recovery across cloud providers
Process called "setup_disaster_recovery" that takes primary_provider as String and backup_provider as String returns Dictionary[String, Any]:
    Let dr_config be empty Dictionary[String, Any]
    
    Note: Set up data replication
    Let replication_config be empty Dictionary[String, Any]
    Set replication_config at "source_provider" to primary_provider
    Set replication_config at "target_provider" to backup_provider
    Set replication_config at "replication_frequency" to "hourly"
    Set replication_config at "encryption" to true
    
    Let replication_result be setup_cross_cloud_replication with replication_config
    Set dr_config at "replication" to replication_result
    
    Note: Configure failover mechanism
    Let failover_config be empty Dictionary[String, Any]
    Set failover_config at "monitoring_interval" to 60  # seconds
    Set failover_config at "health_check_endpoint" to "/health"
    Set failover_config at "automatic_failover" to true
    Set failover_config at "notification_webhook" to "https://alerts.company.com/webhook"
    
    Let failover_result be configure_automatic_failover with failover_config
    Set dr_config at "failover" to failover_result
    
    Return dr_config

Let dr_setup_result be setup_disaster_recovery with "aws" and "azure"

If dr_setup_result at "replication" at "success" as Boolean is true:
    Display "Cross-cloud replication configured successfully"

If dr_setup_result at "failover" at "success" as Boolean is true:
    Display "Automatic failover configured successfully"
```

## Testing Your Code

The cloud module includes comprehensive test coverage. Run the test suite to verify functionality:

```bash
cd runa/
python -m pytest tests/unit/stdlib/test_cloud.runa -v
```

Key test categories:
- Docker container lifecycle management
- Kubernetes resource deployment and scaling
- AWS service integration and authentication
- Azure resource provisioning and management
- GCP service configuration and deployment
- Serverless function deployment across providers
- Terraform infrastructure provisioning and state management
- Cross-cloud disaster recovery and failover

## Performance Considerations

### Efficient Resource Management

```runa
Note: Optimize cloud resource utilization
Process called "optimize_cloud_resources" that takes resource_config as Dictionary[String, Any] returns Dictionary[String, Any]:
    Let optimization_results be empty Dictionary[String, Any]
    
    Note: Configure auto-scaling
    Let autoscaling_config be empty Dictionary[String, Any]
    Set autoscaling_config at "min_instances" to resource_config at "min_instances" as Integer
    Set autoscaling_config at "max_instances" to resource_config at "max_instances" as Integer
    Set autoscaling_config at "target_cpu_utilization" to 70
    Set autoscaling_config at "target_memory_utilization" to 80
    Set autoscaling_config at "scale_up_cooldown" to 300  # seconds
    Set autoscaling_config at "scale_down_cooldown" to 600  # seconds
    
    Let scaling_result be configure_auto_scaling with autoscaling_config
    Set optimization_results at "autoscaling" to scaling_result
    
    Note: Set up resource monitoring
    Let monitoring_config be empty Dictionary[String, Any]
    Set monitoring_config at "metrics" to list containing "CPU", "Memory", "Network", "Disk"
    Set monitoring_config at "alert_thresholds" to empty Dictionary[String, Integer]
    Set monitoring_config at "alert_thresholds" at "cpu_high" to 85
    Set monitoring_config at "alert_thresholds" at "memory_high" to 90
    Set monitoring_config at "alert_thresholds" at "disk_high" to 85
    
    Let monitoring_result be setup_resource_monitoring with monitoring_config
    Set optimization_results at "monitoring" to monitoring_result
    
    Return optimization_results
```

### Cost Optimization

```runa
Note: Monitor and optimize cloud costs
Process called "optimize_cloud_costs" that takes cost_config as Dictionary[String, Any] returns Dictionary[String, Any]:
    Let cost_optimization be empty Dictionary[String, Any]
    
    Note: Set up cost alerts
    Let budget_config be empty Dictionary[String, Any]
    Set budget_config at "monthly_budget" to cost_config at "monthly_budget" as Float
    Set budget_config at "alert_thresholds" to list containing 50, 80, 100  # percentage thresholds
    Set budget_config at "notification_email" to cost_config at "notification_email" as String
    
    Let budget_result be create_cost_budget with budget_config
    Set cost_optimization at "budget" to budget_result
    
    Note: Implement resource tagging
    Let tagging_config be empty Dictionary[String, Any]
    Set tagging_config at "required_tags" to list containing "Environment", "Project", "Owner", "CostCenter"
    Set tagging_config at "enforce_tagging" to true
    
    Let tagging_result be enforce_resource_tagging with tagging_config
    Set cost_optimization at "tagging" to tagging_result
    
    Note: Schedule non-production resource cleanup
    Let cleanup_config be empty Dictionary[String, Any]
    Set cleanup_config at "environments" to list containing "development", "staging"
    Set cleanup_config at "cleanup_schedule" to "0 2 * * *"  # Daily at 2 AM
    Set cleanup_config at "retention_days" to 7
    
    Let cleanup_result be schedule_resource_cleanup with cleanup_config
    Set cost_optimization at "cleanup" to cleanup_result
    
    Return cost_optimization
```

## Advanced Features

### Multi-Cloud Load Balancing

```runa
Note: Implement intelligent load balancing across cloud providers
Process called "setup_multi_cloud_load_balancer" that takes lb_config as Dictionary[String, Any] returns Dictionary[String, Any]:
    Let load_balancer_setup be empty Dictionary[String, Any]
    
    Note: Configure health checks for each provider
    Let health_check_config be empty Dictionary[String, Any]
    Set health_check_config at "check_interval" to 30  # seconds
    Set health_check_config at "timeout" to 5  # seconds
    Set health_check_config at "healthy_threshold" to 2
    Set health_check_config at "unhealthy_threshold" to 3
    Set health_check_config at "path" to "/health"
    
    Let health_checks be setup_cross_cloud_health_checks with health_check_config
    Set load_balancer_setup at "health_checks" to health_checks
    
    Note: Configure traffic routing
    Let routing_config be empty Dictionary[String, Any]
    Set routing_config at "algorithm" to "least_connections"
    Set routing_config at "failover_enabled" to true
    Set routing_config at "geographic_routing" to lb_config at "geographic_routing" as Boolean
    Set routing_config at "latency_based_routing" to lb_config at "latency_based_routing" as Boolean
    
    Let routing_setup be configure_traffic_routing with routing_config
    Set load_balancer_setup at "routing" to routing_setup
    
    Return load_balancer_setup
```

### Container Orchestration at Scale

```runa
Note: Manage large-scale container deployments
Process called "deploy_microservices_architecture" that takes services_config as List[Dictionary[String, Any]] returns Dictionary[String, Any]:
    Let deployment_results be empty Dictionary[String, Any]
    
    For each service_config in services_config:
        Let service_name be service_config at "name" as String
        
        Note: Deploy service to Kubernetes
        Let k8s_deployment_config be empty Dictionary[String, Any]
        Set k8s_deployment_config at "name" to service_name
        Set k8s_deployment_config at "image" to service_config at "image" as String
        Set k8s_deployment_config at "replicas" to service_config at "replicas" as Integer
        Set k8s_deployment_config at "resources" to service_config at "resources" as Dictionary[String, Any]
        
        Let k8s_result be create_kubernetes_deployment with k8s_deployment_config
        
        Note: Create service mesh configuration
        Let mesh_config be empty Dictionary[String, Any]
        Set mesh_config at "service_name" to service_name
        Set mesh_config at "load_balancing" to "round_robin"
        Set mesh_config at "circuit_breaker" to true
        Set mesh_config at "retry_policy" to empty Dictionary[String, Integer]
        Set mesh_config at "retry_policy" at "max_retries" to 3
        Set mesh_config at "retry_policy" at "timeout_ms" to 5000
        
        Let mesh_result be configure_service_mesh with mesh_config
        
        Set deployment_results at service_name to empty Dictionary[String, Any]
        Set deployment_results at service_name at "kubernetes" to k8s_result
        Set deployment_results at service_name at "service_mesh" to mesh_result
    
    Return deployment_results
```

The Runa Cloud module provides comprehensive cloud infrastructure management capabilities suitable for enterprise-scale deployments. Its natural language syntax makes complex cloud operations accessible while maintaining the power and flexibility required for production environments across multiple cloud providers.