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
    buffer = None
    tmp_1 = None
    x = None

    x = 42
    tmp_1 = [1, 2, 3]
    buffer = tmp_1
    # TODO: delete %buffer_3a2a2791
    print("Memory management test completed")
    return

if __name__ == '__main__':
    main()
