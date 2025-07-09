"""
Runa Standard Library - Math Module

Provides mathematical functions and constants for Runa programs.
"""

import math as py_math
import random as py_random

# Mathematical constants
PI = py_math.pi
E = py_math.e
TAU = py_math.tau
INFINITY = py_math.inf

def absolute_value(x):
    """Calculate the absolute value of a number."""
    return abs(x)

def round_number(x, digits=0):
    """Round a number to the specified number of digits."""
    return round(x, digits)

def floor_value(x):
    """Return the floor of a number."""
    return py_math.floor(x)

def ceiling_value(x):
    """Return the ceiling of a number."""
    return py_math.ceil(x)

def square_root(x):
    """Calculate the square root of a number."""
    return py_math.sqrt(x)

def power(base, exponent):
    """Calculate base raised to the power of exponent."""
    return py_math.pow(base, exponent)

def logarithm(x, base=py_math.e):
    """Calculate the logarithm of x to the given base."""
    if base == py_math.e:
        return py_math.log(x)
    else:
        return py_math.log(x, base)

def sine(x):
    """Calculate the sine of x (in radians)."""
    return py_math.sin(x)

def cosine(x):
    """Calculate the cosine of x (in radians)."""
    return py_math.cos(x)

def tangent(x):
    """Calculate the tangent of x (in radians)."""
    return py_math.tan(x)

def arc_sine(x):
    """Calculate the arc sine of x."""
    return py_math.asin(x)

def arc_cosine(x):
    """Calculate the arc cosine of x."""
    return py_math.acos(x)

def arc_tangent(x):
    """Calculate the arc tangent of x."""
    return py_math.atan(x)

def degrees_to_radians(degrees):
    """Convert degrees to radians."""
    return py_math.radians(degrees)

def radians_to_degrees(radians):
    """Convert radians to degrees."""
    return py_math.degrees(radians)

def maximum(*args):
    """Return the maximum value from the arguments."""
    return max(args)

def minimum(*args):
    """Return the minimum value from the arguments."""
    return min(args)

def sum_values(*args):
    """Calculate the sum of all arguments."""
    return sum(args)

def average(*args):
    """Calculate the average of all arguments."""
    return sum(args) / len(args) if args else 0

def random_number(min_val=0.0, max_val=1.0):
    """Generate a random number between min_val and max_val."""
    return py_random.uniform(min_val, max_val)

def random_integer(min_val, max_val):
    """Generate a random integer between min_val and max_val (inclusive)."""
    return py_random.randint(min_val, max_val)

def random_choice(items):
    """Choose a random item from a list."""
    return py_random.choice(items)

def factorial(n):
    """Calculate the factorial of n."""
    return py_math.factorial(int(n))

def greatest_common_divisor(a, b):
    """Calculate the greatest common divisor of a and b."""
    return py_math.gcd(int(a), int(b))

def is_finite(x):
    """Check if a number is finite."""
    return py_math.isfinite(x)

def is_infinite(x):
    """Check if a number is infinite."""
    return py_math.isinf(x)

def is_nan(x):
    """Check if a number is NaN (Not a Number)."""
    return py_math.isnan(x)

# Runa-style function names for natural language calling
calculate_absolute_value = absolute_value
calculate_square_root = square_root
calculate_power = power
calculate_logarithm = logarithm
calculate_sine = sine
calculate_cosine = cosine
calculate_tangent = tangent
calculate_maximum = maximum
calculate_minimum = minimum
calculate_sum = sum_values
calculate_average = average
generate_random_number = random_number
generate_random_integer = random_integer
choose_random_item = random_choice
calculate_factorial = factorial
find_greatest_common_divisor = greatest_common_divisor
check_if_finite = is_finite
check_if_infinite = is_infinite
check_if_nan = is_nan