# JavaScript Transpilation in Runa

JavaScript is a key target language for Runa, particularly valuable for web applications and Node.js environments. This guide covers the specifics of transpiling Runa code to JavaScript.

## Table of Contents

1. [Overview](#overview)
2. [Language Mappings](#language-mappings)
3. [JavaScript-Specific Features](#javascript-specific-features)
4. [Configuration Options](#configuration-options)
5. [Performance Considerations](#performance-considerations)
6. [Interoperability](#interoperability)
7. [Web Development](#web-development)
8. [Troubleshooting](#troubleshooting)

## Overview

JavaScript transpilation converts Runa source code to modern JavaScript (ES2020+) code. The generated JavaScript maintains semantic equivalence while leveraging JavaScript's ecosystem.

### Benefits of JavaScript as a Target

- **Web Compatibility**: Deploy Runa applications directly in browsers
- **Node.js Support**: Run server-side code on the Node.js runtime
- **Full-Stack Development**: Seamless client-server development experience
- **Broad Adoption**: Leverage the world's most widely deployed runtime
- **Modern Features**: Access to modern JavaScript features like async/await, modules, etc.

### Requirements

- Node.js 14.0 or higher recommended for development
- Required packages (automatically installed with Runa):
  - `runalang-js-runtime`: Core runtime support
  - `core-js`: Polyfills for older environments (if needed)

## Language Mappings

### Basic Constructs

| Runa Construct | JavaScript Equivalent |
|----------------|-------------------|
| `Process called name(params)` | `function name(params) {` |
| `Let variable = value` | `let variable = value;` |
| `Constant NAME = value` | `const NAME = value;` |
| `If condition Then` | `if (condition) {` |
| `Otherwise If condition Then` | `else if (condition) {` |
| `Otherwise` | `else {` |
| `End If` | `}` |
| `For item in collection` | `for (const item of collection) {` |
| `For i from 0 to 10` | `for (let i = 0; i <= 10; i++) {` |
| `While condition` | `while (condition) {` |
| `Return value` | `return value;` |
| `Break` | `break;` |
| `Continue` | `continue;` |
| `Print(value)` | `console.log(value);` |
| `Try...Catch...Finally` | `try {...} catch(e) {...} finally {...}` |

### Data Types

| Runa Type | JavaScript Type |
|-----------|-------------|
| `Number` | `number` |
| `Integer` | `number` (integer handling) |
| `Decimal` | `number` (floating-point) |
| `Text` | `string` |
| `Boolean` | `boolean` |
| `List of Type` | `Array` |
| `Map of KeyType to ValueType` | `Map` or object literal |
| `Optional Type` | Value or `null` |
| `Any` | Any JavaScript value |
| `Null` | `null` |
| `Tuple(Type1, Type2, ...)` | Array with specific elements |
| `Structure` | Class or object literal |

### Object-Oriented Programming

| Runa Construct | JavaScript Equivalent |
|----------------|-------------------|
| `Structure called Name` | `class Name {` |
| `Method called name(self, params)` | `name(params) {` |
| `Property name of type Type` | `#name; constructor() { this.#name = null; }` |
| `Static Method called name(params)` | `static name(params) {` |
| `Inherit from BaseClass` | `class Name extends BaseClass {` |

### Functional Programming

| Runa Construct | JavaScript Equivalent |
|----------------|-------------------|
| `Map function over list` | `list.map(function)` |
| `Filter list by condition` | `list.filter(condition)` |
| `Reduce list using function` | `list.reduce(function, initialValue)` |
| `Lambda (params) => expression` | `(params) => expression` |

### Error Handling

| Runa Construct | JavaScript Equivalent |
|----------------|-------------------|
| `Try` | `try {` |
| `Catch error of ErrorType as name` | `catch(name) { if (name instanceof ErrorType) {` |
| `Catch any error as name` | `catch(name) {` |
| `Finally` | `finally {` |
| `Throw new ErrorType(message)` | `throw new ErrorType(message);` |

### Asynchronous Programming

| Runa Construct | JavaScript Equivalent |
|----------------|-------------------|
| `Async Process called name(params)` | `async function name(params) {` |
| `Await expression` | `await expression;` |
| `Promise of Type` | `Promise<Type>` in comments/JSDoc |

## JavaScript-Specific Features

### Module System

Runa automatically leverages ES Modules:

```
# Runa code
Import Math
Import "my_module" as MyModule

Export Process called add(a as Number, b as Number) returns Number
    Return a + b
End Process

# Transpiled JavaScript
import * as Math from 'runa/lib/math.js';
import * as MyModule from './my_module.js';

export function add(a, b) {
    return a + b;
}
```

### Type Safety

TypeScript-like comments can be generated for better IDE support:

```
# Runa code
Process called calculate(value as Number, options as Map of Text to Any) returns Number
    Return value * 2
End Process

# Transpiled JavaScript with JSDoc
/**
 * @param {number} value
 * @param {Object<string, any>} options
 * @returns {number}
 */
function calculate(value, options) {
    return value * 2;
}
```

### Closures and Scoping

Runa handles closures and block scoping:

```
# Runa code
Process called create_counter(initial as Number) returns Process returns Number
    Let count = initial
    
    Return Process called increment() returns Number
        count = count + 1
        Return count
    End Process
End Process

# Transpiled JavaScript
function create_counter(initial) {
    let count = initial;
    
    return function increment() {
        count = count + 1;
        return count;
    };
}
```

### Class Implementation

Runa structures map to modern JavaScript classes:

```
# Runa code
Structure called Person
    Property name of type Text
    Property age of type Number
    
    Method called constructor(name as Text, age as Number)
        self.name = name
        self.age = age
    End Method
    
    Method called greet() returns Text
        Return "Hello, my name is " + self.name
    End Method
End Structure

# Transpiled JavaScript
class Person {
    #name;
    #age;
    
    constructor(name, age) {
        this.#name = name;
        this.#age = age;
    }
    
    greet() {
        return "Hello, my name is " + this.#name;
    }
    
    // Getters and setters
    get name() { return this.#name; }
    set name(value) { this.#name = value; }
    get age() { return this.#age; }
    set age(value) { this.#age = value; }
}
```

## Configuration Options

### JavaScript/ECMAScript Version

You can specify the target ECMAScript version:

```bash
runa compile --target javascript --js-version es2020 my_program.runa
```

In configuration file:

```json
{
  "transpilation": {
    "target": "javascript",
    "js_options": {
      "ecma_version": "es2020",
      "module_format": "esm"
    }
  }
}
```

### Module Format

Choose between ES Modules and CommonJS:

```json
{
  "transpilation": {
    "target": "javascript",
    "js_options": {
      "module_format": "esm" 
      // or "commonjs" for Node.js compatibility
    }
  }
}
```

### Type Checking

Add TypeScript-like JSDoc comments:

```json
{
  "transpilation": {
    "target": "javascript",
    "js_options": {
      "jsdoc_annotations": true,
      "typescript_definitions": true
    }
  }
}
```

### Styling and Formatting

Control JavaScript output styling:

```json
{
  "transpilation": {
    "target": "javascript",
    "js_options": {
      "semicolons": true,
      "single_quotes": true,
      "tab_width": 2,
      "trailing_commas": "es5"
    }
  }
}
```

### Browser Compatibility

Generate code for older browsers:

```json
{
  "transpilation": {
    "target": "javascript",
    "js_options": {
      "target_environments": ["chrome >= 60", "firefox >= 60", "safari >= 12"],
      "include_polyfills": true
    }
  }
}
```

## Performance Considerations

### Memory Management

JavaScript's garbage collection is automatic, but there are techniques for optimizing memory usage:

```
# Runa code
Process called process_data(data as List of Number) returns Number
    Using memory_scope Do
        Let result = data.filter(item => item > 0)
                         .map(item => item * 2)
                         .sum()
        Return result
    End Using
End Process

# Transpiled JavaScript with optimization hints
function process_data(data) {
    // Memory scope handled through function scope
    // Optimize by chaining operations directly
    return data.filter(item => item > 0)
               .map(item => item * 2)
               .reduce((sum, item) => sum + item, 0);
}
```

### Web Workers

Runa can target web workers for parallelism:

```
# Runa code
Process called compute_in_parallel(data as List of Any) returns Promise of Any
    Return Parallel.compute(data, process_chunk)
End Process

# Transpiled JavaScript
function compute_in_parallel(data) {
    return new Promise((resolve, reject) => {
        const worker = new Worker(new URL('./worker.js', import.meta.url));
        worker.onmessage = (event) => resolve(event.data);
        worker.onerror = (error) => reject(error);
        worker.postMessage({ data, operation: 'process_chunk' });
    });
}

// worker.js (generated file)
self.onmessage = function(event) {
    const { data, operation } = event.data;
    if (operation === 'process_chunk') {
        const result = process_chunk(data);
        self.postMessage(result);
    }
};
```

### Optimizing Performance

Runa's compile-time optimizations for JavaScript:

```
# Runa code
Process called matrix_multiply(a as List of List of Number, b as List of List of Number) returns List of List of Number
    // Matrix multiplication implementation
    // ...
    Return result
End Process

# Transpiled JavaScript
function matrix_multiply(a, b) {
    // Optimized with typed arrays when possible
    if (isRegularMatrix(a) && isRegularMatrix(b)) {
        return matrix_multiply_optimized(a, b);
    } else {
        // General case implementation
        // ...
    }
}

function matrix_multiply_optimized(a, b) {
    const rows = a.length;
    const cols = b[0].length;
    const result = new Array(rows);
    for (let i = 0; i < rows; i++) {
        result[i] = new Float64Array(cols);
        // Implementation using typed arrays
        // ...
    }
    return result;
}
```

## Interoperability

### Using JavaScript Libraries

Runa provides direct access to JavaScript libraries:

```
# Runa code
Import JavaScript "axios" as http
Import JavaScript "./utils.js" as Utils

Process called fetch_data(url as Text) returns Promise of Any
    Let response = Await http.get(url)
    Let processed = Utils.process_data(response.data)
    Return processed
End Process

# Transpiled JavaScript
import axios from 'axios';
import * as Utils from './utils.js';

async function fetch_data(url) {
    const response = await axios.get(url);
    const processed = Utils.process_data(response.data);
    return processed;
}
```

### Native JavaScript Blocks

Use inline JavaScript when needed:

```
# Runa code
Process called browser_specific_operation() returns Any
    JavaScript {
        // Access browser-specific APIs
        const userAgent = navigator.userAgent;
        const isMobile = /Android|iPhone|iPad|iPod/i.test(userAgent);
        return {
            userAgent,
            isMobile,
            screenSize: {
                width: window.innerWidth,
                height: window.innerHeight
            }
        };
    }
End Process

# Transpiled JavaScript
function browser_specific_operation() {
    // Access browser-specific APIs
    const userAgent = navigator.userAgent;
    const isMobile = /Android|iPhone|iPad|iPod/i.test(userAgent);
    return {
        userAgent,
        isMobile,
        screenSize: {
            width: window.innerWidth,
            height: window.innerHeight
        }
    };
}
```

## Web Development

### DOM Integration

Runa provides built-in support for DOM manipulation:

```
# Runa code
Import DOM

Process called update_ui(data as List of Any)
    Let container = DOM.get_element_by_id("container")
    container.innerHTML = ""
    
    For item in data
        Let element = DOM.create_element("div")
        element.classList.add("item")
        element.textContent = item.name
        element.addEventListener("click", () => handle_click(item))
        container.appendChild(element)
    End For
End Process

# Transpiled JavaScript
import { DOM } from 'runa/web.js';

function update_ui(data) {
    const container = document.getElementById("container");
    container.innerHTML = "";
    
    for (const item of data) {
        const element = document.createElement("div");
        element.classList.add("item");
        element.textContent = item.name;
        element.addEventListener("click", () => handle_click(item));
        container.appendChild(element);
    }
}
```

### JSX Support

Runa can output JSX for React applications:

```
# Runa code
Import React from "react"

Process called ItemList(props as Any) returns Element
    Return (
        <div className="list">
            <h2>{props.title}</h2>
            <ul>
                {Map render_item over props.items}
            </ul>
        </div>
    )
End Process

Process called render_item(item as Any) returns Element
    Return <li key={item.id}>{item.name}</li>
End Process

# Transpiled JavaScript (JSX)
import React from 'react';

function ItemList(props) {
    return (
        <div className="list">
            <h2>{props.title}</h2>
            <ul>
                {props.items.map(render_item)}
            </ul>
        </div>
    );
}

function render_item(item) {
    return <li key={item.id}>{item.name}</li>;
}
```

### Component Frameworks

Runa integrates with popular frameworks:

```
# Runa code with Vue syntax
Import Vue from "vue"

Export Structure called Counter
    Property count of type Number = 0
    
    Method called increment()
        self.count = self.count + 1
    End Method
    
    Method called render() returns Element
        Return (
            <div>
                <p>Count: {self.count}</p>
                <button @click="self.increment()">Increment</button>
            </div>
        )
    End Method
End Structure

# Transpiled JavaScript (Vue component)
import Vue from 'vue';

export default {
    data() {
        return {
            count: 0
        };
    },
    methods: {
        increment() {
            this.count = this.count + 1;
        }
    },
    render(h) {
        return h('div', [
            h('p', [`Count: ${this.count}`]),
            h('button', {
                on: { click: this.increment }
            }, ['Increment'])
        ]);
    }
};
```

## Troubleshooting

### Common Issues

#### Module Import Errors

**Issue**: Problems with module imports or "Cannot find module" errors.

**Solution**: Verify import paths and module format configuration.

```json
{
  "transpilation": {
    "target": "javascript",
    "js_options": {
      "module_format": "esm",
      "module_resolution": "node"
    }
  }
}
```

#### Browser Compatibility

**Issue**: Code doesn't work in target browsers.

**Solution**: Enable polyfills and set appropriate target environments.

```json
{
  "transpilation": {
    "target": "javascript",
    "js_options": {
      "include_polyfills": true,
      "target_environments": ["ie 11", "edge >= 18"]
    }
  }
}
```

#### Performance Issues

**Issue**: Slow JavaScript performance.

**Solution**: Enable optimizations and review transpiled code.

```json
{
  "transpilation": {
    "target": "javascript",
    "js_options": {
      "optimization_level": "high",
      "use_typed_arrays": true
    }
  }
}
```

#### Runtime Errors

**Issue**: "X is not a function" or similar runtime errors.

**Solution**: Use strict mode and verify runtime library inclusion.

```bash
runa compile --strict --include-runtime my_program.runa
```

### Debugging Transpiled Code

To debug the transpiled JavaScript code:

1. Generate JavaScript with source maps:
   ```bash
   runa compile --source-maps my_program.runa
   ```

2. Use browser DevTools or Node.js debugging on the transpiled code.

3. Add debug mode comments:
   ```bash
   runa compile --debug-comments my_program.runa
   ```

   This adds comments showing the original Runa code:
   ```javascript
   // From Runa: Process called calculate_sum(a as Number, b as Number) returns Number
   function calculate_sum(a, b) {
       // From Runa: Return a + b
       return a + b;
   }
   ```

### Get Help

If you're still having issues:

1. Check the [JavaScript transpilation FAQ](../FAQ/JavaScriptTranspilation.md)
2. Run the validator to check your Runa code:
   ```bash
   runa validate my_program.runa
   ```
3. Reach out to the community via:
   - [GitHub Issues](https://github.com/runalang/runa/issues)
   - [Discord Community](https://discord.gg/runalang)
   - [StackOverflow with the 'runalang' tag](https://stackoverflow.com/questions/tagged/runalang) 