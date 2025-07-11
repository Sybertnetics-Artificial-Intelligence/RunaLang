#!/usr/bin/env python3
"""
Matlab ↔ Runa Converter

Bidirectional converter between Matlab AST and Runa AST, handling matrix operations,
functions, classes, and scientific computing constructs with proper semantic mapping.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass

from .matlab_ast import *
from ....core.runa_ast import *
from ....core.semantic import *


class MatlabToRunaConverter:
    """Converts Matlab AST to Runa AST."""
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.current_scope = "global"
        self.matrix_operations = {
            '+': 'add',
            '-': 'subtract', 
            '*': 'multiply',
            '/': 'divide',
            '^': 'power',
            '.*': 'element_multiply',
            './': 'element_divide',
            '.^': 'element_power',
            '\\': 'left_divide',
            '.\\': 'element_left_divide'
        }
        
    def convert_script(self, matlab_script: MatlabScript) -> ProgramNode:
        """Convert Matlab script to Runa program."""
        statements = []
        
        for stmt in matlab_script.statements:
            runa_stmt = self.convert_statement(stmt)
            if runa_stmt:
                statements.append(runa_stmt)
        
        return ProgramNode(statements=statements)
    
    def convert_statement(self, node: MatlabNode) -> Optional[ASTNode]:
        """Convert a Matlab statement to Runa."""
        if isinstance(node, MatlabFunctionDeclaration):
            return self.convert_function_declaration(node)
        elif isinstance(node, MatlabClassDeclaration):
            return self.convert_class_declaration(node)
        elif isinstance(node, MatlabIfStatement):
            return self.convert_if_statement(node)
        elif isinstance(node, MatlabForLoop):
            return self.convert_for_loop(node)
        elif isinstance(node, MatlabWhileLoop):
            return self.convert_while_loop(node)
        elif isinstance(node, MatlabTryCatchStatement):
            return self.convert_try_catch(node)
        elif isinstance(node, MatlabSwitchStatement):
            return self.convert_switch_statement(node)
        elif isinstance(node, MatlabAssignmentExpression):
            return self.convert_assignment(node)
        elif isinstance(node, MatlabGlobalDeclaration):
            return self.convert_global_declaration(node)
        elif isinstance(node, MatlabPersistentDeclaration):
            return self.convert_persistent_declaration(node)
        elif isinstance(node, MatlabBreakStatement):
            return BreakNode()
        elif isinstance(node, MatlabContinueStatement):
            return ContinueNode()
        elif isinstance(node, MatlabReturnStatement):
            return ReturnNode()
        elif isinstance(node, MatlabExpression):
            return self.convert_expression(node)
        else:
            return None
    
    def convert_function_declaration(self, node: MatlabFunctionDeclaration) -> FunctionNode:
        """Convert Matlab function to Runa function."""
        # Convert parameters
        params = [ParameterNode(name=p, type_annotation=None) for p in node.input_parameters]
        
        # Convert body
        body = []
        for stmt in node.body:
            runa_stmt = self.convert_statement(stmt)
            if runa_stmt:
                body.append(runa_stmt)
        
        # Handle multiple return values - create return statement if outputs specified
        if node.output_parameters:
            if len(node.output_parameters) == 1:
                return_type = None  # Infer from context
            else:
                # Multiple outputs -> tuple type
                return_type = None  # Will need tuple support
        else:
            return_type = None
        
        return FunctionNode(
            name=node.name,
            parameters=params,
            body=body,
            return_type=return_type
        )
    
    def convert_class_declaration(self, node: MatlabClassDeclaration) -> ClassNode:
        """Convert Matlab class to Runa class."""
        # Convert superclasses to inheritance
        inheritance = [create_identifier(sc) for sc in node.superclasses] if node.superclasses else []
        
        # Convert properties and methods
        members = []
        
        # Process properties blocks
        for props_block in node.properties_blocks:
            for prop in props_block.properties:
                # Convert property to field
                initial_value = self.convert_expression(prop.default_value) if prop.default_value else None
                field = FieldNode(
                    name=prop.name,
                    type_annotation=None,  # Infer from initial value
                    initial_value=initial_value
                )
                members.append(field)
        
        # Process methods blocks
        for methods_block in node.methods_blocks:
            for method in methods_block.methods:
                # Convert method to function
                params = [ParameterNode(name=p, type_annotation=None) for p in method.input_parameters]
                
                # Add 'self' parameter for instance methods (except static)
                is_static = method.attributes.get('Static', False)
                if not is_static:
                    self_param = ParameterNode(name='self', type_annotation=None)
                    params.insert(0, self_param)
                
                body = []
                for stmt in method.body:
                    runa_stmt = self.convert_statement(stmt)
                    if runa_stmt:
                        body.append(runa_stmt)
                
                method_node = FunctionNode(
                    name=method.name,
                    parameters=params,
                    body=body,
                    return_type=None
                )
                members.append(method_node)
        
        return ClassNode(
            name=node.name,
            inheritance=inheritance,
            members=members
        )
    
    def convert_if_statement(self, node: MatlabIfStatement) -> IfNode:
        """Convert Matlab if statement to Runa if."""
        condition = self.convert_expression(node.condition) if node.condition else None
        then_body = [self.convert_statement(stmt) for stmt in node.then_body if self.convert_statement(stmt)]
        
        # Handle elseif clauses
        elif_branches = []
        for elseif in node.elseif_clauses:
            elif_condition = self.convert_expression(elseif.condition) if elseif.condition else None
            elif_body = [self.convert_statement(stmt) for stmt in elseif.body if self.convert_statement(stmt)]
            elif_branches.append((elif_condition, elif_body))
        
        # Handle else clause
        else_body = [self.convert_statement(stmt) for stmt in node.else_body if self.convert_statement(stmt)] if node.else_body else None
        
        # Convert to Runa if-elif-else structure
        current_if = IfNode(
            condition=condition,
            then_body=then_body,
            else_body=else_body
        )
        
        # Chain elseif clauses in reverse order
        for elif_condition, elif_body in reversed(elif_branches):
            current_if = IfNode(
                condition=elif_condition,
                then_body=elif_body,
                else_body=[current_if] if current_if else []
            )
        
        return current_if
    
    def convert_for_loop(self, node: MatlabForLoop) -> ForNode:
        """Convert Matlab for loop to Runa for loop."""
        # Matlab: for i = 1:10 or for i = [1,2,3]
        iterable = self.convert_expression(node.iterable) if node.iterable else None
        
        # Convert range notation (1:10) to range() call
        if isinstance(iterable, BinaryExpressionNode) and iterable.operator == ':':
            # Convert to range call
            start = iterable.left
            stop = iterable.right
            iterable = FunctionCallNode(
                function=create_identifier('range'),
                arguments=[start, stop]
            )
        
        body = [self.convert_statement(stmt) for stmt in node.body if self.convert_statement(stmt)]
        
        return ForNode(
            variable=node.variable,
            iterable=iterable,
            body=body
        )
    
    def convert_while_loop(self, node: MatlabWhileLoop) -> WhileNode:
        """Convert Matlab while loop to Runa while loop."""
        condition = self.convert_expression(node.condition) if node.condition else None
        body = [self.convert_statement(stmt) for stmt in node.body if self.convert_statement(stmt)]
        
        return WhileNode(condition=condition, body=body)
    
    def convert_try_catch(self, node: MatlabTryCatchStatement) -> TryNode:
        """Convert Matlab try-catch to Runa try-catch."""
        try_body = [self.convert_statement(stmt) for stmt in node.try_body if self.convert_statement(stmt)]
        catch_body = [self.convert_statement(stmt) for stmt in node.catch_body if self.convert_statement(stmt)]
        
        # Create exception handler
        exception_type = create_identifier('Exception')  # Generic exception
        variable = node.exception_variable or 'error'
        
        catch_clause = ExceptionHandlerNode(
            exception_type=exception_type,
            variable=variable,
            body=catch_body
        )
        
        return TryNode(
            body=try_body,
            exception_handlers=[catch_clause],
            finally_body=[]
        )
    
    def convert_switch_statement(self, node: MatlabSwitchStatement) -> MatchNode:
        """Convert Matlab switch to Runa match."""
        expression = self.convert_expression(node.expression) if node.expression else None
        
        # Convert case clauses to match patterns
        patterns = []
        for case in node.case_clauses:
            # Handle multiple values in case
            for value in case.values:
                pattern_expr = self.convert_expression(value)
                body = [self.convert_statement(stmt) for stmt in case.body if self.convert_statement(stmt)]
                
                pattern = MatchPatternNode(
                    pattern=pattern_expr,
                    body=body
                )
                patterns.append(pattern)
        
        # Handle otherwise clause as default pattern
        if node.otherwise_clause:
            default_body = [self.convert_statement(stmt) for stmt in node.otherwise_clause.body if self.convert_statement(stmt)]
            default_pattern = MatchPatternNode(
                pattern=create_identifier('_'),  # Wildcard pattern
                body=default_body
            )
            patterns.append(default_pattern)
        
        return MatchNode(expression=expression, patterns=patterns)
    
    def convert_assignment(self, node: MatlabAssignmentExpression) -> AssignmentNode:
        """Convert Matlab assignment to Runa assignment."""
        value = self.convert_expression(node.value) if node.value else None
        
        if len(node.targets) == 1:
            # Single assignment
            target = self.convert_expression(node.targets[0])
            return AssignmentNode(target=target, value=value)
        else:
            # Multiple assignment [a, b] = func()
            # Convert to tuple unpacking
            targets = [self.convert_expression(t) for t in node.targets]
            tuple_target = TupleNode(elements=targets)
            return AssignmentNode(target=tuple_target, value=value)
    
    def convert_global_declaration(self, node: MatlabGlobalDeclaration) -> List[VariableNode]:
        """Convert Matlab global declaration to Runa variables with global scope."""
        variables = []
        for var_name in node.variables:
            var_node = VariableNode(
                name=var_name,
                type_annotation=None,
                initial_value=None
            )
            variables.append(var_node)
        return variables
    
    def convert_persistent_declaration(self, node: MatlabPersistentDeclaration) -> List[VariableNode]:
        """Convert Matlab persistent declaration to Runa static variables."""
        variables = []
        for var_name in node.variables:
            var_node = VariableNode(
                name=var_name,
                type_annotation=None,
                initial_value=None
            )
            variables.append(var_node)
        return variables
    
    def convert_expression(self, node: MatlabExpression) -> Optional[ExpressionNode]:
        """Convert Matlab expression to Runa expression."""
        if isinstance(node, MatlabIdentifier):
            return create_identifier(node.name)
        
        elif isinstance(node, MatlabLiteralExpression):
            return LiteralNode(value=node.value)
        
        elif isinstance(node, MatlabStringExpression):
            return StringLiteralNode(value=node.value)
        
        elif isinstance(node, MatlabBinaryExpression):
            return self.convert_binary_expression(node)
        
        elif isinstance(node, MatlabUnaryExpression):
            return self.convert_unary_expression(node)
        
        elif isinstance(node, MatlabFunctionCall):
            return self.convert_function_call(node)
        
        elif isinstance(node, MatlabMethodCall):
            return self.convert_method_call(node)
        
        elif isinstance(node, MatlabFieldAccess):
            return self.convert_field_access(node)
        
        elif isinstance(node, MatlabMatrixExpression):
            return self.convert_matrix_expression(node)
        
        elif isinstance(node, MatlabCellArray):
            return self.convert_cell_array(node)
        
        elif isinstance(node, MatlabIndexingExpression):
            return self.convert_indexing_expression(node)
        
        elif isinstance(node, MatlabAnonymousFunction):
            return self.convert_anonymous_function(node)
        
        elif isinstance(node, MatlabFunctionHandle):
            return self.convert_function_handle(node)
        
        else:
            return None
    
    def convert_binary_expression(self, node: MatlabBinaryExpression) -> BinaryExpressionNode:
        """Convert Matlab binary expression to Runa."""
        left = self.convert_expression(node.left)
        right = self.convert_expression(node.right)
        
        # Handle matrix operations
        if node.operator in self.matrix_operations:
            if node.is_elementwise:
                # Element-wise operations
                operator = self.matrix_operations[node.operator]
                # Could be converted to special element-wise function calls
                return BinaryExpressionNode(left=left, operator=operator, right=right)
            else:
                # Matrix operations
                operator = self.matrix_operations[node.operator]
                return BinaryExpressionNode(left=left, operator=operator, right=right)
        
        # Handle range operator
        elif node.operator == ':':
            # Convert to range() function call or slice
            if isinstance(left, LiteralNode) and isinstance(right, LiteralNode):
                return FunctionCallNode(
                    function=create_identifier('range'),
                    arguments=[left, right]
                )
            else:
                return SliceNode(start=left, stop=right, step=None)
        
        # Standard operators
        else:
            return BinaryExpressionNode(left=left, operator=node.operator, right=right)
    
    def convert_unary_expression(self, node: MatlabUnaryExpression) -> UnaryExpressionNode:
        """Convert Matlab unary expression to Runa."""
        expression = self.convert_expression(node.expression)
        
        # Handle transpose operator
        if node.operator == "'" or node.operator == ".'":
            # Convert to method call: matrix.transpose()
            return MethodCallNode(
                object=expression,
                method_name='transpose',
                arguments=[]
            )
        else:
            return UnaryExpressionNode(operator=node.operator, expression=expression)
    
    def convert_function_call(self, node: MatlabFunctionCall) -> FunctionCallNode:
        """Convert Matlab function call to Runa."""
        function = self.convert_expression(node.function)
        arguments = [self.convert_expression(arg) for arg in node.arguments]
        
        return FunctionCallNode(function=function, arguments=arguments)
    
    def convert_method_call(self, node: MatlabMethodCall) -> MethodCallNode:
        """Convert Matlab method call to Runa."""
        object_expr = self.convert_expression(node.object)
        arguments = [self.convert_expression(arg) for arg in node.arguments]
        
        return MethodCallNode(
            object=object_expr,
            method_name=node.method_name,
            arguments=arguments
        )
    
    def convert_field_access(self, node: MatlabFieldAccess) -> AttributeAccessNode:
        """Convert Matlab field access to Runa attribute access."""
        object_expr = self.convert_expression(node.object)
        
        return AttributeAccessNode(
            object=object_expr,
            attribute=node.field_name
        )
    
    def convert_matrix_expression(self, node: MatlabMatrixExpression) -> ListNode:
        """Convert Matlab matrix to Runa list (or specialized matrix type)."""
        if len(node.rows) == 1:
            # Single row - convert to list
            elements = [self.convert_expression(expr) for expr in node.rows[0]]
            return ListNode(elements=elements)
        else:
            # Multiple rows - convert to list of lists
            rows = []
            for row in node.rows:
                row_elements = [self.convert_expression(expr) for expr in row]
                rows.append(ListNode(elements=row_elements))
            return ListNode(elements=rows)
    
    def convert_cell_array(self, node: MatlabCellArray) -> ListNode:
        """Convert Matlab cell array to Runa list."""
        if len(node.rows) == 1:
            # Single row
            elements = [self.convert_expression(expr) for expr in node.rows[0]]
            return ListNode(elements=elements)
        else:
            # Multiple rows
            rows = []
            for row in node.rows:
                row_elements = [self.convert_expression(expr) for expr in row]
                rows.append(ListNode(elements=row_elements))
            return ListNode(elements=rows)
    
    def convert_indexing_expression(self, node: MatlabIndexingExpression) -> IndexAccessNode:
        """Convert Matlab indexing to Runa index access."""
        array = self.convert_expression(node.array)
        
        if len(node.indices) == 1:
            index = self.convert_expression(node.indices[0])
            return IndexAccessNode(object=array, index=index)
        else:
            # Multiple indices - convert to tuple
            indices = [self.convert_expression(idx) for idx in node.indices]
            index_tuple = TupleNode(elements=indices)
            return IndexAccessNode(object=array, index=index_tuple)
    
    def convert_anonymous_function(self, node: MatlabAnonymousFunction) -> LambdaNode:
        """Convert Matlab anonymous function to Runa lambda."""
        parameters = [ParameterNode(name=p, type_annotation=None) for p in node.parameters]
        body = self.convert_expression(node.expression) if node.expression else None
        
        return LambdaNode(parameters=parameters, body=body)
    
    def convert_function_handle(self, node: MatlabFunctionHandle) -> IdentifierNode:
        """Convert Matlab function handle to Runa identifier."""
        return create_identifier(node.function_name)


class RunaToMatlabConverter:
    """Converts Runa AST to Matlab AST."""
    
    def __init__(self):
        self.current_scope = "global"
        self.operator_map = {
            'add': '+',
            'subtract': '-',
            'multiply': '*',
            'divide': '/',
            'power': '^',
            'element_multiply': '.*',
            'element_divide': './',
            'element_power': '.^'
        }
    
    def convert_program(self, program: ProgramNode) -> MatlabScript:
        """Convert Runa program to Matlab script."""
        statements = []
        comments = []
        
        for stmt in program.statements:
            matlab_stmt = self.convert_statement(stmt)
            if matlab_stmt:
                statements.append(matlab_stmt)
        
        return MatlabScript(statements=statements, comments=comments)
    
    def convert_statement(self, node: ASTNode) -> Optional[MatlabNode]:
        """Convert Runa statement to Matlab."""
        if isinstance(node, FunctionNode):
            return self.convert_function_declaration(node)
        elif isinstance(node, ClassNode):
            return self.convert_class_declaration(node)
        elif isinstance(node, IfNode):
            return self.convert_if_statement(node)
        elif isinstance(node, ForNode):
            return self.convert_for_loop(node)
        elif isinstance(node, WhileNode):
            return self.convert_while_loop(node)
        elif isinstance(node, TryNode):
            return self.convert_try_statement(node)
        elif isinstance(node, MatchNode):
            return self.convert_match_statement(node)
        elif isinstance(node, AssignmentNode):
            return self.convert_assignment(node)
        elif isinstance(node, BreakNode):
            return MatlabBreakStatement()
        elif isinstance(node, ContinueNode):
            return MatlabContinueStatement()
        elif isinstance(node, ReturnNode):
            return MatlabReturnStatement()
        elif isinstance(node, ExpressionNode):
            return self.convert_expression(node)
        else:
            return None
    
    def convert_function_declaration(self, node: FunctionNode) -> MatlabFunctionDeclaration:
        """Convert Runa function to Matlab function."""
        # Extract parameter names
        input_params = [p.name for p in node.parameters]
        
        # Convert body
        body = []
        for stmt in node.body:
            matlab_stmt = self.convert_statement(stmt)
            if matlab_stmt:
                body.append(matlab_stmt)
        
        # Handle return type (if multiple returns, extract from return statements)
        output_params = []
        # TODO: Analyze return statements to determine output parameters
        
        return MatlabFunctionDeclaration(
            name=node.name,
            input_parameters=input_params,
            output_parameters=output_params,
            body=body
        )
    
    def convert_class_declaration(self, node: ClassNode) -> MatlabClassDeclaration:
        """Convert Runa class to Matlab class."""
        # Extract superclass names
        superclasses = []
        for inheritance in node.inheritance:
            if isinstance(inheritance, IdentifierNode):
                superclasses.append(inheritance.name)
        
        # Separate fields and methods
        properties = []
        methods = []
        
        for member in node.members:
            if isinstance(member, FieldNode):
                prop = MatlabPropertyDeclaration(
                    name=member.name,
                    default_value=self.convert_expression(member.initial_value) if member.initial_value else None
                )
                properties.append(prop)
            elif isinstance(member, FunctionNode):
                # Convert to method
                input_params = [p.name for p in member.parameters if p.name != 'self']
                
                body = []
                for stmt in member.body:
                    matlab_stmt = self.convert_statement(stmt)
                    if matlab_stmt:
                        body.append(matlab_stmt)
                
                method = MatlabMethodDeclaration(
                    name=member.name,
                    input_parameters=input_params,
                    output_parameters=[],  # TODO: Extract from returns
                    body=body
                )
                methods.append(method)
        
        # Create properties and methods blocks
        props_block = MatlabPropertiesBlock(properties=properties)
        methods_block = MatlabMethodsBlock(methods=methods)
        
        return MatlabClassDeclaration(
            name=node.name,
            superclasses=superclasses,
            properties_blocks=[props_block] if properties else [],
            methods_blocks=[methods_block] if methods else []
        )
    
    def convert_if_statement(self, node: IfNode) -> MatlabIfStatement:
        """Convert Runa if to Matlab if."""
        condition = self.convert_expression(node.condition) if node.condition else None
        then_body = [self.convert_statement(stmt) for stmt in node.then_body if self.convert_statement(stmt)]
        
        # Handle else body (may contain nested if for elif)
        else_body = []
        elseif_clauses = []
        
        if node.else_body:
            for stmt in node.else_body:
                if isinstance(stmt, IfNode):
                    # This is an elif
                    elif_condition = self.convert_expression(stmt.condition) if stmt.condition else None
                    elif_body = [self.convert_statement(s) for s in stmt.then_body if self.convert_statement(s)]
                    
                    elseif_clause = MatlabElseifClause(
                        condition=elif_condition,
                        body=elif_body
                    )
                    elseif_clauses.append(elseif_clause)
                    
                    # Handle nested else
                    if stmt.else_body:
                        else_body.extend([self.convert_statement(s) for s in stmt.else_body if self.convert_statement(s)])
                else:
                    matlab_stmt = self.convert_statement(stmt)
                    if matlab_stmt:
                        else_body.append(matlab_stmt)
        
        return MatlabIfStatement(
            condition=condition,
            then_body=then_body,
            elseif_clauses=elseif_clauses,
            else_body=else_body
        )
    
    def convert_for_loop(self, node: ForNode) -> MatlabForLoop:
        """Convert Runa for loop to Matlab for."""
        iterable = self.convert_expression(node.iterable) if node.iterable else None
        body = [self.convert_statement(stmt) for stmt in node.body if self.convert_statement(stmt)]
        
        return MatlabForLoop(
            variable=node.variable,
            iterable=iterable,
            body=body
        )
    
    def convert_while_loop(self, node: WhileNode) -> MatlabWhileLoop:
        """Convert Runa while to Matlab while."""
        condition = self.convert_expression(node.condition) if node.condition else None
        body = [self.convert_statement(stmt) for stmt in node.body if self.convert_statement(stmt)]
        
        return MatlabWhileLoop(condition=condition, body=body)
    
    def convert_try_statement(self, node: TryNode) -> MatlabTryCatchStatement:
        """Convert Runa try to Matlab try-catch."""
        try_body = [self.convert_statement(stmt) for stmt in node.body if self.convert_statement(stmt)]
        
        # Handle first exception handler
        catch_body = []
        exception_variable = None
        
        if node.exception_handlers:
            handler = node.exception_handlers[0]  # Take first handler
            catch_body = [self.convert_statement(stmt) for stmt in handler.body if self.convert_statement(stmt)]
            exception_variable = handler.variable
        
        return MatlabTryCatchStatement(
            try_body=try_body,
            catch_body=catch_body,
            exception_variable=exception_variable
        )
    
    def convert_match_statement(self, node: MatchNode) -> MatlabSwitchStatement:
        """Convert Runa match to Matlab switch."""
        expression = self.convert_expression(node.expression) if node.expression else None
        
        case_clauses = []
        otherwise_clause = None
        
        for pattern in node.patterns:
            if isinstance(pattern.pattern, IdentifierNode) and pattern.pattern.name == '_':
                # Wildcard pattern -> otherwise
                body = [self.convert_statement(stmt) for stmt in pattern.body if self.convert_statement(stmt)]
                otherwise_clause = MatlabOtherwiseClause(body=body)
            else:
                # Regular case
                value = self.convert_expression(pattern.pattern)
                body = [self.convert_statement(stmt) for stmt in pattern.body if self.convert_statement(stmt)]
                
                case_clause = MatlabCaseClause(values=[value], body=body)
                case_clauses.append(case_clause)
        
        return MatlabSwitchStatement(
            expression=expression,
            case_clauses=case_clauses,
            otherwise_clause=otherwise_clause
        )
    
    def convert_assignment(self, node: AssignmentNode) -> MatlabAssignmentExpression:
        """Convert Runa assignment to Matlab assignment."""
        value = self.convert_expression(node.value) if node.value else None
        
        # Handle tuple unpacking
        if isinstance(node.target, TupleNode):
            targets = [self.convert_expression(elem) for elem in node.target.elements]
        else:
            targets = [self.convert_expression(node.target)]
        
        return MatlabAssignmentExpression(targets=targets, value=value)
    
    def convert_expression(self, node: ExpressionNode) -> Optional[MatlabExpression]:
        """Convert Runa expression to Matlab expression."""
        if isinstance(node, IdentifierNode):
            return MatlabIdentifier(name=node.name)
        
        elif isinstance(node, LiteralNode):
            return MatlabLiteralExpression(value=node.value)
        
        elif isinstance(node, StringLiteralNode):
            return MatlabStringExpression(value=node.value, is_char_array=True)
        
        elif isinstance(node, BinaryExpressionNode):
            left = self.convert_expression(node.left)
            right = self.convert_expression(node.right)
            
            # Map operators
            operator = self.operator_map.get(node.operator, node.operator)
            is_elementwise = operator.startswith('.')
            
            return MatlabBinaryExpression(
                left=left,
                operator=operator,
                right=right,
                is_elementwise=is_elementwise
            )
        
        elif isinstance(node, UnaryExpressionNode):
            expression = self.convert_expression(node.expression)
            return MatlabUnaryExpression(operator=node.operator, expression=expression)
        
        elif isinstance(node, FunctionCallNode):
            function = self.convert_expression(node.function)
            arguments = [self.convert_expression(arg) for arg in node.arguments]
            return MatlabFunctionCall(function=function, arguments=arguments)
        
        elif isinstance(node, MethodCallNode):
            object_expr = self.convert_expression(node.object)
            arguments = [self.convert_expression(arg) for arg in node.arguments]
            return MatlabMethodCall(
                object=object_expr,
                method_name=node.method_name,
                arguments=arguments
            )
        
        elif isinstance(node, AttributeAccessNode):
            object_expr = self.convert_expression(node.object)
            return MatlabFieldAccess(object=object_expr, field_name=node.attribute)
        
        elif isinstance(node, ListNode):
            # Convert list to matrix (single row)
            elements = [self.convert_expression(elem) for elem in node.elements]
            return MatlabMatrixExpression(rows=[elements])
        
        elif isinstance(node, IndexAccessNode):
            array = self.convert_expression(node.object)
            
            if isinstance(node.index, TupleNode):
                indices = [self.convert_expression(elem) for elem in node.index.elements]
            else:
                indices = [self.convert_expression(node.index)]
            
            return MatlabIndexingExpression(
                array=array,
                indices=indices,
                indexing_type="paren"
            )
        
        elif isinstance(node, LambdaNode):
            params = [p.name for p in node.parameters]
            expression = self.convert_expression(node.body) if node.body else None
            return MatlabAnonymousFunction(parameters=params, expression=expression)
        
        else:
            return None 