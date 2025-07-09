#!/usr/bin/env python3
"""
Comprehensive Round-Trip Translation Tests for Tier 1 Languages

This test suite verifies the complete Runa Universal Translation Pipeline for:
- Python (.py)
- JavaScript (.js) 
- TypeScript (.ts)
- C++ (.cpp)
- Java (.java)

Pipeline Steps Tested:
1. Original Language → Language Parser → Language AST
2. Language AST → Language Converter → Runa AST  
3. Runa AST → Runa Generator → Runa Source Code
4. Runa Source → Runa Parser → Runa AST (verification)
5. Runa AST → Language Converter → Language AST
6. Language AST → Language Generator → Original Language

Verification Criteria:
- Syntax preservation
- Semantic equivalence  
- AST structural integrity
- Round-trip accuracy
- Performance benchmarks
- Error handling
"""

import unittest
import time
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from textwrap import dedent
import difflib

# Add runa source to path
sys.path.insert(0, str(Path(__file__).parent / "runa" / "src"))

# Import Runa pipeline components
from runa.core.pipeline import TranslationPipeline, PipelineStage, TranslationResult
from runa.core.runa_ast import ASTNode
from runa.languages.runa.lexer import RunaLexer
from runa.languages.runa.runa_parser import RunaParser
from runa.languages.runa.runa_generator import RunaGenerator

# Import tier 1 language toolchains
from runa.languages.tier1.python.py_toolchain import PythonToolchain
from runa.languages.tier1.javascript.js_toolchain import JavaScriptToolchain
from runa.languages.tier1.typescript.ts_toolchain import TypeScriptToolchain
from runa.languages.tier1.cpp.cpp_toolchain import CppToolchain
from runa.languages.tier1.java.java_toolchain import JavaToolchain


@dataclass
class PipelineStepResult:
    """Result of a single pipeline step."""
    step_name: str
    success: bool
    execution_time_ms: float
    input_data: Any
    output_data: Any
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = asdict(self)
        # Convert non-serializable types to strings
        if hasattr(self.input_data, '__class__'):
            result['input_data'] = f"<{self.input_data.__class__.__name__}>"
        if hasattr(self.output_data, '__class__'):
            result['output_data'] = f"<{self.output_data.__class__.__name__}>"
        return result


@dataclass 
class RoundTripTestResult:
    """Complete round-trip test result for a language."""
    language: str
    original_code: str
    final_code: str
    pipeline_steps: List[PipelineStepResult]
    total_time_ms: float
    syntax_preserved: bool
    semantics_preserved: bool
    round_trip_success: bool
    similarity_score: float
    errors: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "language": self.language,
            "original_code_length": len(self.original_code),
            "final_code_length": len(self.final_code),
            "pipeline_steps": [step.to_dict() for step in self.pipeline_steps],
            "total_time_ms": self.total_time_ms,
            "syntax_preserved": self.syntax_preserved,
            "semantics_preserved": self.semantics_preserved,
            "round_trip_success": self.round_trip_success,
            "similarity_score": self.similarity_score,
            "error_count": len(self.errors),
            "errors": self.errors
        }


class PipelineStepTracker:
    """Tracks and measures each step of the translation pipeline."""
    
    def __init__(self):
        self.steps: List[PipelineStepResult] = []
        
    def track_step(self, step_name: str, input_data: Any, func, *args, **kwargs) -> PipelineStepResult:
        """Track execution of a pipeline step."""
        start_time = time.time()
        error_message = None
        output_data = None
        success = False
        
        try:
            output_data = func(*args, **kwargs)
            success = True
        except Exception as e:
            error_message = str(e)
            
        execution_time_ms = (time.time() - start_time) * 1000
        
        result = PipelineStepResult(
            step_name=step_name,
            success=success,
            execution_time_ms=execution_time_ms,
            input_data=input_data,
            output_data=output_data,
            error_message=error_message,
            metadata={"args_count": len(args), "kwargs_count": len(kwargs)}
        )
        
        self.steps.append(result)
        return result


class Tier1RoundTripTester:
    """Comprehensive round-trip tester for tier 1 languages."""
    
    def __init__(self):
        self.pipeline = TranslationPipeline()
        self.setup_toolchains()
        
        # Test code samples for each language
        self.test_samples = self._get_test_samples()
        
    def setup_toolchains(self):
        """Initialize and register all tier 1 language toolchains."""
        # Initialize toolchains
        self.python_toolchain = PythonToolchain()
        self.javascript_toolchain = JavaScriptToolchain()
        self.typescript_toolchain = TypeScriptToolchain()
        self.cpp_toolchain = CppToolchain()
        self.java_toolchain = JavaToolchain()
        
        # Register with pipeline
        self.pipeline.register_toolchain(self.python_toolchain)
        self.pipeline.register_toolchain(self.javascript_toolchain)
        self.pipeline.register_toolchain(self.typescript_toolchain)
        self.pipeline.register_toolchain(self.cpp_toolchain)
        self.pipeline.register_toolchain(self.java_toolchain)
        
        # Setup Runa toolchain
        self.runa_parser = RunaParser()
        self.runa_generator = RunaGenerator()
        self.pipeline.register_runa_toolchain(self.runa_parser, self.runa_generator)
        
    def _get_test_samples(self) -> Dict[str, List[str]]:
        """Get comprehensive test code samples for each language."""
        return {
            "python": [
                # Test 1: Basic Functions and Arithmetic
                dedent('''
                def add(x, y):
                    return x + y

                def factorial(n):
                    if n <= 1:
                        return 1
                    return n * factorial(n - 1)
                ''').strip(),
                
                # Test 2: Closures and Nested Functions
                dedent('''
                def make_multiplier(factor):
                    def multiplier(x):
                        return x * factor
                    return multiplier

                def counter():
                    count = 0
                    def increment():
                        nonlocal count
                        count += 1
                        return count
                    def get_count():
                        return count
                    def reset():
                        nonlocal count
                        count = 0
                    
                    increment.get = get_count
                    increment.reset = reset
                    return increment
                ''').strip(),
                
                # Test 3: Classes and Inheritance
                dedent('''
                class Animal:
                    def __init__(self, name):
                        self.name = name
                    
                    def speak(self):
                        return f"{self.name} makes a sound"

                class Dog(Animal):
                    def __init__(self, name, breed):
                        super().__init__(name)
                        self.breed = breed
                    
                    def speak(self):
                        return f"{self.name} barks"
                    
                    def fetch(self):
                        return f"{self.name} fetches the ball"

                class Cat(Animal):
                    def speak(self):
                        return f"{self.name} meows"
                ''').strip(),
                
                # Test 4: Multiple Inheritance
                dedent('''
                class Animal:
                    def __init__(self, name):
                        self.name = name
                    
                    def speak(self):
                        return f"{self.name} makes a sound"

                class Flyable:
                    def fly(self):
                        return "Flying high"

                class Swimmable:
                    def swim(self):
                        return "Swimming deep"

                class Duck(Animal, Flyable, Swimmable):
                    def speak(self):
                        return f"{self.name} quacks"
                ''').strip(),
                
                # Test 5: Properties and Setters
                dedent('''
                class Temperature:
                    def __init__(self, celsius=0):
                        self._celsius = celsius
                    
                    @property
                    def celsius(self):
                        return self._celsius
                    
                    @celsius.setter
                    def celsius(self, value):
                        if value < -273.15:
                            raise ValueError("Below absolute zero")
                        self._celsius = value
                    
                    @property
                    def fahrenheit(self):
                        return self._celsius * 9/5 + 32
                    
                    @fahrenheit.setter
                    def fahrenheit(self, value):
                        self.celsius = (value - 32) * 5/9
                ''').strip(),
                
                # Test 6: Operator Overloading
                dedent('''
                class Vector:
                    def __init__(self, x, y, z=0):
                        self.x = x
                        self.y = y
                        self.z = z
                    
                    def __add__(self, other):
                        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
                    
                    def __sub__(self, other):
                        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
                    
                    def __mul__(self, scalar):
                        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
                    
                    def __eq__(self, other):
                        return self.x == other.x and self.y == other.y and self.z == other.z
                    
                    def __str__(self):
                        return f"Vector({self.x}, {self.y}, {self.z})"
                    
                    def __repr__(self):
                        return f"Vector({self.x}, {self.y}, {self.z})"
                    
                    def __len__(self):
                        return 3
                    
                    def __getitem__(self, index):
                        return [self.x, self.y, self.z][index]
                ''').strip(),
                
                # Test 7: Generators and Iterators
                dedent('''
                def fibonacci():
                    a, b = 0, 1
                    while True:
                        yield a
                        a, b = b, a + b

                def take(n, iterator):
                    result = []
                    for i, value in enumerate(iterator):
                        if i >= n:
                            break
                        result.append(value)
                    return result

                class Range:
                    def __init__(self, start, stop=None, step=1):
                        if stop is None:
                            self.start = 0
                            self.stop = start
                        else:
                            self.start = start
                            self.stop = stop
                        self.step = step
                    
                    def __iter__(self):
                        current = self.start
                        while current < self.stop:
                            yield current
                            current += self.step
                ''').strip(),
                
                # Test 8: List/Dict/Set Comprehensions
                dedent('''
                def comprehension_tests(data):
                    # List comprehensions
                    squares = [x**2 for x in range(10)]
                    even_squares = [x**2 for x in range(10) if x % 2 == 0]
                    matrix = [[i*j for j in range(5)] for i in range(5)]
                    
                    # Dict comprehensions
                    square_dict = {x: x**2 for x in range(5)}
                    filtered_dict = {k: v for k, v in data.items() if v > 0}
                    
                    # Set comprehensions
                    unique_squares = {x**2 for x in [-2, -1, 0, 1, 2]}
                    
                    # Nested comprehensions
                    flattened = [item for sublist in matrix for item in sublist]
                    
                    return squares, even_squares, matrix, square_dict, filtered_dict, unique_squares, flattened
                ''').strip(),
                
                # Test 9: Exception Handling
                dedent('''
                class CustomError(Exception):
                    def __init__(self, message, code):
                        super().__init__(message)
                        self.message = message
                        self.code = code

                def divide_with_handling(a, b):
                    try:
                        result = a / b
                    except ZeroDivisionError:
                        raise CustomError("Cannot divide by zero", 400)
                    except TypeError as e:
                        raise CustomError(f"Type error: {str(e)}", 500) from e
                    else:
                        return result
                    finally:
                        print("Division attempted")

                def multiple_exception_handling(value):
                    try:
                        if isinstance(value, str):
                            return int(value)
                        elif isinstance(value, (int, float)):
                            return 1 / value
                        else:
                            raise TypeError("Unsupported type")
                    except ValueError:
                        return 0
                    except ZeroDivisionError:
                        return float('inf')
                    except Exception as e:
                        print(f"Unexpected error: {e}")
                        raise
                ''').strip(),
                
                # Test 10: Decorators
                dedent('''
                def memoize(func):
                    cache = {}
                    def wrapper(*args):
                        if args not in cache:
                            cache[args] = func(*args)
                        return cache[args]
                    return wrapper

                def repeat(times):
                    def decorator(func):
                        def wrapper(*args, **kwargs):
                            results = []
                            for _ in range(times):
                                results.append(func(*args, **kwargs))
                            return results
                        return wrapper
                    return decorator

                @memoize
                def expensive_fibonacci(n):
                    if n < 2:
                        return n
                    return expensive_fibonacci(n-1) + expensive_fibonacci(n-2)

                @repeat(3)
                def greet(name):
                    return f"Hello, {name}!"
                ''').strip(),
                
                # Test 11: Context Managers
                dedent('''
                class FileManager:
                    def __init__(self, filename, mode):
                        self.filename = filename
                        self.mode = mode
                        self.file = None
                    
                    def __enter__(self):
                        print(f"Opening {self.filename}")
                        self.file = f"MockFile({self.filename}, {self.mode})"
                        return self.file
                    
                    def __exit__(self, exc_type, exc_val, exc_tb):
                        print(f"Closing {self.filename}")
                        if exc_type is not None:
                            print(f"Exception occurred: {exc_val}")
                        return False
                ''').strip(),
                
                # Test 12: Static vs Instance vs Class Methods
                dedent('''
                class MethodTypes:
                    class_var = 100
                    
                    def __init__(self, value):
                        self.instance_var = value
                    
                    def instance_method(self):
                        return f"Instance: {self.instance_var}"
                    
                    @classmethod
                    def class_method(cls):
                        return f"Class: {cls.class_var}"
                    
                    @staticmethod
                    def static_method(x, y):
                        return x + y
                ''').strip(),
                
                # Test 13: String Operations and Formatting
                dedent('''
                def string_operations():
                    name = "Alice"
                    age = 30
                    
                    # Different string formatting methods
                    concat = "Hello, " + name + "!"
                    percent = "Hello, %s! You are %d years old." % (name, age)
                    format_method = "Hello, {}! You are {} years old.".format(name, age)
                    f_string = f"Hello, {name}! You are {age} years old."
                    
                    # String methods
                    upper = name.upper()
                    lower = name.lower()
                    replaced = name.replace('A', 'E')
                    
                    # Multiline strings
                    multiline = "This is\\na multiline\\nstring"
                    
                    # Raw strings
                    raw = r"This has \\n no newlines"
                    
                    return concat, percent, format_method, f_string, upper, lower, replaced, multiline, raw
                ''').strip(),
                
                # Test 14: Complex Control Flow
                dedent('''
                def complex_control_flow(items):
                    results = []
                    
                    for i, item in enumerate(items):
                        if item is None:
                            continue
                        elif isinstance(item, int):
                            if item < 0:
                                results.append(('negative', item))
                            elif item == 0:
                                results.append(('zero', item))
                            else:
                                # Check if prime
                                is_prime = True
                                if item > 1:
                                    for j in range(2, int(item ** 0.5) + 1):
                                        if item % j == 0:
                                            is_prime = False
                                            break
                                
                                if is_prime and item > 1:
                                    results.append(('prime', item))
                                else:
                                    results.append(('composite', item))
                        elif isinstance(item, str):
                            if item.isdigit():
                                results.append(('numeric_string', item))
                            else:
                                results.append(('string', item))
                        else:
                            results.append(('other', item))
                    
                    return results
                ''').strip(),
                
                # Test 15: Variable Scope and Assignment
                dedent('''
                def scope_test():
                    global_var = 100
                    
                    def outer():
                        outer_var = 200
                        
                        def inner():
                            nonlocal outer_var
                            global global_var
                            
                            inner_var = 300
                            outer_var += 10
                            global_var += 1
                            
                            return inner_var + outer_var + global_var
                        
                        return inner()
                    
                    return outer()
                ''').strip(),
            ],
            
            "javascript": [
                # Test 1: Basic Functions and Arithmetic
                '''
                function add(x, y) {
                    return x + y;
                }

                function factorial(n) {
                    if (n <= 1) {
                        return 1;
                    }
                    return n * factorial(n - 1);
                }
                '''.strip(),
                
                # Test 2: Closures and Higher-Order Functions
                '''
                function makeMultiplier(factor) {
                    return function(x) {
                        return x * factor;
                    };
                }

                function createCounter() {
                    let count = 0;
                    
                    function increment() {
                        count++;
                        return count;
                    }
                    
                    increment.get = function() {
                        return count;
                    };
                    
                    increment.reset = function() {
                        count = 0;
                    };
                    
                    return increment;
                }
                '''.strip(),
                
                # Test 3: Classes and Inheritance (ES6)
                '''
                class Animal {
                    constructor(name) {
                        this.name = name;
                    }
                    
                    speak() {
                        return `${this.name} makes a sound`;
                    }
                }

                class Dog extends Animal {
                    constructor(name, breed) {
                        super(name);
                        this.breed = breed;
                    }
                    
                    speak() {
                        return `${this.name} barks`;
                    }
                    
                    fetch() {
                        return `${this.name} fetches the ball`;
                    }
                }

                class Cat extends Animal {
                    speak() {
                        return `${this.name} meows`;
                    }
                }
                '''.strip(),
                
                # Test 4: Mixins (JavaScript style)
                '''
                class Animal {
                    constructor(name) {
                        this.name = name;
                    }
                    
                    speak() {
                        return `${this.name} makes a sound`;
                    }
                }

                const Flyable = {
                    fly() {
                        return "Flying high";
                    }
                };

                const Swimmable = {
                    swim() {
                        return "Swimming deep";
                    }
                };

                class Duck extends Animal {
                    speak() {
                        return `${this.name} quacks`;
                    }
                }

                Object.assign(Duck.prototype, Flyable, Swimmable);
                '''.strip(),
                
                # Test 5: Getters and Setters
                '''
                class Temperature {
                    constructor(celsius = 0) {
                        this._celsius = celsius;
                    }
                    
                    get celsius() {
                        return this._celsius;
                    }
                    
                    set celsius(value) {
                        if (value < -273.15) {
                            throw new Error("Below absolute zero");
                        }
                        this._celsius = value;
                    }
                    
                    get fahrenheit() {
                        return this._celsius * 9/5 + 32;
                    }
                    
                    set fahrenheit(value) {
                        this.celsius = (value - 32) * 5/9;
                    }
                }
                '''.strip(),
                
                # Test 6: Operator Overloading (Symbol approach)
                '''
                class Vector {
                    constructor(x, y, z = 0) {
                        this.x = x;
                        this.y = y;
                        this.z = z;
                    }
                    
                    add(other) {
                        return new Vector(this.x + other.x, this.y + other.y, this.z + other.z);
                    }
                    
                    subtract(other) {
                        return new Vector(this.x - other.x, this.y - other.y, this.z - other.z);
                    }
                    
                    multiply(scalar) {
                        return new Vector(this.x * scalar, this.y * scalar, this.z * scalar);
                    }
                    
                    equals(other) {
                        return this.x === other.x && this.y === other.y && this.z === other.z;
                    }
                    
                    toString() {
                        return `Vector(${this.x}, ${this.y}, ${this.z})`;
                    }
                    
                    get length() {
                        return 3;
                    }
                    
                    get(index) {
                        return [this.x, this.y, this.z][index];
                    }
                }
                '''.strip(),
                
                # Test 7: Generators and Iterators
                '''
                function* fibonacci() {
                    let a = 0, b = 1;
                    while (true) {
                        yield a;
                        [a, b] = [b, a + b];
                    }
                }

                function take(n, iterator) {
                    const result = [];
                    let count = 0;
                    for (const value of iterator) {
                        if (count >= n) break;
                        result.push(value);
                        count++;
                    }
                    return result;
                }

                class Range {
                    constructor(start, stop = null, step = 1) {
                        if (stop === null) {
                            this.start = 0;
                            this.stop = start;
                        } else {
                            this.start = start;
                            this.stop = stop;
                        }
                        this.step = step;
                    }
                    
                    *[Symbol.iterator]() {
                        let current = this.start;
                        while (current < this.stop) {
                            yield current;
                            current += this.step;
                        }
                    }
                }
                '''.strip(),
                
                # Test 8: Array/Object Methods and Transformations
                '''
                function comprehensionTests(data) {
                    // Array transformations
                    const squares = Array.from({length: 10}, (_, i) => i ** 2);
                    const evenSquares = Array.from({length: 10}, (_, i) => i)
                        .filter(x => x % 2 === 0)
                        .map(x => x ** 2);
                    const matrix = Array.from({length: 5}, (_, i) => 
                        Array.from({length: 5}, (_, j) => i * j));
                    
                    // Object transformations
                    const squareObj = Object.fromEntries(
                        Array.from({length: 5}, (_, i) => [i, i ** 2]));
                    const filteredObj = Object.fromEntries(
                        Object.entries(data).filter(([k, v]) => v > 0));
                    
                    // Set transformations
                    const uniqueSquares = new Set([-2, -1, 0, 1, 2].map(x => x ** 2));
                    
                    // Flattening
                    const flattened = matrix.flat();
                    
                    return { squares, evenSquares, matrix, squareObj, filteredObj, uniqueSquares, flattened };
                }
                '''.strip(),
                
                # Test 9: Error Handling
                '''
                class CustomError extends Error {
                    constructor(message, code) {
                        super(message);
                        this.name = 'CustomError';
                        this.message = message;
                        this.code = code;
                    }
                }

                function divideWithHandling(a, b) {
                    try {
                        if (b === 0) {
                            throw new CustomError("Cannot divide by zero", 400);
                        }
                        if (typeof a !== 'number' || typeof b !== 'number') {
                            throw new CustomError(`Type error: Expected numbers`, 500);
                        }
                        return a / b;
                    } finally {
                        console.log("Division attempted");
                    }
                }

                function multipleExceptionHandling(value) {
                    try {
                        if (typeof value === 'string') {
                            const parsed = parseInt(value);
                            if (isNaN(parsed)) throw new Error("Invalid number");
                            return parsed;
                        } else if (typeof value === 'number') {
                            if (value === 0) return Infinity;
                            return 1 / value;
                        } else {
                            throw new TypeError("Unsupported type");
                        }
                    } catch (error) {
                        if (error instanceof TypeError) {
                            console.log(`Type error: ${error.message}`);
                            throw error;
                        } else {
                            return 0;
                        }
                    }
                }
                '''.strip(),
                
                # Test 10: Higher-Order Functions and Decorators (JavaScript style)
                '''
                function memoize(func) {
                    const cache = new Map();
                    return function(...args) {
                        const key = JSON.stringify(args);
                        if (!cache.has(key)) {
                            cache.set(key, func.apply(this, args));
                        }
                        return cache.get(key);
                    };
                }

                function repeat(times) {
                    return function(func) {
                        return function(...args) {
                            const results = [];
                            for (let i = 0; i < times; i++) {
                                results.push(func.apply(this, args));
                            }
                            return results;
                        };
                    };
                }

                const expensiveFibonacci = memoize(function(n) {
                    if (n < 2) return n;
                    return expensiveFibonacci(n - 1) + expensiveFibonacci(n - 2);
                });

                const greet = repeat(3)(function(name) {
                    return `Hello, ${name}!`;
                });
                '''.strip(),
                
                # Test 11: Resource Management Pattern
                '''
                class ResourceManager {
                    constructor(resource, cleanup) {
                        this.resource = resource;
                        this.cleanup = cleanup;
                        this.disposed = false;
                    }
                    
                    use(callback) {
                        try {
                            console.log(`Acquiring resource: ${this.resource}`);
                            return callback(this.resource);
                        } finally {
                            this.dispose();
                        }
                    }
                    
                    dispose() {
                        if (!this.disposed) {
                            console.log(`Disposing resource: ${this.resource}`);
                            if (this.cleanup) this.cleanup();
                            this.disposed = true;
                        }
                    }
                }
                '''.strip(),
                
                # Test 12: Static vs Instance Methods
                '''
                class MethodTypes {
                    static classVar = 100;
                    
                    constructor(value) {
                        this.instanceVar = value;
                    }
                    
                    instanceMethod() {
                        return `Instance: ${this.instanceVar}`;
                    }
                    
                    static classMethod() {
                        return `Class: ${MethodTypes.classVar}`;
                    }
                    
                    static staticMethod(x, y) {
                        return x + y;
                    }
                }
                '''.strip(),
                
                # Test 13: String Operations and Template Literals
                '''
                function stringOperations() {
                    const name = "Alice";
                    const age = 30;
                    
                    // Different string creation methods
                    const concat = "Hello, " + name + "!";
                    const template = `Hello, ${name}! You are ${age} years old.`;
                    
                    // String methods
                    const upper = name.toUpperCase();
                    const lower = name.toLowerCase();
                    const replaced = name.replace('A', 'E');
                    
                    // Multiline strings
                    const multiline = `This is
a multiline
string`;
                    
                    // Tagged template literals
                    function tag(strings, ...values) {
                        return strings.reduce((result, string, i) => 
                            result + string + (values[i] || ''), '');
                    }
                    
                    const tagged = tag`Hello, ${name}! Age: ${age}`;
                    
                    return { concat, template, upper, lower, replaced, multiline, tagged };
                }
                '''.strip(),
                
                # Test 14: Complex Control Flow
                '''
                function complexControlFlow(items) {
                    const results = [];
                    
                    for (let i = 0; i < items.length; i++) {
                        const item = items[i];
                        
                        if (item === null || item === undefined) {
                            continue;
                        } else if (typeof item === 'number') {
                            if (item < 0) {
                                results.push(['negative', item]);
                            } else if (item === 0) {
                                results.push(['zero', item]);
                            } else {
                                // Check if prime
                                let isPrime = true;
                                if (item > 1) {
                                    for (let j = 2; j <= Math.sqrt(item); j++) {
                                        if (item % j === 0) {
                                            isPrime = false;
                                            break;
                                        }
                                    }
                                }
                                
                                if (isPrime && item > 1) {
                                    results.push(['prime', item]);
                                } else {
                                    results.push(['composite', item]);
                                }
                            }
                        } else if (typeof item === 'string') {
                            if (/^\\d+$/.test(item)) {
                                results.push(['numeric_string', item]);
                            } else {
                                results.push(['string', item]);
                            }
                        } else {
                            results.push(['other', item]);
                        }
                    }
                    
                    return results;
                }
                '''.strip(),
                
                # Test 15: Scope and Closures
                '''
                function scopeTest() {
                    let globalVar = 100;
                    
                    function outer() {
                        let outerVar = 200;
                        
                        function inner() {
                            let innerVar = 300;
                            outerVar += 10;
                            globalVar += 1;
                            
                            return innerVar + outerVar + globalVar;
                        }
                        
                        return inner();
                    }
                    
                    return outer();
                }
                '''.strip(),
            ],
            
            "typescript": [
                # Test 1: Basic Functions and Arithmetic with Types
                '''
                function add(x: number, y: number): number {
                    return x + y;
                }

                function factorial(n: number): number {
                    if (n <= 1) {
                        return 1;
                    }
                    return n * factorial(n - 1);
                }
                '''.strip(),
                
                # Test 2: Closures and Higher-Order Functions with Types
                '''
                function makeMultiplier(factor: number): (x: number) => number {
                    return function(x: number): number {
                        return x * factor;
                    };
                }

                interface Counter {
                    (): number;
                    get(): number;
                    reset(): void;
                }

                function createCounter(): Counter {
                    let count: number = 0;
                    
                    function increment(): number {
                        count++;
                        return count;
                    }
                    
                    increment.get = function(): number {
                        return count;
                    };
                    
                    increment.reset = function(): void {
                        count = 0;
                    };
                    
                    return increment as Counter;
                }
                '''.strip(),
                
                # Test 3: Classes and Inheritance with TypeScript
                '''
                abstract class Animal {
                    protected name: string;
                    
                    constructor(name: string) {
                        this.name = name;
                    }
                    
                    abstract speak(): string;
                    
                    getName(): string {
                        return this.name;
                    }
                }

                class Dog extends Animal {
                    private breed: string;
                    
                    constructor(name: string, breed: string) {
                        super(name);
                        this.breed = breed;
                    }
                    
                    speak(): string {
                        return `${this.name} barks`;
                    }
                    
                    fetch(): string {
                        return `${this.name} fetches the ball`;
                    }
                    
                    getBreed(): string {
                        return this.breed;
                    }
                }

                class Cat extends Animal {
                    speak(): string {
                        return `${this.name} meows`;
                    }
                }
                '''.strip(),
                
                # Test 4: Interfaces and Multiple Inheritance
                '''
                interface Animal {
                    name: string;
                    speak(): string;
                }

                interface Flyable {
                    fly(): string;
                }

                interface Swimmable {
                    swim(): string;
                }

                class Duck implements Animal, Flyable, Swimmable {
                    name: string;
                    
                    constructor(name: string) {
                        this.name = name;
                    }
                    
                    speak(): string {
                        return `${this.name} quacks`;
                    }
                    
                    fly(): string {
                        return "Flying high";
                    }
                    
                    swim(): string {
                        return "Swimming deep";
                    }
                }
                '''.strip(),
                
                # Test 5: Getters, Setters, and Property Decorators
                '''
                class Temperature {
                    private _celsius: number;
                    
                    constructor(celsius: number = 0) {
                        this._celsius = celsius;
                    }
                    
                    get celsius(): number {
                        return this._celsius;
                    }
                    
                    set celsius(value: number) {
                        if (value < -273.15) {
                            throw new Error("Below absolute zero");
                        }
                        this._celsius = value;
                    }
                    
                    get fahrenheit(): number {
                        return this._celsius * 9/5 + 32;
                    }
                    
                    set fahrenheit(value: number) {
                        this.celsius = (value - 32) * 5/9;
                    }
                }
                '''.strip(),
                
                # Test 6: Operator Overloading with TypeScript Methods
                '''
                class Vector {
                    constructor(
                        public readonly x: number,
                        public readonly y: number,
                        public readonly z: number = 0
                    ) {}
                    
                    add(other: Vector): Vector {
                        return new Vector(this.x + other.x, this.y + other.y, this.z + other.z);
                    }
                    
                    subtract(other: Vector): Vector {
                        return new Vector(this.x - other.x, this.y - other.y, this.z - other.z);
                    }
                    
                    multiply(scalar: number): Vector {
                        return new Vector(this.x * scalar, this.y * scalar, this.z * scalar);
                    }
                    
                    equals(other: Vector): boolean {
                        return this.x === other.x && this.y === other.y && this.z === other.z;
                    }
                    
                    toString(): string {
                        return `Vector(${this.x}, ${this.y}, ${this.z})`;
                    }
                    
                    get length(): number {
                        return 3;
                    }
                    
                    get(index: number): number {
                        return [this.x, this.y, this.z][index];
                    }
                }
                '''.strip(),
                
                # Test 7: Generators and Iterators with Types
                '''
                function* fibonacci(): Generator<number, never, unknown> {
                    let a: number = 0, b: number = 1;
                    while (true) {
                        yield a;
                        [a, b] = [b, a + b];
                    }
                }

                function take<T>(n: number, iterator: Iterable<T>): T[] {
                    const result: T[] = [];
                    let count: number = 0;
                    for (const value of iterator) {
                        if (count >= n) break;
                        result.push(value);
                        count++;
                    }
                    return result;
                }

                class Range implements Iterable<number> {
                    private start: number;
                    private stop: number;
                    private step: number;
                    
                    constructor(start: number, stop?: number, step: number = 1) {
                        if (stop === undefined) {
                            this.start = 0;
                            this.stop = start;
                        } else {
                            this.start = start;
                            this.stop = stop;
                        }
                        this.step = step;
                    }
                    
                    *[Symbol.iterator](): Iterator<number> {
                        let current: number = this.start;
                        while (current < this.stop) {
                            yield current;
                            current += this.step;
                        }
                    }
                }
                '''.strip(),
                
                # Test 8: Advanced Types and Transformations
                '''
                interface ComprehensionResult {
                    squares: number[];
                    evenSquares: number[];
                    matrix: number[][];
                    squareObj: Record<string, number>;
                    filteredObj: Record<string, number>;
                    uniqueSquares: Set<number>;
                    flattened: number[];
                }

                function comprehensionTests(data: Record<string, number>): ComprehensionResult {
                    // Array transformations with proper typing
                    const squares: number[] = Array.from({length: 10}, (_, i) => i ** 2);
                    const evenSquares: number[] = Array.from({length: 10}, (_, i) => i)
                        .filter((x: number) => x % 2 === 0)
                        .map((x: number) => x ** 2);
                    const matrix: number[][] = Array.from({length: 5}, (_, i) => 
                        Array.from({length: 5}, (_, j) => i * j));
                    
                    // Object transformations with mapped types
                    const squareObj: Record<string, number> = Object.fromEntries(
                        Array.from({length: 5}, (_, i) => [i.toString(), i ** 2]));
                    const filteredObj: Record<string, number> = Object.fromEntries(
                        Object.entries(data).filter(([k, v]) => v > 0));
                    
                    // Set transformations
                    const uniqueSquares: Set<number> = new Set([-2, -1, 0, 1, 2].map(x => x ** 2));
                    
                    // Flattening with proper types
                    const flattened: number[] = matrix.flat();
                    
                    return { squares, evenSquares, matrix, squareObj, filteredObj, uniqueSquares, flattened };
                }
                '''.strip(),
                
                # Test 9: Error Handling with Custom Types
                '''
                class CustomError extends Error {
                    public readonly code: number;
                    
                    constructor(message: string, code: number) {
                        super(message);
                        this.name = 'CustomError';
                        this.code = code;
                    }
                }

                function divideWithHandling(a: number, b: number): number {
                    try {
                        if (b === 0) {
                            throw new CustomError("Cannot divide by zero", 400);
                        }
                        return a / b;
                    } finally {
                        console.log("Division attempted");
                    }
                }

                type ProcessableValue = string | number;

                function multipleExceptionHandling(value: ProcessableValue): number {
                    try {
                        if (typeof value === 'string') {
                            const parsed: number = parseInt(value);
                            if (isNaN(parsed)) throw new Error("Invalid number");
                            return parsed;
                        } else if (typeof value === 'number') {
                            if (value === 0) return Infinity;
                            return 1 / value;
                        } else {
                            // This should never happen with proper typing
                            const _exhaustive: never = value;
                            throw new TypeError("Unsupported type");
                        }
                    } catch (error) {
                        if (error instanceof TypeError) {
                            console.log(`Type error: ${error.message}`);
                            throw error;
                        } else {
                            return 0;
                        }
                    }
                }
                '''.strip(),
                
                # Test 10: Generic Functions and Decorators
                '''
                type Memoized<T extends (...args: any[]) => any> = T & { cache: Map<string, ReturnType<T>> };

                function memoize<T extends (...args: any[]) => any>(func: T): Memoized<T> {
                    const cache = new Map<string, ReturnType<T>>();
                    const memoized = function(...args: Parameters<T>): ReturnType<T> {
                        const key: string = JSON.stringify(args);
                        if (!cache.has(key)) {
                            cache.set(key, func.apply(this, args));
                        }
                        return cache.get(key)!;
                    } as Memoized<T>;
                    
                    memoized.cache = cache;
                    return memoized;
                }

                function repeat<T extends (...args: any[]) => any>(times: number): (func: T) => (...args: Parameters<T>) => ReturnType<T>[] {
                    return function<U extends T>(func: U): (...args: Parameters<U>) => ReturnType<U>[] {
                        return function(...args: Parameters<U>): ReturnType<U>[] {
                            const results: ReturnType<U>[] = [];
                            for (let i = 0; i < times; i++) {
                                results.push(func.apply(this, args));
                            }
                            return results;
                        };
                    };
                }

                const expensiveFibonacci: Memoized<(n: number) => number> = memoize(function(n: number): number {
                    if (n < 2) return n;
                    return expensiveFibonacci(n - 1) + expensiveFibonacci(n - 2);
                });

                const greet: (...args: [string]) => string[] = repeat(3)(function(name: string): string {
                    return `Hello, ${name}!`;
                });
                '''.strip(),
                
                # Test 11: Advanced Class Features and Decorators
                '''
                interface Disposable {
                    dispose(): void;
                }

                class ResourceManager implements Disposable {
                    private resource: string;
                    private cleanup?: () => void;
                    private disposed: boolean = false;
                    
                    constructor(resource: string, cleanup?: () => void) {
                        this.resource = resource;
                        this.cleanup = cleanup;
                    }
                    
                    use<T>(callback: (resource: string) => T): T {
                        try {
                            console.log(`Acquiring resource: ${this.resource}`);
                            return callback(this.resource);
                        } finally {
                            this.dispose();
                        }
                    }
                    
                    dispose(): void {
                        if (!this.disposed) {
                            console.log(`Disposing resource: ${this.resource}`);
                            if (this.cleanup) this.cleanup();
                            this.disposed = true;
                        }
                    }
                }
                '''.strip(),
                
                # Test 12: Static vs Instance Methods with TypeScript
                '''
                class MethodTypes {
                    static readonly classVar: number = 100;
                    private instanceVar: number;
                    
                    constructor(value: number) {
                        this.instanceVar = value;
                    }
                    
                    instanceMethod(): string {
                        return `Instance: ${this.instanceVar}`;
                    }
                    
                    static classMethod(): string {
                        return `Class: ${MethodTypes.classVar}`;
                    }
                    
                    static staticMethod(x: number, y: number): number {
                        return x + y;
                    }
                }
                '''.strip(),
                
                # Test 13: Template Literals and String Types
                '''
                type Greeting = `Hello, ${string}!`;
                type AgeMessage<T extends number> = `You are ${T} years old.`;

                interface StringOperationsResult {
                    concat: string;
                    template: Greeting;
                    upper: string;
                    lower: string;
                    replaced: string;
                    multiline: string;
                    tagged: string;
                }

                function stringOperations(): StringOperationsResult {
                    const name: string = "Alice";
                    const age: number = 30;
                    
                    // Different string creation methods
                    const concat: string = "Hello, " + name + "!";
                    const template: Greeting = `Hello, ${name}!` as Greeting;
                    
                    // String methods
                    const upper: string = name.toUpperCase();
                    const lower: string = name.toLowerCase();
                    const replaced: string = name.replace('A', 'E');
                    
                    // Multiline strings
                    const multiline: string = `This is
a multiline
string`;
                    
                    // Tagged template literals
                    function tag(strings: TemplateStringsArray, ...values: any[]): string {
                        return strings.reduce((result, string, i) => 
                            result + string + (values[i] || ''), '');
                    }
                    
                    const tagged: string = tag`Hello, ${name}! Age: ${age}`;
                    
                    return { concat, template, upper, lower, replaced, multiline, tagged };
                }
                '''.strip(),
                
                # Test 14: Union Types and Control Flow
                '''
                type ItemType = 'negative' | 'zero' | 'prime' | 'composite' | 'numeric_string' | 'string' | 'other';
                type ProcessableItem = number | string | null | undefined;
                type Result = [ItemType, ProcessableItem];

                function complexControlFlow(items: ProcessableItem[]): Result[] {
                    const results: Result[] = [];
                    
                    for (let i = 0; i < items.length; i++) {
                        const item: ProcessableItem = items[i];
                        
                        if (item === null || item === undefined) {
                            continue;
                        } else if (typeof item === 'number') {
                            if (item < 0) {
                                results.push(['negative', item]);
                            } else if (item === 0) {
                                results.push(['zero', item]);
                            } else {
                                // Check if prime
                                let isPrime: boolean = true;
                                if (item > 1) {
                                    for (let j = 2; j <= Math.sqrt(item); j++) {
                                        if (item % j === 0) {
                                            isPrime = false;
                                            break;
                                        }
                                    }
                                }
                                
                                if (isPrime && item > 1) {
                                    results.push(['prime', item]);
                                } else {
                                    results.push(['composite', item]);
                                }
                            }
                        } else if (typeof item === 'string') {
                            if (/^\\d+$/.test(item)) {
                                results.push(['numeric_string', item]);
                            } else {
                                results.push(['string', item]);
                            }
                        } else {
                            // TypeScript ensures this is never reached with proper typing
                            const _exhaustive: never = item;
                            results.push(['other', item]);
                        }
                    }
                    
                    return results;
                }
                '''.strip(),
                
                # Test 15: Advanced Scoping with TypeScript
                '''
                function scopeTest(): number {
                    let globalVar: number = 100;
                    
                    function outer(): number {
                        let outerVar: number = 200;
                        
                        function inner(): number {
                            let innerVar: number = 300;
                            outerVar += 10;
                            globalVar += 1;
                            
                            return innerVar + outerVar + globalVar;
                        }
                        
                        return inner();
                    }
                    
                    return outer();
                }
                '''.strip(),
            ],
            
            "cpp": [
                # Test 1: Basic Functions and Arithmetic
                '''
                #include <iostream>
                
                int add(int x, int y) {
                    return x + y;
                }
                
                long long factorial(int n) {
                    if (n <= 1) {
                        return 1;
                    }
                    return n * factorial(n - 1);
                }
                '''.strip(),
                
                # Test 2: Function Objects and Closures (C++ style)
                '''
                #include <functional>
                #include <iostream>
                
                std::function<int(int)> makeMultiplier(int factor) {
                    return [factor](int x) {
                        return x * factor;
                    };
                }
                
                class Counter {
                private:
                    int count = 0;
                    
                public:
                    int operator()() {
                        return ++count;
                    }
                    
                    int get() const {
                        return count;
                    }
                    
                    void reset() {
                        count = 0;
                    }
                };
                '''.strip(),
                
                # Test 3: Classes and Inheritance
                '''
                #include <string>
                #include <memory>
                
                class Animal {
                protected:
                    std::string name;
                    
                public:
                    Animal(const std::string& name) : name(name) {}
                    virtual ~Animal() = default;
                    virtual std::string speak() const = 0;
                    
                    const std::string& getName() const {
                        return name;
                    }
                };
                
                class Dog : public Animal {
                private:
                    std::string breed;
                    
                public:
                    Dog(const std::string& name, const std::string& breed) 
                        : Animal(name), breed(breed) {}
                    
                    std::string speak() const override {
                        return name + " barks";
                    }
                    
                    std::string fetch() const {
                        return name + " fetches the ball";
                    }
                    
                    const std::string& getBreed() const {
                        return breed;
                    }
                };
                
                class Cat : public Animal {
                public:
                    Cat(const std::string& name) : Animal(name) {}
                    
                    std::string speak() const override {
                        return name + " meows";
                    }
                };
                '''.strip(),
                
                # Test 4: Multiple Inheritance and Mixins
                '''
                #include <string>
                
                class Animal {
                protected:
                    std::string name;
                    
                public:
                    Animal(const std::string& name) : name(name) {}
                    virtual ~Animal() = default;
                    virtual std::string speak() const = 0;
                };
                
                class Flyable {
                public:
                    virtual ~Flyable() = default;
                    virtual std::string fly() const {
                        return "Flying high";
                    }
                };
                
                class Swimmable {
                public:
                    virtual ~Swimmable() = default;
                    virtual std::string swim() const {
                        return "Swimming deep";
                    }
                };
                
                class Duck : public Animal, public Flyable, public Swimmable {
                public:
                    Duck(const std::string& name) : Animal(name) {}
                    
                    std::string speak() const override {
                        return name + " quacks";
                    }
                };
                '''.strip(),
                
                # Test 5: Properties (C++ style with getters/setters)
                '''
                #include <stdexcept>
                
                class Temperature {
                private:
                    double _celsius;
                    
                public:
                    Temperature(double celsius = 0.0) : _celsius(celsius) {}
                    
                    double getCelsius() const {
                        return _celsius;
                    }
                    
                    void setCelsius(double value) {
                        if (value < -273.15) {
                            throw std::invalid_argument("Below absolute zero");
                        }
                        _celsius = value;
                    }
                    
                    double getFahrenheit() const {
                        return _celsius * 9.0/5.0 + 32.0;
                    }
                    
                    void setFahrenheit(double value) {
                        setCelsius((value - 32.0) * 5.0/9.0);
                    }
                    
                    // Property-like access using overloaded operators
                    Temperature& operator=(double celsius) {
                        setCelsius(celsius);
                        return *this;
                    }
                    
                    operator double() const {
                        return getCelsius();
                    }
                };
                '''.strip(),
                
                # Test 6: Operator Overloading
                '''
                #include <iostream>
                #include <array>
                
                class Vector {
                private:
                    double x, y, z;
                    
                public:
                    Vector(double x = 0, double y = 0, double z = 0) : x(x), y(y), z(z) {}
                    
                    Vector operator+(const Vector& other) const {
                        return Vector(x + other.x, y + other.y, z + other.z);
                    }
                    
                    Vector operator-(const Vector& other) const {
                        return Vector(x - other.x, y - other.y, z - other.z);
                    }
                    
                    Vector operator*(double scalar) const {
                        return Vector(x * scalar, y * scalar, z * scalar);
                    }
                    
                    bool operator==(const Vector& other) const {
                        return x == other.x && y == other.y && z == other.z;
                    }
                    
                    friend std::ostream& operator<<(std::ostream& os, const Vector& v) {
                        os << "Vector(" << v.x << ", " << v.y << ", " << v.z << ")";
                        return os;
                    }
                    
                    size_t size() const {
                        return 3;
                    }
                    
                    double operator[](size_t index) const {
                        switch(index) {
                            case 0: return x;
                            case 1: return y;
                            case 2: return z;
                            default: throw std::out_of_range("Vector index out of range");
                        }
                    }
                    
                    double& operator[](size_t index) {
                        switch(index) {
                            case 0: return x;
                            case 1: return y;
                            case 2: return z;
                            default: throw std::out_of_range("Vector index out of range");
                        }
                    }
                };
                '''.strip(),
                
                # Test 7: Iterators and Generators (C++ style)
                '''
                #include <vector>
                #include <iterator>
                #include <algorithm>
                
                class FibonacciGenerator {
                private:
                    mutable long long a = 0, b = 1;
                    
                public:
                    class iterator {
                    private:
                        FibonacciGenerator* gen;
                        long long current;
                        size_t position;
                        
                    public:
                        using iterator_category = std::input_iterator_tag;
                        using value_type = long long;
                        using difference_type = std::ptrdiff_t;
                        using pointer = const long long*;
                        using reference = const long long&;
                        
                        iterator(FibonacciGenerator* g, size_t pos) : gen(g), position(pos) {
                            if (pos == 0) {
                                current = g->next();
                            }
                        }
                        
                        iterator& operator++() {
                            current = gen->next();
                            ++position;
                            return *this;
                        }
                        
                        const long long& operator*() const {
                            return current;
                        }
                        
                        bool operator!=(const iterator& other) const {
                            return position != other.position;
                        }
                    };
                    
                    long long next() const {
                        long long result = a;
                        long long temp = a + b;
                        a = b;
                        b = temp;
                        return result;
                    }
                    
                    iterator begin() {
                        return iterator(this, 0);
                    }
                    
                    iterator end() {
                        return iterator(this, SIZE_MAX);
                    }
                };
                
                template<typename T>
                std::vector<T> take(size_t n, const T& container) {
                    std::vector<T> result;
                    auto it = container.begin();
                    for (size_t i = 0; i < n && it != container.end(); ++i, ++it) {
                        result.push_back(*it);
                    }
                    return result;
                }
                
                class Range {
                private:
                    int start, stop, step;
                    
                public:
                    Range(int start, int stop = -1, int step = 1) 
                        : start(stop == -1 ? 0 : start), 
                          stop(stop == -1 ? start : stop), 
                          step(step) {}
                    
                    class iterator {
                    private:
                        int current;
                        int step;
                        int stop;
                        
                    public:
                        iterator(int start, int stop, int step) : current(start), step(step), stop(stop) {}
                        
                        iterator& operator++() {
                            current += step;
                            return *this;
                        }
                        
                        int operator*() const {
                            return current;
                        }
                        
                        bool operator!=(const iterator& other) const {
                            return current < stop;
                        }
                    };
                    
                    iterator begin() const {
                        return iterator(start, stop, step);
                    }
                    
                    iterator end() const {
                        return iterator(stop, stop, step);
                    }
                };
                '''.strip(),
                
                # Test 8: STL Algorithms and Modern C++ Features
                '''
                #include <vector>
                #include <map>
                #include <set>
                #include <algorithm>
                #include <numeric>
                
                struct ComprehensionResult {
                    std::vector<int> squares;
                    std::vector<int> evenSquares;
                    std::vector<std::vector<int>> matrix;
                    std::map<int, int> squareMap;
                    std::map<std::string, int> filteredMap;
                    std::set<int> uniqueSquares;
                    std::vector<int> flattened;
                };
                
                ComprehensionResult comprehensionTests(const std::map<std::string, int>& data) {
                    ComprehensionResult result;
                    
                    // Generate squares
                    result.squares.resize(10);
                    std::iota(result.squares.begin(), result.squares.end(), 0);
                    std::transform(result.squares.begin(), result.squares.end(), 
                                   result.squares.begin(), [](int x) { return x * x; });
                    
                    // Even squares
                    std::vector<int> evens;
                    for (int i = 0; i < 10; i += 2) {
                        evens.push_back(i);
                    }
                    std::transform(evens.begin(), evens.end(), 
                                   std::back_inserter(result.evenSquares), 
                                   [](int x) { return x * x; });
                    
                    // Matrix
                    result.matrix.resize(5);
                    for (int i = 0; i < 5; ++i) {
                        result.matrix[i].resize(5);
                        for (int j = 0; j < 5; ++j) {
                            result.matrix[i][j] = i * j;
                        }
                    }
                    
                    // Square map
                    for (int i = 0; i < 5; ++i) {
                        result.squareMap[i] = i * i;
                    }
                    
                    // Filtered map
                    std::copy_if(data.begin(), data.end(), 
                                 std::inserter(result.filteredMap, result.filteredMap.end()),
                                 [](const auto& pair) { return pair.second > 0; });
                    
                    // Unique squares
                    std::vector<int> temp = {-2, -1, 0, 1, 2};
                    std::transform(temp.begin(), temp.end(), 
                                   std::inserter(result.uniqueSquares, result.uniqueSquares.end()),
                                   [](int x) { return x * x; });
                    
                    // Flatten matrix
                    for (const auto& row : result.matrix) {
                        result.flattened.insert(result.flattened.end(), row.begin(), row.end());
                    }
                    
                    return result;
                }
                '''.strip(),
                
                # Test 9: Exception Handling
                '''
                #include <exception>
                #include <string>
                #include <typeinfo>
                
                class CustomError : public std::exception {
                private:
                    std::string message;
                    int code;
                    
                public:
                    CustomError(const std::string& msg, int c) : message(msg), code(c) {}
                    
                    const char* what() const noexcept override {
                        return message.c_str();
                    }
                    
                    int getCode() const {
                        return code;
                    }
                };
                
                double divideWithHandling(double a, double b) {
                    try {
                        if (b == 0.0) {
                            throw CustomError("Cannot divide by zero", 400);
                        }
                        return a / b;
                    } catch (...) {
                        std::cout << "Division attempted" << std::endl;
                        throw;
                    }
                }
                
                template<typename T>
                double multipleExceptionHandling(const T& value) {
                    try {
                        if constexpr (std::is_same_v<T, std::string>) {
                            try {
                                return std::stod(value);
                            } catch (const std::invalid_argument&) {
                                return 0.0;
                            }
                        } else if constexpr (std::is_arithmetic_v<T>) {
                            if (value == 0) {
                                return std::numeric_limits<double>::infinity();
                            }
                            return 1.0 / static_cast<double>(value);
                        } else {
                            throw std::invalid_argument("Unsupported type");
                        }
                    } catch (const std::exception& e) {
                        std::cout << "Unexpected error: " << e.what() << std::endl;
                        throw;
                    }
                }
                '''.strip(),
                
                # Test 10: Function Templates and Generic Programming
                '''
                #include <unordered_map>
                #include <functional>
                #include <vector>
                
                template<typename Func>
                class Memoized {
                private:
                    Func func;
                    mutable std::unordered_map<std::string, typename std::result_of<Func()>::type> cache;
                    
                public:
                    Memoized(Func f) : func(f) {}
                    
                    template<typename... Args>
                    auto operator()(Args&&... args) const -> decltype(func(std::forward<Args>(args)...)) {
                        // Simple hash for demonstration - real implementation would be more sophisticated
                        std::string key = std::to_string(sizeof...(args));
                        
                        auto it = cache.find(key);
                        if (it != cache.end()) {
                            return it->second;
                        }
                        
                        auto result = func(std::forward<Args>(args)...);
                        cache[key] = result;
                        return result;
                    }
                };
                
                template<typename Func>
                auto memoize(Func&& func) {
                    return Memoized<Func>(std::forward<Func>(func));
                }
                
                template<int N, typename Func>
                auto repeat(Func&& func) {
                    return [func](auto&&... args) {
                        std::vector<decltype(func(args...))> results;
                        for (int i = 0; i < N; ++i) {
                            results.push_back(func(args...));
                        }
                        return results;
                    };
                }
                
                auto expensiveFibonacci = memoize([](int n) -> long long {
                    if (n < 2) return n;
                    return expensiveFibonacci(n - 1) + expensiveFibonacci(n - 2);
                });
                
                auto greet = repeat<3>([](const std::string& name) {
                    return "Hello, " + name + "!";
                });
                '''.strip(),
                
                # Test 11: RAII and Resource Management
                '''
                #include <iostream>
                #include <memory>
                #include <functional>
                
                class ResourceManager {
                private:
                    std::string resource;
                    std::function<void()> cleanup;
                    bool disposed = false;
                    
                public:
                    ResourceManager(const std::string& res, std::function<void()> cleanupFunc = nullptr)
                        : resource(res), cleanup(cleanupFunc) {
                        std::cout << "Acquiring resource: " << resource << std::endl;
                    }
                    
                    ~ResourceManager() {
                        dispose();
                    }
                    
                    // Delete copy constructor and assignment operator
                    ResourceManager(const ResourceManager&) = delete;
                    ResourceManager& operator=(const ResourceManager&) = delete;
                    
                    // Move constructor and assignment operator
                    ResourceManager(ResourceManager&& other) noexcept
                        : resource(std::move(other.resource)), 
                          cleanup(std::move(other.cleanup)),
                          disposed(other.disposed) {
                        other.disposed = true;
                    }
                    
                    ResourceManager& operator=(ResourceManager&& other) noexcept {
                        if (this != &other) {
                            dispose();
                            resource = std::move(other.resource);
                            cleanup = std::move(other.cleanup);
                            disposed = other.disposed;
                            other.disposed = true;
                        }
                        return *this;
                    }
                    
                    template<typename Func>
                    auto use(Func&& callback) -> decltype(callback(resource)) {
                        return callback(resource);
                    }
                    
                    void dispose() {
                        if (!disposed) {
                            std::cout << "Disposing resource: " << resource << std::endl;
                            if (cleanup) cleanup();
                            disposed = true;
                        }
                    }
                };
                '''.strip(),
                
                # Test 12: Static vs Member Functions
                '''
                #include <string>
                
                class MethodTypes {
                private:
                    int instanceVar;
                    
                public:
                    static const int classVar = 100;
                    
                    MethodTypes(int value) : instanceVar(value) {}
                    
                    std::string instanceMethod() const {
                        return "Instance: " + std::to_string(instanceVar);
                    }
                    
                    static std::string classMethod() {
                        return "Class: " + std::to_string(classVar);
                    }
                    
                    static int staticMethod(int x, int y) {
                        return x + y;
                    }
                    
                    // Const member function
                    int getValue() const {
                        return instanceVar;
                    }
                    
                    // Non-const member function
                    void setValue(int value) {
                        instanceVar = value;
                    }
                };
                
                const int MethodTypes::classVar;
                '''.strip(),
                
                # Test 13: String Operations and Modern C++
                '''
                #include <string>
                #include <sstream>
                #include <algorithm>
                #include <cctype>
                
                struct StringOperationsResult {
                    std::string concat;
                    std::string formatted;
                    std::string upper;
                    std::string lower;
                    std::string replaced;
                    std::string multiline;
                };
                
                StringOperationsResult stringOperations() {
                    std::string name = "Alice";
                    int age = 30;
                    
                    StringOperationsResult result;
                    
                    // String concatenation
                    result.concat = "Hello, " + name + "!";
                    
                    // String formatting (C++20 style or stringstream)
                    std::ostringstream oss;
                    oss << "Hello, " << name << "! You are " << age << " years old.";
                    result.formatted = oss.str();
                    
                    // String case conversion
                    result.upper = name;
                    std::transform(result.upper.begin(), result.upper.end(), 
                                   result.upper.begin(), ::toupper);
                    
                    result.lower = name;
                    std::transform(result.lower.begin(), result.lower.end(), 
                                   result.lower.begin(), ::tolower);
                    
                    // String replacement
                    result.replaced = name;
                    std::replace(result.replaced.begin(), result.replaced.end(), 'A', 'E');
                    
                    // Raw string literal (C++11)
                    result.multiline = R"(This is
a multiline
string)";
                    
                    return result;
                }
                '''.strip(),
                
                # Test 14: Complex Control Flow with Modern C++
                '''
                #include <vector>
                #include <string>
                #include <variant>
                #include <cmath>
                #include <regex>
                
                enum class ItemType {
                    NEGATIVE, ZERO, PRIME, COMPOSITE, NUMERIC_STRING, STRING, OTHER
                };
                
                using ProcessableItem = std::variant<int, std::string, std::nullptr_t>;
                using Result = std::pair<ItemType, ProcessableItem>;
                
                std::vector<Result> complexControlFlow(const std::vector<ProcessableItem>& items) {
                    std::vector<Result> results;
                    
                    for (const auto& item : items) {
                        std::visit([&results](const auto& value) {
                            using T = std::decay_t<decltype(value)>;
                            
                            if constexpr (std::is_same_v<T, std::nullptr_t>) {
                                // Skip null items
                                return;
                            } else if constexpr (std::is_same_v<T, int>) {
                                if (value < 0) {
                                    results.emplace_back(ItemType::NEGATIVE, value);
                                } else if (value == 0) {
                                    results.emplace_back(ItemType::ZERO, value);
                                } else {
                                    // Check if prime
                                    bool isPrime = true;
                                    if (value > 1) {
                                        for (int j = 2; j <= static_cast<int>(std::sqrt(value)); ++j) {
                                            if (value % j == 0) {
                                                isPrime = false;
                                                break;
                                            }
                                        }
                                    }
                                    
                                    if (isPrime && value > 1) {
                                        results.emplace_back(ItemType::PRIME, value);
                                    } else {
                                        results.emplace_back(ItemType::COMPOSITE, value);
                                    }
                                }
                            } else if constexpr (std::is_same_v<T, std::string>) {
                                std::regex numeric_regex(R"(^\\d+$)");
                                if (std::regex_match(value, numeric_regex)) {
                                    results.emplace_back(ItemType::NUMERIC_STRING, value);
                                } else {
                                    results.emplace_back(ItemType::STRING, value);
                                }
                            } else {
                                results.emplace_back(ItemType::OTHER, value);
                            }
                        }, item);
                    }
                    
                    return results;
                }
                '''.strip(),
                
                # Test 15: Scoping and Lambda Captures
                '''
                #include <functional>
                
                std::function<int()> scopeTest() {
                    int globalVar = 100;
                    
                    auto outer = [globalVar]() mutable {
                        int outerVar = 200;
                        
                        auto inner = [&outerVar, &globalVar]() {
                            int innerVar = 300;
                            outerVar += 10;
                            globalVar += 1;
                            
                            return innerVar + outerVar + globalVar;
                        };
                        
                        return inner();
                    };
                    
                    return outer;
                }
                '''.strip(),
            ],
            
            "java": [
                # Test 1: Basic Methods and Arithmetic
                '''
                public class Test1 {
                    public static int add(int x, int y) {
                        return x + y;
                    }

                    public static long factorial(int n) {
                        if (n <= 1) {
                            return 1;
                        }
                        return n * factorial(n - 1);
                    }
                }
                '''.strip(),

                # Test 2: Closures and Higher-Order Functions (Java style)
                '''
                import java.util.function.Function;
                import java.util.function.Supplier;

                public class Test2 {
                    public static Function<Integer, Integer> makeMultiplier(int factor) {
                        return (Integer x) -> x * factor;
                    }

                    public static Supplier<Integer> counter() {
                        final int[] count = {0};
                        return () -> ++count[0];
                    }
                }
                '''.strip(),

                # Test 3: Classes and Inheritance
                '''
                public abstract class Animal {
                    protected String name;

                    public Animal(String name) {
                        this.name = name;
                    }

                    public abstract String speak();

                    public String getName() {
                        return name;
                    }
                }

                class Dog extends Animal {
                    private String breed;

                    public Dog(String name, String breed) {
                        super(name);
                        this.breed = breed;
                    }

                    @Override
                    public String speak() {
                        return this.name + " barks";
                    }

                    public String fetch() {
                        return this.name + " fetches the ball";
                    }
                }

                class Cat extends Animal {
                    public Cat(String name) {
                        super(name);
                    }

                    @Override
                    public String speak() {
                        return this.name + " meows";
                    }
                }
                '''.strip(),

                # Test 4: Interfaces and Multiple Inheritance
                '''
                public interface Animal {
                    String getName();
                    String speak();
                }

                public interface Flyable {
                    String fly();
                }

                public interface Swimmable {
                    String swim();
                }

                class Duck implements Animal, Flyable, Swimmable {
                    private String name;

                    public Duck(String name) {
                        this.name = name;
                    }

                    @Override
                    public String getName() {
                        return name;
                    }

                    @Override
                    public String speak() {
                        return name + " quacks";
                    }

                    @Override
                    public String fly() {
                        return "Flying high";
                    }

                    @Override
                    public String swim() {
                        return "Swimming deep";
                    }
                }
                '''.strip(),

                # Test 5: Properties (Getters and Setters)
                '''
                public class Temperature {
                    private double celsius;

                    public Temperature(double celsius) {
                        this.setCelsius(celsius);
                    }

                    public double getCelsius() {
                        return this.celsius;
                    }

                    public void setCelsius(double value) {
                        if (value < -273.15) {
                            throw new IllegalArgumentException("Below absolute zero");
                        }
                        this.celsius = value;
                    }

                    public double getFahrenheit() {
                        return this.celsius * 9.0/5.0 + 32.0;
                    }

                    public void setFahrenheit(double value) {
                        this.setCelsius((value - 32.0) * 5.0/9.0);
                    }
                }
                '''.strip(),
                
                # Test 6: Records and Operator-like Methods
                '''
                public record Vector(double x, double y, double z) {
                    public Vector {
                        // Compact constructor
                    }

                    public Vector add(Vector other) {
                        return new Vector(this.x + other.x, this.y + other.y, this.z + other.z);
                    }
                    
                    public Vector subtract(Vector other) {
                        return new Vector(this.x - other.x, this.y - other.y, this.z - other.z);
                    }

                    public Vector multiply(double scalar) {
                        return new Vector(this.x * scalar, this.y * scalar, this.z * scalar);
                    }

                    @Override
                    public String toString() {
                        return String.format("Vector(%.1f, %.1f, %.1f)", x, y, z);
                    }
                }
                '''.strip(),

                # Test 7: Iterators and Streams
                '''
                import java.util.stream.Stream;
                import java.util.stream.Collectors;
                import java.util.List;

                public class Test7 {
                    public static Stream<Long> fibonacci() {
                        return Stream.iterate(new long[]{0, 1}, p -> new long[]{p[1], p[0] + p[1]})
                                     .mapToLong(p -> p[0])
                                     .boxed();
                    }

                    public static <T> List<T> take(long n, Stream<T> stream) {
                        return stream.limit(n).collect(Collectors.toList());
                    }
                }
                '''.strip(),
                
                # Test 8: Streams and Collections
                '''
                import java.util.List;
                import java.util.Map;
                import java.util.Set;
                import java.util.stream.Collectors;
                import java.util.stream.IntStream;

                public class Test8 {
                    public static List<Integer> getSquares() {
                        return IntStream.range(0, 10)
                                        .map(x -> x * x)
                                        .boxed()
                                        .collect(Collectors.toList());
                    }

                    public static Map<Integer, Integer> getSquareMap() {
                        return IntStream.range(0, 5)
                                        .boxed()
                                        .collect(Collectors.toMap(k -> k, v -> v * v));
                    }
                }
                '''.strip(),
                
                # Test 9: Exception Handling
                '''
                public class CustomError extends RuntimeException {
                    private final int code;

                    public CustomError(String message, int code) {
                        super(message);
                        this.code = code;
                    }

                    public int getCode() {
                        return code;
                    }
                }

                public class Test9 {
                    public double divideWithHandling(double a, double b) {
                        try {
                            if (b == 0) {
                                throw new CustomError("Cannot divide by zero", 400);
                            }
                            return a / b;
                        } finally {
                            System.out.println("Division attempted");
                        }
                    }
                }
                '''.strip(),
                
                # Test 10: Annotations and Reflection (Java's Decorator Pattern)
                '''
                import java.lang.annotation.*;
                
                @Retention(RetentionPolicy.RUNTIME)
                @Target(ElementType.METHOD)
                public @interface Repeat {
                    int times();
                }

                public class Test10 {
                    @Repeat(times = 3)
                    public String greet(String name) {
                        return "Hello, " + name + "!";
                    }
                }
                '''.strip(),
                
                # Test 11: try-with-resources (Context Manager)
                '''
                import java.io.Closeable;
                import java.io.IOException;

                public class FileManager implements Closeable {
                    private String filename;

                    public FileManager(String filename, String mode) {
                        System.out.println("Opening " + filename);
                        this.filename = filename;
                    }

                    @Override
                    public void close() throws IOException {
                        System.out.println("Closing " + filename);
                    }
                }

                public class Test11 {
                    public void useFile() {
                        try (FileManager fm = new FileManager("test.txt", "w")) {
                            // use file manager
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                }
                '''.strip(),
                
                # Test 12: Static vs Instance Methods
                '''
                public class MethodTypes {
                    public static final int CLASS_VAR = 100;
                    private int instanceVar;

                    public MethodTypes(int value) {
                        this.instanceVar = value;
                    }

                    public String instanceMethod() {
                        return "Instance: " + this.instanceVar;
                    }

                    public static String classMethod() {
                        return "Class: " + CLASS_VAR;
                    }
                }
                '''.strip(),
            ]
        }
    
    def test_round_trip(self, language: str, source_code: str) -> RoundTripTestResult:
        """Test complete round-trip translation for a language."""
        start_time = time.time()
        tracker = PipelineStepTracker()
        errors = []
        
        try:
            # Step 1: Original Language → Language Parser → Language AST
            toolchain = self._get_toolchain(language)
            parse_result = tracker.track_step(
                f"{language.upper()}_PARSE",
                source_code,
                toolchain.parse,
                source_code
            )
            
            if not parse_result.success:
                errors.append(f"Parse failed: {parse_result.error_message}")
                return self._create_failed_result(language, source_code, tracker, errors, start_time)
            
            language_ast = parse_result.output_data.data
            
            # Step 2: Language AST → Language Converter → Runa AST
            to_runa_result = tracker.track_step(
                f"{language.upper()}_TO_RUNA",
                language_ast,
                toolchain.to_runa,
                language_ast
            )
            
            if not to_runa_result.success:
                errors.append(f"To Runa conversion failed: {to_runa_result.error_message}")
                return self._create_failed_result(language, source_code, tracker, errors, start_time)
            
            runa_ast_1 = to_runa_result.output_data.target_ast
            
            # Step 3: Runa AST → Runa Generator → Runa Source Code
            runa_generate_result = tracker.track_step(
                "RUNA_GENERATE",
                runa_ast_1,
                self.runa_generator.generate,
                runa_ast_1
            )
            
            if not runa_generate_result.success:
                errors.append(f"Runa generation failed: {runa_generate_result.error_message}")
                return self._create_failed_result(language, source_code, tracker, errors, start_time)
            
            runa_code = runa_generate_result.output_data
            
            # Step 4: Runa Source → Runa Parser → Runa AST (verification)
            runa_parse_result = tracker.track_step(
                "RUNA_PARSE_VERIFY",
                runa_code,
                self.runa_parser.parse,
                runa_code
            )
            
            if not runa_parse_result.success:
                errors.append(f"Runa parsing verification failed: {runa_parse_result.error_message}")
                return self._create_failed_result(language, source_code, tracker, errors, start_time)
            
            runa_ast_2 = runa_parse_result.output_data
            
            # Step 5: Runa AST → Language Converter → Language AST
            from_runa_result = tracker.track_step(
                f"RUNA_TO_{language.upper()}",
                runa_ast_2,
                toolchain.from_runa,
                runa_ast_2
            )
            
            if not from_runa_result.success:
                errors.append(f"From Runa conversion failed: {from_runa_result.error_message}")
                return self._create_failed_result(language, source_code, tracker, errors, start_time)
            
            language_ast_2 = from_runa_result.output_data.target_ast
            
            # Step 6: Language AST → Language Generator → Original Language
            generate_result = tracker.track_step(
                f"{language.upper()}_GENERATE",
                language_ast_2,
                toolchain.generate,
                language_ast_2
            )
            
            if not generate_result.success:
                errors.append(f"Code generation failed: {generate_result.error_message}")
                return self._create_failed_result(language, source_code, tracker, errors, start_time)
            
            final_code = generate_result.output_data.data
            
            # Calculate metrics
            total_time_ms = (time.time() - start_time) * 1000
            similarity_score = self._calculate_similarity(source_code, final_code)
            syntax_preserved = self._verify_syntax_preservation(language, source_code, final_code)
            semantics_preserved = self._verify_semantics_preservation(language, language_ast, language_ast_2)
            
            return RoundTripTestResult(
                language=language,
                original_code=source_code,
                final_code=final_code,
                pipeline_steps=tracker.steps,
                total_time_ms=total_time_ms,
                syntax_preserved=syntax_preserved,
                semantics_preserved=semantics_preserved,
                round_trip_success=len(errors) == 0,
                similarity_score=similarity_score,
                errors=errors
            )
            
        except Exception as e:
            errors.append(f"Unexpected error: {str(e)}")
            return self._create_failed_result(language, source_code, tracker, errors, start_time)
    
    def _get_toolchain(self, language: str):
        """Get the appropriate toolchain for a language."""
        toolchain_map = {
            "python": self.python_toolchain,
            "javascript": self.javascript_toolchain,
            "typescript": self.typescript_toolchain,
            "cpp": self.cpp_toolchain,
            "java": self.java_toolchain
        }
        return toolchain_map[language.lower()]
    
    def _create_failed_result(self, language: str, source_code: str, tracker: PipelineStepTracker, 
                            errors: List[str], start_time: float) -> RoundTripTestResult:
        """Create a failed test result."""
        total_time_ms = (time.time() - start_time) * 1000
        return RoundTripTestResult(
            language=language,
            original_code=source_code,
            final_code="",
            pipeline_steps=tracker.steps,
            total_time_ms=total_time_ms,
            syntax_preserved=False,
            semantics_preserved=False,
            round_trip_success=False,
            similarity_score=0.0,
            errors=errors
        )
    
    def _calculate_similarity(self, code1: str, code2: str) -> float:
        """Calculate similarity score between two code samples."""
        # Use difflib to calculate similarity
        ratio = difflib.SequenceMatcher(None, code1.strip(), code2.strip()).ratio()
        return round(ratio * 100, 2)
    
    def _verify_syntax_preservation(self, language: str, original: str, final: str) -> bool:
        """Verify that syntax is preserved during round-trip."""
        try:
            # Try to parse both original and final code
            toolchain = self._get_toolchain(language)
            original_parse = toolchain.parse(original)
            final_parse = toolchain.parse(final)
            return original_parse.success and final_parse.success
        except:
            return False
    
    def _verify_semantics_preservation(self, language: str, ast1: ASTNode, ast2: ASTNode) -> bool:
        """Verify that semantics are preserved between ASTs."""
        try:
            # Use toolchain's built-in AST comparison if available
            toolchain = self._get_toolchain(language)
            if hasattr(toolchain, '_compare_semantics'):
                return toolchain._compare_semantics(ast1, ast2)
            else:
                # Fallback to basic structure comparison
                return str(ast1) == str(ast2)
        except:
            return False
    
    def _get_file_extension(self, language: str) -> str:
        """Get the primary file extension for a language."""
        toolchain = self._get_toolchain(language)
        return toolchain.metadata.file_extensions[0].lstrip('.')

    def save_detailed_results(self, results: Dict[str, List[RoundTripTestResult]], base_output_dir: Path):
        """Saves detailed results for each test case to a structured directory."""
        base_output_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n💾 Saving detailed output to: {base_output_dir}")

        for language, language_results in results.items():
            lang_dir = base_output_dir / language
            lang_dir.mkdir(exist_ok=True)
            ext = self._get_file_extension(language)
            
            for i, result in enumerate(language_results):
                test_name = f"test_{i+1:02d}"
                
                # Save original code
                original_path = lang_dir / f"{test_name}_original.{ext}"
                with open(original_path, 'w', encoding='utf-8') as f:
                    f.write(result.original_code)

                # Save final code if available
                if result.final_code:
                    final_path = lang_dir / f"{test_name}_final.{ext}"
                    with open(final_path, 'w', encoding='utf-8') as f:
                        f.write(result.final_code)
                
                # Save individual test report
                report_path = lang_dir / f"{test_name}_report.json"
                with open(report_path, 'w', encoding='utf-8') as f:
                    json.dump(result.to_dict(), f, indent=2)

    def run_comprehensive_tests(self) -> Dict[str, List[RoundTripTestResult]]:
        """Run comprehensive round-trip tests for all tier 1 languages."""
        results = {}
        
        for language, test_samples in self.test_samples.items():
            print(f"\nTesting {language.upper()} round-trip translation...")
            language_results = []
            
            for i, sample in enumerate(test_samples):
                print(f"  Sample {i+1}/{len(test_samples)}: ", end="", flush=True)
                result = self.test_round_trip(language, sample)
                language_results.append(result)
                
                if result.round_trip_success:
                    print(f"✅ SUCCESS (similarity: {result.similarity_score}%)")
                else:
                    print(f"❌ FAILED ({len(result.errors)} errors)")
                    for error in result.errors:
                        print(f"    - {error}")
            
            results[language] = language_results
        
        return results
    
    def generate_report(self, results: Dict[str, List[RoundTripTestResult]]) -> Dict[str, Any]:
        """Generate a summary test report."""
        report = {
            "test_summary": {},
            "performance_metrics": {},
            "errors_by_language": {},
            "recommendations": []
        }
        
        for language, language_results in results.items():
            successful_tests = [r for r in language_results if r.round_trip_success]
            failed_tests = [r for r in language_results if not r.round_trip_success]
            
            # Summary
            report["test_summary"][language] = {
                "total_tests": len(language_results),
                "successful": len(successful_tests),
                "failed": len(failed_tests),
                "success_rate": round(len(successful_tests) / len(language_results) * 100, 2) if language_results else 0,
                "average_similarity": round(sum(r.similarity_score for r in successful_tests) / max(len(successful_tests), 1), 2),
                "average_time_ms": round(sum(r.total_time_ms for r in language_results) / max(len(language_results), 1), 2)
            }
            
            # Performance metrics
            times = [r.total_time_ms for r in language_results]
            similarities = [r.similarity_score for r in successful_tests]
            
            report["performance_metrics"][language] = {
                "min_time_ms": min(times) if times else 0,
                "max_time_ms": max(times) if times else 0,
                "avg_time_ms": sum(times) / len(times) if times else 0,
                "min_similarity": min(similarities) if similarities else 0,
                "max_similarity": max(similarities) if similarities else 0,
                "avg_similarity": sum(similarities) / len(similarities) if similarities else 0
            }
            
            # Error analysis
            all_errors = []
            for result in failed_tests:
                all_errors.extend(result.errors)
            
            report["errors_by_language"][language] = {
                "total_errors": len(all_errors),
                "unique_errors": list(set(all_errors)),
                "error_frequency": {error: all_errors.count(error) for error in set(all_errors)}
            }
        
        # Generate recommendations
        report["recommendations"] = self._generate_recommendations(results)
        
        return report


    def _generate_recommendations(self, results: Dict[str, List[RoundTripTestResult]]) -> List[str]:
        """Generate recommendations based on test results."""
        recommendations = []
        
        for language, language_results in results.items():
            failed_tests = [r for r in language_results if not r.round_trip_success]
            
            if failed_tests:
                # Analyze common failure patterns
                common_errors = {}
                for result in failed_tests:
                    for error in result.errors:
                        error_type = error.split(':')[0] if ':' in error else error
                        common_errors[error_type] = common_errors.get(error_type, 0) + 1
                
                most_common_error = max(common_errors.items(), key=lambda x: x[1]) if common_errors else None
                
                if most_common_error:
                    recommendations.append(
                        f"{language.upper()}: Focus on fixing '{most_common_error[0]}' errors "
                        f"(occurs in {most_common_error[1]} tests)"
                    )
            
            # Performance recommendations
            avg_time = sum(r.total_time_ms for r in language_results) / len(language_results)
            if avg_time > 1000:  # More than 1 second
                recommendations.append(
                    f"{language.upper()}: Consider optimizing pipeline - average time {avg_time:.1f}ms is high"
                )
            
            # Similarity recommendations
            successful_tests = [r for r in language_results if r.round_trip_success]
            if successful_tests:
                avg_similarity = sum(r.similarity_score for r in successful_tests) / len(successful_tests)
                if avg_similarity < 80:
                    recommendations.append(
                        f"{language.upper()}: Low code similarity ({avg_similarity:.1f}%) suggests "
                        "semantic preservation issues"
                    )
        
        return recommendations


class TestTier1RoundTrip(unittest.TestCase):
    """Unit tests for tier 1 round-trip translation."""
    
    def setUp(self):
        """Set up test environment."""
        self.tester = Tier1RoundTripTester()
        
    def test_python_round_trip(self):
        """Test Python round-trip translation."""
        sample = self.tester.test_samples["python"][0]
        result = self.tester.test_round_trip("python", sample)
        
        self.assertTrue(result.round_trip_success, f"Python round-trip failed: {result.errors}")
        self.assertGreater(result.similarity_score, 70, "Python similarity too low")
        self.assertTrue(result.syntax_preserved, "Python syntax not preserved")
        
    def test_javascript_round_trip(self):
        """Test JavaScript round-trip translation."""
        sample = self.tester.test_samples["javascript"][0]
        result = self.tester.test_round_trip("javascript", sample)
        
        self.assertTrue(result.round_trip_success, f"JavaScript round-trip failed: {result.errors}")
        self.assertGreater(result.similarity_score, 70, "JavaScript similarity too low")
        self.assertTrue(result.syntax_preserved, "JavaScript syntax not preserved")
        
    def test_typescript_round_trip(self):
        """Test TypeScript round-trip translation."""
        sample = self.tester.test_samples["typescript"][0]
        result = self.tester.test_round_trip("typescript", sample)
        
        self.assertTrue(result.round_trip_success, f"TypeScript round-trip failed: {result.errors}")
        self.assertGreater(result.similarity_score, 70, "TypeScript similarity too low")
        self.assertTrue(result.syntax_preserved, "TypeScript syntax not preserved")
        
    def test_cpp_round_trip(self):
        """Test C++ round-trip translation."""
        sample = self.tester.test_samples["cpp"][0]
        result = self.tester.test_round_trip("cpp", sample)
        
        self.assertTrue(result.round_trip_success, f"C++ round-trip failed: {result.errors}")
        self.assertGreater(result.similarity_score, 70, "C++ similarity too low")
        self.assertTrue(result.syntax_preserved, "C++ syntax not preserved")
        
    def test_java_round_trip(self):
        """Test Java round-trip translation."""
        sample = self.tester.test_samples["java"][0]
        result = self.tester.test_round_trip("java", sample)
        
        self.assertTrue(result.round_trip_success, f"Java round-trip failed: {result.errors}")
        self.assertGreater(result.similarity_score, 70, "Java similarity too low")
        self.assertTrue(result.syntax_preserved, "Java syntax not preserved")
        
    def test_all_languages_comprehensive(self):
        """Run comprehensive tests for all languages."""
        results = self.tester.run_comprehensive_tests()
        
        # Verify all languages were tested
        self.assertEqual(set(results.keys()), {"python", "javascript", "typescript", "cpp", "java"})
        
        # Check that each language has test results
        for language, language_results in results.items():
            self.assertGreater(len(language_results), 0, f"No test results for {language}")
            
        # Define output directory
        output_dir = Path(__file__).parent / "round trip output"
        
        # Save detailed results
        self.tester.save_detailed_results(results, output_dir)
        
        # Generate and validate summary report
        report = self.tester.generate_report(results)
        
        self.assertIn("test_summary", report)
        self.assertIn("performance_metrics", report)
        self.assertIn("recommendations", report)
        
        # Save summary report
        output_file = output_dir / "summary_report.json"
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Summary test report saved to: {output_file}")
        
        # Print summary
        self._print_test_summary(report)
        
    def _print_test_summary(self, report: Dict[str, Any]):
        """Print a formatted test summary."""
        print("\n" + "="*80)
        print("TIER 1 ROUND-TRIP TRANSLATION TEST SUMMARY")
        print("="*80)
        
        for language, summary in report["test_summary"].items():
            print(f"\n{language.upper()}:")
            print(f"  ✅ Success Rate: {summary['success_rate']}% ({summary['successful']}/{summary['total_tests']})")
            print(f"  📊 Avg Similarity: {summary['average_similarity']}%")
            print(f"  ⏱️  Avg Time: {summary['average_time_ms']:.1f}ms")
            
        print(f"\n📋 RECOMMENDATIONS:")
        for rec in report["recommendations"]:
            print(f"  • {rec}")
            
        print("\n" + "="*80)


def main():
    """Main function to run comprehensive tests."""
    print("🚀 Starting Tier 1 Round-Trip Translation Tests...")
    print("Testing: Python, JavaScript, TypeScript, C++, Java")
    print("-" * 60)
    
    # Create tester and run tests
    tester = Tier1RoundTripTester()
    results = tester.run_comprehensive_tests()
    
    # Define output directory
    output_dir = Path(__file__).parent / "round trip output"

    # Save detailed results
    tester.save_detailed_results(results, output_dir)
    
    # Generate report
    report = tester.generate_report(results)
    
    # Save summary report
    output_file = output_dir / "summary_report.json"
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📊 Summary test report saved to: {output_file}")
    
    # Print summary
    print("\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    
    total_tests = sum(summary["total_tests"] for summary in report["test_summary"].values())
    total_successful = sum(summary["successful"] for summary in report["test_summary"].values())
    overall_success_rate = round(total_successful / total_tests * 100, 2) if total_tests > 0 else 0
    
    print(f"Overall Success Rate: {overall_success_rate}% ({total_successful}/{total_tests})")
    
    for language, summary in report["test_summary"].items():
        status = "✅" if summary["success_rate"] == 100 else "⚠️" if summary["success_rate"] >= 75 else "❌"
        print(f"{status} {language.upper()}: {summary['success_rate']}% success")
    
    print("\nRecommendations:")
    for rec in report["recommendations"]:
        print(f"  • {rec}")
    
    return overall_success_rate >= 75


if __name__ == "__main__":
    # Can be run as a script or with unittest
    if len(sys.argv) > 1 and sys.argv[1] == "unittest":
        unittest.main(argv=sys.argv[1:])
    else:
        success = main()
        sys.exit(0 if success else 1) 