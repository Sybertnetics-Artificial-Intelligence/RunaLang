# Template Engine Module

The Template Engine module provides advanced templating capabilities for code and text generation, supporting inheritance, control flow, partials, macros, and sophisticated variable interpolation. This module is essential for building powerful code generation systems and dynamic content creation.

## Table of Contents

- [Overview](#overview)
- [Core Types](#core-types)
- [API Reference](#api-reference)
- [Template Syntax](#template-syntax)
- [Usage Examples](#usage-examples)
- [Advanced Patterns](#advanced-patterns)
- [Performance Considerations](#performance-considerations)
- [Best Practices](#best-practices)

## Overview

The Template Engine module provides comprehensive templating capabilities:

- **Variable Interpolation**: Dynamic variable substitution with type safety
- **Control Flow**: Conditional rendering and loops within templates
- **Template Inheritance**: Parent-child template relationships
- **Partials and Includes**: Reusable template components
- **Macro System**: Template-level macro definitions and expansions
- **Error Handling**: Comprehensive error reporting and recovery

### Key Features

- **Rich Template Syntax**: Intuitive template syntax optimized for readability
- **Type-Safe Rendering**: Comprehensive type checking during template rendering
- **Performance Optimized**: Efficient template compilation and rendering
- **Extensible**: Support for custom renderers and template types
- **AI Integration**: Hooks for AI-driven template generation
- **Production Ready**: Robust error handling and validation

## Core Types

### TemplateEngine

The main engine for template operations.

```runa
Type called "TemplateEngine":
    config as TemplateEngineConfig          Note: Engine configuration
    templates as Dictionary[String, Template]  Note: Registered templates
    renderers as Dictionary[String, TemplateRenderer]  Note: Custom renderers
    stats as TemplateEngineStats            Note: Rendering statistics
    metadata as Dictionary[String, Any]     Note: Additional metadata
```

### TemplateEngineConfig

Configuration for the template engine.

```runa
Type called "TemplateEngineConfig":
    enable_inheritance as Boolean           Note: Enable template inheritance
    enable_macros as Boolean               Note: Enable macro processing
    enable_partials as Boolean             Note: Enable partial includes
    enable_control_flow as Boolean         Note: Enable if/for constructs
    ai_mode as Boolean                     Note: Enable AI-driven features
    metadata as Dictionary[String, Any]    Note: Additional configuration
```

### Template

Represents a compiled template ready for rendering.

```runa
Type called "Template":
    template_id as String                  Note: Unique template identifier
    template_type as String                Note: Type of template
    template_code as String                Note: Template source code
    variables as List[TemplateVariable]    Note: Template variables
    partials as List[String]               Note: Referenced partials
    macros as List[String]                 Note: Defined macros
    parent as Optional[String]             Note: Parent template reference
    metadata as Dictionary[String, Any]    Note: Template metadata
```

### TemplateVariable

Definition of a template variable.

```runa
Type called "TemplateVariable":
    name as String                         Note: Variable name
    variable_type as String                Note: Expected type
    default_value as Any                   Note: Default value if not provided
    metadata as Dictionary[String, Any]    Note: Variable metadata
```

## API Reference

### Core Template Functions

#### register_template

Registers a template in the engine.

```runa
Process called "register_template" that takes 
    engine as TemplateEngine 
    and template as Template 
    returns Boolean
```

**Parameters:**
- `engine`: Template engine instance
- `template`: Template to register

**Returns:** True if successfully registered

**Example:**
```runa
Import "advanced/metaprogramming/template_engine" as Templates

Note: Create template engine
Let config be Templates.TemplateEngineConfig with 
    enable_inheritance as true
    and enable_macros as true
    and enable_partials as true
    and enable_control_flow as true
    and ai_mode as false
    and metadata as dictionary containing

Let engine be Templates.TemplateEngine with 
    config as config
    and templates as dictionary containing
    and renderers as dictionary containing
    and stats as Templates.TemplateEngineStats with 
        total_rendered as 0
        and total_errors as 0
        and metadata as dictionary containing
    and metadata as dictionary containing

Note: Create a simple template
Let hello_template be Templates.Template with 
    template_id as "greeting"
    and template_type as "default"
    and template_code as "Hello, {{name}}! Welcome to {{place}}."
    and variables as list containing 
        Templates.TemplateVariable with name as "name" and variable_type as "string" and default_value as "World" and metadata as dictionary containing,
        Templates.TemplateVariable with name as "place" and variable_type as "string" and default_value as "Runa" and metadata as dictionary containing
    and partials as list containing
    and macros as list containing
    and parent as None
    and metadata as dictionary containing

Let success be Templates.register_template with engine as engine and template as hello_template
Display "Template registered: " plus success
```

#### render_template

Renders a template with the provided context.

```runa
Process called "render_template" that takes 
    engine as TemplateEngine 
    and template_id as String 
    and context as Dictionary[String, Any] 
    returns String
```

**Parameters:**
- `engine`: Template engine instance
- `template_id`: ID of template to render
- `context`: Variables to substitute in template

**Returns:** Rendered template string

**Throws:** TemplateEngineError if template not found or rendering fails

**Example:**
```runa
Let context be dictionary containing 
    "name" as "Alice",
    "place" as "the metaverse"

Let rendered be Templates.render_template with 
    engine as engine 
    and template_id as "greeting" 
    and context as context

Display "Rendered: " plus rendered
Note: Output: "Hello, Alice! Welcome to the metaverse."
```

### Template Inheritance

#### render_with_inheritance

Renders a template considering inheritance hierarchy.

```runa
Process called "render_with_inheritance" that takes 
    engine as TemplateEngine 
    and template_id as String 
    and context as Dictionary[String, Any] 
    returns String
```

**Example:**
```runa
Note: Create base template
Let base_template be Templates.Template with 
    template_id as "base"
    and template_type as "default"
    and template_code as "
<!DOCTYPE html>
<html>
<head>
    <title>{{title}}</title>
</head>
<body>
    {{content}}
</body>
</html>
    "
    and variables as list containing 
        Templates.TemplateVariable with name as "title" and variable_type as "string" and default_value as "Page" and metadata as dictionary containing,
        Templates.TemplateVariable with name as "content" and variable_type as "string" and default_value as "" and metadata as dictionary containing
    and partials as list containing
    and macros as list containing
    and parent as None
    and metadata as dictionary containing

Note: Create child template
Let page_template be Templates.Template with 
    template_id as "page"
    and template_type as "default"
    and template_code as "<h1>{{heading}}</h1>\n<p>{{body}}</p>"
    and variables as list containing 
        Templates.TemplateVariable with name as "heading" and variable_type as "string" and default_value as "Welcome" and metadata as dictionary containing,
        Templates.TemplateVariable with name as "body" and variable_type as "string" and default_value as "Content goes here" and metadata as dictionary containing
    and partials as list containing
    and macros as list containing
    and parent as "base"
    and metadata as dictionary containing

Templates.register_template with engine as engine and template as base_template
Templates.register_template with engine as engine and template as page_template

Let page_context be dictionary containing 
    "title" as "My Page",
    "heading" as "Welcome to Runa",
    "body" as "This is a powerful programming language."

Let rendered_page be Templates.render_template with 
    engine as engine 
    and template_id as "page" 
    and context as page_context

Display "Rendered page:"
Display rendered_page
```

### Partials and Includes

#### render_partial

Renders a partial template for inclusion in other templates.

```runa
Process called "render_partial" that takes 
    engine as TemplateEngine 
    and partial_id as String 
    and context as Dictionary[String, Any] 
    returns String
```

**Example:**
```runa
Note: Create a header partial
Let header_partial be Templates.Template with 
    template_id as "header"
    and template_type as "partial"
    and template_code as "<header><h1>{{site_name}}</h1><nav>{{navigation}}</nav></header>"
    and variables as list containing 
        Templates.TemplateVariable with name as "site_name" and variable_type as "string" and default_value as "My Site" and metadata as dictionary containing,
        Templates.TemplateVariable with name as "navigation" and variable_type as "string" and default_value as "<a href='/'>Home</a>" and metadata as dictionary containing
    and partials as list containing
    and macros as list containing
    and parent as None
    and metadata as dictionary containing

Templates.register_template with engine as engine and template as header_partial

Note: Use the partial
Let header_context be dictionary containing 
    "site_name" as "Runa Documentation",
    "navigation" as "<a href='/'>Home</a> | <a href='/docs'>Docs</a> | <a href='/examples'>Examples</a>"

Let rendered_header be Templates.render_partial with 
    engine as engine 
    and partial_id as "header" 
    and context as header_context

Display "Rendered header:"
Display rendered_header
```

### Macro System

#### render_macro

Renders a template macro with arguments.

```runa
Process called "render_macro" that takes 
    engine as TemplateEngine 
    and macro_name as String 
    and args as Dictionary[String, Any] 
    returns String
```

**Example:**
```runa
Note: Register a macro for generating form fields
Process called "form_field_macro" that takes template as Template and context as Dictionary[String, Any] returns String:
    Let field_type be context.get with key as "type" and default as "text"
    Let field_name be context.get with key as "name" and default as "field"
    Let field_label be context.get with key as "label" and default as field_name
    Let field_required be context.get with key as "required" and default as false
    
    Let required_attr be if field_required then " required" else ""
    Return "<label for='" plus field_name plus "'>" plus field_label plus "</label>\n<input type='" plus field_type plus "' name='" plus field_name plus "' id='" plus field_name plus "'" plus required_attr plus ">"

Set engine.renderers["form_field"] to form_field_macro

Note: Use the macro
Let field_args be dictionary containing 
    "type" as "email",
    "name" as "user_email",
    "label" as "Email Address",
    "required" as true

Let rendered_field be Templates.render_macro with 
    engine as engine 
    and macro_name as "form_field" 
    and args as field_args

Display "Rendered form field:"
Display rendered_field
```

## Template Syntax

### Variable Interpolation

Variables are enclosed in double curly braces:

```
Hello, {{name}}!
Your age is {{age}} years.
```

### Control Flow

#### Conditional Rendering

```
{{#if user_logged_in}}
    Welcome back, {{username}}!
{{/if}}

{{#if is_admin}}
    <a href="/admin">Admin Panel</a>
{{else}}
    <span>User Dashboard</span>
{{/if}}
```

#### Loops

```
{{#for item in items}}
    <li>{{item.name}} - {{item.price}}</li>
{{/for}}

{{#for user in users}}
    <div class="user">
        <h3>{{user.name}}</h3>
        <p>{{user.email}}</p>
    </div>
{{/for}}
```

### Comments

```
{{! This is a template comment and won't appear in output }}
```

### Escaping

Variables are automatically escaped for safety. Use triple braces for raw output:

```
{{safe_variable}}    {{! Escaped output }}
{{{raw_html}}}       {{! Raw output }}
```

## Usage Examples

### Basic Template Rendering

```runa
Import "advanced/metaprogramming/template_engine" as Templates

Note: Set up template engine
Let config be Templates.TemplateEngineConfig with 
    enable_inheritance as true
    and enable_macros as true
    and enable_partials as true
    and enable_control_flow as true
    and ai_mode as false
    and metadata as dictionary containing

Let engine be Templates.TemplateEngine with 
    config as config
    and templates as dictionary containing
    and renderers as dictionary containing
    and stats as Templates.TemplateEngineStats with 
        total_rendered as 0
        and total_errors as 0
        and metadata as dictionary containing
    and metadata as dictionary containing

Note: Create a product listing template
Let product_template be Templates.Template with 
    template_id as "product_list"
    and template_type as "default"
    and template_code as "
<div class='products'>
    <h2>{{category}} Products</h2>
    {{#for product in products}}
        <div class='product'>
            <h3>{{product.name}}</h3>
            <p class='price'>${{product.price}}</p>
            {{#if product.on_sale}}
                <span class='sale-badge'>ON SALE!</span>
            {{/if}}
            <p class='description'>{{product.description}}</p>
        </div>
    {{/for}}
</div>
    "
    and variables as list containing 
        Templates.TemplateVariable with name as "category" and variable_type as "string" and default_value as "All" and metadata as dictionary containing,
        Templates.TemplateVariable with name as "products" and variable_type as "list" and default_value as list containing and metadata as dictionary containing
    and partials as list containing
    and macros as list containing
    and parent as None
    and metadata as dictionary containing

Templates.register_template with engine as engine and template as product_template

Note: Render with sample data
Let product_data be dictionary containing 
    "category" as "Electronics",
    "products" as list containing 
        dictionary containing 
            "name" as "Laptop",
            "price" as 999.99,
            "on_sale" as true,
            "description" as "High-performance laptop for developers",
        dictionary containing 
            "name" as "Mouse",
            "price" as 29.99,
            "on_sale" as false,
            "description" as "Ergonomic wireless mouse",
        dictionary containing 
            "name" as "Keyboard",
            "price" as 79.99,
            "on_sale" as true,
            "description" as "Mechanical keyboard with RGB lighting"

Let rendered_products be Templates.render_template with 
    engine as engine 
    and template_id as "product_list" 
    and context as product_data

Display "Rendered product list:"
Display rendered_products
```

### Email Template System

```runa
Note: Create email template system
Process called "create_email_template_system" that takes engine as Templates.TemplateEngine returns EmailTemplateSystem:
    Note: Base email template
    Let base_email_template be Templates.Template with 
        template_id as "email_base"
        and template_type as "default"
        and template_code as "
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <title>{{subject}}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f0f0f0; padding: 20px; }
        .content { padding: 20px; }
        .footer { background: #f0f0f0; padding: 10px; font-size: 12px; }
    </style>
</head>
<body>
    <div class='header'>
        <h1>{{company_name}}</h1>
    </div>
    <div class='content'>
        {{content}}
    </div>
    <div class='footer'>
        <p>© 2024 {{company_name}}. All rights reserved.</p>
        <p>{{unsubscribe_link}}</p>
    </div>
</body>
</html>
        "
        and variables as list containing 
            Templates.TemplateVariable with name as "subject" and variable_type as "string" and default_value as "Email" and metadata as dictionary containing,
            Templates.TemplateVariable with name as "company_name" and variable_type as "string" and default_value as "Company" and metadata as dictionary containing,
            Templates.TemplateVariable with name as "content" and variable_type as "string" and default_value as "" and metadata as dictionary containing,
            Templates.TemplateVariable with name as "unsubscribe_link" and variable_type as "string" and default_value as "<a href='#'>Unsubscribe</a>" and metadata as dictionary containing
        and partials as list containing
        and macros as list containing
        and parent as None
        and metadata as dictionary containing

    Note: Welcome email template
    Let welcome_email_template be Templates.Template with 
        template_id as "welcome_email"
        and template_type as "default"
        and template_code as "
<h2>Welcome, {{user_name}}!</h2>
<p>Thank you for joining {{company_name}}. We're excited to have you on board!</p>
<p>Here's what you can do next:</p>
<ul>
    <li><a href='{{profile_url}}'>Complete your profile</a></li>
    <li><a href='{{docs_url}}'>Read our documentation</a></li>
    <li><a href='{{support_url}}'>Contact support if you need help</a></li>
</ul>
<p>Best regards,<br>The {{company_name}} Team</p>
        "
        and variables as list containing 
            Templates.TemplateVariable with name as "user_name" and variable_type as "string" and default_value as "User" and metadata as dictionary containing,
            Templates.TemplateVariable with name as "profile_url" and variable_type as "string" and default_value as "#" and metadata as dictionary containing,
            Templates.TemplateVariable with name as "docs_url" and variable_type as "string" and default_value as "#" and metadata as dictionary containing,
            Templates.TemplateVariable with name as "support_url" and variable_type as "string" and default_value as "#" and metadata as dictionary containing
        and partials as list containing
        and macros as list containing
        and parent as "email_base"
        and metadata as dictionary containing

    Note: Password reset email template
    Let reset_email_template be Templates.Template with 
        template_id as "password_reset"
        and template_type as "default"
        and template_code as "
<h2>Password Reset Request</h2>
<p>Hello {{user_name}},</p>
<p>We received a request to reset your password. If this was you, click the link below:</p>
<p><a href='{{reset_url}}' style='background: #007cba; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;'>Reset Password</a></p>
<p>This link will expire in {{expiry_hours}} hours.</p>
<p>If you didn't request this reset, please ignore this email.</p>
<p>Best regards,<br>The {{company_name}} Security Team</p>
        "
        and variables as list containing 
            Templates.TemplateVariable with name as "user_name" and variable_type as "string" and default_value as "User" and metadata as dictionary containing,
            Templates.TemplateVariable with name as "reset_url" and variable_type as "string" and default_value as "#" and metadata as dictionary containing,
            Templates.TemplateVariable with name as "expiry_hours" and variable_type as "integer" and default_value as 24 and metadata as dictionary containing
        and partials as list containing
        and macros as list containing
        and parent as "email_base"
        and metadata as dictionary containing

    Templates.register_template with engine as engine and template as base_email_template
    Templates.register_template with engine as engine and template as welcome_email_template
    Templates.register_template with engine as engine and template as reset_email_template

    Process called "send_welcome_email" that takes user_data as Dictionary[String, Any] returns String:
        Let email_context be dictionary containing 
            "subject" as "Welcome to " plus user_data.get with key as "company_name" and default as "Our Platform",
            "company_name" as user_data.get with key as "company_name" and default as "Our Platform",
            "user_name" as user_data.get with key as "name" and default as "User",
            "profile_url" as user_data.get with key as "profile_url" and default as "/profile",
            "docs_url" as user_data.get with key as "docs_url" and default as "/docs",
            "support_url" as user_data.get with key as "support_url" and default as "/support",
            "unsubscribe_link" as "<a href='/unsubscribe?token=" plus user_data.get with key as "unsubscribe_token" and default as "token" plus "'>Unsubscribe</a>"

        Return Templates.render_template with 
            engine as engine 
            and template_id as "welcome_email" 
            and context as email_context

    Process called "send_password_reset" that takes user_data as Dictionary[String, Any] returns String:
        Let email_context be dictionary containing 
            "subject" as "Password Reset - " plus user_data.get with key as "company_name" and default as "Our Platform",
            "company_name" as user_data.get with key as "company_name" and default as "Our Platform",
            "user_name" as user_data.get with key as "name" and default as "User",
            "reset_url" as user_data.get with key as "reset_url" and default as "/reset",
            "expiry_hours" as user_data.get with key as "expiry_hours" and default as 24,
            "unsubscribe_link" as "<a href='/unsubscribe?token=" plus user_data.get with key as "unsubscribe_token" and default as "token" plus "'>Unsubscribe</a>"

        Return Templates.render_template with 
            engine as engine 
            and template_id as "password_reset" 
            and context as email_context

    Return EmailTemplateSystem with 
        send_welcome_email as send_welcome_email
        and send_password_reset as send_password_reset
        and metadata as dictionary containing

Let email_system be create_email_template_system with engine as engine

Note: Send welcome email
Let new_user be dictionary containing 
    "name" as "Alice Johnson",
    "company_name" as "Runa Technologies",
    "profile_url" as "https://runa.tech/profile",
    "docs_url" as "https://runa.tech/docs",
    "support_url" as "https://runa.tech/support",
    "unsubscribe_token" as "abc123"

Let welcome_email be email_system.send_welcome_email with user_data as new_user
Display "Welcome email:"
Display welcome_email
```

### Code Generation Templates

```runa
Note: Use templates for code generation
Process called "code_generation_templates" that takes engine as Templates.TemplateEngine returns None:
    Note: Function template
    Let function_template be Templates.Template with 
        template_id as "runa_function"
        and template_type as "code"
        and template_code as "
Process called \"{{function_name}}\" that takes {{parameters}} returns {{return_type}}:
    {{#if has_documentation}}
    Note: {{documentation}}
    {{/if}}
    {{#for statement in body}}
    {{statement}}
    {{/for}}
        "
        and variables as list containing 
            Templates.TemplateVariable with name as "function_name" and variable_type as "string" and default_value as "my_function" and metadata as dictionary containing,
            Templates.TemplateVariable with name as "parameters" and variable_type as "string" and default_value as "" and metadata as dictionary containing,
            Templates.TemplateVariable with name as "return_type" and variable_type as "string" and default_value as "None" and metadata as dictionary containing,
            Templates.TemplateVariable with name as "has_documentation" and variable_type as "boolean" and default_value as false and metadata as dictionary containing,
            Templates.TemplateVariable with name as "documentation" and variable_type as "string" and default_value as "" and metadata as dictionary containing,
            Templates.TemplateVariable with name as "body" and variable_type as "list" and default_value as list containing and metadata as dictionary containing
        and partials as list containing
        and macros as list containing
        and parent as None
        and metadata as dictionary containing

    Note: Class template
    Let class_template be Templates.Template with 
        template_id as "runa_class"
        and template_type as "code"
        and template_code as "
Type called \"{{class_name}}\":
    {{#for field in fields}}
    {{field.name}} as {{field.type}}
    {{/for}}

{{#for method in methods}}
Process called \"{{method.name}}\" that takes {{method.parameters}} returns {{method.return_type}}:
    {{#for statement in method.body}}
    {{statement}}
    {{/for}}

{{/for}}
        "
        and variables as list containing 
            Templates.TemplateVariable with name as "class_name" and variable_type as "string" and default_value as "MyClass" and metadata as dictionary containing,
            Templates.TemplateVariable with name as "fields" and variable_type as "list" and default_value as list containing and metadata as dictionary containing,
            Templates.TemplateVariable with name as "methods" and variable_type as "list" and default_value as list containing and metadata as dictionary containing
        and partials as list containing
        and macros as list containing
        and parent as None
        and metadata as dictionary containing

    Templates.register_template with engine as engine and template as function_template
    Templates.register_template with engine as engine and template as class_template

    Note: Generate a function
    Let function_spec be dictionary containing 
        "function_name" as "calculate_fibonacci",
        "parameters" as "n as Integer",
        "return_type" as "Integer",
        "has_documentation" as true,
        "documentation" as "Calculates the nth Fibonacci number using recursion",
        "body" as list containing 
            "If n is less than or equal to 1:",
            "    Return n",
            "Return calculate_fibonacci with n as (n minus 1) plus calculate_fibonacci with n as (n minus 2)"

    Let generated_function be Templates.render_template with 
        engine as engine 
        and template_id as "runa_function" 
        and context as function_spec

    Display "Generated function:"
    Display generated_function

    Note: Generate a class
    Let class_spec be dictionary containing 
        "class_name" as "BankAccount",
        "fields" as list containing 
            dictionary containing "name" as "account_number" and "type" as "String",
            dictionary containing "name" as "balance" and "type" as "Float",
            dictionary containing "name" as "owner_name" and "type" as "String",
        "methods" as list containing 
            dictionary containing 
                "name" as "deposit",
                "parameters" as "amount as Float",
                "return_type" as "None",
                "body" as list containing 
                    "If amount is greater than 0:",
                    "    Set self.balance to self.balance plus amount",
                    "Otherwise:",
                    "    Raise ValueError with message as \"Deposit amount must be positive\"",
            dictionary containing 
                "name" as "withdraw",
                "parameters" as "amount as Float",
                "return_type" as "Boolean",
                "body" as list containing 
                    "If amount is greater than 0 and amount is less than or equal to self.balance:",
                    "    Set self.balance to self.balance minus amount",
                    "    Return true",
                    "Return false"

    Let generated_class be Templates.render_template with 
        engine as engine 
        and template_id as "runa_class" 
        and context as class_spec

    Display "Generated class:"
    Display generated_class

code_generation_templates with engine as engine
```

## Advanced Patterns

### Template Compilation and Caching

```runa
Note: Advanced template compilation system
Type called "CompiledTemplate":
    template_id as String
    compiled_code as Function
    dependencies as List[String]
    cache_key as String
    compilation_time as Integer

Process called "create_template_compiler" that takes engine as Templates.TemplateEngine returns TemplateCompiler:
    Let compiled_cache be dictionary containing
    
    Process called "compile_template" that takes template_id as String returns CompiledTemplate:
        Let cache_key be "compiled_" plus template_id
        
        If cache_key in compiled_cache:
            Return compiled_cache[cache_key]
        
        Let template be engine.templates[template_id]
        Let start_time be get_current_time
        
        Note: Parse template and create optimized rendering function
        Let compiled_function be create_optimized_renderer with template as template
        
        Let compilation_time be get_current_time minus start_time
        Let dependencies be extract_template_dependencies with template as template
        
        Let compiled_template be CompiledTemplate with 
            template_id as template_id
            and compiled_code as compiled_function
            and dependencies as dependencies
            and cache_key as cache_key
            and compilation_time as compilation_time
        
        Set compiled_cache[cache_key] to compiled_template
        Return compiled_template
    
    Process called "render_compiled" that takes template_id as String and context as Dictionary[String, Any] returns String:
        Let compiled be compile_template with template_id as template_id
        Return compiled.compiled_code with context as context
    
    Process called "invalidate_cache" that takes template_id as String returns None:
        Let cache_key be "compiled_" plus template_id
        If cache_key in compiled_cache:
            Remove cache_key from compiled_cache
        
        Note: Invalidate dependent templates
        For each cached_key in compiled_cache:
            Let cached_template be compiled_cache[cached_key]
            If template_id in cached_template.dependencies:
                Remove cached_key from compiled_cache
    
    Return TemplateCompiler with 
        compile_template as compile_template
        and render_compiled as render_compiled
        and invalidate_cache as invalidate_cache
        and compiled_cache as compiled_cache
        and metadata as dictionary containing

Let compiler be create_template_compiler with engine as engine

Note: Use compiled templates for better performance
Let rendered be compiler.render_compiled with 
    template_id as "product_list" 
    and context as product_data

Display "Compiled template result:"
Display rendered
```

### Dynamic Template Generation

```runa
Note: Generate templates dynamically based on schemas
Process called "schema_driven_template_generation" that takes engine as Templates.TemplateEngine and schema as Dictionary[String, Any] returns String:
    Let template_code be ""
    
    Note: Generate form template based on schema
    If schema["type"] is "form":
        Set template_code to "<form action='{{action}}' method='{{method}}'>\n"
        
        For each field in schema["fields"]:
            Let field_type be field.get with key as "type" and default as "text"
            Let field_name be field["name"]
            Let field_label be field.get with key as "label" and default as field_name
            
            Set template_code to template_code plus "    <label for='" plus field_name plus "'>" plus field_label plus "</label>\n"
            
            If field_type is "select":
                Set template_code to template_code plus "    <select name='" plus field_name plus "' id='" plus field_name plus "'>\n"
                Set template_code to template_code plus "        {{#for option in " plus field_name plus "_options}}\n"
                Set template_code to template_code plus "        <option value='{{option.value}}'>{{option.label}}</option>\n"
                Set template_code to template_code plus "        {{/for}}\n"
                Set template_code to template_code plus "    </select>\n"
            Else if field_type is "textarea":
                Set template_code to template_code plus "    <textarea name='" plus field_name plus "' id='" plus field_name plus "'>{{" plus field_name plus "}}</textarea>\n"
            Else:
                Set template_code to template_code plus "    <input type='" plus field_type plus "' name='" plus field_name plus "' id='" plus field_name plus "' value='{{" plus field_name plus "}}' />\n"
        
        Set template_code to template_code plus "    <button type='submit'>{{submit_text}}</button>\n"
        Set template_code to template_code plus "</form>"
    
    Note: Create variables list from schema
    Let variables be list containing
    For each field in schema.get with key as "fields" and default as list containing:
        Add Templates.TemplateVariable with 
            name as field["name"]
            and variable_type as field.get with key as "type" and default as "string"
            and default_value as field.get with key as "default" and default as ""
            and metadata as dictionary containing to variables
    
    Note: Add common form variables
    Add Templates.TemplateVariable with name as "action" and variable_type as "string" and default_value as "/submit" and metadata as dictionary containing to variables
    Add Templates.TemplateVariable with name as "method" and variable_type as "string" and default_value as "POST" and metadata as dictionary containing to variables
    Add Templates.TemplateVariable with name as "submit_text" and variable_type as "string" and default_value as "Submit" and metadata as dictionary containing to variables
    
    Note: Create and register the template
    Let dynamic_template be Templates.Template with 
        template_id as schema["id"]
        and template_type as "dynamic"
        and template_code as template_code
        and variables as variables
        and partials as list containing
        and macros as list containing
        and parent as None
        and metadata as dictionary containing "generated_from_schema" as true

    Templates.register_template with engine as engine and template as dynamic_template
    Return template_code

Note: Generate a contact form template
Let contact_form_schema be dictionary containing 
    "id" as "contact_form",
    "type" as "form",
    "fields" as list containing 
        dictionary containing "name" as "name" and "type" as "text" and "label" as "Full Name",
        dictionary containing "name" as "email" and "type" as "email" and "label" as "Email Address",
        dictionary containing "name" as "subject" and "type" as "text" and "label" as "Subject",
        dictionary containing "name" as "message" and "type" as "textarea" and "label" as "Message"

Let generated_template_code be schema_driven_template_generation with 
    engine as engine 
    and schema as contact_form_schema

Display "Generated template code:"
Display generated_template_code

Note: Render the generated form
Let form_context be dictionary containing 
    "action" as "/contact",
    "method" as "POST",
    "submit_text" as "Send Message",
    "name" as "",
    "email" as "",
    "subject" as "",
    "message" as ""

Let rendered_form be Templates.render_template with 
    engine as engine 
    and template_id as "contact_form" 
    and context as form_context

Display "Rendered form:"
Display rendered_form
```

### Template Debugging and Profiling

```runa
Note: Template debugging and profiling system
Type called "TemplateDebugger":
    engine as Templates.TemplateEngine
    debug_mode as Boolean
    profiling_enabled as Boolean
    render_history as List[RenderOperation]

Type called "RenderOperation":
    template_id as String
    context as Dictionary[String, Any]
    start_time as Integer
    end_time as Integer
    result as String
    variables_used as List[String]
    partials_rendered as List[String]

Process called "create_template_debugger" that takes engine as Templates.TemplateEngine returns TemplateDebugger:
    Process called "debug_render" that takes template_id as String and context as Dictionary[String, Any] returns String:
        Let start_time be get_current_time
        
        If debugger.debug_mode:
            Display "=== Template Render Debug ==="
            Display "Template: " plus template_id
            Display "Context variables:"
            For each key in context:
                Display "  " plus key plus ": " plus context[key]
        
        Let result be Templates.render_template with 
            engine as debugger.engine 
            and template_id as template_id 
            and context as context
        
        Let end_time be get_current_time
        Let render_time be end_time minus start_time
        
        If debugger.debug_mode:
            Display "Render time: " plus render_time plus "ms"
            Display "Output length: " plus length of result plus " characters"
            Display "=== End Debug ==="
        
        If debugger.profiling_enabled:
            Let operation be RenderOperation with 
                template_id as template_id
                and context as context
                and start_time as start_time
                and end_time as end_time
                and result as result
                and variables_used as extract_variables_from_template with template_id as template_id
                and partials_rendered as list containing
            
            Add operation to debugger.render_history
        
        Return result
    
    Process called "get_performance_report" returns String:
        If length of debugger.render_history is 0:
            Return "No render operations recorded."
        
        Let total_time be 0
        Let template_counts be dictionary containing
        
        For each operation in debugger.render_history:
            Let render_time be operation.end_time minus operation.start_time
            Set total_time to total_time plus render_time
            
            If operation.template_id in template_counts:
                Set template_counts[operation.template_id] to template_counts[operation.template_id] plus 1
            Else:
                Set template_counts[operation.template_id] to 1
        
        Let report be "=== Template Performance Report ===\n"
        Set report to report plus "Total operations: " plus length of debugger.render_history plus "\n"
        Set report to report plus "Total time: " plus total_time plus "ms\n"
        Set report to report plus "Average time: " plus (total_time divided by length of debugger.render_history) plus "ms\n\n"
        Set report to report plus "Template usage:\n"
        
        For each template_id in template_counts:
            Set report to report plus "  " plus template_id plus ": " plus template_counts[template_id] plus " renders\n"
        
        Return report
    
    Return TemplateDebugger with 
        engine as engine
        and debug_mode as true
        and profiling_enabled as true
        and render_history as list containing
        and debug_render as debug_render
        and get_performance_report as get_performance_report
        and metadata as dictionary containing

Let debugger be create_template_debugger with engine as engine

Note: Use debugger for template rendering
Let debug_result be debugger.debug_render with 
    template_id as "product_list" 
    and context as product_data

Let performance_report be debugger.get_performance_report
Display performance_report
```

## Performance Considerations

### Template Compilation

- **Parse Once**: Templates are parsed once and cached for subsequent renders
- **Variable Substitution**: Optimized variable lookup and substitution
- **Control Flow**: Efficient evaluation of conditionals and loops
- **Memory Usage**: Minimal memory overhead for template storage

### Optimization Strategies

```runa
Note: Template performance optimization
Process called "optimize_template_performance" that takes engine as Templates.TemplateEngine returns None:
    Note: Pre-compile frequently used templates
    Let frequent_templates be list containing "header", "footer", "product_list", "user_profile"
    
    For each template_id in frequent_templates:
        If template_id in engine.templates:
            Note: Pre-process and optimize template
            Let template be engine.templates[template_id]
            optimize_template_code with template as template
    
    Note: Set up template caching
    Set engine.metadata["cache_enabled"] to true
    Set engine.metadata["cache_max_size"] to 1000
    Set engine.metadata["cache_ttl"] to 3600  Note: 1 hour

Process called "optimize_template_code" that takes template as Templates.Template returns None:
    Note: Optimize template code for faster rendering
    Let optimized_code be template.template_code
    
    Note: Remove unnecessary whitespace
    Set optimized_code to trim_whitespace with text as optimized_code
    
    Note: Pre-process variables for faster lookup
    Let variables_map be dictionary containing
    For each variable in template.variables:
        Set variables_map[variable.name] to variable
    
    Set template.metadata["variables_map"] to variables_map
    Set template.metadata["optimized"] to true

optimize_template_performance with engine as engine
```

## Best Practices

### 1. Template Organization

Organize templates in a logical hierarchy:

```runa
Note: Good template organization
Let templates_structure be dictionary containing 
    "layouts" as list containing "base", "admin", "public",
    "partials" as list containing "header", "footer", "navigation",
    "emails" as list containing "welcome", "password_reset", "notification",
    "forms" as list containing "login", "register", "contact"

Note: Use consistent naming conventions
Note: base_layout.html, email_welcome.html, partial_header.html
```

### 2. Context Validation

Always validate template context:

```runa
Process called "safe_template_render" that takes engine as Templates.TemplateEngine and template_id as String and context as Dictionary[String, Any] returns String:
    Note: Validate required variables
    If template_id in engine.templates:
        Let template be engine.templates[template_id]
        
        For each variable in template.variables:
            If variable.name not in context and variable.default_value is None:
                Display "Warning: Required variable '" plus variable.name plus "' not provided for template '" plus template_id plus "'"
                Set context[variable.name] to ""
    
    Return Templates.render_template with 
        engine as engine 
        and template_id as template_id 
        and context as context
```

### 3. Error Handling

Implement comprehensive error handling:

```runa
Process called "robust_template_rendering" that takes engine as Templates.TemplateEngine and template_id as String and context as Dictionary[String, Any] returns String:
    Try:
        Return Templates.render_template with 
            engine as engine 
            and template_id as template_id 
            and context as context
    Catch error as Templates.TemplateEngineError:
        Display "Template rendering error: " plus error.message
        Note: Return fallback content
        Return "<div class='error'>Template '" plus template_id plus "' could not be rendered</div>"
    Catch unexpected_error:
        Display "Unexpected error during template rendering: " plus unexpected_error
        Return "<div class='error'>An unexpected error occurred</div>"
```

### 4. Security Considerations

Always escape user input in templates:

```runa
Note: Good: Escaped output (default)
Note: {{user_input}}

Note: Caution: Raw output (only when necessary)
Note: {{{trusted_html}}}

Note: Validate context data before rendering
Process called "sanitize_template_context" that takes context as Dictionary[String, Any] returns Dictionary[String, Any]:
    Let sanitized be dictionary containing
    
    For each key in context:
        Let value be context[key]
        If value is String:
            Set sanitized[key] to escape_html with text as value
        Else:
            Set sanitized[key] to value
    
    Return sanitized
```

### 5. Performance Monitoring

Monitor template performance in production:

```runa
Process called "monitor_template_performance" that takes engine as Templates.TemplateEngine returns None:
    Note: Track slow templates
    Set engine.metadata["performance_monitoring"] to true
    Set engine.metadata["slow_threshold_ms"] to 100
    
    Note: Log performance metrics
    If "performance_log" not in engine.metadata:
        Set engine.metadata["performance_log"] to list containing
```

The Template Engine module provides powerful and flexible templating capabilities for generating dynamic content, from simple variable substitution to complex inheritance hierarchies and control flow structures. Its comprehensive feature set makes it suitable for everything from web development to code generation systems.