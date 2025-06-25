#!/usr/bin/env python3
"""
Runa Bootstrap Runner
====================

Python-based bootstrap runner for executing Runa VM files written in Runa syntax.
This is the bridge between Python and Runa during the bootstrap phase.

Usage:
    python runa_bootstrap.py <runa_file.runa> [options]
"""

import sys
import os
import time
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class RunaBootstrapRunner:
    """
    Bootstrap runner for executing Runa VM files written in Runa syntax.
    
    This runner interprets Runa syntax and executes it using Python as the runtime.
    It's the foundation for the bootstrap process until Runa can compile itself.
    """
    
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, Any] = {}
        self.imports: Dict[str, Any] = {}
        self.execution_stats = {
            'start_time': None,
            'end_time': None,
            'instructions_executed': 0,
            'memory_allocated': 0,
            'errors': []
        }
    
    def run_file(self, file_path: str, debug: bool = False) -> Any:
        """
        Execute a Runa file and return the result.
        
        Args:
            file_path: Path to the .runa file
            debug: Enable debug mode
            
        Returns:
            Result of the execution
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Runa file not found: {file_path}")
        
        logger.info(f"Executing Runa file: {file_path}")
        self.execution_stats['start_time'] = time.time()
        
        try:
            # Read and parse the Runa file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Preprocess the Runa code
            preprocessed_code = self.preprocess_runa_code(content)
            
            # Execute the Runa code
            result = self.execute_runa_code(preprocessed_code, debug)
            
            self.execution_stats['end_time'] = time.time()
            execution_time = self.execution_stats['end_time'] - self.execution_stats['start_time']
            
            logger.info(f"Execution completed in {execution_time:.3f}s")
            logger.info(f"Instructions executed: {self.execution_stats['instructions_executed']}")
            
            return result
            
        except Exception as e:
            self.execution_stats['errors'].append(str(e))
            logger.error(f"Execution failed: {e}")
            raise
    
    def preprocess_runa_code(self, code: str) -> str:
        """
        Preprocess Runa code to expand for-loops and other complex constructs.
        This is a workaround for the bootstrap runner's limited execution model.
        """
        lines = code.split('\n')
        expanded_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for for-each loops with index
            if line.startswith('For each ') and ' with index ' in line and ' in ' in line:
                # Parse the for-loop
                loop_def = line[9:].strip()  # Remove "For each "
                parts = loop_def.split(' with index ')
                var_name = parts[0].strip()
                index_and_collection = parts[1].strip()
                
                if ' in ' in index_and_collection:
                    index_var, collection_name = index_and_collection.split(' in ', 1)
                    index_var = index_var.strip()
                    collection_name = collection_name.strip().rstrip(':')
                    
                    # Find the loop body (indented lines)
                    loop_body = []
                    i += 1
                    while i < len(lines) and (lines[i].startswith('    ') or lines[i].strip() == ''):
                        if lines[i].strip():  # Skip empty lines
                            loop_body.append(lines[i][4:])  # Remove indentation
                        i += 1
                    i -= 1  # Back up one line
                    
                    # Generate expanded code
                    expanded_lines.append(f"# Expanded for-loop: {line}")
                    
                    # For now, just handle the case we know exists (basic collection access)
                    # In a full implementation, we'd evaluate the collection
                    # For the VM, we know there are typically small loops, so we'll simulate
                    for idx in range(10):  # Assume max 10 iterations for safety
                        expanded_lines.append(f"# Loop iteration {idx}")
                        expanded_lines.append(f"Let {index_var} be {idx}")
                        
                        # Check if collection exists and has this index
                        expanded_lines.append(f"If {idx} is less than length of {collection_name}:")
                        expanded_lines.append(f"    Let {var_name} be {collection_name} at index {idx}")
                        
                        # Add loop body with proper variable substitution
                        for body_line in loop_body:
                            expanded_lines.append(f"    {body_line}")
                            
                        # Add early exit condition
                        expanded_lines.append(f"If {idx} is greater than or equal to length of {collection_name}:")
                        expanded_lines.append(f"    # Exit loop")
                        expanded_lines.append(f"    Continue")
            else:
                expanded_lines.append(line)
            
            i += 1
        
        return '\n'.join(expanded_lines)
    
    def execute_runa_code(self, code: str, debug: bool = False) -> Any:
        """
        Execute Runa code and return the result.
        
        Args:
            code: Runa source code
            debug: Enable debug mode
            
        Returns:
            Result of the execution
        """
        lines = code.split('\n')
        result = None
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            if debug:
                logger.debug(f"Line {line_num}: {line}")
            
            try:
                result = self.execute_line(line, line_num)
                self.execution_stats['instructions_executed'] += 1
                
            except Exception as e:
                error_msg = f"Error at line {line_num}: {e}"
                logger.error(error_msg)
                if debug:
                    logger.error(f"Line content: {line}")
                raise RuntimeError(error_msg) from e
        
        return result
    
    def execute_line(self, line: str, line_num: int) -> Any:
        """
        Execute a single line of Runa code.
        
        Args:
            line: Single line of Runa code
            line_num: Line number for error reporting
            
        Returns:
            Result of the line execution
        """
        # Handle imports
        if line.startswith('Let required_modules be'):
            return self.handle_imports(line)
        
        # Handle type definitions
        elif line.startswith('Type '):
            return self.handle_type_definition(line)
        
        # Handle variable declarations - but check for dictionary creation first
        elif line.startswith('Let '):
            # Check if this is a dictionary creation within a variable declaration
            if 'Dictionary with' in line:
                # Extract the dictionary creation part
                dict_part = line[line.find('Dictionary with'):]
                dict_result = self.handle_dictionary_creation(dict_part)
                
                # Handle the variable assignment
                var_part, _ = line.split(' be ', 1)
                var_name = var_part[4:].strip()  # Remove "Let "
                self.variables[var_name] = dict_result
                return dict_result
            else:
                return self.handle_variable_declaration(line)
        
        # Handle process definitions
        elif line.startswith('Process called '):
            return self.handle_process_definition(line)
        
        # Handle function calls
        elif ' with ' in line and '(' not in line and 'Dictionary with' not in line:
            return self.handle_function_call(line)
        
        # Handle control flow
        elif line.startswith('If '):
            return self.handle_if_statement(line)
        elif line.startswith('Otherwise if '):
            return self.handle_otherwise_if_statement(line)
        elif line.startswith('Otherwise:'):
            return self.handle_otherwise_statement(line)
        elif line.startswith('For each '):
            return self.handle_for_loop(line)
        elif line.startswith('While '):
            return self.handle_while_loop(line)
        elif line.strip() == 'Continue':
            return self.handle_continue_statement()
        elif line.strip() == 'Break':
            return self.handle_break_statement()
        elif line.strip() == 'Pass':
            return None  # No-op
        
        # Handle return statements
        elif line.startswith('Return '):
            return self.handle_return_statement(line)
        
        # Handle display statements
        elif line.startswith('Display '):
            return self.handle_display_statement(line)
        
        # Handle try-catch
        elif line.startswith('Try:') or line.startswith('Catch '):
            return self.handle_try_catch(line)
        
        # Handle arithmetic operations
        elif any(op in line for op in [' plus ', ' minus ', ' multiplied by ', ' divided by ']):
            return self.handle_arithmetic(line)
        
        # Handle comparisons
        elif any(op in line for op in [' is equal to ', ' is greater than ', ' is less than ']):
            return self.handle_comparison(line)
        
        # Handle logical operations
        elif any(op in line for op in [' and ', ' or ']):
            return self.handle_logical_operation(line)
        
        # Handle list operations
        elif line.startswith('list containing'):
            return self.handle_list_creation(line)
        
        # Handle dictionary operations - BEFORE other patterns
        elif line.startswith('dictionary with:') or line.startswith('Dictionary with'):
            return self.handle_dictionary_creation(line)
        
        # Handle string operations
        elif ' followed by ' in line:
            return self.handle_string_concatenation(line)
        
        # Handle collection operations (enhanced pattern matching)
        elif (line.startswith('length of ') or ' at index ' in line or ' at key ' in line):
            return self.handle_collection_operation(line)
        
        # Handle aggregation operations
        elif line.startswith('the sum of all '):
            return self.handle_aggregation(line)
        
        # Handle complex expressions that might be function calls or operations
        elif any(keyword in line for keyword in ['current time', 'empty dictionary', 'empty list']):
            return self.evaluate_expression(line)
        
        # Skip comments and documentation strings
        elif line.startswith('#') or line.startswith('"""') or line.startswith("'''"):
            return None
        
        # Default: try to evaluate as expression
        else:
            try:
                return self.evaluate_expression(line)
            except Exception as e:
                logger.warning(f"Could not evaluate line as expression: {line} - {e}")
                return None
    
    def handle_imports(self, line: str) -> None:
        """Handle Runa import statements."""
        # Extract module names from the line
        # Example: "Let required_modules be list containing "time", "logging", "typing""
        import_match = line.find('list containing')
        if import_match != -1:
            modules_str = line[import_match + len('list containing'):].strip()
            # Parse the modules (simplified)
            modules = [m.strip().strip('"') for m in modules_str.split(',')]
            
            for module_name in modules:
                try:
                    self.imports[module_name] = __import__(module_name)
                    logger.debug(f"Imported module: {module_name}")
                except ImportError as e:
                    logger.warning(f"Failed to import {module_name}: {e}")
    
    def handle_type_definition(self, line: str) -> None:
        """Handle Runa type definitions."""
        # Example: "Type VMState is "idle" OR "running" OR "paused""
        type_match = line.find('Type ')
        if type_match != -1:
            type_def = line[type_match + len('Type '):]
            type_name, type_body = type_def.split(' is ', 1)
            type_name = type_name.strip()
            
            # Store type definition
            self.variables[f"Type_{type_name}"] = {
                'name': type_name,
                'definition': type_body.strip(),
                'kind': 'type'
            }
            logger.debug(f"Defined type: {type_name}")
    
    def handle_variable_declaration(self, line: str) -> Any:
        """Handle Runa variable declarations."""
        # Example: "Let user_name be "Alice""
        # Example: "Let user_age be 25"
        # Example: "Let result be value1 plus value2"
        # Example: "Let vm at key "state" be "idle""
        
        if ' be ' in line:
            var_part, value_part = line.split(' be ', 1)
            var_part = var_part[4:].strip()  # Remove "Let "
            
            # Check if this is a dictionary key assignment
            if ' at key ' in var_part:
                # Handle: "vm at key "state" be "idle""
                obj_name, key_part = var_part.split(' at key ', 1)
                obj_name = obj_name.strip()
                key_name = key_part.strip().strip('"\'')
                
                # Get or create the object
                if obj_name not in self.variables:
                    self.variables[obj_name] = {}
                
                obj = self.variables[obj_name]
                if not isinstance(obj, dict):
                    obj = {}
                    self.variables[obj_name] = obj
                
                # Evaluate the value and assign to the key
                value = self.evaluate_expression(value_part.strip())
                obj[key_name] = value
                
                logger.debug(f"Set {obj_name}['{key_name}'] = {value}")
                return value
            else:
                # Regular variable declaration
                var_name = var_part
                value = self.evaluate_expression(value_part.strip())
                
                # Store the variable with proper type
                self.variables[var_name] = value
                return value
        return None
    
    def handle_process_definition(self, line: str) -> None:
        """Handle Runa process/function definitions."""
        # Example: "Process called "RunaVM" that takes memory_size as Integer:"
        process_match = line.find('Process called ')
        if process_match != -1:
            process_def = line[process_match + len('Process called '):]
            
            # Extract process name and parameters
            if ' that takes ' in process_def:
                name_part, params_part = process_def.split(' that takes ', 1)
                process_name = name_part.strip().strip('"')
                params = params_part.split(' and ')
                
                # Store process definition
                self.functions[process_name] = {
                    'name': process_name,
                    'parameters': [p.strip() for p in params],
                    'body': [],
                    'kind': 'process'
                }
                logger.debug(f"Defined process: {process_name}")
    
    def handle_function_call(self, line: str) -> Any:
        """Handle Runa function calls."""
        # Example: "create RunaVM with memory_size as 1024"
        if ' with ' in line:
            func_part, args_part = line.split(' with ', 1)
            
            if func_part.strip() == 'create':
                # Handle object creation
                class_name = args_part.split(' ')[0]
                return self.create_object(class_name, args_part)
            else:
                # Handle regular function calls
                return self.call_function(func_part.strip(), args_part)
        
        return None
    
    def create_object(self, class_name: str, args_part: str) -> Dict[str, Any]:
        """Create an object instance."""
        # Parse arguments
        args = {}
        if ' as ' in args_part:
            arg_pairs = args_part.split(' and ')
            for pair in arg_pairs:
                if ' as ' in pair:
                    key, value = pair.split(' as ', 1)
                    key = key.strip()
                    value = self.evaluate_expression(value.strip())
                    args[key] = value
        
        # Create object based on class name
        if class_name == 'RunaVM':
            return self.create_runa_vm(args)
        elif class_name == 'ErrorHandler':
            return self.create_error_handler(args)
        elif class_name == 'PerformanceMonitor':
            return self.create_performance_monitor(args)
        else:
            # Generic object creation
            return {
                'class': class_name,
                'args': args,
                'kind': 'object'
            }
    
    def create_runa_vm(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a RunaVM instance."""
        memory_size = args.get('memory_size', 1024)
        
        return {
            'class': 'RunaVM',
            'memory_size': memory_size,
            'state': 'ready',
            'call_stack': [],
            'operand_stack': [],
            'globals': {},
            'constants': [],
            'heap': {},
            'next_heap_id': 1,
            'instruction_count': 0,
            'start_time': time.time(),
            'kind': 'vm'
        }
    
    def create_error_handler(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create an ErrorHandler instance."""
        return {
            'class': 'ErrorHandler',
            'errors': [],
            'warnings': [],
            'kind': 'error_handler'
        }
    
    def create_performance_monitor(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a PerformanceMonitor instance."""
        return {
            'class': 'PerformanceMonitor',
            'operations': {},
            'start_time': time.time(),
            'kind': 'performance_monitor'
        }
    
    def call_function(self, func_name: str, args_part: str) -> Any:
        """Call a function with arguments."""
        # Parse arguments
        args = {}
        if ' as ' in args_part:
            arg_pairs = args_part.split(' and ')
            for pair in arg_pairs:
                if ' as ' in pair:
                    key, value = pair.split(' as ', 1)
                    key = key.strip()
                    value = self.evaluate_expression(value.strip())
                    args[key] = value
        
        # Call the function
        if func_name in self.functions:
            return self.execute_function(self.functions[func_name], args)
        else:
            # Built-in function
            return self.call_builtin_function(func_name, args)
    
    def execute_function(self, func_def: Dict[str, Any], args: Dict[str, Any]) -> Any:
        """Execute a user-defined function."""
        # For now, return a placeholder
        return {
            'function': func_def['name'],
            'args': args,
            'result': None
        }
    
    def call_builtin_function(self, func_name: str, args: Dict[str, Any]) -> Any:
        """Call a built-in function."""
        if func_name == 'current time':
            return time.time()
        elif func_name == 'empty dictionary':
            return {}
        elif func_name == 'empty list':
            return []
        elif func_name == 'length of':
            # Get the collection from args
            collection_name = list(args.keys())[0] if args else None
            if collection_name and collection_name in self.variables:
                collection = self.variables[collection_name]
                if isinstance(collection, (list, dict)):
                    return len(collection)
            return 0
        elif func_name == 'create PerformanceMonitor':
            return {'type': 'PerformanceMonitor', 'stats': {}}
        elif func_name == 'create RunaRuntime':
            return {'type': 'RunaRuntime', 'global_variables': {}, 'global_functions': {}}
        elif func_name == 'JITCompiler':
            return {'type': 'JITCompiler', 'compiled_blocks': {}, 'hot_threshold': 10}
        elif func_name == 'generate native code':
            # For bootstrap, return a mock function
            return lambda vm_context, runtime: None
        elif func_name == 'pop from':
            # Handle stack operations
            collection_name = list(args.keys())[0] if args else None
            if collection_name and collection_name in self.variables:
                collection = self.variables[collection_name]
                if isinstance(collection, list) and collection:
                    return collection.pop()
            return None
        elif func_name == 'import':
            # Handle module imports
            module_name = list(args.keys())[0] if args else None
            if module_name:
                try:
                    import importlib
                    return importlib.import_module(module_name)
                except ImportError:
                    logger.warning(f"Failed to import module: {module_name}")
                    return None
        else:
            logger.warning(f"Unknown built-in function: {func_name}")
            return None
    
    def handle_if_statement(self, line: str) -> Any:
        """Handle Runa if statements."""
        # Example: "If user age is greater than 21:"
        condition = line[3:].strip()  # Remove "If "
        return self.evaluate_condition(condition)
    
    def handle_for_loop(self, line: str) -> Any:
        """Handle Runa for-each loops."""
        # Example: "For each color in colors:" or "For each instruction with index i in instructions:"
        loop_def = line[9:].strip()  # Remove "For each "
        
        if ' with index ' in loop_def:
            # Handle: "For each instruction with index i in instructions"
            parts = loop_def.split(' with index ')
            var_name = parts[0].strip()
            index_and_collection = parts[1].strip()
            
            if ' in ' in index_and_collection:
                index_var, collection_name = index_and_collection.split(' in ', 1)
                index_var = index_var.strip()
                collection_name = collection_name.strip()
                
                # Get the collection
                collection = self.variables.get(collection_name, [])
                if isinstance(collection, (list, dict)):
                    return {
                        'type': 'for_loop_with_index',
                        'variable': var_name,
                        'index_variable': index_var,
                        'collection': collection_name,
                        'items': collection
                    }
        elif ' in ' in loop_def:
            # Handle: "For each color in colors"
            var_name, collection_name = loop_def.split(' in ', 1)
            var_name = var_name.strip()
            collection_name = collection_name.strip()
            
            # Get the collection
            collection = self.variables.get(collection_name, [])
            if isinstance(collection, (list, dict)):
                return {
                    'type': 'for_loop',
                    'variable': var_name,
                    'collection': collection_name,
                    'items': collection
                }
        return None
    
    def handle_while_loop(self, line: str) -> Any:
        """Handle Runa while loops."""
        # Example: "While condition:"
        condition = line[6:].strip()  # Remove "While "
        return self.evaluate_condition(condition)
    
    def handle_return_statement(self, line: str) -> Any:
        """Handle Runa return statements."""
        # Example: "Return result"
        value = line[7:].strip()  # Remove "Return "
        return self.evaluate_expression(value)
    
    def handle_display_statement(self, line: str) -> Any:
        """Handle Runa display statements."""
        # Example: "Display result with message "Success""
        # Example: "Display "Hello World""
        # Example: "Display vm at key "stack""
        display_part = line[8:].strip()  # Remove "Display "
        
        if ' with message ' in display_part:
            value_part, message_part = display_part.split(' with message ', 1)
            value = self.evaluate_expression(value_part)
            message = message_part.strip().strip('"')
            print(f"{message}: {value}")
        else:
            value = self.evaluate_expression(display_part)
            print(value)
        
        return value
    
    def handle_try_catch(self, line: str) -> Any:
        """Handle Runa try-catch statements."""
        # Example: "Try:" or "Catch error:"
        if line.startswith('Try:'):
            return {'type': 'try_block'}
        elif line.startswith('Catch '):
            error_var = line[6:].strip()  # Remove "Catch "
            return {'type': 'catch_block', 'error_variable': error_var}
        return None
    
    def handle_arithmetic(self, line: str) -> Any:
        """Handle Runa arithmetic operations."""
        # Example: "width multiplied by height"
        # Example: "vm at key "stack" plus instruction at key "value""
        
        try:
            if ' multiplied by ' in line:
                left, right = line.split(' multiplied by ', 1)
                left_val = self.evaluate_expression(left.strip())
                right_val = self.evaluate_expression(right.strip())
                return left_val * right_val
            elif ' plus ' in line:
                left, right = line.split(' plus ', 1)
                left_val = self.evaluate_expression(left.strip())
                right_val = self.evaluate_expression(right.strip())
                
                # Add detailed error logging for debugging None values
                if left_val is None or right_val is None:
                    logger.error(f"Plus operation with None values:")
                    logger.error(f"  Left expression: '{left.strip()}' = {left_val}")
                    logger.error(f"  Right expression: '{right.strip()}' = {right_val}")
                    
                    # Show the variables involved
                    if left.strip() in self.variables:
                        logger.error(f"  Variable '{left.strip()}' contains: {self.variables[left.strip()]}")
                    if right.strip() in self.variables:
                        logger.error(f"  Variable '{right.strip()}' contains: {self.variables[right.strip()]}")
                
                # Handle list concatenation
                if isinstance(left_val, list):
                    if isinstance(right_val, list):
                        return left_val + right_val
                    else:
                        return left_val + [right_val]
                else:
                    return left_val + right_val
            elif ' minus ' in line:
                left, right = line.split(' minus ', 1)
                left_val = self.evaluate_expression(left.strip())
                right_val = self.evaluate_expression(right.strip())
                
                # Add detailed error logging for debugging
                logger.debug(f"Arithmetic subtraction: '{left.strip()}' = {left_val} (type: {type(left_val).__name__})")
                logger.debug(f"                       '{right.strip()}' = {right_val} (type: {type(right_val).__name__})")
                
                return left_val - right_val
            elif ' divided by ' in line:
                left, right = line.split(' divided by ', 1)
                left_val = self.evaluate_expression(left.strip())
                right_val = self.evaluate_expression(right.strip())
                if right_val == 0:
                    raise ValueError("Division by zero")
                return left_val / right_val
            return None
        except Exception as e:
            # Enhanced error reporting
            logger.error(f"Arithmetic operation failed on line: '{line}'")
            if ' minus ' in line:
                left, right = line.split(' minus ', 1)
                try:
                    left_val = self.evaluate_expression(left.strip())
                    logger.error(f"  Left operand '{left.strip()}' evaluated to: {left_val} (type: {type(left_val).__name__})")
                except Exception as left_error:
                    logger.error(f"  Left operand '{left.strip()}' evaluation failed: {left_error}")
                
                try:
                    right_val = self.evaluate_expression(right.strip())
                    logger.error(f"  Right operand '{right.strip()}' evaluated to: {right_val} (type: {type(right_val).__name__})")
                except Exception as right_error:
                    logger.error(f"  Right operand '{right.strip()}' evaluation failed: {right_error}")
            
            logger.error(f"Current variables: {list(self.variables.keys())}")
            raise e
    
    def handle_comparison(self, line: str) -> Any:
        """Handle Runa comparison operations."""
        # Example: "user age is greater than 21"
        if ' is greater than ' in line:
            left, right = line.split(' is greater than ', 1)
            left_val = self.evaluate_expression(left.strip())
            right_val = self.evaluate_expression(right.strip())
            return left_val > right_val
        elif ' is less than ' in line:
            left, right = line.split(' is less than ', 1)
            left_val = self.evaluate_expression(left.strip())
            right_val = self.evaluate_expression(right.strip())
            return left_val < right_val
        elif ' is equal to ' in line:
            left, right = line.split(' is equal to ', 1)
            left_val = self.evaluate_expression(left.strip())
            right_val = self.evaluate_expression(right.strip())
            return left_val == right_val
        return None
    
    def handle_logical_operation(self, line: str) -> Any:
        """Handle Runa logical operations."""
        # Example: "condition1 and condition2"
        if ' and ' in line:
            left, right = line.split(' and ', 1)
            left_val = self.evaluate_expression(left.strip())
            right_val = self.evaluate_expression(right.strip())
            return left_val and right_val
        elif ' or ' in line:
            left, right = line.split(' or ', 1)
            left_val = self.evaluate_expression(left.strip())
            right_val = self.evaluate_expression(right.strip())
            return left_val or right_val
        return None
    
    def handle_list_creation(self, line: str) -> List[Any]:
        """Handle Runa list creation."""
        # Example: "list containing item1, item2, item3"
        if 'list containing' in line:
            items_part = line[line.find('list containing') + len('list containing'):].strip()
            if items_part:
                items = [self.evaluate_expression(item.strip()) for item in items_part.split(',')]
                return items
        return []
    
    def handle_dictionary_creation(self, line: str) -> Dict[str, Any]:
        """Handle Runa dictionary creation."""
        # Example: "dictionary with: key1 as value1 key2 as value2"
        # Example: "Dictionary with opcode as "LOAD_CONST" and value as result"
        # Example: "dictionary with:\n    optimization_levels as dictionary with:\n        0 as "basic""
        
        result_dict = {}
        
        if 'dictionary with:' in line or 'Dictionary with' in line:
            # Extract the content after "dictionary with:" or "Dictionary with"
            if 'dictionary with:' in line:
                dict_content = line.split('dictionary with:', 1)[1].strip()
            else:
                dict_content = line.split('Dictionary with', 1)[1].strip()
            
            # If there's content, parse it
            if dict_content:
                # Handle "and" separated key-value pairs
                # Example: "opcode as "LOAD_CONST" and value as result"
                if ' and ' in dict_content:
                    pairs = dict_content.split(' and ')
                else:
                    pairs = [dict_content]
                
                for pair in pairs:
                    if ' as ' in pair:
                        key_part, value_part = pair.split(' as ', 1)
                        key = key_part.strip()
                        
                        # If the value is another dictionary creation, handle recursively
                        if value_part.strip().startswith('dictionary with:') or value_part.strip().startswith('Dictionary with'):
                            value = self.handle_dictionary_creation(value_part.strip())
                        else:
                            value = self.evaluate_expression(value_part.strip())
                        
                        result_dict[key] = value
            
            return result_dict
        return {}
    
    def handle_string_concatenation(self, line: str) -> str:
        """Handle Runa string concatenation."""
        # Example: "user name followed by " Smith""
        if ' followed by ' in line:
            left, right = line.split(' followed by ', 1)
            left_val = self.evaluate_expression(left.strip())
            right_val = self.evaluate_expression(right.strip())
            return str(left_val) + str(right_val)
        return line
    
    def handle_collection_operation(self, line: str) -> Any:
        """Handle Runa collection operations."""
        # Example: "length of colors" or "colors at index 0" or "instructions at index i minus 1"
        if line.startswith('length of '):
            collection_name = line[len('length of '):].strip()
            collection = self.variables.get(collection_name, [])
            if isinstance(collection, (list, dict)):
                return len(collection)
            return 0
        elif ' at index ' in line:
            collection_name, index_part = line.split(' at index ', 1)
            collection_name = collection_name.strip()
            
            # Handle complex index expressions like "i minus 1"
            # Need to parse this carefully to handle operator precedence
            index_expr = index_part.strip()
            logger.debug(f"Collection operation - collection: '{collection_name}', index_expr: '{index_expr}'")
            
            # If the index expression contains arithmetic, evaluate it first
            if any(op in index_expr for op in [' plus ', ' minus ', ' multiplied by ', ' divided by ']):
                logger.debug(f"Index expression contains arithmetic: '{index_expr}'")
                index = self.handle_arithmetic(index_expr)
                logger.debug(f"Arithmetic result: {index} (type: {type(index)})")
            else:
                logger.debug(f"Index expression is simple: '{index_expr}'")
                index = self.evaluate_expression(index_expr)
                logger.debug(f"Evaluation result: {index} (type: {type(index)})")
            
            collection = self.variables.get(collection_name, [])
            logger.debug(f"Collection: {collection} (length: {len(collection) if isinstance(collection, (list, dict)) else 'N/A'})")
            
            if isinstance(collection, (list, dict)) and isinstance(index, int):
                if isinstance(collection, list) and 0 <= index < len(collection):
                    result = collection[index]
                    logger.debug(f"Collection access successful: {result}")
                    return result
                elif isinstance(collection, dict) and str(index) in collection:
                    result = collection[str(index)]
                    logger.debug(f"Dictionary access successful: {result}")
                    return result
            else:
                logger.debug(f"Collection access failed - collection type: {type(collection)}, index type: {type(index)}")
        elif ' at key ' in line:
            # Handle dictionary key access like "vm at key 'state'" or "vm at key "stack""
            parts = line.split(' at key ', 1)
            obj_name = parts[0].strip()
            key_expr = parts[1].strip()
            
            # Remove quotes from key if present
            if (key_expr.startswith('"') and key_expr.endswith('"')) or (key_expr.startswith("'") and key_expr.endswith("'")):
                key_name = key_expr[1:-1]
            else:
                # The key might be a variable reference
                key_name = self.evaluate_expression(key_expr)
            
            logger.debug(f"Dictionary access - object: '{obj_name}', key: '{key_name}'")
            
            obj = self.variables.get(obj_name, {})
            logger.debug(f"Object value: {obj}")
            
            if isinstance(obj, dict) and str(key_name) in obj:
                result = obj[str(key_name)]
                logger.debug(f"Dictionary access successful: {result}")
                return result
            else:
                logger.error(f"Dictionary access failed - key '{key_name}' not found")
                logger.error(f"  Object '{obj_name}' contains: {obj}")
                logger.error(f"  Available keys: {list(obj.keys()) if isinstance(obj, dict) else 'Not a dictionary'}")
                logger.error(f"  Looking for key: '{key_name}' (type: {type(key_name)})")
                return None
        return None
    
    def handle_aggregation(self, line: str) -> Any:
        """Handle Runa aggregation operations."""
        # Example: "the sum of all numbers in list"
        if line.startswith('the sum of all '):
            # Extract variable name and collection
            var_part = line[len('the sum of all '):]
            if ' in ' in var_part:
                var_name, collection_name = var_part.split(' in ', 1)
                var_name = var_name.strip()
                collection_name = collection_name.strip()
                
                collection = self.variables.get(collection_name, [])
                if isinstance(collection, (list, dict)):
                    # Calculate sum (simplified)
                    total = 0
                    for item in collection:
                        if isinstance(item, (int, float)):
                            total += item
                    return total
        return 0
    
    def evaluate_condition(self, condition: str) -> bool:
        """Evaluate a condition expression."""
        # For now, return True
        # In a full implementation, we'd parse and evaluate the condition
        return True
    
    def evaluate_expression(self, expression: str) -> Any:
        """Evaluate a general expression."""
        expression = expression.strip()
        
        # Handle OR expressions first (e.g., "instruction at key "value" OR None")
        if ' OR ' in expression:
            left_expr, right_expr = expression.split(' OR ', 1)
            left_val = self.evaluate_expression(left_expr.strip())
            
            # In Runa, OR means "use left if it exists/is not None, otherwise use right"
            if left_val is not None:
                return left_val
            else:
                return self.evaluate_expression(right_expr.strip())
        
        # Handle 'type of' expressions
        if expression.startswith('type of '):
            value_expr = expression[len('type of '):].strip()
            value = self.evaluate_expression(value_expr)
            return type(value).__name__
        
        # Check if it's a variable reference
        if expression in self.variables:
            return self.variables[expression]
        
        # Check for special builtin functions
        if expression == 'current time':
            return time.time()
        elif expression == 'empty dictionary':
            return {}
        elif expression == 'empty list':
            return []
        elif expression.lower() == 'none':
            return None
        
        # Check if it's a literal
        if expression.isdigit():
            return int(expression)
        elif expression.replace('.', '').isdigit() and '.' in expression:
            return float(expression)
        elif expression.lower() in ['true', 'false']:
            return expression.lower() == 'true'
        elif expression.startswith('"') and expression.endswith('"'):
            return expression[1:-1]
        
        # Check if it's a collection operation FIRST (before arithmetic)
        if expression.startswith('length of ') or ' at index ' in expression or ' at key ' in expression:
            return self.handle_collection_operation(expression)
        
        # Check if it's a function call
        if ' with ' in expression:
            return self.handle_function_call(expression)
        
        # Check if it's an arithmetic operation
        if any(op in expression for op in [' plus ', ' minus ', ' multiplied by ', ' divided by ']):
            return self.handle_arithmetic(expression)
        
        # Check if it's a string concatenation
        if ' followed by ' in expression:
            return self.handle_string_concatenation(expression)
        
        # Check if it's a list creation
        if expression.startswith('list containing'):
            return self.handle_list_creation(expression)
        
        # Check if it's a dictionary creation
        if expression.startswith('dictionary with:') or expression.startswith('Dictionary with'):
            return self.handle_dictionary_creation(expression)
        
        # Try to convert to number if it looks like a number
        try:
            if '.' in expression:
                return float(expression)
            else:
                return int(expression)
        except ValueError:
            pass
        
        # Default: return the expression as a string (this might cause the string issue)
        # For debugging, let's see what expressions are falling through
        logger.debug(f"Expression not recognized, returning as string: '{expression}'")
        return expression
    
    def handle_otherwise_if_statement(self, line: str) -> Any:
        """Handle Runa otherwise if statements."""
        # Example: "Otherwise if operator is equal to "plus":"
        condition_part = line[len('Otherwise if '):].strip()
        if condition_part.endswith(':'):
            condition_part = condition_part[:-1]
        
        condition_result = self.evaluate_condition(condition_part)
        logger.debug(f"Otherwise if condition '{condition_part}' evaluated to: {condition_result}")
        return condition_result
    
    def handle_otherwise_statement(self, line: str) -> Any:
        """Handle Runa otherwise statements."""
        # Example: "Otherwise:"
        logger.debug("Otherwise statement executed")
        return True
    
    def handle_continue_statement(self) -> Any:
        """Handle Runa continue statements."""
        logger.debug("Continue statement executed")
        # In a full implementation, this would affect loop control
        return "CONTINUE"
    
    def handle_break_statement(self) -> Any:
        """Handle Runa break statements."""
        logger.debug("Break statement executed")
        # In a full implementation, this would affect loop control
        return "BREAK"


def main():
    """Main entry point for the Runa bootstrap runner."""
    if len(sys.argv) < 2:
        print("Usage: python runa_bootstrap.py <runa_file.runa> [--debug]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    debug = '--debug' in sys.argv
    
    if not file_path.endswith('.runa'):
        print("Error: File must have .runa extension")
        sys.exit(1)
    
    try:
        runner = RunaBootstrapRunner()
        result = runner.run_file(file_path, debug)
        
        if debug:
            print(f"\nExecution completed successfully!")
            print(f"Result: {result}")
            print(f"Variables: {runner.variables}")
            print(f"Functions: {list(runner.functions.keys())}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 