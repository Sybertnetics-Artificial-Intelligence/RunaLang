# Runa API Specification

**Version:** 1.0
**Status:** Canonical
**Last Updated:** 2025-10-08

---

## Overview

**Runa replaces API specification formats with executable `.runa` files.**

**Replaces:**
- ❌ OpenAPI/Swagger (YAML/JSON)
- ❌ API Blueprint
- ❌ RAML
- ❌ Postman collections

---

## Basic API Specification

**File:** `api_spec.runa`

```runa
Note: API specification
Note: Replaces OpenAPI/Swagger

Import "runa/api" as API

Type called "Endpoint":
    path as String
    method as String
    description as String
    parameters as List[Parameter]
    request_body as Schema
    responses as Dictionary[Integer, Response]
End Type

Process called "define_api" returns API.Specification:
    Return API.spec("My API", "1.0.0",
        API.server("https://api.example.com"),

        API.endpoint("GET", "/users",
            API.description("Get all users"),
            API.query_param("page", "integer", optional(true)),
            API.query_param("limit", "integer", optional(true)),
            API.response(200, "Success", user_list_schema()),
            API.response(401, "Unauthorized", error_schema())
        ),

        API.endpoint("POST", "/users",
            API.description("Create a new user"),
            API.request_body(user_create_schema()),
            API.response(201, "Created", user_schema()),
            API.response(400, "Bad Request", error_schema())
        ),

        API.endpoint("GET", "/users/{id}",
            API.description("Get user by ID"),
            API.path_param("id", "integer"),
            API.response(200, "Success", user_schema()),
            API.response(404, "Not Found", error_schema())
        )
    )
End Process

Process called "user_schema" returns API.Schema:
    Return API.object_schema(
        API.field("id", "integer"),
        API.field("email", "string", format("email")),
        API.field("created_at", "string", format("date-time"))
    )
End Process

Process called "main":
    Let api_spec be define_api()
    Call API.generate_docs(api_spec, "api_docs.html")
    Call display("✓ API documentation generated")
End Process
```

---

## OpenAPI/Swagger Comparison

**Before (openapi.yaml):**
```yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
servers:
  - url: https://api.example.com
paths:
  /users:
    get:
      summary: Get all users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
        - name: limit
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
  /users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Success
        '404':
          description: Not Found

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        email:
          type: string
          format: email
```

**After (api_spec.runa):**
```runa
Let api be API.specification("My API", "1.0.0",
    endpoint("GET", "/users",
        query("page", INT, optional),
        query("limit", INT, optional),
        response(200, user_list_schema)
    ),

    endpoint("GET", "/users/{id}",
        path("id", INT, required),
        response(200, user_schema),
        response(404, error_schema)
    )
)

Let user_schema be object_schema(
    field("id", INT),
    field("email", STRING, format("email"))
)
```

---

## Authentication Specification

```runa
Process called "api_with_auth" returns API.Specification:
    Return API.spec("Secure API", "1.0.0",
        API.security_scheme("bearer", "JWT",
            API.bearer_format("JWT")
        ),

        API.endpoint("GET", "/protected",
            API.security("bearer"),
            API.response(200, "Success", data_schema()),
            API.response(401, "Unauthorized")
        )
    )
End Process
```

---

## Request/Response Examples

```runa
Process called "endpoint_with_examples" returns Endpoint:
    Return API.endpoint("POST", "/users",
        API.request_body(user_create_schema(),
            API.example("basic_user", a dictionary containing:
                "email" as "user@example.com",
                "password" as "securepassword123"
            End Dictionary)
        ),

        API.response(201, "Created", user_schema(),
            API.example("created_user", a dictionary containing:
                "id" as 1,
                "email" as "user@example.com",
                "created_at" as "2025-10-08T12:00:00Z"
            End Dictionary)
        )
    )
End Process
```

---

## API Client Generation

```runa
Process called "generate_client":
    Let api_spec be define_api()

    Note: Generate client library
    Call API.generate_client(api_spec, "typescript", "client/")
    Call API.generate_client(api_spec, "python", "client/")
    Call API.generate_client(api_spec, "go", "client/")

    Call display("✓ API clients generated")
End Process
```

---

## Validation

```runa
Process called "validate_request" that takes endpoint as String, data as Dictionary[String, Any] returns Boolean:
    Let api_spec be define_api()
    Let validation_result be API.validate(api_spec, endpoint, data)

    If validation_result.is_valid:
        Return true
    Otherwise:
        For Each error in validation_result.errors:
            Call display("Validation error: " + error.message)
        End For
        Return false
    End If
End Process
```

---

## Summary

**Runa replaces API specs with:**
- ✅ Type-safe endpoint definitions
- ✅ Executable specifications
- ✅ Automatic client generation
- ✅ Built-in validation

**Stop using:** OpenAPI YAML/JSON
**Start using:** `api_spec.runa`

---

**End of Document**
