# Runa Kubernetes Deployment Specification

**Version:** 1.0
**Status:** Canonical
**Last Updated:** 2025-10-08

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
    image as String
    replicas as Integer
    ports as List[Integer]
    env as Dictionary[String, String]
End Type

Type called "ServiceSpec":
    name as String
    type as String
    ports as List[Integer]
    selector as Dictionary[String, String]
End Type

Process called "define_deployment" returns PodSpec:
    Return a value of type PodSpec with
        image as "myapp:1.0",
        replicas as 3,
        ports as a list containing 8080,
        env as a dictionary containing:
            "DATABASE_URL" as "postgresql://db:5432/myapp",
            "REDIS_URL" as "redis://redis:6379"
        End Dictionary
End Process

Process called "define_service" returns ServiceSpec:
    Return a value of type ServiceSpec with
        name as "myapp-service",
        type as "LoadBalancer",
        ports as a list containing 80,
        selector as a dictionary containing:
            "app" as "myapp"
        End Dictionary
End Process

Process called "main":
    Let deployment be define_deployment()
    Let service be define_service()

    Call K8s.apply_deployment("myapp", deployment)
    Call K8s.apply_service(service)

    Call display("✓ Kubernetes resources applied")
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
Let deployment be K8s.deployment("myapp", a dictionary containing:
    "image" as "myapp:1.0",
    "replicas" as 3,
    "port" as 8080,
    "env" as a dictionary containing:
        "DATABASE_URL" as "postgresql://db:5432/myapp"
    End Dictionary
End Dictionary)

Call K8s.apply(deployment)
```

---

## ConfigMap and Secrets

```runa
Process called "create_config":
    Let config_map be K8s.configmap("app-config", a dictionary containing:
        "API_URL" as "https://api.example.com",
        "MAX_CONNECTIONS" as "100",
        "LOG_LEVEL" as "INFO"
    End Dictionary)

    Let secret be K8s.secret("app-secrets", a dictionary containing:
        "DATABASE_PASSWORD" as "supersecret",
        "API_KEY" as "abc123xyz789"
    End Dictionary)

    Call K8s.apply(config_map)
    Call K8s.apply(secret)
End Process
```

---

## Helm Chart Replacement

**File:** `helm_app.runa`

```runa
Note: Replaces Helm chart with values

Type called "HelmValues":
    release_name as String
    namespace as String
    replicas as Integer
    image_tag as String
    service_type as String
End Type

Process called "install_helm_chart" that takes values as HelmValues:
    Let deployment be K8s.deployment(values.release_name, a dictionary containing:
        "image" as "myapp:" + values.image_tag,
        "replicas" as values.replicas
    End Dictionary)

    Let service be K8s.service(values.release_name + "-service", a dictionary containing:
        "type" as values.service_type
    End Dictionary)

    Call K8s.create_namespace(values.namespace)
    Call K8s.apply_in_namespace(values.namespace, deployment)
    Call K8s.apply_in_namespace(values.namespace, service)
End Process

Process called "main":
    Let prod_values be a value of type HelmValues with
        release_name as "myapp-prod",
        namespace as "production",
        replicas as 5,
        image_tag as "1.0.0",
        service_type as "LoadBalancer"

    Call install_helm_chart(prod_values)
End Process
```

---

## StatefulSet for Databases

```runa
Process called "deploy_database":
    Let statefulset be K8s.statefulset("postgres", a dictionary containing:
        "image" as "postgres:14",
        "replicas" as 3,
        "volume_claim_template" as a dictionary containing:
            "storage" as "10Gi",
            "storage_class" as "fast-ssd"
        End Dictionary,
        "env" as a dictionary containing:
            "POSTGRES_PASSWORD" as "secret"
        End Dictionary
    End Dictionary)

    Call K8s.apply(statefulset)
End Process
```

---

## Ingress Configuration

```runa
Process called "configure_ingress":
    Let ingress be K8s.ingress("myapp-ingress", a dictionary containing:
        "host" as "myapp.example.com",
        "tls_enabled" as true,
        "cert_secret" as "myapp-tls-cert",
        "rules" as a list containing:
            route("/", "myapp-service", 80),
            route("/api", "api-service", 8080)
        End
    End Dictionary)

    Call K8s.apply(ingress)
End Process

Process called "route" that takes path as String, service as String, port as Integer returns Dictionary[String, Any]:
    Return a dictionary containing:
        "path" as path,
        "service" as service,
        "port" as port
    End Dictionary
End Process
```

---

## Multi-Environment Deployment

```runa
Process called "deploy_to_environment" that takes env as String:
    Let config be match env:
        When "development":
            env_config(1, "dev", "NodePort")
        When "staging":
            env_config(3, "staging", "LoadBalancer")
        When "production":
            env_config(5, "prod", "LoadBalancer")
        Otherwise:
            panic("Unknown environment: " + env)
    End Match

    Call deploy_with_config(config)
End Process

Process called "env_config" that takes replicas as Integer, namespace as String, service_type as String returns Dictionary[String, Any]:
    Return a dictionary containing:
        "replicas" as replicas,
        "namespace" as namespace,
        "service_type" as service_type
    End Dictionary
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
