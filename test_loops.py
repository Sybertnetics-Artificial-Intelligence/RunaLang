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
    i = None
    number = None
    number_index = None
    number_iterable = None
    numbers = None
    repeat_counter_0 = None
    tmp_1 = None
    tmp_10 = None
    tmp_2 = None
    tmp_3 = None
    tmp_4 = None
    tmp_5 = None
    tmp_6 = None
    tmp_7 = None
    tmp_8 = None
    tmp_9 = None

    tmp_1 = [1, 2, 3, 4, 5]
    numbers = tmp_1
    number_iterable = numbers
    number_index = 0
    tmp_2 = len(number_iterable)
    tmp_3 = number_index < tmp_2
    while number_index < tmp_2:
        number = number_iterable[number_index]
        print(number)
        tmp_4 = number_index + 1
        number_index = tmp_4
    i = 1
    tmp_5 = i < 5
    while i < 5:
        print(i)
        tmp_6 = i + 1
        i = tmp_6
    tmp_7 = i < 10
    while i < 10:
        tmp_8 = i + 1
        i = tmp_8
        print(i)
    repeat_counter_0 = 0
    tmp_9 = repeat_counter_0 < 3
    while repeat_counter_0 < 3:
        print("Hello")
        tmp_10 = repeat_counter_0 + 1
        repeat_counter_0 = tmp_10
    return

if __name__ == '__main__':
    main()
