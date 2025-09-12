# Field and Method Access in Runa (Mode-Scoped)

**Last Updated**: 2025-09-08  
**Note**: This documentation reflects the current implementation with mathematical symbol enforcement.

## Overview

Runa supports both natural language and technical syntax for accessing fields and methods. Usage is scoped by mode:

- **Canon**: natural phrases like "the name of user" and "the area of circle".
- **Developer**: dot notation as a technical shorthand (e.g., `user.name`, `circle.area`).
- **Viewer**: read-only natural phrasing; dot notation is not displayed.

**Mathematical Symbol Note**: Mathematical operations in method examples use natural language operators (`multiplied by`, `plus`, `minus`) which are always valid. Mathematical symbols (`*`, `+`, `-`) are restricted to mathematical contexts only.

## Field Access

### Natural Language Syntax (Recommended for Basic/Intermediate Examples)

```runa
Let radius be the radius of circle
Let name be the name of user
Let width be the width of rectangle
Let value be the value of counter
Let balance be the balance of account
Let status be the status of order
```

### Developer Mode Technical Syntax

```runa
Let radius be circle.radius
Let name be user.name
Let width be rectangle.width
Let value be counter.value
Let balance be account.balance
Let status be order.status
```

## Method Access

### Natural Language Syntax (Recommended for Basic/Intermediate Examples)

```runa
Let area be the area of circle
Let magnitude be the magnitude of complex_number
Let result be the output of process with input as value
Let sum be the sum of a and b
Let length be the length of string
Let count be the count of items
```

### Technical Syntax (For Advanced/Backend Development)

```runa
Let area be circle.area
Let magnitude be complex_number.magnitude
Let result be process with self as value
Let sum be add with a as a and b as b
Let length be string.length
Let count be items.count
```

## Collection Access (Mode-Scoped)

### Developer Mode Bracket Notation (Dictionaries and Lists)

```runa
Let value be my_dict["key"]
Let item be my_list[0]
Let element be array at index 5
Let first_item be list at index 0
Let last_item be list at index length of list minus 1
Let value2 be my_dict at key "id"
```

### Canon/Viewer Natural Language for Collections

```runa
Let value be the value of my_dict at key
Let item be the first item of my_list
Let element be the element of array at index 5
Let first_item be the first item of list
Let last_item be the last item of list
```

## Type Definitions with Methods

```runa
Type called "Circle":
    radius as Float

    Process called "area" returns Float:
        Return 3.14159 multiplied by the radius of self to the power of 2
        Note: Or: Return 3.14159 multiplied by self.radius to the power of 2

    Process called "circumference" returns Float:
        Return 2 multiplied by 3.14159 multiplied by the radius of self
        Note: Or: Return 2 multiplied by 3.14159 multiplied by self.radius

    Process called "diameter" returns Float:
        Return 2 multiplied by the radius of self
        Note: Or: Return 2 multiplied by self.radius
```

## Usage Guidelines

### 1. **Basic and Intermediate Examples**
Use natural language syntax for better readability and accessibility:
```runa
Let user_name be the name of current_user
Let account_balance be the balance of user_account
Let transaction_count be the count of transactions
Let is_active be the status of user_account
```

### 2. **Advanced/Backend Development**
Use technical syntax for efficiency and familiarity:
```runa
Let user_name be current_user.name
Let account_balance be user_account.balance
Let transaction_count be transactions.count
Let is_active be user_account.status
```

### 3. **Documentation Standards**
- Always provide natural language examples first
- Include technical syntax as alternatives
- Use natural language in tutorials and beginner guides
- Use technical syntax in advanced documentation and API references

### 4. **Consistency**
- Choose one style per project or module for consistency
- Document the chosen style in project guidelines
- Use linters or style checkers to enforce consistency

## Examples by Audience

### For Non-Developers/Domain Experts

```runa
Let customer_name be the name of current_customer
Let order_total be the total of current_order
Let product_count be the count of products in cart
Let delivery_date be the date of delivery
Let payment_status be the status of payment
```

### For Experienced Developers

```runa
Let customer_name be current_customer.name
Let order_total be current_order.total
Let product_count be cart.products.count
Let delivery_date be delivery.date
Let payment_status be payment.status
```

### For AI/Advanced Development

```runa
Let result be process_data with input as data and config as settings
Let output be neural_network.forward with input as features
Let gradient be loss_function.backward with prediction as pred and target as target
Let embedding be model.encode with text as input_text
Let classification be classifier.predict with features as feature_vector
```

## Complex Object Access

### Nested Field Access

```runa
Note: Natural Language
Let street be the street of the address of user
Let city be the city of the address of user
Let country be the country of the address of user

Note: Technical Syntax
Let street be user.address.street
Let city be user.address.city
Let country be user.address.country
```

### Method Chaining

```runa
Note: Natural Language
Let processed_data be the result of process_data with input as raw_data
Let filtered_data be the result of filter_data with data as processed_data and criteria as filter_criteria
Let final_result be the result of format_output with data as filtered_data

Note: Technical Syntax
Let processed_data be process_data with input as raw_data
Let filtered_data be filter_data with data as processed_data and criteria as filter_criteria
Let final_result be format_output with data as filtered_data
```

## Error Handling

### Safe Field Access

```runa
Note: Natural Language with Error Handling
Try:
    Let value be the field of object
    Display "Field accessed successfully"
Catch err (FieldNotFoundError):
    Display "Field not found: " with message the name of field
Catch err (Error):
    Display "Error accessing field: " with message the message of err

Note: Technical Syntax with Error Handling
Try:
    Let value be object.field
    Display "Field accessed successfully"
Catch err (FieldNotFoundError):
    Display "Field not found: " with message field
Catch err (Error):
    Display "Error accessing field: " with message err.message
```

## Performance Considerations

### Natural Language vs Technical Syntax

- **Natural Language (Canon/Viewer)**: More readable, better for documentation and teaching
- **Technical Syntax (Developer)**: More concise, better for performance-critical code
- **Compilation**: Canon and Developer compile to the same representations under AOTT
- **Parsing**: Developer syntax may be slightly faster to parse; Canon remains the canonical AST

## Best Practices

1. **Use Natural Language for:**
   - Tutorials and documentation
   - Beginner-friendly examples
   - Domain-specific code
   - Educational materials

2. **Use Technical Syntax for:**
   - Performance-critical code
   - Advanced algorithms
   - Backend services
   - Library implementations

3. **Be Consistent:**
   - Choose one style per project
   - Document your choice
   - Use automated tools to enforce consistency

4. **Consider Your Audience:**
   - Non-developers: Natural language
   - Experienced developers: Technical syntax
   - Mixed audience: Provide both examples

## Migration Guide

### From Dot Notation to Natural Language

```runa
Note: Before (Technical)
Let area be circle.area
Let name be user.name
Let count be items.count

Note: After (Natural Language)
Let area be the area of circle
Let name be the name of user
Let count be the count of items
```

### From Natural Language to Dot Notation

```runa
Note: Before (Natural Language)
Let area be the area of circle
Let name be the name of user
Let count be the count of items

Note: After (Technical)
Let area be circle.area
Let name be user.name
Let count be items.count
```

## Conclusion

Runa's dual syntax approach provides flexibility for different audiences and use cases. Choose the syntax that best fits your project's needs and audience, but always prioritize consistency and clarity in your codebase. 

## Open Issues

1. Expand examples to cover Viewer transformations for complex chaining scenarios.
2. Formalize guidance for nested collection access in Canon without brackets.