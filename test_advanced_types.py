# Generated Python code from Runa
# Natural language programming made executable

import sys
import math

# Helper functions for Runa built-ins

def calculate_interest(principal, rate, years=1):
    """Calculate simple interest."""
    return principal * rate * years

def calculate_total(*args, **kwargs):
    """Calculate total from various arguments."""
    total = 0
    for value in args:
        if isinstance(value, (int, float)):
            total += value
    for value in kwargs.values():
        if isinstance(value, (int, float)):
            total += value
    return total

def calculate_discount(original_price, discount_rate):
    """Calculate discounted price."""
    discount_amount = original_price * discount_rate
    return original_price - discount_amount

def format_currency(amount, symbol="$"):
    """Format amount as currency."""
    return f"{symbol}{amount:.2f}"

def main():
    # Local variables
    message = None
    numbers = None
    optional_age = None
    optional_name = None
    tmp_1 = None
    tmp_2 = None
    user_id = None
    value = None
    words = None

    value = 42
    message = "Hello"
    tmp_1 = [1, 2, 3]
    numbers = tmp_1
    tmp_2 = ["a", "b", "c"]
    words = tmp_2
    optional_name = "John"
    optional_age = 25
    user_id = 12345
    print("Advanced type system test completed")
    return

if __name__ == '__main__':
    main()
