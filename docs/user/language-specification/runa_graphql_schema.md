# Runa GraphQL Schema Specification

**Version:** 1.0
**Status:** Canonical
**Last Updated:** 2025-10-08

---

## Overview

**Runa replaces GraphQL SDL with executable `.runa` schema files.**

**Replaces:**
- ❌ GraphQL SDL (.graphql files)
- ❌ Apollo Schema
- ❌ GraphQL Code Generator configs

---

## Basic GraphQL Schema

**File:** `graphql_schema.runa`

```runa
Note: GraphQL schema definition
Note: Replaces .graphql SDL files

Import "runa/graphql" as GQL

Process called "define_schema" returns GQL.Schema:
    Return GQL.schema(
        GQL.type("User",
            GQL.field("id", GQL.ID, non_null(true)),
            GQL.field("email", GQL.String, non_null(true)),
            GQL.field("posts", GQL.list_of("Post")),
            GQL.field("created_at", GQL.String)
        ),

        GQL.type("Post",
            GQL.field("id", GQL.ID, non_null(true)),
            GQL.field("title", GQL.String, non_null(true)),
            GQL.field("content", GQL.String),
            GQL.field("author", "User", non_null(true)),
            GQL.field("published_at", GQL.String)
        ),

        GQL.query(
            GQL.field("users", GQL.list_of("User")),
            GQL.field("user", "User",
                GQL.arg("id", GQL.ID, non_null(true))
            ),
            GQL.field("posts", GQL.list_of("Post"),
                GQL.arg("limit", GQL.Int),
                GQL.arg("offset", GQL.Int)
            )
        ),

        GQL.mutation(
            GQL.field("createUser", "User",
                GQL.arg("email", GQL.String, non_null(true)),
                GQL.arg("password", GQL.String, non_null(true))
            ),
            GQL.field("createPost", "Post",
                GQL.arg("title", GQL.String, non_null(true)),
                GQL.arg("content", GQL.String),
                GQL.arg("author_id", GQL.ID, non_null(true))
            )
        )
    )
End Process

Let SCHEMA be define_schema()
```

---

## GraphQL SDL Comparison

**Before (schema.graphql):**
```graphql
type User {
  id: ID!
  email: String!
  posts: [Post!]!
  created_at: String
}

type Post {
  id: ID!
  title: String!
  content: String
  author: User!
  published_at: String
}

type Query {
  users: [User!]!
  user(id: ID!): User
  posts(limit: Int, offset: Int): [Post!]!
}

type Mutation {
  createUser(email: String!, password: String!): User!
  createPost(title: String!, content: String, author_id: ID!): Post!
}
```

**After (graphql_schema.runa):**
```runa
Note: Equivalent Runa schema (shown above)
```

---

## Resolvers

```runa
Process called "define_resolvers" returns GQL.Resolvers:
    Return GQL.resolvers(
        GQL.query_resolver("users", resolve_all_users),
        GQL.query_resolver("user", resolve_user_by_id),
        GQL.mutation_resolver("createUser", create_user),
        GQL.field_resolver("User", "posts", resolve_user_posts)
    )
End Process

Process called "resolve_all_users" returns List[User]:
    Let users be DB.query("User").all()
    Return users
End Process

Process called "resolve_user_by_id" that takes id as Integer returns User:
    Let user be DB.query("User").where("id", id).first()
    Return user
End Process

Process called "resolve_user_posts" that takes user as User returns List[Post]:
    Let posts be DB.query("Post").where("author_id", user.id).all()
    Return posts
End Process

Process called "create_user" that takes email as String, password as String returns User:
    Let user be DB.insert("User", a dictionary containing:
        "email" as email,
        "password_hash" as hash_password(password)
    End Dictionary)
    Return user
End Process
```

---

## Subscriptions

```runa
Process called "schema_with_subscriptions" returns GQL.Schema:
    Return GQL.schema(
        Note: ... types and queries ...

        GQL.subscription(
            GQL.field("post_created", "Post"),
            GQL.field("user_updated", "User",
                GQL.arg("id", GQL.ID, non_null(true))
            )
        )
    )
End Process

Process called "define_subscription_resolvers" returns GQL.Resolvers:
    Return GQL.resolvers(
        GQL.subscription_resolver("post_created", subscribe_post_created),
        GQL.subscription_resolver("user_updated", subscribe_user_updated)
    )
End Process

Process called "subscribe_post_created" returns GQL.Subscription:
    Return GQL.pubsub_subscribe("POST_CREATED")
End Process
```

---

## Input Types

```runa
Process called "schema_with_inputs" returns GQL.Schema:
    Return GQL.schema(
        GQL.input_type("CreateUserInput",
            GQL.field("email", GQL.String, non_null(true)),
            GQL.field("password", GQL.String, non_null(true)),
            GQL.field("name", GQL.String)
        ),

        GQL.mutation(
            GQL.field("createUser", "User",
                GQL.arg("input", "CreateUserInput", non_null(true))
            )
        )
    )
End Process
```

---

## Directives

```runa
Process called "schema_with_directives" returns GQL.Schema:
    Return GQL.schema(
        GQL.directive("auth",
            GQL.arg("requires", GQL.String)
        ),

        GQL.type("User",
            GQL.field("id", GQL.ID),
            GQL.field("email", GQL.String,
                GQL.apply_directive("auth", "USER")
            ),
            GQL.field("admin_notes", GQL.String,
                GQL.apply_directive("auth", "ADMIN")
            )
        )
    )
End Process
```

---

## Summary

**Runa replaces GraphQL SDL with:**
- ✅ Type-safe schema definitions
- ✅ Integrated resolvers
- ✅ Executable specifications
- ✅ Built-in validation

**Stop using:** .graphql SDL files
**Start using:** `graphql_schema.runa`

---

**End of Document**
