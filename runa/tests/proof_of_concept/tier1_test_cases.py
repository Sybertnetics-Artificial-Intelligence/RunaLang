"""
Runa Tier 1 Language Test Battery
=================================

Comprehensive test cases for demonstrating Runa's capabilities with Tier 1 languages.
These tests include both Runa-to-target and source-to-Runa-to-target translations.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

class TestComplexity(Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXTREME = "extreme"
    BREAKING = "breaking"

class TestType(Enum):
    SYNTAX = "syntax"
    SEMANTIC = "semantic"
    ROUNDTRIP = "roundtrip"
    CROSS_LANGUAGE = "cross_language"
    CROSS_DOMAIN = "cross_domain"
    FEATURE_SHOWCASE = "feature_showcase"
    EDGE_CASE = "edge_case"
    PERFORMANCE = "performance"

@dataclass
class TestCase:
    name: str
    description: str
    complexity: TestComplexity
    test_type: TestType
    source_language: str
    target_languages: List[str]
    source_code: str
    expected_behavior: str
    known_issues: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Optional: Expected Runa intermediate representation
    expected_runa: Optional[str] = None

# ============================================================================
# TIER 1 TEST BATTERY - LANGUAGE SPECIFIC
# ============================================================================

def get_tier1_test_cases() -> List[TestCase]:
    """Returns comprehensive test cases for Tier 1 languages"""
    
    test_cases = []
    
    # ========================================================================
    # 1. JAVASCRIPT SOURCE TESTS
    # ========================================================================
    
    test_cases.append(TestCase(
        name="js_basic_hello_world",
        description="Basic JavaScript Hello World to all targets",
        complexity=TestComplexity.BASIC,
        test_type=TestType.ROUNDTRIP,
        source_language="javascript",
        target_languages=["python", "java", "csharp", "typescript"],
        source_code='''console.log("Hello, World!");''',
        expected_runa='''Display "Hello, World!"''',
        expected_behavior="Should output 'Hello, World!' in all target languages",
        metadata={"features": ["console_output", "string_literal"]}
    ))
    
    test_cases.append(TestCase(
        name="js_async_fetch_pattern",
        description="JavaScript async/await pattern translation",
        complexity=TestComplexity.INTERMEDIATE,
        test_type=TestType.CROSS_DOMAIN,
        source_language="javascript",
        target_languages=["python", "csharp", "typescript"],
        source_code='''
async function fetchUserData(userId) {
    try {
        const response = await fetch(`https://api.example.com/users/${userId}`);
        const data = await response.json();
        
        const posts = await fetch(`https://api.example.com/users/${userId}/posts`);
        const postsData = await posts.json();
        
        return {
            user: data,
            posts: postsData,
            fetchedAt: Date.now()
        };
    } catch (error) {
        console.error("Failed to fetch:", error);
        return {
            error: "Failed to fetch user data",
            userId: userId
        };
    }
}

// Usage
(async () => {
    const result = await fetchUserData("12345");
    console.log("Result:", result);
})();
''',
        expected_behavior="Should translate async patterns correctly across languages",
        known_issues=["Different async implementations across languages"],
        metadata={"features": ["async_await", "error_handling", "http_fetch", "template_literals"]}
    ))
    
    test_cases.append(TestCase(
        name="js_functional_array_methods",
        description="JavaScript functional array operations",
        complexity=TestComplexity.INTERMEDIATE,
        test_type=TestType.SEMANTIC,
        source_language="javascript",
        target_languages=["python", "java", "csharp"],
        source_code='''
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// Chain of functional operations
const result = numbers
    .filter(n => n % 2 === 0)
    .map(n => n * n)
    .reduce((sum, n) => sum + n, 0);

console.log("Sum of squares of even numbers:", result);

// More complex example with objects
const people = [
    { name: "Alice", age: 28, skills: ["Python", "ML"], salary: 95000 },
    { name: "Bob", age: 35, skills: ["JavaScript", "React"], salary: 85000 },
    { name: "Charlie", age: 42, skills: ["Java", "Spring"], salary: 110000 },
    { name: "Diana", age: 31, skills: ["Python", "Django"], salary: 90000 }
];

const seniorPythonDevs = people
    .filter(p => p.age > 30 && p.skills.includes("Python"))
    .map(p => ({
        name: p.name,
        level: p.age > 40 ? "senior" : "mid",
        adjustedSalary: p.salary * 1.1
    }))
    .sort((a, b) => b.adjustedSalary - a.adjustedSalary);

console.log("Senior Python developers:", seniorPythonDevs);
''',
        expected_behavior="Should preserve functional programming semantics",
        metadata={"features": ["array_methods", "arrow_functions", "method_chaining", "object_literals"]}
    ))
    
    # ========================================================================
    # 2. PYTHON SOURCE TESTS
    # ========================================================================
    
    test_cases.append(TestCase(
        name="python_class_inheritance",
        description="Python class with inheritance and methods",
        complexity=TestComplexity.INTERMEDIATE,
        test_type=TestType.CROSS_DOMAIN,
        source_language="python",
        target_languages=["javascript", "typescript", "java", "csharp"],
        source_code='''
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class Shape(ABC):
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass
    
    def describe(self) -> str:
        return f"{self.name}: Area={self.area():.2f}, Perimeter={self.perimeter():.2f}"

class Circle(Shape):
    def __init__(self, radius: float):
        super().__init__("Circle")
        self.radius = radius
    
    def area(self) -> float:
        return 3.14159 * self.radius ** 2
    
    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        super().__init__("Rectangle")
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

# Usage
shapes: List[Shape] = [
    Circle(5.0),
    Rectangle(4.0, 6.0),
    Circle(3.0)
]

for shape in shapes:
    print(shape.describe())

# Calculate total area
total_area = sum(shape.area() for shape in shapes)
print(f"Total area: {total_area:.2f}")
''',
        expected_behavior="Should translate OOP concepts correctly",
        metadata={"features": ["classes", "inheritance", "abstract_methods", "type_hints", "f_strings"]}
    ))
    
    test_cases.append(TestCase(
        name="python_decorators_context_managers",
        description="Python decorators and context managers",
        complexity=TestComplexity.ADVANCED,
        test_type=TestType.FEATURE_SHOWCASE,
        source_language="python",
        target_languages=["javascript", "typescript"],
        source_code='''
import time
from functools import wraps
from contextlib import contextmanager
from typing import Callable, Any

# Decorator example
def timing_decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.3f} seconds")
        return result
    return wrapper

# Context manager example
@contextmanager
def resource_manager(name: str):
    print(f"Acquiring resource: {name}")
    resource = {"name": name, "data": [1, 2, 3, 4, 5]}
    try:
        yield resource
    finally:
        print(f"Releasing resource: {name}")

# Memoization decorator
def memoize(func: Callable) -> Callable:
    cache = {}
    
    @wraps(func)
    def wrapper(*args: Any) -> Any:
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper

# Usage
@timing_decorator
@memoize
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Test decorators
print("Testing fibonacci with memoization:")
for i in range(10):
    print(f"fib({i}) = {fibonacci(i)}")

# Test context manager
with resource_manager("database") as db:
    print(f"Using resource: {db}")
    total = sum(db["data"])
    print(f"Sum of data: {total}")
''',
        expected_behavior="Should handle Python-specific patterns appropriately",
        known_issues=["Decorators and context managers don't have direct equivalents in all languages"],
        metadata={"features": ["decorators", "context_managers", "memoization", "function_wrapping"]}
    ))
    
    # ========================================================================
    # 3. TYPESCRIPT SOURCE TESTS
    # ========================================================================
    
    test_cases.append(TestCase(
        name="typescript_generics_interfaces",
        description="TypeScript generics and interface definitions",
        complexity=TestComplexity.INTERMEDIATE,
        test_type=TestType.CROSS_DOMAIN,
        source_language="typescript",
        target_languages=["python", "java", "csharp"],
        source_code='''
// Generic interfaces and types
interface Repository<T> {
    findById(id: string): Promise<T | null>;
    findAll(): Promise<T[]>;
    save(entity: T): Promise<T>;
    delete(id: string): Promise<boolean>;
}

interface Timestamped {
    createdAt: Date;
    updatedAt: Date;
}

interface User extends Timestamped {
    id: string;
    name: string;
    email: string;
    age: number;
}

// Generic class implementation
class InMemoryRepository<T extends { id: string }> implements Repository<T> {
    private storage: Map<string, T> = new Map();

    async findById(id: string): Promise<T | null> {
        return this.storage.get(id) || null;
    }

    async findAll(): Promise<T[]> {
        return Array.from(this.storage.values());
    }

    async save(entity: T): Promise<T> {
        this.storage.set(entity.id, entity);
        return entity;
    }

    async delete(id: string): Promise<boolean> {
        return this.storage.delete(id);
    }
}

// Type guards
function isUser(obj: any): obj is User {
    return obj && 
           typeof obj.id === 'string' &&
           typeof obj.name === 'string' &&
           typeof obj.email === 'string' &&
           typeof obj.age === 'number';
}

// Usage with async/await
async function testRepository() {
    const userRepo = new InMemoryRepository<User>();
    
    const user: User = {
        id: '123',
        name: 'Alice',
        email: 'alice@example.com',
        age: 30,
        createdAt: new Date(),
        updatedAt: new Date()
    };
    
    await userRepo.save(user);
    const found = await userRepo.findById('123');
    
    if (found && isUser(found)) {
        console.log(`Found user: ${found.name}`);
    }
    
    const allUsers = await userRepo.findAll();
    console.log(`Total users: ${allUsers.length}`);
}

testRepository();
''',
        expected_behavior="Should handle TypeScript's advanced type system",
        metadata={"features": ["generics", "interfaces", "type_guards", "async_await", "classes"]}
    ))
    
    test_cases.append(TestCase(
        name="typescript_discriminated_unions",
        description="TypeScript discriminated unions and pattern matching",
        complexity=TestComplexity.ADVANCED,
        test_type=TestType.FEATURE_SHOWCASE,
        source_language="typescript",
        target_languages=["python", "csharp"],
        source_code='''
// Discriminated union types
type Result<T, E> = 
    | { kind: 'success'; value: T }
    | { kind: 'error'; error: E };

type Shape = 
    | { kind: 'circle'; radius: number }
    | { kind: 'rectangle'; width: number; height: number }
    | { kind: 'triangle'; base: number; height: number };

// Pattern matching with discriminated unions
function calculateArea(shape: Shape): number {
    switch (shape.kind) {
        case 'circle':
            return Math.PI * shape.radius ** 2;
        case 'rectangle':
            return shape.width * shape.height;
        case 'triangle':
            return 0.5 * shape.base * shape.height;
        default:
            // Exhaustive check
            const _exhaustive: never = shape;
            throw new Error(`Unknown shape: ${_exhaustive}`);
    }
}

// Result type usage
function safeDivide(a: number, b: number): Result<number, string> {
    if (b === 0) {
        return { kind: 'error', error: 'Division by zero' };
    }
    return { kind: 'success', value: a / b };
}

// Advanced type manipulation
type DeepReadonly<T> = {
    readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

type PartialRecord<K extends keyof any, V> = {
    [P in K]?: V;
};

// Usage
const shapes: Shape[] = [
    { kind: 'circle', radius: 5 },
    { kind: 'rectangle', width: 4, height: 6 },
    { kind: 'triangle', base: 3, height: 4 }
];

shapes.forEach(shape => {
    console.log(`Area of ${shape.kind}: ${calculateArea(shape)}`);
});

const result = safeDivide(10, 2);
if (result.kind === 'success') {
    console.log(`Result: ${result.value}`);
} else {
    console.log(`Error: ${result.error}`);
}
''',
        expected_behavior="Should handle advanced TypeScript type features",
        metadata={"features": ["discriminated_unions", "type_manipulation", "exhaustive_checks", "conditional_types"]}
    ))
    
    # ========================================================================
    # 4. JAVA SOURCE TESTS
    # ========================================================================
    
    test_cases.append(TestCase(
        name="java_stream_api",
        description="Java Stream API and functional programming",
        complexity=TestComplexity.INTERMEDIATE,
        test_type=TestType.CROSS_DOMAIN,
        source_language="java",
        target_languages=["javascript", "python", "csharp"],
        source_code='''
import java.util.*;
import java.util.stream.*;
import java.util.function.*;

public class StreamExample {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        
        // Functional stream operations
        int sumOfSquaresOfEvens = numbers.stream()
            .filter(n -> n % 2 == 0)
            .map(n -> n * n)
            .reduce(0, Integer::sum);
        
        System.out.println("Sum of squares of even numbers: " + sumOfSquaresOfEvens);
        
        // Complex object processing
        List<Person> people = Arrays.asList(
            new Person("Alice", 28, Arrays.asList("Python", "ML"), 95000),
            new Person("Bob", 35, Arrays.asList("JavaScript", "React"), 85000),
            new Person("Charlie", 42, Arrays.asList("Java", "Spring"), 110000),
            new Person("Diana", 31, Arrays.asList("Python", "Django"), 90000)
        );
        
        Map<String, List<Person>> groupedBySkill = people.stream()
            .flatMap(p -> p.skills.stream()
                .map(skill -> new AbstractMap.SimpleEntry<>(skill, p)))
            .collect(Collectors.groupingBy(
                Map.Entry::getKey,
                Collectors.mapping(Map.Entry::getValue, Collectors.toList())
            ));
        
        groupedBySkill.forEach((skill, devs) -> {
            System.out.println(skill + ": " + 
                devs.stream().map(p -> p.name).collect(Collectors.joining(", ")));
        });
        
        // Parallel processing
        long count = IntStream.range(0, 1000000)
            .parallel()
            .filter(n -> isPrime(n))
            .count();
        
        System.out.println("Prime numbers up to 1M: " + count);
    }
    
    static class Person {
        String name;
        int age;
        List<String> skills;
        double salary;
        
        Person(String name, int age, List<String> skills, double salary) {
            this.name = name;
            this.age = age;
            this.skills = skills;
            this.salary = salary;
        }
    }
    
    static boolean isPrime(int n) {
        if (n <= 1) return false;
        if (n <= 3) return true;
        if (n % 2 == 0 || n % 3 == 0) return false;
        for (int i = 5; i * i <= n; i += 6) {
            if (n % i == 0 || n % (i + 2) == 0) return false;
        }
        return true;
    }
}
''',
        expected_behavior="Should translate Java Stream API to equivalent constructs",
        metadata={"features": ["streams", "lambda_expressions", "collectors", "parallel_processing"]}
    ))
    
    # ========================================================================
    # 5. C# SOURCE TESTS
    # ========================================================================
    
    test_cases.append(TestCase(
        name="csharp_linq_async",
        description="C# LINQ queries and async patterns",
        complexity=TestComplexity.INTERMEDIATE,
        test_type=TestType.CROSS_DOMAIN,
        source_language="csharp",
        target_languages=["javascript", "python", "java"],
        source_code='''
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

public class Product
{
    public int Id { get; set; }
    public string Name { get; set; }
    public decimal Price { get; set; }
    public string Category { get; set; }
    public int Stock { get; set; }
}

public class OrderService
{
    private readonly List<Product> products = new List<Product>
    {
        new Product { Id = 1, Name = "Laptop", Price = 999.99m, Category = "Electronics", Stock = 10 },
        new Product { Id = 2, Name = "Mouse", Price = 29.99m, Category = "Electronics", Stock = 50 },
        new Product { Id = 3, Name = "Desk", Price = 299.99m, Category = "Furniture", Stock = 5 },
        new Product { Id = 4, Name = "Chair", Price = 199.99m, Category = "Furniture", Stock = 15 }
    };
    
    public async Task<IEnumerable<Product>> GetProductsAsync(string category = null)
    {
        await Task.Delay(100); // Simulate async operation
        
        var query = products.AsQueryable();
        
        if (!string.IsNullOrEmpty(category))
        {
            query = query.Where(p => p.Category == category);
        }
        
        return query
            .Where(p => p.Stock > 0)
            .OrderByDescending(p => p.Price)
            .ToList();
    }
    
    public async Task<decimal> CalculateTotalValueAsync()
    {
        await Task.Delay(50);
        
        return products
            .Select(p => p.Price * p.Stock)
            .Sum();
    }
    
    public async Task<Dictionary<string, int>> GetStockByCategoryAsync()
    {
        await Task.Delay(50);
        
        return products
            .GroupBy(p => p.Category)
            .ToDictionary(
                g => g.Key,
                g => g.Sum(p => p.Stock)
            );
    }
}

// Usage
public class Program
{
    public static async Task Main(string[] args)
    {
        var service = new OrderService();
        
        var electronics = await service.GetProductsAsync("Electronics");
        Console.WriteLine("Electronics:");
        foreach (var product in electronics)
        {
            Console.WriteLine($"  {product.Name}: ${product.Price}");
        }
        
        var totalValue = await service.CalculateTotalValueAsync();
        Console.WriteLine($"Total inventory value: ${totalValue}");
        
        var stockByCategory = await service.GetStockByCategoryAsync();
        foreach (var kvp in stockByCategory)
        {
            Console.WriteLine($"{kvp.Key}: {kvp.Value} items");
        }
    }
}
''',
        expected_behavior="Should translate LINQ and C# async patterns",
        metadata={"features": ["linq", "async_await", "properties", "nullable_types", "generics"]}
    ))
    
    # ========================================================================
    # 6. C++ SOURCE TESTS
    # ========================================================================
    
    test_cases.append(TestCase(
        name="cpp_templates_stl",
        description="C++ templates and STL usage",
        complexity=TestComplexity.ADVANCED,
        test_type=TestType.CROSS_DOMAIN,
        source_language="cpp",
        target_languages=["python", "java", "csharp"],
        source_code='''
#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <memory>
#include <functional>

// Template class
template<typename T>
class Stack {
private:
    std::vector<T> elements;
    
public:
    void push(const T& element) {
        elements.push_back(element);
    }
    
    T pop() {
        if (elements.empty()) {
            throw std::runtime_error("Stack is empty");
        }
        T element = elements.back();
        elements.pop_back();
        return element;
    }
    
    bool empty() const {
        return elements.empty();
    }
    
    size_t size() const {
        return elements.size();
    }
};

// Template function
template<typename Container, typename Predicate>
auto filter(const Container& container, Predicate pred) {
    Container result;
    std::copy_if(container.begin(), container.end(), 
                 std::back_inserter(result), pred);
    return result;
}

// Modern C++ with auto and lambdas
int main() {
    // STL algorithms
    std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    
    auto evens = filter(numbers, [](int n) { return n % 2 == 0; });
    
    auto sum_of_squares = std::accumulate(evens.begin(), evens.end(), 0,
        [](int sum, int n) { return sum + n * n; });
    
    std::cout << "Sum of squares of even numbers: " << sum_of_squares << std::endl;
    
    // Smart pointers
    auto stack = std::make_unique<Stack<int>>();
    for (int i = 1; i <= 5; ++i) {
        stack->push(i * 10);
    }
    
    std::cout << "Stack contents: ";
    while (!stack->empty()) {
        std::cout << stack->pop() << " ";
    }
    std::cout << std::endl;
    
    // Range-based for loop
    std::vector<std::string> words = {"Hello", "from", "modern", "C++"};
    for (const auto& word : words) {
        std::cout << word << " ";
    }
    std::cout << std::endl;
    
    return 0;
}
''',
        expected_behavior="Should handle C++ templates and modern features",
        known_issues=["Templates and smart pointers need special handling"],
        metadata={"features": ["templates", "stl", "lambdas", "smart_pointers", "auto"]}
    ))
    
    # ========================================================================
    # 7. SQL TO PROGRAMMATIC TESTS
    # ========================================================================
    
    test_cases.append(TestCase(
        name="sql_complex_query",
        description="Complex SQL query to programmatic code",
        complexity=TestComplexity.INTERMEDIATE,
        test_type=TestType.CROSS_LANGUAGE,
        source_language="sql",
        target_languages=["python", "javascript", "java"],
        source_code='''
-- Complex analytical query with CTEs and window functions
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        customer_id,
        product_category,
        SUM(order_amount) as total_sales,
        COUNT(DISTINCT order_id) as order_count
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE order_date >= '2024-01-01'
    GROUP BY 1, 2, 3
),
customer_rankings AS (
    SELECT 
        month,
        customer_id,
        product_category,
        total_sales,
        order_count,
        ROW_NUMBER() OVER (PARTITION BY month, product_category ORDER BY total_sales DESC) as category_rank,
        PERCENT_RANK() OVER (PARTITION BY month ORDER BY total_sales DESC) as overall_percentile
    FROM monthly_sales
)
SELECT 
    cr.month,
    cr.customer_id,
    c.customer_name,
    cr.product_category,
    cr.total_sales,
    cr.order_count,
    cr.category_rank,
    ROUND(cr.overall_percentile * 100, 2) as percentile,
    CASE 
        WHEN cr.overall_percentile >= 0.9 THEN 'Top 10%'
        WHEN cr.overall_percentile >= 0.75 THEN 'Top 25%'
        WHEN cr.overall_percentile >= 0.5 THEN 'Top 50%'
        ELSE 'Bottom 50%'
    END as customer_tier
FROM customer_rankings cr
JOIN customers c ON cr.customer_id = c.customer_id
WHERE cr.category_rank <= 5
ORDER BY cr.month, cr.product_category, cr.category_rank;
''',
        expected_behavior="Should translate SQL logic to programmatic equivalents",
        metadata={"features": ["cte", "window_functions", "joins", "aggregations", "case_statements"]}
    ))
    
    # ========================================================================
    # 8. CROSS-LANGUAGE ROUNDTRIP TESTS
    # ========================================================================
    
    test_cases.append(TestCase(
        name="cross_language_data_structures",
        description="Data structure implementations across all languages",
        complexity=TestComplexity.ADVANCED,
        test_type=TestType.CROSS_LANGUAGE,
        source_language="python",
        target_languages=["javascript", "typescript", "java", "csharp", "cpp"],
        source_code='''
from typing import Generic, TypeVar, Optional, List
from dataclasses import dataclass

T = TypeVar('T')

class LinkedListNode(Generic[T]):
    def __init__(self, value: T, next_node: Optional['LinkedListNode[T]'] = None):
        self.value = value
        self.next = next_node

class LinkedList(Generic[T]):
    def __init__(self):
        self.head: Optional[LinkedListNode[T]] = None
        self.size = 0
    
    def append(self, value: T) -> None:
        if not self.head:
            self.head = LinkedListNode(value)
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = LinkedListNode(value)
        self.size += 1
    
    def prepend(self, value: T) -> None:
        self.head = LinkedListNode(value, self.head)
        self.size += 1
    
    def find(self, value: T) -> Optional[LinkedListNode[T]]:
        current = self.head
        while current:
            if current.value == value:
                return current
            current = current.next
        return None
    
    def remove(self, value: T) -> bool:
        if not self.head:
            return False
        
        if self.head.value == value:
            self.head = self.head.next
            self.size -= 1
            return True
        
        current = self.head
        while current.next:
            if current.next.value == value:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        return False
    
    def to_list(self) -> List[T]:
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result

# Binary tree implementation
@dataclass
class TreeNode(Generic[T]):
    value: T
    left: Optional['TreeNode[T]'] = None
    right: Optional['TreeNode[T]'] = None

class BinarySearchTree(Generic[T]):
    def __init__(self):
        self.root: Optional[TreeNode[T]] = None
    
    def insert(self, value: T) -> None:
        self.root = self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node: Optional[TreeNode[T]], value: T) -> TreeNode[T]:
        if node is None:
            return TreeNode(value)
        
        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        else:
            node.right = self._insert_recursive(node.right, value)
        
        return node
    
    def search(self, value: T) -> bool:
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node: Optional[TreeNode[T]], value: T) -> bool:
        if node is None:
            return False
        if node.value == value:
            return True
        if value < node.value:
            return self._search_recursive(node.left, value)
        return self._search_recursive(node.right, value)
    
    def inorder_traversal(self) -> List[T]:
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[TreeNode[T]], result: List[T]) -> None:
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

# Test both data structures
if __name__ == "__main__":
    # Test linked list
    ll = LinkedList[int]()
    for i in [5, 2, 8, 3, 9, 1]:
        ll.append(i)
    
    print(f"Linked list: {ll.to_list()}")
    print(f"Size: {ll.size}")
    
    ll.remove(8)
    print(f"After removing 8: {ll.to_list()}")
    
    # Test binary search tree
    bst = BinarySearchTree[int]()
    for i in [5, 2, 8, 3, 9, 1, 7]:
        bst.insert(i)
    
    print(f"BST inorder: {bst.inorder_traversal()}")
    print(f"Search for 7: {bst.search(7)}")
    print(f"Search for 4: {bst.search(4)}")
''',
        expected_behavior="Should maintain data structure semantics across all languages",
        metadata={"features": ["generics", "classes", "recursion", "data_structures"]}
    ))
    
    # ========================================================================
    # 9. EDGE CASES AND BREAKING TESTS
    # ========================================================================
    
    test_cases.append(TestCase(
        name="extreme_nested_complexity",
        description="Extremely nested and complex code structures",
        complexity=TestComplexity.BREAKING,
        test_type=TestType.EDGE_CASE,
        source_language="javascript",
        target_languages=["python", "java"],
        source_code='''
// Extreme nesting and complexity test
function extremeComplexity(data) {
    // Deep object nesting
    const config = {
        level1: {
            level2: {
                level3: {
                    level4: {
                        level5: {
                            processors: [
                                {
                                    name: "filter",
                                    fn: (items) => items.filter(x => {
                                        return x.data.metrics.performance.score > 
                                               x.data.metrics.baseline.average * 1.2;
                                    })
                                },
                                {
                                    name: "transform",
                                    fn: (items) => items.map(x => ({
                                        ...x,
                                        processed: {
                                            ...x.processed,
                                            timestamp: Date.now(),
                                            flags: {
                                                ...x.processed?.flags,
                                                validated: true
                                            }
                                        }
                                    }))
                                }
                            ]
                        }
                    }
                }
            }
        }
    };
    
    // Deeply nested function calls
    const result = data
        .map(item => ({
            ...item,
            value: ((((item.value * 2 + 3) / 4 - 5) * 6 + 7) / 8 - 9) * 10
        }))
        .filter(item => {
            const conditions = [
                item.value > 0,
                item.value < 1000,
                item.type === "valid",
                item.metadata?.tags?.includes("important"),
                !item.flags?.deleted
            ];
            return conditions.every(c => c) && 
                   (item.priority === "high" || 
                    (item.priority === "medium" && item.score > 50));
        })
        .reduce((acc, item) => {
            const key = `${item.category}_${item.subcategory || 'default'}`;
            if (!acc[key]) {
                acc[key] = {
                    items: [],
                    total: 0,
                    average: 0,
                    metadata: {
                        first_seen: Date.now(),
                        last_updated: Date.now(),
                        count: 0
                    }
                };
            }
            acc[key].items.push(item);
            acc[key].total += item.value;
            acc[key].metadata.count++;
            acc[key].average = acc[key].total / acc[key].metadata.count;
            acc[key].metadata.last_updated = Date.now();
            return acc;
        }, {});
    
    // Recursive async function with error handling
    async function processRecursively(obj, depth = 0) {
        if (depth > 10) {
            throw new Error("Maximum recursion depth exceeded");
        }
        
        try {
            if (Array.isArray(obj)) {
                return await Promise.all(
                    obj.map(item => processRecursively(item, depth + 1))
                );
            } else if (obj && typeof obj === 'object') {
                const processed = {};
                for (const [key, value] of Object.entries(obj)) {
                    processed[key] = await processRecursively(value, depth + 1);
                }
                return processed;
            } else if (typeof obj === 'function') {
                return await obj();
            } else {
                return obj;
            }
        } catch (error) {
            console.error(`Error at depth ${depth}:`, error);
            return null;
        }
    }
    
    // Extreme ternary nesting
    const category = 
        data.length > 100 ? 'huge' :
        data.length > 50 ? 'large' :
        data.length > 20 ? 'medium' :
        data.length > 10 ? 'small' :
        data.length > 5 ? 'tiny' :
        data.length > 0 ? 'minimal' : 'empty';
    
    return {
        result,
        config: config.level1.level2.level3.level4.level5,
        category,
        processRecursively
    };
}

// Test with complex data
const testData = Array.from({ length: 25 }, (_, i) => ({
    value: Math.random() * 100,
    type: i % 3 === 0 ? 'valid' : 'invalid',
    category: `cat_${i % 5}`,
    subcategory: i % 2 === 0 ? `subcat_${i % 3}` : null,
    priority: i % 4 === 0 ? 'high' : i % 3 === 0 ? 'medium' : 'low',
    score: Math.random() * 100,
    metadata: {
        tags: i % 2 === 0 ? ['important', 'verified'] : ['standard'],
        created: Date.now() - i * 1000000
    },
    flags: {
        deleted: i % 7 === 0,
        archived: i % 5 === 0
    },
    data: {
        metrics: {
            performance: {
                score: Math.random() * 100
            },
            baseline: {
                average: 50
            }
        }
    }
}));

console.log(extremeComplexity(testData));
''',
        expected_behavior="Should handle or gracefully fail on extreme complexity",
        known_issues=["May hit recursion or complexity limits in some languages"],
        metadata={"features": ["deep_nesting", "complex_expressions", "spread_syntax", "async_recursion"]}
    ))
    
    test_cases.append(TestCase(
        name="unicode_special_chars",
        description="Unicode and special character handling",
        complexity=TestComplexity.ADVANCED,
        test_type=TestType.EDGE_CASE,
        source_language="python",
        target_languages=["javascript", "java", "csharp"],
        source_code='''
# -*- coding: utf-8 -*-
"""Test Unicode and special character handling across languages"""

# Unicode string tests
unicode_tests = {
    "emoji": "Hello 👋 World 🌍! Python 🐍 is awesome! 🚀",
    "japanese": "こんにちは世界",
    "arabic": "مرحبا بالعالم",
    "russian": "Привет мир",
    "math": "∑(i=0 to n) = ∫∮ ∇×F·dA ≈ π²",
    "special": "Line1\\nLine2\\tTabbed\\r\\nWindows®™",
    "zalgo": "T̴̢̺͎̿ȅ̷̳s̸̱̈́t̶̮̾ ̷̱̈Z̸̬̈́ã̶̱ḽ̷̬g̴̣̈́o̸̤̎",
    "rtl": "‏מימין לשמאל",
    "combined": "café, naïve, résumé, Zürich"
}

def process_unicode_strings(strings_dict):
    """Process and analyze Unicode strings"""
    results = {}
    
    for name, text in strings_dict.items():
        results[name] = {
            "original": text,
            "length": len(text),
            "bytes": len(text.encode('utf-8')),
            "codepoints": [ord(c) for c in text[:5]],  # First 5 codepoints
            "reversed": text[::-1],
            "upper": text.upper(),
            "normalized": unicodedata.normalize('NFC', text) if 'unicodedata' in globals() else text
        }
    
    return results

# Test string interpolation with Unicode
def format_unicode_message(name: str, emoji: str, number: float) -> str:
    """Test various string formatting methods"""
    # f-string
    f_string = f"Hello {name} {emoji}! Your score is {number:.2f}%"
    
    # format method
    format_string = "Hello {} {}! Your score is {:.2f}%".format(name, emoji, number)
    
    # % formatting
    percent_string = "Hello %s %s! Your score is %.2f%%" % (name, emoji, number)
    
    # Template string (if available)
    template = f"""
    ╔══════════════════════════════╗
    ║ User: {name:<20} ║
    ║ Status: {emoji} Active       ║
    ║ Score: {number:>6.2f}%       ║
    ╚══════════════════════════════╝
    """
    
    return {
        "f_string": f_string,
        "format": format_string,
        "percent": percent_string,
        "template": template
    }

# Test edge cases
edge_cases = [
    "",  # Empty string
    " ",  # Single space
    "\\",  # Single backslash
    "\"'`",  # Quote characters
    "\\x00\\x01\\x02",  # Control characters
    "a" * 1000,  # Long string
    "${variable}",  # Template literal syntax
    "%(name)s",  # Format specifiers
    "{0} {1} {0}",  # Repeated placeholders
]

# Execute tests
results = process_unicode_strings(unicode_tests)
for name, result in results.items():
    print(f"{name}: {result['length']} chars, {result['bytes']} bytes")

formatted = format_unicode_message("María José", "🎉", 98.765)
for format_type, message in formatted.items():
    print(f"{format_type}:\\n{message}")

print("\\nEdge cases:")
for i, case in enumerate(edge_cases):
    print(f"{i}: repr={repr(case)}, len={len(case)}")
''',
        expected_behavior="Should handle Unicode and special characters correctly",
        known_issues=["Unicode handling varies significantly across languages"],
        metadata={"features": ["unicode", "string_formatting", "special_chars", "encoding"]}
    ))
    
    # ========================================================================
    # 10. PERFORMANCE AND OPTIMIZATION TESTS
    # ========================================================================
    
    test_cases.append(TestCase(
        name="performance_optimization_patterns",
        description="Performance-critical code patterns",
        complexity=TestComplexity.ADVANCED,
        test_type=TestType.PERFORMANCE,
        source_language="javascript",
        target_languages=["python", "java", "cpp"],
        source_code='''
// Performance-critical algorithms and optimizations

// Memoization implementation
function memoize(fn) {
    const cache = new Map();
    return function(...args) {
        const key = JSON.stringify(args);
        if (cache.has(key)) {
            return cache.get(key);
        }
        const result = fn.apply(this, args);
        cache.set(key, result);
        return result;
    };
}

// Dynamic programming - Longest Common Subsequence
const lcs = memoize(function(str1, str2, i = 0, j = 0) {
    if (i >= str1.length || j >= str2.length) {
        return 0;
    }
    
    if (str1[i] === str2[j]) {
        return 1 + lcs(str1, str2, i + 1, j + 1);
    }
    
    return Math.max(
        lcs(str1, str2, i + 1, j),
        lcs(str1, str2, i, j + 1)
    );
});

// Efficient prime sieve
function sieveOfEratosthenes(limit) {
    const sieve = new Array(limit + 1).fill(true);
    sieve[0] = sieve[1] = false;
    
    for (let i = 2; i * i <= limit; i++) {
        if (sieve[i]) {
            for (let j = i * i; j <= limit; j += i) {
                sieve[j] = false;
            }
        }
    }
    
    return sieve.reduce((primes, isPrime, num) => {
        if (isPrime) primes.push(num);
        return primes;
    }, []);
}

// Matrix multiplication with cache optimization
function matrixMultiply(A, B) {
    const rowsA = A.length;
    const colsA = A[0].length;
    const colsB = B[0].length;
    
    // Initialize result matrix
    const C = Array(rowsA).fill(null).map(() => Array(colsB).fill(0));
    
    // Cache-friendly multiplication (row-major order)
    for (let i = 0; i < rowsA; i++) {
        for (let k = 0; k < colsA; k++) {
            const aik = A[i][k];
            for (let j = 0; j < colsB; j++) {
                C[i][j] += aik * B[k][j];
            }
        }
    }
    
    return C;
}

// Parallel-like processing simulation
async function parallelMap(items, asyncFn, concurrency = 4) {
    const results = [];
    const executing = [];
    
    for (const [index, item] of items.entries()) {
        const promise = asyncFn(item).then(result => {
            results[index] = result;
        });
        
        executing.push(promise);
        
        if (executing.length >= concurrency) {
            await Promise.race(executing);
            executing.splice(executing.findIndex(p => p === promise), 1);
        }
    }
    
    await Promise.all(executing);
    return results;
}

// Benchmark function
function benchmark(name, fn, iterations = 1000) {
    const start = performance.now();
    
    for (let i = 0; i < iterations; i++) {
        fn();
    }
    
    const end = performance.now();
    const avgTime = (end - start) / iterations;
    
    console.log(`${name}: ${avgTime.toFixed(3)}ms average (${iterations} iterations)`);
    return avgTime;
}

// Run performance tests
console.log("Performance Test Results:");

// Test memoization effectiveness
benchmark("LCS without memoization", () => {
    const str1 = "ABCDGH";
    const str2 = "AEDFHR";
    // Direct recursive call would be much slower
    lcs(str1, str2);
});

// Test prime generation
benchmark("Sieve of Eratosthenes (n=10000)", () => {
    sieveOfEratosthenes(10000);
}, 10);

// Test matrix multiplication
const A = Array(50).fill(null).map(() => Array(50).fill(null).map(() => Math.random()));
const B = Array(50).fill(null).map(() => Array(50).fill(null).map(() => Math.random()));

benchmark("Matrix multiplication 50x50", () => {
    matrixMultiply(A, B);
}, 100);

// Test parallel processing
(async () => {
    const urls = Array(20).fill(null).map((_, i) => `https://api.example.com/data/${i}`);
    
    const mockFetch = async (url) => {
        await new Promise(resolve => setTimeout(resolve, Math.random() * 100));
        return { url, data: Math.random() };
    };
    
    console.time("Parallel fetch");
    await parallelMap(urls, mockFetch, 5);
    console.timeEnd("Parallel fetch");
})();
''',
        expected_behavior="Should translate performance patterns appropriately",
        metadata={"features": ["memoization", "dynamic_programming", "matrix_ops", "parallel_processing", "benchmarking"]}
    ))
    
    # ========================================================================
    # 11. RUNA-SPECIFIC TESTS
    # ========================================================================
    
    test_cases.append(TestCase(
        name="runa_complete_features",
        description="Complete Runa language feature test",
        complexity=TestComplexity.ADVANCED,
        test_type=TestType.FEATURE_SHOWCASE,
        source_language="runa",
        target_languages=["python", "typescript", "java"],
        source_code='''
# Comprehensive Runa feature demonstration

# Type definitions with constraints
Type Comparable[T] is Interface with:
    compare_to as Function[T, Integer]

Type Serializable is Interface with:
    to_json as Function[String]
    from_json as Function[String, Self]

# Algebraic data type
Type Result[T, E] is
    | Success with value as T
    | Failure with error as E

# Generic function with constraints
Process called "BinarySearch"[T: Comparable] that takes array (List[T]) and target (T) returns Result[Integer, String]:
    Let low be 0
    Let high be length of array minus 1
    
    While low is less than or equal to high:
        Let mid be (low plus high) divided by 2
        Let comparison be array at index mid compare_to target
        
        If comparison is equal to 0:
            Return Success with value as mid
        Otherwise if comparison is less than 0:
            Set low to mid plus 1
        Otherwise:
            Set high to mid minus 1
    
    Return Failure with error as "Element not found"

# Pattern matching with guards
Process called "DescribeResult"[T, E] that takes result (Result[T, E]) returns String:
    Match result:
        When Success with value as v If v is of type Integer:
            Return "Found at index " followed by v
        When Success with value as v:
            Return "Success: " followed by v
        When Failure with error as e:
            Return "Error: " followed by e

# Async process with error handling
Async Process called "FetchAndProcess" that takes urls (List[String]) returns List[Result[Dictionary, String]]:
    Let results be list containing
    
    For each url in urls:
        Try:
            Let response be await HttpGet with url as url
            Let data be ParseJson with json as response
            Add Success with value as data to results
        Catch error:
            Add Failure with error as "Failed to fetch " followed by url to results
    
    Return results

# Higher-order functions and pipelines
Let numbers be list containing 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

Let processed be numbers
    |> Filter with predicate as lambda n: n modulo 2 is equal to 0
    |> Map with transform as lambda n: n multiplied by n
    |> Reduce with reducer as lambda acc and n: acc plus n and initial as 0

Display "Sum of squares of even numbers: " followed by processed

# AI-to-AI communication
@Task:
    objective: "Implement efficient sorting algorithm"
    constraints: ["Must handle 1M+ elements", "Stable sort required"]
@End_Task

@Reasoning:
    Choosing merge sort because:
    1. It's stable (preserves relative order of equal elements)
    2. O(n log n) worst-case performance
    3. Can be parallelized for large datasets
@End_Reasoning

@Implementation:
Process called "MergeSort"[T: Comparable] that takes array (List[T]) returns List[T]:
    If length of array is less than or equal to 1:
        Return array
    
    Let mid be length of array divided by 2
    Let left be array at index 0 to index mid minus 1
    Let right be array at index mid to index length of array minus 1
    
    Let sorted_left be MergeSort with array as left
    Let sorted_right be MergeSort with array as right
    
    Return Merge with left as sorted_left and right as sorted_right
@End_Implementation

# Complex type with methods
Type Matrix is Dictionary with:
    rows as Integer
    cols as Integer
    data as List[List[Float]]
    
    multiply as Function[Matrix, Matrix]
    transpose as Function[Matrix]
    determinant as Function[Float]

# Neural network definition (AI-specific feature)
Define neural network "TextClassifier":
    Input layer accepts sequences of 512 tokens
    Use transformer architecture with 12 layers
    Hidden dimension is 768
    Number of attention heads is 12
    Output layer has 5 classes with softmax activation

Configure training for TextClassifier:
    Use dataset "movie_reviews" with 90/10 train/validation split
    Apply dropout with rate 0.1
    Use AdamW optimizer with learning rate 2e-5
    Train for 10 epochs with early stopping
    Save best model based on validation accuracy

# Test everything
Let test_array be list containing 5, 2, 8, 1, 9, 3, 7
Let sorted_array be MergeSort with array as test_array
Display "Sorted: " followed by sorted_array

Let search_result be BinarySearch with array as sorted_array and target as 7
Display DescribeResult with result as search_result
''',
        expected_behavior="Should demonstrate all Runa features correctly",
        metadata={"features": ["all_runa_features", "ai_annotations", "generics", "pattern_matching", "async", "neural_networks"]}
    ))
    
    return test_cases

# ============================================================================
# TEST EXECUTION HELPERS
# ============================================================================

def generate_test_metadata(test_case: TestCase) -> Dict[str, Any]:
    """Generate additional metadata for test execution"""
    return {
        "test_id": f"{test_case.source_language}_{test_case.name}",
        "timestamp": "2024-01-01T00:00:00Z",  # Will be set by runner
        "version": "1.0.0",
        "tags": [
            test_case.complexity.value,
            test_case.test_type.value,
            test_case.source_language
        ] + test_case.target_languages,
        "expected_features": test_case.metadata.get("features", []),
        "known_issues": test_case.known_issues or [],
        "validation_rules": {
            "syntax": True,
            "semantics": True,
            "roundtrip": test_case.test_type == TestType.ROUNDTRIP,
            "performance": test_case.test_type == TestType.PERFORMANCE
        }
    }

def export_test_cases_json(output_file: str = "tier1_test_cases.json"):
    """Export all test cases to JSON format"""
    import json
    
    test_cases = get_tier1_test_cases()
    
    export_data = []
    for test_case in test_cases:
        export_data.append({
            "name": test_case.name,
            "description": test_case.description,
            "complexity": test_case.complexity.value,
            "test_type": test_case.test_type.value,
            "source_language": test_case.source_language,
            "target_languages": test_case.target_languages,
            "source_code": test_case.source_code,
            "expected_runa": test_case.expected_runa,
            "expected_behavior": test_case.expected_behavior,
            "known_issues": test_case.known_issues,
            "metadata": {**test_case.metadata, **generate_test_metadata(test_case)}
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"Exported {len(export_data)} test cases to {output_file}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Get all test cases
    test_cases = get_tier1_test_cases()
    
    # Print summary
    print(f"Total test cases: {len(test_cases)}")
    print("\nTest cases by source language:")
    
    by_source = {}
    for tc in test_cases:
        by_source.setdefault(tc.source_language, []).append(tc)
    
    for lang, cases in sorted(by_source.items()):
        print(f"  {lang}: {len(cases)} tests")
        for case in cases:
            print(f"    - {case.name} ({case.complexity.value})")
    
    print("\nTest cases by complexity:")
    by_complexity = {}
    for tc in test_cases:
        by_complexity.setdefault(tc.complexity, []).append(tc)
    
    for complexity, cases in sorted(by_complexity.items(), key=lambda x: x[0].value):
        print(f"  {complexity.value}: {len(cases)} tests")
    
    # Export to JSON
    export_test_cases_json()