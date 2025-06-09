"""
Mathematical functions for the Runa programming language.

This module provides standard mathematical functions and constants.
"""

import math
import random
import cmath
import statistics
from typing import List, Any, Optional, Union, Dict

from ...vm.vm import VirtualMachine, VMValue, VMValueType


def register_math_functions(vm: VirtualMachine) -> None:
    """
    Register mathematical functions with the VM.
    
    Args:
        vm: The virtual machine to register the functions with
    """
    # Constants
    vm.native_functions["math_pi"] = _math_pi
    vm.native_functions["math_e"] = _math_e
    vm.native_functions["math_tau"] = _math_tau
    vm.native_functions["math_inf"] = _math_inf
    vm.native_functions["math_nan"] = _math_nan
    
    # Basic math
    vm.native_functions["math_abs"] = _math_abs
    vm.native_functions["math_ceil"] = _math_ceil
    vm.native_functions["math_floor"] = _math_floor
    vm.native_functions["math_round"] = _math_round
    vm.native_functions["math_trunc"] = _math_trunc
    vm.native_functions["math_sqrt"] = _math_sqrt
    vm.native_functions["math_pow"] = _math_pow
    vm.native_functions["math_exp"] = _math_exp
    vm.native_functions["math_log"] = _math_log
    vm.native_functions["math_log10"] = _math_log10
    vm.native_functions["math_log2"] = _math_log2
    
    # Trigonometry
    vm.native_functions["math_sin"] = _math_sin
    vm.native_functions["math_cos"] = _math_cos
    vm.native_functions["math_tan"] = _math_tan
    vm.native_functions["math_asin"] = _math_asin
    vm.native_functions["math_acos"] = _math_acos
    vm.native_functions["math_atan"] = _math_atan
    vm.native_functions["math_atan2"] = _math_atan2
    vm.native_functions["math_degrees"] = _math_degrees
    vm.native_functions["math_radians"] = _math_radians
    
    # Statistics
    vm.native_functions["math_min"] = _math_min
    vm.native_functions["math_max"] = _math_max
    vm.native_functions["math_sum"] = _math_sum
    vm.native_functions["math_mean"] = _math_mean
    vm.native_functions["math_median"] = _math_median
    vm.native_functions["math_mode"] = _math_mode
    vm.native_functions["math_stdev"] = _math_stdev
    vm.native_functions["math_variance"] = _math_variance
    
    # Random
    vm.native_functions["math_random"] = _math_random
    vm.native_functions["math_random_int"] = _math_random_int
    vm.native_functions["math_random_choice"] = _math_random_choice
    vm.native_functions["math_random_shuffle"] = _math_random_shuffle
    vm.native_functions["math_random_seed"] = _math_random_seed


# Constants

def _math_pi(vm: VirtualMachine) -> VMValue:
    """Return the mathematical constant π."""
    return VMValue(VMValueType.FLOAT, math.pi)

def _math_e(vm: VirtualMachine) -> VMValue:
    """Return the mathematical constant e."""
    return VMValue(VMValueType.FLOAT, math.e)

def _math_tau(vm: VirtualMachine) -> VMValue:
    """Return the mathematical constant τ (2π)."""
    return VMValue(VMValueType.FLOAT, math.tau)

def _math_inf(vm: VirtualMachine) -> VMValue:
    """Return positive infinity."""
    return VMValue(VMValueType.FLOAT, float('inf'))

def _math_nan(vm: VirtualMachine) -> VMValue:
    """Return a floating-point NaN (Not a Number) value."""
    return VMValue(VMValueType.FLOAT, float('nan'))


# Basic math functions

def _math_abs(vm: VirtualMachine, x: VMValue) -> VMValue:
    """Return the absolute value of x."""
    if x.type == VMValueType.INTEGER:
        return VMValue(VMValueType.INTEGER, abs(x.value))
    elif x.type == VMValueType.FLOAT:
        return VMValue(VMValueType.FLOAT, abs(x.value))
    else:
        return VMValue(VMValueType.NULL, None)

def _math_ceil(vm: VirtualMachine, x: VMValue) -> VMValue:
    """Return the ceiling of x as an integer."""
    if x.type in [VMValueType.INTEGER, VMValueType.FLOAT]:
        return VMValue(VMValueType.INTEGER, math.ceil(x.value))
    else:
        return VMValue(VMValueType.NULL, None)

def _math_floor(vm: VirtualMachine, x: VMValue) -> VMValue:
    """Return the floor of x as an integer."""
    if x.type in [VMValueType.INTEGER, VMValueType.FLOAT]:
        return VMValue(VMValueType.INTEGER, math.floor(x.value))
    else:
        return VMValue(VMValueType.NULL, None)

def _math_round(vm: VirtualMachine, x: VMValue, ndigits: VMValue = None) -> VMValue:
    """Round x to the nearest integer or to ndigits precision after the decimal point."""
    if x.type not in [VMValueType.INTEGER, VMValueType.FLOAT]:
        return VMValue(VMValueType.NULL, None)
    
    digits = 0
    if ndigits and ndigits.type == VMValueType.INTEGER:
        digits = ndigits.value
    
    result = round(x.value, digits)
    
    # If no digits specified and result is an integer, return as integer
    if not ndigits and result == int(result):
        return VMValue(VMValueType.INTEGER, int(result))
    
    return VMValue(VMValueType.FLOAT, result)

def _math_trunc(vm: VirtualMachine, x: VMValue) -> VMValue:
    """Return the integer part of x."""
    if x.type in [VMValueType.INTEGER, VMValueType.FLOAT]:
        return VMValue(VMValueType.INTEGER, math.trunc(x.value))
    else:
        return VMValue(VMValueType.NULL, None)

def _math_sqrt(vm: VirtualMachine, x: VMValue) -> VMValue:
    """Return the square root of x."""
    if x.type not in [VMValueType.INTEGER, VMValueType.FLOAT]:
        return VMValue(VMValueType.NULL, None)
    
    if x.value < 0:
        return VMValue(VMValueType.NULL, None)
    
    return VMValue(VMValueType.FLOAT, math.sqrt(x.value))

def _math_pow(vm: VirtualMachine, x: VMValue, y: VMValue) -> VMValue:
    """Return x raised to the power y."""
    if (x.type not in [VMValueType.INTEGER, VMValueType.FLOAT] or
        y.type not in [VMValueType.INTEGER, VMValueType.FLOAT]):
        return VMValue(VMValueType.NULL, None)
    
    try:
        result = math.pow(x.value, y.value)
        # Try to return an integer if the result is an integer
        if result == int(result):
            return VMValue(VMValueType.INTEGER, int(result))
        return VMValue(VMValueType.FLOAT, result)
    except (ValueError, OverflowError):
        return VMValue(VMValueType.NULL, None)

def _math_exp(vm: VirtualMachine, x: VMValue) -> VMValue:
    """Return e raised to the power x."""
    if x.type not in [VMValueType.INTEGER, VMValueType.FLOAT]:
        return VMValue(VMValueType.NULL, None)
    
    try:
        return VMValue(VMValueType.FLOAT, math.exp(x.value))
    except (ValueError, OverflowError):
        return VMValue(VMValueType.NULL, None)

def _math_log(vm: VirtualMachine, x: VMValue, base: VMValue = None) -> VMValue:
    """Return the logarithm of x to the given base."""
    if x.type not in [VMValueType.INTEGER, VMValueType.FLOAT]:
        return VMValue(VMValueType.NULL, None)
    
    if x.value <= 0:
        return VMValue(VMValueType.NULL, None)
    
    try:
        if base and base.type in [VMValueType.INTEGER, VMValueType.FLOAT]:
            if base.value <= 0:
                return VMValue(VMValueType.NULL, None)
            result = math.log(x.value, base.value)
        else:
            result = math.log(x.value)
        
        return VMValue(VMValueType.FLOAT, result)
    except (ValueError, ZeroDivisionError):
        return VMValue(VMValueType.NULL, None)

def _math_log10(vm: VirtualMachine, x: VMValue) -> VMValue:
    """Return the base-10 logarithm of x."""
    if x.type not in [VMValueType.INTEGER, VMValueType.FLOAT]:
        return VMValue(VMValueType.NULL, None)
    
    if x.value <= 0:
        return VMValue(VMValueType.NULL, None)
    
    try:
        return VMValue(VMValueType.FLOAT, math.log10(x.value))
    except ValueError:
        return VMValue(VMValueType.NULL, None)

def _math_log2(vm: VirtualMachine, x: VMValue) -> VMValue:
    """Return the base-2 logarithm of x."""
    if x.type not in [VMValueType.INTEGER, VMValueType.FLOAT]:
        return VMValue(VMValueType.NULL, None)
    
    if x.value <= 0:
        return VMValue(VMValueType.NULL, None)
    
    try:
        return VMValue(VMValueType.FLOAT, math.log2(x.value))
    except ValueError:
        return VMValue(VMValueType.NULL, None)


# Trigonometric functions

def _math_sin(vm: VirtualMachine, x: VMValue) -> VMValue:
    """Return the sine of x radians."""
    if x.type not in [VMValueType.INTEGER, VMValueType.FLOAT]:
        return VMValue(VMValueType.NULL, None)
    
    return VMValue(VMValueType.FLOAT, math.sin(x.value))

def _math_cos(vm: VirtualMachine, x: VMValue) -> VMValue:
    """Return the cosine of x radians."""
    if x.type not in [VMValueType.INTEGER, VMValueType.FLOAT]:
        return VMValue(VMValueType.NULL, None)
    
    return VMValue(VMValueType.FLOAT, math.cos(x.value))

def _math_tan(vm: VirtualMachine, x: VMValue) -> VMValue:
    """Return the tangent of x radians."""
    if x.type not in [VMValueType.INTEGER, VMValueType.FLOAT]:
        return VMValue(VMValueType.NULL, None)
    
    try:
        return VMValue(VMValueType.FLOAT, math.tan(x.value))
    except (ValueError, OverflowError):
        return VMValue(VMValueType.NULL, None)

def _math_asin(vm: VirtualMachine, x: VMValue) -> VMValue:
    """Return the arc sine of x, in radians."""
    if x.type not in [VMValueType.INTEGER, VMValueType.FLOAT]:
        return VMValue(VMValueType.NULL, None)
    
    try:
        return VMValue(VMValueType.FLOAT, math.asin(x.value))
    except ValueError:
        return VMValue(VMValueType.NULL, None)

def _math_acos(vm: VirtualMachine, x: VMValue) -> VMValue:
    """Return the arc cosine of x, in radians."""
    if x.type not in [VMValueType.INTEGER, VMValueType.FLOAT]:
        return VMValue(VMValueType.NULL, None)
    
    try:
        return VMValue(VMValueType.FLOAT, math.acos(x.value))
    except ValueError:
        return VMValue(VMValueType.NULL, None)

def _math_atan(vm: VirtualMachine, x: VMValue) -> VMValue:
    """Return the arc tangent of x, in radians."""
    if x.type not in [VMValueType.INTEGER, VMValueType.FLOAT]:
        return VMValue(VMValueType.NULL, None)
    
    return VMValue(VMValueType.FLOAT, math.atan(x.value))

def _math_atan2(vm: VirtualMachine, y: VMValue, x: VMValue) -> VMValue:
    """Return the arc tangent of y/x, in radians."""
    if (y.type not in [VMValueType.INTEGER, VMValueType.FLOAT] or
        x.type not in [VMValueType.INTEGER, VMValueType.FLOAT]):
        return VMValue(VMValueType.NULL, None)
    
    return VMValue(VMValueType.FLOAT, math.atan2(y.value, x.value))

def _math_degrees(vm: VirtualMachine, x: VMValue) -> VMValue:
    """Convert angle x from radians to degrees."""
    if x.type not in [VMValueType.INTEGER, VMValueType.FLOAT]:
        return VMValue(VMValueType.NULL, None)
    
    return VMValue(VMValueType.FLOAT, math.degrees(x.value))

def _math_radians(vm: VirtualMachine, x: VMValue) -> VMValue:
    """Convert angle x from degrees to radians."""
    if x.type not in [VMValueType.INTEGER, VMValueType.FLOAT]:
        return VMValue(VMValueType.NULL, None)
    
    return VMValue(VMValueType.FLOAT, math.radians(x.value))


# Statistical functions

def _math_min(vm: VirtualMachine, *args) -> VMValue:
    """Return the smallest of the given arguments."""
    if not args:
        return VMValue(VMValueType.NULL, None)
    
    # If the first argument is a list, use that
    if args[0].type == VMValueType.LIST:
        values = [val for val in args[0].value 
                 if val.type in [VMValueType.INTEGER, VMValueType.FLOAT]]
    else:
        values = [val for val in args 
                 if val.type in [VMValueType.INTEGER, VMValueType.FLOAT]]
    
    if not values:
        return VMValue(VMValueType.NULL, None)
    
    min_value = min(values, key=lambda x: x.value)
    return min_value

def _math_max(vm: VirtualMachine, *args) -> VMValue:
    """Return the largest of the given arguments."""
    if not args:
        return VMValue(VMValueType.NULL, None)
    
    # If the first argument is a list, use that
    if args[0].type == VMValueType.LIST:
        values = [val for val in args[0].value 
                 if val.type in [VMValueType.INTEGER, VMValueType.FLOAT]]
    else:
        values = [val for val in args 
                 if val.type in [VMValueType.INTEGER, VMValueType.FLOAT]]
    
    if not values:
        return VMValue(VMValueType.NULL, None)
    
    max_value = max(values, key=lambda x: x.value)
    return max_value

def _math_sum(vm: VirtualMachine, values: VMValue) -> VMValue:
    """Return the sum of a list of numbers."""
    if values.type != VMValueType.LIST:
        return VMValue(VMValueType.NULL, None)
    
    numeric_values = [val.value for val in values.value 
                     if val.type in [VMValueType.INTEGER, VMValueType.FLOAT]]
    
    if not numeric_values:
        return VMValue(VMValueType.INTEGER, 0)
    
    result = sum(numeric_values)
    
    # Try to return an integer if the result is an integer
    if result == int(result):
        return VMValue(VMValueType.INTEGER, int(result))
    return VMValue(VMValueType.FLOAT, result)

def _math_mean(vm: VirtualMachine, values: VMValue) -> VMValue:
    """Return the arithmetic mean of a list of numbers."""
    if values.type != VMValueType.LIST:
        return VMValue(VMValueType.NULL, None)
    
    numeric_values = [val.value for val in values.value 
                     if val.type in [VMValueType.INTEGER, VMValueType.FLOAT]]
    
    if not numeric_values:
        return VMValue(VMValueType.NULL, None)
    
    try:
        result = statistics.mean(numeric_values)
        return VMValue(VMValueType.FLOAT, result)
    except statistics.StatisticsError:
        return VMValue(VMValueType.NULL, None)

def _math_median(vm: VirtualMachine, values: VMValue) -> VMValue:
    """Return the median of a list of numbers."""
    if values.type != VMValueType.LIST:
        return VMValue(VMValueType.NULL, None)
    
    numeric_values = [val.value for val in values.value 
                     if val.type in [VMValueType.INTEGER, VMValueType.FLOAT]]
    
    if not numeric_values:
        return VMValue(VMValueType.NULL, None)
    
    try:
        result = statistics.median(numeric_values)
        if result == int(result):
            return VMValue(VMValueType.INTEGER, int(result))
        return VMValue(VMValueType.FLOAT, result)
    except statistics.StatisticsError:
        return VMValue(VMValueType.NULL, None)

def _math_mode(vm: VirtualMachine, values: VMValue) -> VMValue:
    """Return the mode of a list of numbers."""
    if values.type != VMValueType.LIST:
        return VMValue(VMValueType.NULL, None)
    
    numeric_values = [val.value for val in values.value 
                     if val.type in [VMValueType.INTEGER, VMValueType.FLOAT]]
    
    if not numeric_values:
        return VMValue(VMValueType.NULL, None)
    
    try:
        result = statistics.mode(numeric_values)
        if result == int(result):
            return VMValue(VMValueType.INTEGER, int(result))
        return VMValue(VMValueType.FLOAT, result)
    except statistics.StatisticsError:
        return VMValue(VMValueType.NULL, None)

def _math_stdev(vm: VirtualMachine, values: VMValue) -> VMValue:
    """Return the standard deviation of a list of numbers."""
    if values.type != VMValueType.LIST:
        return VMValue(VMValueType.NULL, None)
    
    numeric_values = [val.value for val in values.value 
                     if val.type in [VMValueType.INTEGER, VMValueType.FLOAT]]
    
    if len(numeric_values) < 2:
        return VMValue(VMValueType.NULL, None)
    
    try:
        result = statistics.stdev(numeric_values)
        return VMValue(VMValueType.FLOAT, result)
    except statistics.StatisticsError:
        return VMValue(VMValueType.NULL, None)

def _math_variance(vm: VirtualMachine, values: VMValue) -> VMValue:
    """Return the variance of a list of numbers."""
    if values.type != VMValueType.LIST:
        return VMValue(VMValueType.NULL, None)
    
    numeric_values = [val.value for val in values.value 
                     if val.type in [VMValueType.INTEGER, VMValueType.FLOAT]]
    
    if len(numeric_values) < 2:
        return VMValue(VMValueType.NULL, None)
    
    try:
        result = statistics.variance(numeric_values)
        return VMValue(VMValueType.FLOAT, result)
    except statistics.StatisticsError:
        return VMValue(VMValueType.NULL, None)


# Random functions

def _math_random(vm: VirtualMachine) -> VMValue:
    """Return a random float in [0.0, 1.0)."""
    return VMValue(VMValueType.FLOAT, random.random())

def _math_random_int(vm: VirtualMachine, a: VMValue, b: VMValue) -> VMValue:
    """Return a random integer in [a, b]."""
    if a.type != VMValueType.INTEGER or b.type != VMValueType.INTEGER:
        return VMValue(VMValueType.NULL, None)
    
    return VMValue(VMValueType.INTEGER, random.randint(a.value, b.value))

def _math_random_choice(vm: VirtualMachine, sequence: VMValue) -> VMValue:
    """Return a random element from a list."""
    if sequence.type != VMValueType.LIST or not sequence.value:
        return VMValue(VMValueType.NULL, None)
    
    return random.choice(sequence.value)

def _math_random_shuffle(vm: VirtualMachine, sequence: VMValue) -> VMValue:
    """Shuffle a list in place."""
    if sequence.type != VMValueType.LIST:
        return VMValue(VMValueType.LIST, [])
    
    result = sequence.value.copy()
    random.shuffle(result)
    return VMValue(VMValueType.LIST, result)

def _math_random_seed(vm: VirtualMachine, seed: VMValue = None) -> VMValue:
    """Seed the random number generator."""
    if seed and seed.type == VMValueType.INTEGER:
        random.seed(seed.value)
    else:
        random.seed()
    
    return VMValue(VMValueType.NULL, None) 