#!/usr/bin/env python3
"""
Unit tests for C# ↔ Runa Converter

Tests bidirectional conversion between C# AST and Runa AST,
focusing on .NET framework features, LINQ, and C#-specific constructs.
"""

import unittest
from unittest.mock import Mock, patch
from typing import List, Dict, Any
import sys
import os

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../src'))

from runa.languages.tier1.csharp.csharp_converter import CSharpToRunaConverter, RunaToCSharpConverter
from runa.languages.tier1.csharp.csharp_ast import *
from runa.core.runa_ast import *


class TestCSharpToRunaConverter(unittest.TestCase):
    """Test C# AST to Runa AST conversion."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.converter = CSharpToRunaConverter()
    
    def test_variable_declaration(self):
        """Test conversion of variable declarations."""
        # C#: int x = 42;
        csharp_ast = CSharpCompilationUnit([
            CSharpVariableDeclaration(
                type=CSharpPredefinedType('int'),
                declarators=[
                    CSharpVariableDeclarator(
                        identifier='x',
                        initializer=CSharpLiteralExpression(value=42)
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(csharp_ast)
        
        self.assertIsInstance(runa_program, Program)
        self.assertEqual(len(runa_program.statements), 1)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        self.assertEqual(stmt.name, 'x')
        self.assertIsInstance(stmt.type_annotation, TypeReference)
        self.assertEqual(stmt.type_annotation.name, 'int')
        self.assertIsInstance(stmt.value, NumericLiteral)
        self.assertEqual(stmt.value.value, 42)
    
    def test_var_declaration(self):
        """Test conversion of var declarations with type inference."""
        # C#: var message = "Hello World";
        csharp_ast = CSharpCompilationUnit([
            CSharpVariableDeclaration(
                type=CSharpVarKeyword(),
                declarators=[
                    CSharpVariableDeclarator(
                        identifier='message',
                        initializer=CSharpLiteralExpression(value="Hello World")
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(csharp_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        self.assertEqual(stmt.name, 'message')
        # Type should be inferred from value
        self.assertIsInstance(stmt.value, StringLiteral)
    
    def test_method_declaration(self):
        """Test conversion of method declarations."""
        # C#: public int Add(int a, int b) { return a + b; }
        csharp_ast = CSharpCompilationUnit([
            CSharpClassDeclaration(
                identifier='Calculator',
                members=[
                    CSharpMethodDeclaration(
                        modifiers=[CSharpPublicKeyword()],
                        return_type=CSharpPredefinedType('int'),
                        identifier='Add',
                        parameter_list=[
                            CSharpParameter(
                                type=CSharpPredefinedType('int'),
                                identifier='a'
                            ),
                            CSharpParameter(
                                type=CSharpPredefinedType('int'),
                                identifier='b'
                            )
                        ],
                        body=CSharpBlock([
                            CSharpReturnStatement(
                                expression=CSharpBinaryExpression(
                                    left=CSharpIdentifierName('a'),
                                    operator_token='+',
                                    right=CSharpIdentifierName('b')
                                )
                            )
                        ])
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(csharp_ast)
        
        class_stmt = runa_program.statements[0]
        self.assertIsInstance(class_stmt, ClassDeclaration)
        
        method = class_stmt.methods[0]
        self.assertIsInstance(method, FunctionDeclaration)
        self.assertEqual(method.name, 'Add')
        self.assertEqual(len(method.parameters), 2)
        self.assertEqual(method.access_modifier, 'public')
    
    def test_property_declaration(self):
        """Test conversion of C# properties."""
        # C#: public string Name { get; set; }
        csharp_ast = CSharpCompilationUnit([
            CSharpClassDeclaration(
                identifier='Person',
                members=[
                    CSharpPropertyDeclaration(
                        modifiers=[CSharpPublicKeyword()],
                        type=CSharpPredefinedType('string'),
                        identifier='Name',
                        accessor_list=[
                            CSharpAccessorDeclaration(kind='get'),
                            CSharpAccessorDeclaration(kind='set')
                        ]
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(csharp_ast)
        
        class_stmt = runa_program.statements[0]
        property = class_stmt.properties[0]
        self.assertIsInstance(property, PropertyDeclaration)
        self.assertEqual(property.name, 'Name')
        self.assertTrue(property.has_getter)
        self.assertTrue(property.has_setter)
    
    def test_namespace_declaration(self):
        """Test conversion of namespace declarations."""
        # C#: namespace MyProject.Models { }
        csharp_ast = CSharpCompilationUnit([
            CSharpNamespaceDeclaration(
                name='MyProject.Models',
                members=[]
            )
        ])
        
        runa_program = self.converter.convert(csharp_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, NamespaceDeclaration)
        self.assertEqual(stmt.name, 'MyProject.Models')
    
    def test_using_directive(self):
        """Test conversion of using directives."""
        # C#: using System; using System.Collections.Generic;
        csharp_ast = CSharpCompilationUnit([
            CSharpUsingDirective(name='System'),
            CSharpUsingDirective(name='System.Collections.Generic')
        ])
        
        runa_program = self.converter.convert(csharp_ast)
        
        # Using directives should be converted to import statements
        import_stmts = [s for s in runa_program.statements if isinstance(s, ImportStatement)]
        self.assertEqual(len(import_stmts), 2)
        self.assertEqual(import_stmts[0].module, 'System')
        self.assertEqual(import_stmts[1].module, 'System.Collections.Generic')
    
    def test_generic_class(self):
        """Test conversion of generic classes."""
        # C#: public class Container<T> where T : class { }
        csharp_ast = CSharpCompilationUnit([
            CSharpClassDeclaration(
                modifiers=[CSharpPublicKeyword()],
                identifier='Container',
                type_parameter_list=[
                    CSharpTypeParameter(identifier='T')
                ],
                constraint_clauses=[
                    CSharpTypeParameterConstraintClause(
                        name='T',
                        constraints=[CSharpClassConstraint()]
                    )
                ],
                members=[]
            )
        ])
        
        runa_program = self.converter.convert(csharp_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, ClassDeclaration)
        self.assertEqual(stmt.name, 'Container')
        self.assertEqual(len(stmt.type_parameters), 1)
        self.assertEqual(stmt.type_parameters[0].name, 'T')
        # Check that constraints are preserved
        self.assertIsNotNone(stmt.type_parameters[0].constraints)
    
    def test_interface_declaration(self):
        """Test conversion of interface declarations."""
        # C#: public interface IDrawable { void Draw(); }
        csharp_ast = CSharpCompilationUnit([
            CSharpInterfaceDeclaration(
                modifiers=[CSharpPublicKeyword()],
                identifier='IDrawable',
                members=[
                    CSharpMethodDeclaration(
                        return_type=CSharpPredefinedType('void'),
                        identifier='Draw',
                        parameter_list=[]
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(csharp_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, InterfaceDeclaration)
        self.assertEqual(stmt.name, 'IDrawable')
        self.assertEqual(len(stmt.methods), 1)
        self.assertEqual(stmt.methods[0].name, 'Draw')
    
    def test_linq_query(self):
        """Test conversion of LINQ queries."""
        # C#: var result = from x in numbers where x > 5 select x * 2;
        csharp_ast = CSharpCompilationUnit([
            CSharpVariableDeclaration(
                type=CSharpVarKeyword(),
                declarators=[
                    CSharpVariableDeclarator(
                        identifier='result',
                        initializer=CSharpQueryExpression(
                            from_clause=CSharpFromClause(
                                identifier='x',
                                expression=CSharpIdentifierName('numbers')
                            ),
                            body=CSharpQueryBody(
                                clauses=[
                                    CSharpWhereClause(
                                        condition=CSharpBinaryExpression(
                                            left=CSharpIdentifierName('x'),
                                            operator_token='>',
                                            right=CSharpLiteralExpression(value=5)
                                        )
                                    )
                                ],
                                select_clause=CSharpSelectClause(
                                    expression=CSharpBinaryExpression(
                                        left=CSharpIdentifierName('x'),
                                        operator_token='*',
                                        right=CSharpLiteralExpression(value=2)
                                    )
                                )
                            )
                        )
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(csharp_ast)
        
        # LINQ should be converted to functional programming constructs
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        # The converted expression should represent the filtering and mapping
        self.assertIsNotNone(stmt.value)
    
    def test_async_await(self):
        """Test conversion of async/await patterns."""
        # C#: public async Task<string> FetchDataAsync() { return await client.GetStringAsync(url); }
        csharp_ast = CSharpCompilationUnit([
            CSharpClassDeclaration(
                identifier='DataService',
                members=[
                    CSharpMethodDeclaration(
                        modifiers=[CSharpPublicKeyword(), CSharpAsyncKeyword()],
                        return_type=CSharpGenericName(
                            identifier='Task',
                            type_argument_list=[CSharpPredefinedType('string')]
                        ),
                        identifier='FetchDataAsync',
                        parameter_list=[],
                        body=CSharpBlock([
                            CSharpReturnStatement(
                                expression=CSharpAwaitExpression(
                                    expression=CSharpInvocationExpression(
                                        expression=CSharpMemberAccessExpression(
                                            expression=CSharpIdentifierName('client'),
                                            name=CSharpIdentifierName('GetStringAsync')
                                        ),
                                        argument_list=[CSharpIdentifierName('url')]
                                    )
                                )
                            )
                        ])
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(csharp_ast)
        
        class_stmt = runa_program.statements[0]
        method = class_stmt.methods[0]
        self.assertTrue(method.is_async)
        # Check that await expressions are preserved
        return_stmt = method.body[0]
        self.assertIsInstance(return_stmt.value, AwaitExpression)
    
    def test_nullable_types(self):
        """Test conversion of nullable types."""
        # C#: int? nullableInt = null;
        csharp_ast = CSharpCompilationUnit([
            CSharpVariableDeclaration(
                type=CSharpNullableType(
                    element_type=CSharpPredefinedType('int')
                ),
                declarators=[
                    CSharpVariableDeclarator(
                        identifier='nullableInt',
                        initializer=CSharpLiteralExpression(value=None)
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(csharp_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        # Nullable type should be converted to optional type
        self.assertIsInstance(stmt.type_annotation, OptionalType)
        self.assertEqual(stmt.type_annotation.inner_type.name, 'int')
    
    def test_exception_handling(self):
        """Test conversion of try-catch-finally blocks."""
        # C#: try { risky(); } catch (Exception ex) { handle(ex); } finally { cleanup(); }
        csharp_ast = CSharpCompilationUnit([
            CSharpTryStatement(
                block=CSharpBlock([
                    CSharpExpressionStatement(
                        expression=CSharpInvocationExpression(
                            expression=CSharpIdentifierName('risky'),
                            argument_list=[]
                        )
                    )
                ]),
                catches=[
                    CSharpCatchClause(
                        declaration=CSharpCatchDeclaration(
                            type=CSharpIdentifierName('Exception'),
                            identifier='ex'
                        ),
                        block=CSharpBlock([
                            CSharpExpressionStatement(
                                expression=CSharpInvocationExpression(
                                    expression=CSharpIdentifierName('handle'),
                                    argument_list=[CSharpIdentifierName('ex')]
                                )
                            )
                        ])
                    )
                ],
                finally_clause=CSharpFinallyClause(
                    block=CSharpBlock([
                        CSharpExpressionStatement(
                            expression=CSharpInvocationExpression(
                                expression=CSharpIdentifierName('cleanup'),
                                argument_list=[]
                            )
                        )
                    ])
                )
            )
        ])
        
        runa_program = self.converter.convert(csharp_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, TryStatement)
        self.assertEqual(len(stmt.handlers), 1)
        self.assertIsNotNone(stmt.finally_clause)


class TestRunaToCSharpConverter(unittest.TestCase):
    """Test Runa AST to C# AST conversion."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.converter = RunaToCSharpConverter()
    
    def test_variable_declaration_conversion(self):
        """Test conversion of variable declarations."""
        # Runa: Let x as Integer be 42
        runa_program = Program([
            VariableDeclaration(
                name='x',
                type_annotation=TypeReference(name='Integer'),
                value=NumericLiteral(value=42)
            )
        ])
        
        csharp_unit = self.converter.convert(runa_program)
        
        self.assertIsInstance(csharp_unit, CSharpCompilationUnit)
        stmt = csharp_unit.members[0]
        self.assertIsInstance(stmt, CSharpVariableDeclaration)
        self.assertEqual(stmt.type.keyword, 'int')  # Integer -> int mapping
        self.assertEqual(stmt.declarators[0].identifier, 'x')
    
    def test_function_conversion(self):
        """Test conversion of function declarations to methods."""
        # Runa: Define public Add with a as Integer and b as Integer returning Integer
        runa_program = Program([
            FunctionDeclaration(
                name='Add',
                parameters=[
                    Parameter(
                        name='a',
                        type_annotation=TypeReference(name='Integer')
                    ),
                    Parameter(
                        name='b',
                        type_annotation=TypeReference(name='Integer')
                    )
                ],
                return_type=TypeReference(name='Integer'),
                access_modifier='public',
                body=[
                    ReturnStatement(
                        value=BinaryOperation(
                            left=Identifier(name='a'),
                            operator='plus',
                            right=Identifier(name='b')
                        )
                    )
                ]
            )
        ])
        
        csharp_unit = self.converter.convert(runa_program)
        
        # Function should be converted to method in a generated class
        class_decl = csharp_unit.members[0]
        self.assertIsInstance(class_decl, CSharpClassDeclaration)
        
        method = class_decl.members[0]
        self.assertIsInstance(method, CSharpMethodDeclaration)
        self.assertEqual(method.identifier, 'Add')
        self.assertEqual(len(method.parameter_list), 2)
    
    def test_class_conversion(self):
        """Test conversion of class declarations."""
        # Runa: Define public type Person with Name as String property
        runa_program = Program([
            ClassDeclaration(
                name='Person',
                access_modifier='public',
                properties=[
                    PropertyDeclaration(
                        name='Name',
                        type_annotation=TypeReference(name='String'),
                        has_getter=True,
                        has_setter=True
                    )
                ]
            )
        ])
        
        csharp_unit = self.converter.convert(runa_program)
        
        class_decl = csharp_unit.members[0]
        self.assertIsInstance(class_decl, CSharpClassDeclaration)
        self.assertEqual(class_decl.identifier, 'Person')
        
        property = class_decl.members[0]
        self.assertIsInstance(property, CSharpPropertyDeclaration)
        self.assertEqual(property.identifier, 'Name')
    
    def test_interface_conversion(self):
        """Test conversion of interface declarations."""
        # Runa: Define interface IDrawable with Draw method
        runa_program = Program([
            InterfaceDeclaration(
                name='IDrawable',
                methods=[
                    FunctionDeclaration(
                        name='Draw',
                        parameters=[]
                    )
                ]
            )
        ])
        
        csharp_unit = self.converter.convert(runa_program)
        
        interface_decl = csharp_unit.members[0]
        self.assertIsInstance(interface_decl, CSharpInterfaceDeclaration)
        self.assertEqual(interface_decl.identifier, 'IDrawable')
        
        method = interface_decl.members[0]
        self.assertEqual(method.identifier, 'Draw')
    
    def test_async_conversion(self):
        """Test conversion of async functions."""
        # Runa: Define async FetchData returning Task of String
        runa_program = Program([
            FunctionDeclaration(
                name='FetchData',
                parameters=[],
                return_type=TypeReference(name='Task[String]'),
                is_async=True,
                body=[
                    ReturnStatement(
                        value=AwaitExpression(
                            expression=FunctionCall(
                                function=Identifier(name='GetAsync'),
                                arguments=[StringLiteral(value="/api/data")]
                            )
                        )
                    )
                ]
            )
        ])
        
        csharp_unit = self.converter.convert(runa_program)
        
        method = csharp_unit.members[0].members[0]  # Method inside generated class
        self.assertIn('async', [mod.keyword for mod in method.modifiers if hasattr(mod, 'keyword')])
        self.assertIsInstance(method.return_type, CSharpGenericName)
        self.assertEqual(method.return_type.identifier, 'Task')


class TestCSharpSpecificFeatures(unittest.TestCase):
    """Test C#-specific language features."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.csharp_to_runa = CSharpToRunaConverter()
        self.runa_to_csharp = RunaToCSharpConverter()
    
    def test_extension_methods(self):
        """Test handling of extension methods."""
        # C#: public static class StringExtensions { public static bool IsEmpty(this string str) { } }
        csharp_ast = CSharpCompilationUnit([
            CSharpClassDeclaration(
                modifiers=[CSharpPublicKeyword(), CSharpStaticKeyword()],
                identifier='StringExtensions',
                members=[
                    CSharpMethodDeclaration(
                        modifiers=[CSharpPublicKeyword(), CSharpStaticKeyword()],
                        return_type=CSharpPredefinedType('bool'),
                        identifier='IsEmpty',
                        parameter_list=[
                            CSharpParameter(
                                modifiers=[CSharpThisKeyword()],
                                type=CSharpPredefinedType('string'),
                                identifier='str'
                            )
                        ],
                        body=CSharpBlock([])
                    )
                ]
            )
        ])
        
        runa_program = self.csharp_to_runa.convert(csharp_ast)
        
        # Extension methods should be converted with special annotations
        class_stmt = runa_program.statements[0]
        method = class_stmt.methods[0]
        self.assertTrue(method.is_extension_method)
    
    def test_operator_overloading(self):
        """Test handling of operator overloading."""
        # C#: public static Vector operator +(Vector a, Vector b) { }
        csharp_ast = CSharpCompilationUnit([
            CSharpClassDeclaration(
                identifier='Vector',
                members=[
                    CSharpOperatorDeclaration(
                        modifiers=[CSharpPublicKeyword(), CSharpStaticKeyword()],
                        return_type=CSharpIdentifierName('Vector'),
                        operator_token='+',
                        parameter_list=[
                            CSharpParameter(
                                type=CSharpIdentifierName('Vector'),
                                identifier='a'
                            ),
                            CSharpParameter(
                                type=CSharpIdentifierName('Vector'),
                                identifier='b'
                            )
                        ],
                        body=CSharpBlock([])
                    )
                ]
            )
        ])
        
        runa_program = self.csharp_to_runa.convert(csharp_ast)
        
        # Operator overloading should be converted to special methods
        class_stmt = runa_program.statements[0]
        operator_method = next(m for m in class_stmt.methods if m.is_operator_overload)
        self.assertEqual(operator_method.operator_symbol, '+')
    
    def test_partial_classes(self):
        """Test handling of partial classes."""
        # C#: public partial class PartialClass { }
        csharp_ast = CSharpCompilationUnit([
            CSharpClassDeclaration(
                modifiers=[CSharpPublicKeyword(), CSharpPartialKeyword()],
                identifier='PartialClass',
                members=[]
            )
        ])
        
        runa_program = self.csharp_to_runa.convert(csharp_ast)
        
        # Partial classes should be marked appropriately
        class_stmt = runa_program.statements[0]
        self.assertTrue(class_stmt.is_partial)


class TestCSharpRoundTrip(unittest.TestCase):
    """Test round-trip conversion for C#-specific patterns."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.csharp_to_runa = CSharpToRunaConverter()
        self.runa_to_csharp = RunaToCSharpConverter()
    
    def test_roundtrip_generic_constraints(self):
        """Test round-trip conversion of generic constraints."""
        original_csharp = CSharpCompilationUnit([
            CSharpClassDeclaration(
                modifiers=[CSharpPublicKeyword()],
                identifier='Repository',
                type_parameter_list=[
                    CSharpTypeParameter(identifier='T')
                ],
                constraint_clauses=[
                    CSharpTypeParameterConstraintClause(
                        name='T',
                        constraints=[
                            CSharpClassConstraint(),
                            CSharpTypeConstraint(type=CSharpIdentifierName('IEntity'))
                        ]
                    )
                ],
                members=[]
            )
        ])
        
        # Round-trip conversion
        runa_program = self.csharp_to_runa.convert(original_csharp)
        converted_csharp = self.runa_to_csharp.convert(runa_program)
        
        # Verify generic constraints are preserved
        class_decl = converted_csharp.members[0]
        self.assertEqual(len(class_decl.constraint_clauses), 1)
        self.assertEqual(len(class_decl.constraint_clauses[0].constraints), 2)
    
    def test_property_preservation(self):
        """Test that C# property patterns are preserved."""
        original_csharp = CSharpCompilationUnit([
            CSharpClassDeclaration(
                identifier='Person',
                members=[
                    CSharpPropertyDeclaration(
                        modifiers=[CSharpPublicKeyword()],
                        type=CSharpPredefinedType('string'),
                        identifier='Name',
                        accessor_list=[
                            CSharpAccessorDeclaration(
                                kind='get',
                                body=CSharpBlock([
                                    CSharpReturnStatement(
                                        expression=CSharpIdentifierName('_name')
                                    )
                                ])
                            ),
                            CSharpAccessorDeclaration(
                                kind='set',
                                body=CSharpBlock([
                                    CSharpExpressionStatement(
                                        expression=CSharpAssignmentExpression(
                                            left=CSharpIdentifierName('_name'),
                                            operator_token='=',
                                            right=CSharpIdentifierName('value')
                                        )
                                    )
                                ])
                            )
                        ]
                    )
                ]
            )
        ])
        
        # Round-trip conversion
        runa_program = self.csharp_to_runa.convert(original_csharp)
        converted_csharp = self.runa_to_csharp.convert(runa_program)
        
        # Verify property structure is maintained
        class_decl = converted_csharp.members[0]
        property = class_decl.members[0]
        self.assertIsInstance(property, CSharpPropertyDeclaration)
        self.assertEqual(len(property.accessor_list), 2)


if __name__ == '__main__':
    unittest.main()
