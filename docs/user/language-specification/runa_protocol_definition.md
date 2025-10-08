# Runa Protocol Definition Specification

**Version:** 1.0
**Status:** Canonical
**Last Updated:** 2025-10-08

---

## Overview

**Runa replaces binary protocol definitions with executable `.runa` files.**

**Replaces:**
- ❌ Protocol Buffers (.proto)
- ❌ Apache Thrift (.thrift)
- ❌ Apache Avro schemas
- ❌ FlatBuffers schemas

---

## Basic Protocol Definition

**File:** `protocol.runa`

```runa
Note: Protocol definition
Note: Replaces Protocol Buffers .proto files

Import "runa/protocol" as Proto

Type called "Message":
    id as Integer
    name as String
    fields as List[Field]
End Type

Process called "define_protocol" returns Proto.Protocol:
    Return Proto.protocol("UserService", "1.0",
        Proto.message("User",
            Proto.field(1, "id", Proto.INT64, required(true)),
            Proto.field(2, "email", Proto.STRING, required(true)),
            Proto.field(3, "name", Proto.STRING, optional(true)),
            Proto.field(4, "created_at", Proto.TIMESTAMP, required(true))
        ),

        Proto.message("CreateUserRequest",
            Proto.field(1, "email", Proto.STRING, required(true)),
            Proto.field(2, "password", Proto.STRING, required(true))
        ),

        Proto.message("CreateUserResponse",
            Proto.field(1, "user", "User", required(true)),
            Proto.field(2, "success", Proto.BOOL, required(true))
        ),

        Proto.service("UserService",
            Proto.rpc("CreateUser", "CreateUserRequest", "CreateUserResponse"),
            Proto.rpc("GetUser", "GetUserRequest", "User"),
            Proto.rpc("ListUsers", "ListUsersRequest", "ListUsersResponse")
        )
    )
End Process

Let PROTOCOL be define_protocol()
```

---

## Protobuf Comparison

**Before (.proto):**
```protobuf
syntax = "proto3";

package userservice;

message User {
  int64 id = 1;
  string email = 2;
  string name = 3;
  int64 created_at = 4;
}

message CreateUserRequest {
  string email = 1;
  string password = 2;
}

message CreateUserResponse {
  User user = 1;
  bool success = 2;
}

service UserService {
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
  rpc GetUser(GetUserRequest) returns (User);
  rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
}
```

**After (protocol.runa):**
```runa
Note: Equivalent Runa protocol (shown above)
```

---

## Enumerations

```runa
Process called "protocol_with_enums" returns Proto.Protocol:
    Return Proto.protocol("MessageService", "1.0",
        Proto.enum("MessageStatus",
            Proto.enum_value("PENDING", 0),
            Proto.enum_value("SENT", 1),
            Proto.enum_value("DELIVERED", 2),
            Proto.enum_value("READ", 3)
        ),

        Proto.message("Message",
            Proto.field(1, "id", Proto.INT64),
            Proto.field(2, "content", Proto.STRING),
            Proto.field(3, "status", "MessageStatus")
        )
    )
End Process
```

---

## Nested Messages

```runa
Process called "protocol_with_nested" returns Proto.Protocol:
    Return Proto.protocol("AddressBook", "1.0",
        Proto.message("Person",
            Proto.field(1, "name", Proto.STRING),
            Proto.field(2, "id", Proto.INT32),
            Proto.field(3, "email", Proto.STRING),

            Proto.nested_message("PhoneNumber",
                Proto.field(1, "number", Proto.STRING),
                Proto.field(2, "type", "PhoneType")
            ),

            Proto.field(4, "phones", Proto.REPEATED, "PhoneNumber")
        ),

        Proto.enum("PhoneType",
            Proto.enum_value("MOBILE", 0),
            Proto.enum_value("HOME", 1),
            Proto.enum_value("WORK", 2)
        )
    )
End Process
```

---

## Binary Serialization

```runa
Process called "serialize_message" that takes user as User returns Bytes:
    Let proto be define_protocol()
    Let serialized be Proto.serialize(proto, "User", user)
    Return serialized
End Process

Process called "deserialize_message" that takes data as Bytes returns User:
    Let proto be define_protocol()
    Let user be Proto.deserialize(proto, "User", data)
    Return user
End Process
```

---

## Code Generation

```runa
Process called "generate_protocol_code":
    Let proto be define_protocol()

    Note: Generate code for multiple languages
    Call Proto.generate_code(proto, "rust", "generated/rust/")
    Call Proto.generate_code(proto, "go", "generated/go/")
    Call Proto.generate_code(proto, "python", "generated/python/")

    Call display("✓ Protocol code generated")
End Process
```

---

## Thrift Comparison

**Before (.thrift):**
```thrift
struct User {
  1: i64 id,
  2: string email,
  3: optional string name
}

service UserService {
  User getUser(1: i64 id),
  list<User> listUsers(),
  User createUser(1: string email, 2: string password)
}
```

**After (protocol.runa):**
```runa
Let protocol be Proto.protocol("UserService", "1.0",
    Proto.struct("User",
        Proto.field(1, "id", Proto.I64),
        Proto.field(2, "email", Proto.STRING),
        Proto.field(3, "name", Proto.STRING, optional(true))
    ),

    Proto.service("UserService",
        Proto.method("getUser",
            Proto.param(1, "id", Proto.I64),
            Proto.returns("User")
        ),
        Proto.method("listUsers",
            Proto.returns(Proto.list_of("User"))
        ),
        Proto.method("createUser",
            Proto.param(1, "email", Proto.STRING),
            Proto.param(2, "password", Proto.STRING),
            Proto.returns("User")
        )
    )
)
```

---

## Summary

**Runa replaces protocol definitions with:**
- ✅ Type-safe message definitions
- ✅ Binary serialization
- ✅ Multi-language code generation
- ✅ RPC service definitions

**Stop using:** .proto, .thrift files
**Start using:** `protocol.runa`

---

**End of Document**
