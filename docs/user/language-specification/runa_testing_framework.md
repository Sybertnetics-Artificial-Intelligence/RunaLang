# Runa Testing Framework Specification

**Version:** 1.0
**Status:** Canonical
**Last Updated:** 2025-10-08

---

## Overview

**Runa replaces all testing frameworks with built-in test syntax.**

**Replaces:**
- ❌ Jest, Mocha, Jasmine (JavaScript)
- ❌ pytest, unittest (Python)
- ❌ JUnit, TestNG (Java)
- ❌ RSpec, Minitest (Ruby)
- ❌ Go testing package

---

## Basic Test File

**File:** `tests/test_calculator.runa`

```runa
Note: Unit tests for calculator module
Note: Replaces Jest, pytest, JUnit, etc.

Import "calculator.runa" as Calc
Import "runa/test" as Test

@Reasoning:
  Test suite for calculator functions.
  Ensures arithmetic operations work correctly.
@End Reasoning

Process called "test_addition":
    Note: Test addition function
    Let result be Calc.add(2, 3)
    Call Test.assert_equal(result, 5, "2 + 3 should equal 5")

    Let result2 be Calc.add(-1, 1)
    Call Test.assert_equal(result2, 0, "(-1) + 1 should equal 0")
End Process

Process called "test_subtraction":
    Note: Test subtraction function
    Let result be Calc.subtract(10, 3)
    Call Test.assert_equal(result, 7, "10 - 3 should equal 7")

    Let result2 be Calc.subtract(5, 10)
    Call Test.assert_equal(result2, -5, "5 - 10 should equal -5")
End Process

Process called "test_multiplication":
    Let result be Calc.multiply(4, 5)
    Call Test.assert_equal(result, 20, "4 * 5 should equal 20")
End Process

Process called "test_division":
    Let result be Calc.divide(10, 2)
    Call Test.assert_equal(result, 5, "10 / 2 should equal 5")
End Process

Process called "test_division_by_zero":
    Note: Test error handling
    Call Test.assert_raises(ZeroDivisionError, divide_by_zero)
End Process

Process called "divide_by_zero":
    Call Calc.divide(10, 0)
End Process

Note: Test runner discovers all processes starting with "test_"
```

**Usage:**
```bash
# Run all tests
runa test

# Run specific test file
runa test tests/test_calculator.runa

# Run with coverage
runa test --coverage
```

---

## Test Assertions

```runa
Process called "test_all_assertions":
    Note: Equality assertions
    Call Test.assert_equal(5, 5)
    Call Test.assert_not_equal(5, 10)

    Note: Boolean assertions
    Call Test.assert_true(true)
    Call Test.assert_false(false)

    Note: Null checks
    Call Test.assert_null(null)
    Call Test.assert_not_null("value")

    Note: Collection assertions
    Let list be a list containing 1, 2, 3
    Call Test.assert_contains(list, 2)
    Call Test.assert_length(list, 3)

    Note: String assertions
    Call Test.assert_starts_with("Hello World", "Hello")
    Call Test.assert_ends_with("Hello World", "World")
    Call Test.assert_contains_substring("Hello World", "lo Wo")

    Note: Numeric assertions
    Call Test.assert_greater_than(10, 5)
    Call Test.assert_less_than(5, 10)
    Call Test.assert_in_range(7, 5, 10)

    Note: Exception assertions
    Call Test.assert_raises(ValueError, function_that_throws)
End Process
```

---

## Test Fixtures (Setup/Teardown)

```runa
Type called "TestContext":
    database as Database
    test_user as User
End Type

Process called "setup" returns TestContext:
    Note: Run before each test
    Let db be DB.connect_test_database()
    Let user be create_test_user("test@example.com")

    Return a value of type TestContext with
        database as db,
        test_user as user
End Process

Process called "teardown" that takes context as TestContext:
    Note: Run after each test
    Call DB.disconnect(context.database)
    Call delete_test_user(context.test_user)
End Process

Process called "test_user_creation":
    Let context be setup()

    Note: Test logic here
    Let user be context.test_user
    Call Test.assert_equal(user.email, "test@example.com")

    Call teardown(context)
End Process
```

---

## Parametrized Tests

```runa
Process called "test_addition_parametrized":
    Let test_cases be a list containing:
        case(2, 3, 5),
        case(10, 5, 15),
        case(-1, 1, 0),
        case(0, 0, 0),
        case(100, 200, 300)

    For Each test_case in test_cases:
        Let result be Calc.add(test_case.a, test_case.b)
        Call Test.assert_equal(
            result,
            test_case.expected,
            string_from(test_case.a) + " + " + string_from(test_case.b) + " should equal " + string_from(test_case.expected)
        )
    End For
End Process

Type called "TestCase":
    a as Integer
    b as Integer
    expected as Integer
End Type

Process called "case" that takes a as Integer, b as Integer, expected as Integer returns TestCase:
    Return a value of type TestCase with a as a, b as b, expected as expected
End Process
```

---

## Mocking

```runa
Process called "test_with_mock":
    Note: Create mock database
    Let mock_db be Test.create_mock("Database")

    Note: Define mock behavior
    Call Test.when(mock_db, "query", a list containing "users")
        .then_return(a list containing test_user())

    Note: Test function that uses database
    Let users be fetch_users(mock_db)

    Call Test.assert_length(users, 1)
    Call Test.verify_called(mock_db, "query", a list containing "users")
End Process

Process called "test_user" returns User:
    Return a value of type User with
        id as 1,
        email as "test@example.com"
End Process
```

---

## Integration Tests

**File:** `tests/integration/test_api.runa`

```runa
Note: Integration tests for API

Import "runa/test" as Test
Import "runa/http" as HTTP

Process called "test_user_registration_flow":
    Note: Start test server
    Let server be Test.start_test_server("localhost", 8080)

    Note: Register user
    Let response be HTTP.post("http://localhost:8080/register", a dictionary containing:
        "email" as "newuser@example.com",
        "password" as "securepassword"
    End Dictionary)

    Call Test.assert_equal(response.status_code, 201)
    Call Test.assert_contains(response.body, "user_id")

    Note: Login
    Let login_response be HTTP.post("http://localhost:8080/login", a dictionary containing:
        "email" as "newuser@example.com",
        "password" as "securepassword"
    End Dictionary)

    Call Test.assert_equal(login_response.status_code, 200)
    Call Test.assert_contains(login_response.body, "auth_token")

    Note: Stop test server
    Call Test.stop_test_server(server)
End Process
```

---

## Test Coverage

```runa
Process called "generate_coverage_report":
    Note: Run tests with coverage tracking
    Let results be Test.run_all_tests_with_coverage("tests/")

    Call display("Total Coverage: " + string_from(results.coverage_percent) + "%")

    Note: Generate HTML report
    Call Test.generate_coverage_html(results, "coverage/index.html")

    Note: Enforce minimum coverage
    If results.coverage_percent < 80.0:
        Call panic("Coverage below 80% threshold")
    End If
End Process
```

---

## Jest/Pytest Comparison

**Before (Jest):**
```javascript
describe('Calculator', () => {
  test('adds two numbers', () => {
    expect(add(2, 3)).toBe(5);
  });

  test('subtracts two numbers', () => {
    expect(subtract(10, 3)).toBe(7);
  });
});
```

**Before (pytest):**
```python
def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(10, 3) == 7
```

**After (Runa):**
```runa
Process called "test_add":
    Call Test.assert_equal(add(2, 3), 5)
End Process

Process called "test_subtract":
    Call Test.assert_equal(subtract(10, 3), 7)
End Process
```

---

## Snapshot Testing

```runa
Process called "test_ui_component_snapshot":
    Let component be render_user_card(test_user())

    Note: Create or compare snapshot
    Call Test.assert_snapshot_matches(component, "user_card_snapshot")
End Process

Process called "update_snapshots":
    Note: Update all snapshots
    Call Test.update_all_snapshots("tests/")
End Process
```

---

## Performance/Benchmark Tests

```runa
Process called "test_performance":
    Let start_time be current_time_milliseconds()

    Note: Run operation 1000 times
    For i from 1 to 1000:
        Call expensive_operation()
    End For

    Let end_time be current_time_milliseconds()
    Let duration be end_time - start_time

    Call Test.assert_less_than(duration, 1000, "Operation should complete in under 1 second")
End Process

Process called "benchmark_sorting_algorithms":
    Let data be generate_random_list(10000)

    Let bubble_time be Test.benchmark(bubble_sort, data)
    Let quick_time be Test.benchmark(quick_sort, data)
    Let merge_time be Test.benchmark(merge_sort, data)

    Call display("Bubble Sort: " + string_from(bubble_time) + "ms")
    Call display("Quick Sort: " + string_from(quick_time) + "ms")
    Call display("Merge Sort: " + string_from(merge_time) + "ms")
End Process
```

---

## Summary

**Runa replaces testing frameworks with:**
- ✅ Built-in test syntax (no external framework)
- ✅ Unified assertions
- ✅ Integrated mocking and fixtures
- ✅ Coverage reporting
- ✅ Snapshot testing
- ✅ Performance benchmarks

**Stop using:** Jest, pytest, JUnit, RSpec
**Start using:** `test_*.runa` files with built-in Test module

---

**End of Document**
