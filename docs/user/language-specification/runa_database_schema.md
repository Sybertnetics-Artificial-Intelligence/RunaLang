# Runa Database Schema Specification

**Version:** 1.0
**Status:** Canonical
**Last Updated:** 2025-10-08

---

## Overview

**Runa replaces SQL DDL with executable `.runa` schema files.**

**Replaces:**
- ❌ SQL DDL (CREATE TABLE, ALTER TABLE, etc.)
- ❌ ORM models (Django, SQLAlchemy, ActiveRecord)
- ❌ Prisma schema
- ❌ Database migration files

---

## Basic Schema Definition

**File:** `schema.runa`

```runa
Note: Database schema definition
Note: Replaces SQL DDL, ORM models, Prisma schema

Import "runa/database" as DB

Type called "TableColumn":
    name as String
    type as String
    nullable as Boolean
    default_value as String
    primary_key as Boolean
    unique as Boolean
End Type

Type called "TableSchema":
    name as String
    columns as List[TableColumn]
    indexes as List[Index]
    foreign_keys as List[ForeignKey]
End Type

Process called "define_users_table" returns TableSchema:
    Return a value of type TableSchema with
        name as "users",
        columns as a list containing:
            col("id", "INTEGER", false, "", true, true),
            col("email", "VARCHAR(255)", false, "", false, true),
            col("password_hash", "VARCHAR(255)", false, "", false, false),
            col("created_at", "TIMESTAMP", false, "CURRENT_TIMESTAMP", false, false),
            col("updated_at", "TIMESTAMP", false, "CURRENT_TIMESTAMP", false, false)
        End,
        indexes as a list containing:
            index("idx_email", "email")
        End,
        foreign_keys as an empty list
End Process

Process called "col" that takes name as String, type as String, nullable as Boolean, default_val as String, pk as Boolean, unique as Boolean returns TableColumn:
    Return a value of type TableColumn with
        name as name,
        type as type,
        nullable as nullable,
        default_value as default_val,
        primary_key as pk,
        unique as unique
End Process

Process called "index" that takes name as String, column as String returns Index:
    Return DB.create_index(name, column)
End Process

Process called "main":
    Let users_table be define_users_table()
    Call DB.create_table(users_table)
    Call display("✓ Tables created")
End Process
```

---

## SQL DDL Comparison

**Before (schema.sql):**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_email ON users(email);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    published_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**After (schema.runa):**
```runa
Process called "define_schema":
    Let users be DB.table("users",
        DB.column("id", DB.INTEGER, primary_key(true)),
        DB.column("email", DB.VARCHAR(255), unique(true)),
        DB.column("password_hash", DB.VARCHAR(255)),
        DB.column("created_at", DB.TIMESTAMP, default("CURRENT_TIMESTAMP")),
        DB.index("email")
    )

    Let posts be DB.table("posts",
        DB.column("id", DB.INTEGER, primary_key(true)),
        DB.column("user_id", DB.INTEGER, not_null(true)),
        DB.column("title", DB.VARCHAR(255)),
        DB.column("content", DB.TEXT),
        DB.column("published_at", DB.TIMESTAMP, nullable(true)),
        DB.foreign_key("user_id", "users", "id", on_delete("CASCADE"))
    )

    Call DB.create_tables(a list containing users, posts)
End Process
```

---

## Migrations

**File:** `migrations/001_create_users.runa`

```runa
Note: Database migration
Note: Replaces SQL migration files

Import "runa/database/migration" as Migration

Process called "up":
    Note: Apply migration
    Call Migration.create_table("users",
        Migration.column("id", "INTEGER", primary_key(true)),
        Migration.column("email", "VARCHAR(255)", unique(true)),
        Migration.column("created_at", "TIMESTAMP", default("NOW()"))
    )

    Call display("✓ Migration applied: create users table")
End Process

Process called "down":
    Note: Rollback migration
    Call Migration.drop_table("users")

    Call display("✓ Migration rolled back: drop users table")
End Process
```

**File:** `migrations/002_add_user_profile.runa`

```runa
Process called "up":
    Note: Add column to existing table
    Call Migration.add_column("users", "bio", "TEXT", nullable(true))
    Call Migration.add_column("users", "avatar_url", "VARCHAR(255)", nullable(true))

    Call display("✓ Migration applied: add profile columns")
End Process

Process called "down":
    Call Migration.drop_column("users", "bio")
    Call Migration.drop_column("users", "avatar_url")

    Call display("✓ Migration rolled back: remove profile columns")
End Process
```

---

## ORM Model Comparison

**Before (Django ORM):**
```python
from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(null=True)
```

**After (Runa ORM):**
```runa
Type called "User":
    id as Integer
    email as String
    password_hash as String
    created_at as Timestamp
End Type

Type called "Post":
    id as Integer
    user_id as Integer
    title as String
    content as String
    published_at as Timestamp
End Type

Process called "define_user_model" returns DB.Model:
    Return DB.model("User", "users",
        DB.field("id", DB.INTEGER, primary_key(true)),
        DB.field("email", DB.VARCHAR(255), unique(true)),
        DB.field("password_hash", DB.VARCHAR(255)),
        DB.field("created_at", DB.TIMESTAMP, auto_now_add(true))
    )
End Process

Process called "define_post_model" returns DB.Model:
    Return DB.model("Post", "posts",
        DB.field("id", DB.INTEGER, primary_key(true)),
        DB.field("user_id", DB.INTEGER, foreign_key("User", "id")),
        DB.field("title", DB.VARCHAR(255)),
        DB.field("content", DB.TEXT),
        DB.field("published_at", DB.TIMESTAMP, nullable(true))
    )
End Process
```

---

## Query Interface

```runa
Process called "query_users":
    Note: Find all users with .com email addresses
    Let users be DB.query("User")
        .where("email", "LIKE", "%.com")
        .order_by("created_at", "DESC")
        .limit(10)
        .execute()

    For Each user in users:
        Call display(user.email)
    End For
End Process

Process called "create_user" that takes email as String, password as String:
    Let user be DB.insert("User", a dictionary containing:
        "email" as email,
        "password_hash" as hash_password(password),
        "created_at" as DB.now()
    End Dictionary)

    Return user
End Process
```

---

## Prisma Comparison

**Before (schema.prisma):**
```prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  posts     Post[]
  createdAt DateTime @default(now())
}

model Post {
  id          Int       @id @default(autoincrement())
  title       String
  content     String?
  published   Boolean   @default(false)
  author      User      @relation(fields: [authorId], references: [id])
  authorId    Int
  publishedAt DateTime?
}
```

**After (schema.runa):**
```runa
Let User_model be DB.model("User", "users",
    DB.id_field(),
    DB.field("email", DB.STRING, unique(true)),
    DB.has_many("posts", "Post"),
    DB.timestamp("created_at", auto_now_add(true))
)

Let Post_model be DB.model("Post", "posts",
    DB.id_field(),
    DB.field("title", DB.STRING),
    DB.field("content", DB.STRING, nullable(true)),
    DB.field("published", DB.BOOLEAN, default(false)),
    DB.belongs_to("author", "User", foreign_key("author_id")),
    DB.timestamp("published_at", nullable(true))
)
```

---

## Summary

**Runa replaces SQL/ORM with:**
- ✅ Type-safe schema definitions
- ✅ Executable migrations
- ✅ Unified query interface
- ✅ Replaces SQL, Django ORM, Prisma, etc.

**Stop using:** SQL DDL, ORM models
**Start using:** `schema.runa`, `migrations/*.runa`

---

**End of Document**
