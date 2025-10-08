# Runa Web Markup Specification (Aether Framework)

**Version:** 1.0
**Status:** Canonical - Aether Framework
**Last Updated:** 2025-10-08

---

## Overview

**Runa replaces HTML with executable `.runa` markup files.**

**Replaces:**
- ❌ HTML
- ❌ JSX/TSX (React)
- ❌ Vue templates
- ❌ Svelte components

---

## Basic Web Page

**File:** `index.runa`

```runa
Note: Web page markup in Runa (Aether Framework)
Note: Replaces HTML

Import "runa/aether" as Web

Process called "render_page" returns Web.Element:
    Return Web.html(
        Web.head(
            Web.title("My Application"),
            Web.meta("charset", "UTF-8"),
            Web.link("stylesheet", "styles.runa")
        ),
        Web.body(
            Web.header(
                Web.h1("Welcome to My App")
            ),
            Web.main(
                Web.section(
                    Web.p("This is a paragraph"),
                    Web.button("Click Me", on_click)
                )
            ),
            Web.footer(
                Web.p("© 2025 My Company")
            )
        )
    )
End Process

Process called "on_click":
    Call Web.alert("Button clicked!")
End Process

Process called "main":
    Let page be render_page()
    Call Web.render(page, "root")
End Process
```

---

## HTML Comparison

**Before (index.html):**
```html
<!DOCTYPE html>
<html>
<head>
    <title>My Application</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>Welcome to My App</h1>
    </header>
    <main>
        <section>
            <p>This is a paragraph</p>
            <button onclick="handleClick()">Click Me</button>
        </section>
    </main>
    <footer>
        <p>© 2025 My Company</p>
    </footer>
</body>
</html>
```

**After (index.runa):**
```runa
Process called "render_page" returns Web.Element:
    Return Web.page(
        Web.header(Web.h1("Welcome to My App")),
        Web.main(
            Web.section(
                Web.p("This is a paragraph"),
                Web.button("Click Me", on_click)
            )
        ),
        Web.footer(Web.p("© 2025 My Company"))
    )
End Process
```

---

## Dynamic Content

```runa
Process called "render_user_list" that takes users as List[User] returns Web.Element:
    Let user_elements be an empty list

    For Each user in users:
        Let user_card be Web.div(
            Web.h3(user.name),
            Web.p("Email: " + user.email),
            Web.button("View Profile", view_profile(user.id))
        )
        Add user_card to user_elements
    End For

    Return Web.div(
        Web.h2("Users"),
        Web.div(user_elements)
    )
End Process
```

---

## Forms

```runa
Process called "render_login_form" returns Web.Element:
    Return Web.form(
        Web.input("text", "username", "Username"),
        Web.input("password", "password", "Password"),
        Web.button("Login", handle_login),
        on_submit(handle_login)
    )
End Process

Process called "handle_login":
    Let username be Web.get_value("username")
    Let password be Web.get_value("password")

    Call authenticate(username, password)
End Process
```

---

## Component System

```runa
Process called "Card" that takes title as String, content as String returns Web.Element:
    Return Web.div(
        Web.class("card"),
        Web.h3(title),
        Web.p(content)
    )
End Process

Process called "render_dashboard" returns Web.Element:
    Return Web.div(
        Card("Statistics", "100 users online"),
        Card("Activity", "50 new sign-ups today"),
        Card("Revenue", "$10,000 this month")
    )
End Process
```

---

## JSX Comparison

**Before (React JSX):**
```jsx
function UserProfile({ user }) {
  return (
    <div className="profile">
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      <button onClick={() => editUser(user.id)}>Edit</button>
    </div>
  );
}
```

**After (Runa Aether):**
```runa
Process called "UserProfile" that takes user as User returns Web.Element:
    Return Web.div(
        Web.class("profile"),
        Web.h2(user.name),
        Web.p(user.email),
        Web.button("Edit", edit_user(user.id))
    )
End Process
```

---

## State Management

```runa
Type called "AppState":
    count as Integer
    user as User
    loading as Boolean
End Type

Process called "render_counter" that takes state as AppState returns Web.Element:
    Return Web.div(
        Web.h2("Count: " + string_from(state.count)),
        Web.button("Increment", increment),
        Web.button("Decrement", decrement)
    )
End Process

Process called "increment":
    Call Web.update_state(a dictionary containing:
        "count" as Web.get_state("count") + 1
    End Dictionary)
End Process
```

---

## Summary

**Runa replaces HTML/JSX with:**
- ✅ Type-safe markup
- ✅ Component functions
- ✅ Integrated state management
- ✅ No template strings

**Stop using:** HTML, JSX, Vue templates
**Start using:** Aether Framework (`.runa`)

---

**End of Document**
