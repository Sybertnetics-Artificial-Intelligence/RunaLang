# Runa Unit Testing Framework

## Overview

The Runa Unit Testing Framework provides a comprehensive solution for testing Runa applications. It offers a simple, intuitive syntax for defining test suites and cases while providing powerful features for test organization, execution, and reporting.

## Core Features

### Test Suite Creation

```runa
import runa.test.unit_test_framework as test

Let my_suite = test.create_test_suite("Suite Name", "Optional description")
```

### Adding Tests

```runa
my_suite.add_test("Test Name", function() {
    # Test logic here
    test.assert_equal(actual, expected, "Optional message")
}, ["optional", "tags"])
```

### Lifecycle Hooks

```runa
# Run once before all tests in the suite
my_suite.before_all = function() {
    # Setup resources, connections, etc.
}

# Run once after all tests in the suite
my_suite.after_all = function() {
    # Clean up resources, connections, etc.
}

# Run before each test
my_suite.before_each = function() {
    # Setup for individual test
}

# Run after each test
my_suite.after_each = function() {
    # Clean up after individual test
}
```

### Assertions

The framework provides a rich set of assertions:

```runa
test.assert_true(value, "Optional message")
test.assert_false(value, "Optional message")
test.assert_equal(actual, expected, "Optional message")
test.assert_not_equal(actual, expected, "Optional message")
test.assert_deep_equal(actual, expected, "Optional message")
test.assert_greater_than(actual, expected, "Optional message")
test.assert_less_than(actual, expected, "Optional message")
test.assert_throws(function, errorType, "Optional message")
test.assert_does_not_throw(function, "Optional message")
test.assert_contains(collection, item, "Optional message")
test.assert_match(string, pattern, "Optional message")
```

### Test Configuration

Configure test execution options:

```runa
my_suite.configure({
    "fail_fast": true,           # Stop on first failure
    "timeout": 5000,             # Test timeout in milliseconds
    "report_format": "json",     # Output format (json, xml, text)
    "report_file": "./report.json", # Save results to file
    "verbose": true,             # Detailed output
    "color_output": true,        # Colored console output
    "test_dir": "./tests"        # Custom test directory
})
```

### Running Tests

```runa
# Run all tests in the suite
Let results = my_suite.run()

# Run tests with specific tags
Let results = my_suite.run(["tag1", "tag2"])

# Examine results
Print("Passed: " + results.passed)
Print("Failed: " + results.failed)
Print("Errors: " + results.errors)
Print("Skipped: " + results.skipped)
```

### Skipping Tests

```runa
# Skip a test that's not ready yet
my_suite.skip("Test to skip", function() {
    # This test will be marked as skipped
}, ["skipped"])
```

## Advanced Features

### Test Filtering

Run specific tests based on name patterns or tags:

```runa
my_suite.run({
    "include_tags": ["critical", "core"],
    "exclude_tags": ["slow", "network"],
    "pattern": "Auth*"  # Run tests whose names match the pattern
})
```

### Parameterized Tests

Run a test with multiple sets of input data:

```runa
my_suite.add_parameterized_test("Parameterized Test", 
    function(a, b, expected) {
        Let result = a + b
        test.assert_equal(result, expected)
    },
    [
        [1, 1, 2],
        [2, 3, 5],
        [5, 8, 13]
    ],
    ["math"]
)
```

### Mocking

Create mock objects to isolate tests from external dependencies:

```runa
Let db_mock = test.create_mock("Database")
db_mock.method("query").returns(["result1", "result2"])

# Use the mock in tests
Let results = db_mock.query("SELECT * FROM users")
test.assert_equal(results.length, 2)
```

### Custom Reporters

Create custom test reporters:

```runa
Let custom_reporter = {
    "start_suite": function(suite_name) {
        Print("Starting suite: " + suite_name)
    },
    "end_suite": function(suite_name, results) {
        Print("Suite completed: " + suite_name)
    },
    "start_test": function(test_name) {
        Print("Running: " + test_name)
    },
    "end_test": function(test_name, result) {
        Print("Test " + test_name + ": " + result.status)
    }
}

my_suite.set_reporter(custom_reporter)
```

## Example

Here's a complete example showing how to use the testing framework:

```runa
import runa.test.unit_test_framework as test

# Create a test suite
Let math_suite = test.create_test_suite("Math Tests", "Testing math operations")

# Add setup
math_suite.before_all = function() {
    Print("Setting up test environment")
}

# Add tests
math_suite.add_test("Addition Test", function() {
    Let sum = 2 + 2
    test.assert_equal(sum, 4, "2 + 2 should equal 4")
}, ["basic"])

math_suite.add_test("Division Test", function() {
    Let result = 10 / 2
    test.assert_equal(result, 5, "10 / 2 should equal 5")
}, ["basic"])

# Run the tests
Let results = math_suite.run()

# Display results
Print("Tests run: " + (results.passed + results.failed))
Print("Passed: " + results.passed)
Print("Failed: " + results.failed)
```

## Best Practices

1. **Organize Related Tests**: Group related tests into the same suite for better organization.

2. **Use Descriptive Names**: Give your tests clear, descriptive names that indicate what they're testing.

3. **Keep Tests Independent**: Each test should be able to run independently without relying on other tests.

4. **Clean Up After Tests**: Use `after_each` and `after_all` hooks to clean up resources.

5. **Test One Thing at a Time**: Each test should focus on testing a single aspect or functionality.

6. **Use Tags Effectively**: Tag tests to categorize them (e.g., "slow", "network", "critical") for selective running.

7. **Manage Test Data**: Create test data in setup methods and clean it up afterward.

8. **Avoid Test Interdependencies**: Tests should not depend on the state from other tests.

9. **Test Edge Cases**: Include tests for boundary conditions and error cases.

10. **Keep Tests Fast**: Fast tests enable more frequent testing during development.

## CLI Usage

The Runa test runner can be used from the command line:

```
runa test [options] [test_files]

Options:
  --tag=<tag>         Run tests with specific tag
  --exclude=<tag>     Exclude tests with specific tag
  --pattern=<pattern> Run tests matching name pattern
  --report=<format>   Output format (json, xml, text)
  --output=<file>     Save report to file
  --fail-fast         Stop on first failure
  --verbose           Show detailed output
  --timeout=<ms>      Test timeout in milliseconds
```

## References

- [API Reference](../API/TestFramework.md)
- [Example Tests](../../src/tests/example_test.runa) 