# Runa Infrastructure as Code Specification

**Version:** 1.0
**Status:** Canonical
**Last Updated:** 2025-10-08

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
    name as String
    instance_type as String
    ami as String
    region as String
    tags as Dictionary[String, String]
End Type

Type called "Database":
    name as String
    engine as String
    instance_class as String
    storage_gb as Integer
End Type

Type called "Infrastructure":
    vms as List[VirtualMachine]
    databases as List[Database]
    networks as List[Network]
End Type

Process called "define_infrastructure" returns Infrastructure:
    Let web_vm be a value of type VirtualMachine with
        name as "web-server",
        instance_type as "t3.medium",
        ami as "ami-12345",
        region as "us-east-1",
        tags as a dictionary containing:
            "Environment" as "production",
            "Role" as "web"
        End Dictionary

    Let db be a value of type Database with
        name as "prod-db",
        engine as "postgresql",
        instance_class as "db.t3.large",
        storage_gb as 100

    Return a value of type Infrastructure with
        vms as a list containing web_vm,
        databases as a list containing db,
        networks as an empty list
End Process

Process called "main":
    Let infra be define_infrastructure()

    Call Cloud.apply(infra)
    Call display("✓ Infrastructure provisioned")
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
    Let web_instance be vm(
        "web-server",
        "t3.medium",
        "ami-12345",
        tags("Environment", "production")
    )

    Let database be db(
        "prod-db",
        "postgresql",
        "db.t3.large",
        100
    )

    Call Cloud.provision(web_instance)
    Call Cloud.provision(database)
End Process
```

---

## Multi-Cloud Infrastructure

```runa
Process called "multi_cloud_deployment":
    Note: AWS Resources
    Let aws_vm be Cloud.aws_instance(
        "web-server-aws",
        "t3.medium",
        "us-east-1"
    )

    Note: Azure Resources
    Let azure_vm be Cloud.azure_vm(
        "web-server-azure",
        "Standard_B2s",
        "eastus"
    )

    Note: GCP Resources
    Let gcp_vm be Cloud.gcp_instance(
        "web-server-gcp",
        "n1-standard-2",
        "us-central1"
    )

    Call Cloud.provision_all(a list containing aws_vm, azure_vm, gcp_vm)
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
    Let diff be Cloud.plan(current_state, desired_state)

    Call display("Changes to apply:")
    For Each change in diff.changes:
        Call display("  " + change.action + ": " + change.resource)
    End For

    Note: Apply changes
    Call Cloud.apply_diff(diff)

    Note: Save new state
    Call Cloud.save_state("production", desired_state)
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
Let web_server be Cloud.resource("AWS::EC2::Instance", a dictionary containing:
    "InstanceType" as "t3.medium",
    "ImageId" as "ami-12345",
    "Tags" as a list containing tag("Name", "web-server")
End Dictionary)
```

---

## Kubernetes Infrastructure

```runa
Process called "provision_k8s_cluster":
    Let cluster be Cloud.kubernetes_cluster(
        "prod-cluster",
        "1.27",
        3  Note: node count
    )

    Let node_pool be Cloud.node_pool(
        cluster,
        "default-pool",
        "n1-standard-4",
        5
    )

    Call Cloud.provision(cluster)
    Call Cloud.provision(node_pool)
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
