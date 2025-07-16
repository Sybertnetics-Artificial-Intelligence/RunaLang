#!/usr/bin/env python3
"""
Unit tests for TypeScript ↔ Runa Converter

Tests bidirectional conversion between TypeScript AST and Runa AST,
focusing on type system preservation and TypeScript-specific features.
"""

import unittest
from unittest.mock import Mock, patch
from typing import List, Dict, Any
import sys
import os

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../src'))

from runa.languages.tier1.typescript.ts_converter import TSToRunaConverter, RunaToTSConverter
from runa.languages.tier1.typescript.ts_ast import *
from runa.core.runa_ast import *


class TestTSToRunaConverter(unittest.TestCase):
    """Test TypeScript AST to Runa AST conversion."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.converter = TSToRunaConverter()
    
    def test_typed_variable_declaration(self):
        """Test conversion of typed variable declarations."""
        # TypeScript: let x: number = 42;
        ts_ast = TSProgram([
            TSVariableStatement([
                TSVariableDeclaration(
                    name=TSIdentifier(name='x'),
                    type=TSNumberKeyword(),
                    initializer=TSNumericLiteral(value=42)
                )
            ])
        ])
        
        runa_program = self.converter.convert(ts_ast)
        
        self.assertIsInstance(runa_program, Program)
        self.assertEqual(len(runa_program.statements), 1)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        self.assertEqual(stmt.name, 'x')
        self.assertIsInstance(stmt.type_annotation, TypeReference)
        self.assertEqual(stmt.type_annotation.name, 'number')
        self.assertIsInstance(stmt.value, NumericLiteral)
    
    def test_interface_declaration(self):
        """Test conversion of interface declarations."""
        # TypeScript: interface Person { name: string; age: number; }
        ts_ast = TSProgram([
            TSInterfaceDeclaration(
                name=TSIdentifier(name='Person'),
                members=[
                    TSPropertySignature(
                        name=TSIdentifier(name='name'),
                        type=TSStringKeyword()
                    ),
                    TSPropertySignature(
                        name=TSIdentifier(name='age'),
                        type=TSNumberKeyword()
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(ts_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, InterfaceDeclaration)
        self.assertEqual(stmt.name, 'Person')
        self.assertEqual(len(stmt.properties), 2)
        
        # Check property types
        name_prop = stmt.properties[0]
        self.assertEqual(name_prop.name, 'name')
        self.assertEqual(name_prop.type_annotation.name, 'string')
    
    def test_function_with_typed_parameters(self):
        """Test conversion of functions with typed parameters."""
        # TypeScript: function add(a: number, b: number): number { return a + b; }
        ts_ast = TSProgram([
            TSFunctionDeclaration(
                name=TSIdentifier(name='add'),
                parameters=[
                    TSParameter(
                        name=TSIdentifier(name='a'),
                        type=TSNumberKeyword()
                    ),
                    TSParameter(
                        name=TSIdentifier(name='b'),
                        type=TSNumberKeyword()
                    )
                ],
                return_type=TSNumberKeyword(),
                body=TSBlock([
                    TSReturnStatement(
                        expression=TSBinaryExpression(
                            left=TSIdentifier(name='a'),
                            operator='+',
                            right=TSIdentifier(name='b')
                        )
                    )
                ])
            )
        ])
        
        runa_program = self.converter.convert(ts_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, FunctionDeclaration)
        self.assertEqual(stmt.name, 'add')
        self.assertEqual(len(stmt.parameters), 2)
        
        # Check parameter types
        param_a = stmt.parameters[0]
        self.assertEqual(param_a.name, 'a')
        self.assertIsInstance(param_a.type_annotation, TypeReference)
        
        # Check return type
        self.assertIsInstance(stmt.return_type, TypeReference)
        self.assertEqual(stmt.return_type.name, 'number')
    
    def test_generic_function(self):
        """Test conversion of generic functions."""
        # TypeScript: function identity<T>(arg: T): T { return arg; }
        ts_ast = TSProgram([
            TSFunctionDeclaration(
                name=TSIdentifier(name='identity'),
                type_parameters=[
                    TSTypeParameter(name=TSIdentifier(name='T'))
                ],
                parameters=[
                    TSParameter(
                        name=TSIdentifier(name='arg'),
                        type=TSTypeReference(name=TSIdentifier(name='T'))
                    )
                ],
                return_type=TSTypeReference(name=TSIdentifier(name='T')),
                body=TSBlock([
                    TSReturnStatement(
                        expression=TSIdentifier(name='arg')
                    )
                ])
            )
        ])
        
        runa_program = self.converter.convert(ts_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, FunctionDeclaration)
        self.assertEqual(stmt.name, 'identity')
        self.assertEqual(len(stmt.type_parameters), 1)
        self.assertEqual(stmt.type_parameters[0].name, 'T')
    
    def test_class_with_access_modifiers(self):
        """Test conversion of classes with access modifiers."""
        # TypeScript: class Person { private name: string; public constructor(name: string) { this.name = name; } }
        ts_ast = TSProgram([
            TSClassDeclaration(
                name=TSIdentifier(name='Person'),
                members=[
                    TSPropertyDeclaration(
                        name=TSIdentifier(name='name'),
                        type=TSStringKeyword(),
                        access_modifier='private'
                    ),
                    TSConstructorDeclaration(
                        parameters=[
                            TSParameter(
                                name=TSIdentifier(name='name'),
                                type=TSStringKeyword()
                            )
                        ],
                        body=TSBlock([
                            TSExpressionStatement(
                                expression=TSBinaryExpression(
                                    left=TSPropertyAccessExpression(
                                        expression=TSThisKeyword(),
                                        name=TSIdentifier(name='name')
                                    ),
                                    operator='=',
                                    right=TSIdentifier(name='name')
                                )
                            )
                        ]),
                        access_modifier='public'
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(ts_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, ClassDeclaration)
        self.assertEqual(stmt.name, 'Person')
        
        # Check that access modifiers are preserved
        property = stmt.properties[0]
        self.assertEqual(property.access_modifier, 'private')
    
    def test_union_types(self):
        """Test conversion of union types."""
        # TypeScript: let value: string | number = "hello";
        ts_ast = TSProgram([
            TSVariableStatement([
                TSVariableDeclaration(
                    name=TSIdentifier(name='value'),
                    type=TSUnionType([
                        TSStringKeyword(),
                        TSNumberKeyword()
                    ]),
                    initializer=TSStringLiteral(value="hello")
                )
            ])
        ])
        
        runa_program = self.converter.convert(ts_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        self.assertIsInstance(stmt.type_annotation, UnionType)
        self.assertEqual(len(stmt.type_annotation.types), 2)
    
    def test_array_types(self):
        """Test conversion of array types."""
        # TypeScript: let numbers: number[] = [1, 2, 3];
        ts_ast = TSProgram([
            TSVariableStatement([
                TSVariableDeclaration(
                    name=TSIdentifier(name='numbers'),
                    type=TSArrayType(
                        element_type=TSNumberKeyword()
                    ),
                    initializer=TSArrayLiteralExpression([
                        TSNumericLiteral(value=1),
                        TSNumericLiteral(value=2),
                        TSNumericLiteral(value=3)
                    ])
                )
            ])
        ])
        
        runa_program = self.converter.convert(ts_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        self.assertIsInstance(stmt.type_annotation, ArrayType)
        self.assertEqual(stmt.type_annotation.element_type.name, 'number')
    
    def test_optional_properties(self):
        """Test conversion of optional properties."""
        # TypeScript: interface Config { host: string; port?: number; }
        ts_ast = TSProgram([
            TSInterfaceDeclaration(
                name=TSIdentifier(name='Config'),
                members=[
                    TSPropertySignature(
                        name=TSIdentifier(name='host'),
                        type=TSStringKeyword()
                    ),
                    TSPropertySignature(
                        name=TSIdentifier(name='port'),
                        type=TSNumberKeyword(),
                        optional=True
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(ts_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, InterfaceDeclaration)
        
        # Check optional property
        port_prop = stmt.properties[1]
        self.assertEqual(port_prop.name, 'port')
        self.assertTrue(port_prop.is_optional)
    
    def test_type_assertion(self):
        """Test conversion of type assertions."""
        # TypeScript: let value = (someValue as string).length;
        ts_ast = TSProgram([
            TSVariableStatement([
                TSVariableDeclaration(
                    name=TSIdentifier(name='value'),
                    initializer=TSPropertyAccessExpression(
                        expression=TSTypeAssertion(
                            type=TSStringKeyword(),
                            expression=TSIdentifier(name='someValue')
                        ),
                        name=TSIdentifier(name='length')
                    )
                )
            ])
        ])
        
        runa_program = self.converter.convert(ts_ast)
        
        # Type assertion should be converted appropriately
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
    
    def test_enum_declaration(self):
        """Test conversion of enum declarations."""
        # TypeScript: enum Color { Red, Green, Blue }
        ts_ast = TSProgram([
            TSEnumDeclaration(
                name=TSIdentifier(name='Color'),
                members=[
                    TSEnumMember(name=TSIdentifier(name='Red')),
                    TSEnumMember(name=TSIdentifier(name='Green')),
                    TSEnumMember(name=TSIdentifier(name='Blue'))
                ]
            )
        ])
        
        runa_program = self.converter.convert(ts_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, EnumDeclaration)
        self.assertEqual(stmt.name, 'Color')
        self.assertEqual(len(stmt.members), 3)
    
    def test_namespace_declaration(self):
        """Test conversion of namespace declarations."""
        # TypeScript: namespace Utils { export function helper() { } }
        ts_ast = TSProgram([
            TSNamespaceDeclaration(
                name=TSIdentifier(name='Utils'),
                body=[
                    TSFunctionDeclaration(
                        name=TSIdentifier(name='helper'),
                        parameters=[],
                        body=TSBlock([]),
                        export=True
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(ts_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, NamespaceDeclaration)
        self.assertEqual(stmt.name, 'Utils')


class TestRunaToTSConverter(unittest.TestCase):
    """Test Runa AST to TypeScript AST conversion."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.converter = RunaToTSConverter()
    
    def test_typed_variable_conversion(self):
        """Test conversion of typed variable declarations."""
        # Runa: Let x as Number be 42
        runa_program = Program([
            VariableDeclaration(
                name='x',
                type_annotation=TypeReference(name='Number'),
                value=NumericLiteral(value=42)
            )
        ])
        
        ts_program = self.converter.convert(runa_program)
        
        self.assertIsInstance(ts_program, TSProgram)
        stmt = ts_program.body[0]
        self.assertIsInstance(stmt, TSVariableStatement)
        
        var_decl = stmt.declarations[0]
        self.assertEqual(var_decl.name.name, 'x')
        self.assertIsInstance(var_decl.type, TSNumberKeyword)
    
    def test_interface_conversion(self):
        """Test conversion of interface declarations."""
        # Runa: Define interface Person with name as String and age as Number
        runa_program = Program([
            InterfaceDeclaration(
                name='Person',
                properties=[
                    PropertyDeclaration(
                        name='name',
                        type_annotation=TypeReference(name='String')
                    ),
                    PropertyDeclaration(
                        name='age',
                        type_annotation=TypeReference(name='Number')
                    )
                ]
            )
        ])
        
        ts_program = self.converter.convert(runa_program)
        
        stmt = ts_program.body[0]
        self.assertIsInstance(stmt, TSInterfaceDeclaration)
        self.assertEqual(stmt.name.name, 'Person')
        self.assertEqual(len(stmt.members), 2)
    
    def test_generic_function_conversion(self):
        """Test conversion of generic functions."""
        # Runa: Define generic function identity with type T taking arg as T returning T
        runa_program = Program([
            FunctionDeclaration(
                name='identity',
                type_parameters=[TypeParameter(name='T')],
                parameters=[
                    Parameter(
                        name='arg',
                        type_annotation=TypeReference(name='T')
                    )
                ],
                return_type=TypeReference(name='T'),
                body=[
                    ReturnStatement(
                        value=Identifier(name='arg')
                    )
                ]
            )
        ])
        
        ts_program = self.converter.convert(runa_program)
        
        stmt = ts_program.body[0]
        self.assertIsInstance(stmt, TSFunctionDeclaration)
        self.assertEqual(stmt.name.name, 'identity')
        self.assertEqual(len(stmt.type_parameters), 1)
    
    def test_union_type_conversion(self):
        """Test conversion of union types."""
        # Runa: Let value as (String or Number) be "hello"
        runa_program = Program([
            VariableDeclaration(
                name='value',
                type_annotation=UnionType([
                    TypeReference(name='String'),
                    TypeReference(name='Number')
                ]),
                value=StringLiteral(value="hello")
            )
        ])
        
        ts_program = self.converter.convert(runa_program)
        
        stmt = ts_program.body[0]
        var_decl = stmt.declarations[0]
        self.assertIsInstance(var_decl.type, TSUnionType)
        self.assertEqual(len(var_decl.type.types), 2)
    
    def test_optional_property_conversion(self):
        """Test conversion of optional properties."""
        # Runa: Define interface Config with host as String and optional port as Number
        runa_program = Program([
            InterfaceDeclaration(
                name='Config',
                properties=[
                    PropertyDeclaration(
                        name='host',
                        type_annotation=TypeReference(name='String')
                    ),
                    PropertyDeclaration(
                        name='port',
                        type_annotation=TypeReference(name='Number'),
                        is_optional=True
                    )
                ]
            )
        ])
        
        ts_program = self.converter.convert(runa_program)
        
        stmt = ts_program.body[0]
        self.assertIsInstance(stmt, TSInterfaceDeclaration)
        
        # Check optional property
        port_prop = stmt.members[1]
        self.assertTrue(port_prop.optional)
    
    def test_access_modifier_conversion(self):
        """Test conversion of access modifiers."""
        # Runa: Define class Person with private name as String
        runa_program = Program([
            ClassDeclaration(
                name='Person',
                properties=[
                    PropertyDeclaration(
                        name='name',
                        type_annotation=TypeReference(name='String'),
                        access_modifier='private'
                    )
                ]
            )
        ])
        
        ts_program = self.converter.convert(runa_program)
        
        stmt = ts_program.body[0]
        self.assertIsInstance(stmt, TSClassDeclaration)
        
        property = stmt.members[0]
        self.assertEqual(property.access_modifier, 'private')


class TestTypeScriptSpecificFeatures(unittest.TestCase):
    """Test TypeScript-specific language features."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ts_to_runa = TSToRunaConverter()
        self.runa_to_ts = RunaToTSConverter()
    
    def test_mapped_types(self):
        """Test handling of mapped types."""
        # TypeScript: type Readonly<T> = { readonly [P in keyof T]: T[P] }
        ts_ast = TSProgram([
            TSTypeAliasDeclaration(
                name=TSIdentifier(name='Readonly'),
                type_parameters=[
                    TSTypeParameter(name=TSIdentifier(name='T'))
                ],
                type=TSMappedType(
                    type_parameter=TSTypeParameter(name=TSIdentifier(name='P')),
                    constraint=TSTypeOperator(
                        operator='keyof',
                        type=TSTypeReference(name=TSIdentifier(name='T'))
                    ),
                    type=TSIndexedAccessType(
                        object_type=TSTypeReference(name=TSIdentifier(name='T')),
                        index_type=TSTypeReference(name=TSIdentifier(name='P'))
                    ),
                    readonly=True
                )
            )
        ])
        
        runa_program = self.ts_to_runa.convert(ts_ast)
        
        # Mapped types should be converted to appropriate Runa construct
        self.assertIsInstance(runa_program, Program)
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, TypeAliasDeclaration)
    
    def test_conditional_types(self):
        """Test handling of conditional types."""
        # TypeScript: type Check<T> = T extends string ? true : false
        ts_ast = TSProgram([
            TSTypeAliasDeclaration(
                name=TSIdentifier(name='Check'),
                type_parameters=[
                    TSTypeParameter(name=TSIdentifier(name='T'))
                ],
                type=TSConditionalType(
                    check_type=TSTypeReference(name=TSIdentifier(name='T')),
                    extends_type=TSStringKeyword(),
                    true_type=TSLiteralType(value=True),
                    false_type=TSLiteralType(value=False)
                )
            )
        ])
        
        runa_program = self.ts_to_runa.convert(ts_ast)
        
        # Conditional types should be handled appropriately
        self.assertIsInstance(runa_program, Program)
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, TypeAliasDeclaration)
    
    def test_decorator_support(self):
        """Test handling of decorators."""
        # TypeScript: @Component class MyComponent { }
        ts_ast = TSProgram([
            TSClassDeclaration(
                name=TSIdentifier(name='MyComponent'),
                decorators=[
                    TSDecorator(
                        expression=TSIdentifier(name='Component')
                    )
                ],
                members=[]
            )
        ])
        
        runa_program = self.ts_to_runa.convert(ts_ast)
        
        # Decorators should be preserved or converted to attributes
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, ClassDeclaration)
        self.assertGreater(len(stmt.decorators), 0)
    
    def test_module_declarations(self):
        """Test handling of module declarations."""
        # TypeScript: declare module "my-module" { export function test(): void; }
        ts_ast = TSProgram([
            TSModuleDeclaration(
                name=TSStringLiteral(value="my-module"),
                body=[
                    TSFunctionDeclaration(
                        name=TSIdentifier(name='test'),
                        parameters=[],
                        return_type=TSVoidKeyword(),
                        body=None,  # Declare only
                        export=True
                    )
                ],
                declare=True
            )
        ])
        
        runa_program = self.ts_to_runa.convert(ts_ast)
        
        # Module declarations should be converted appropriately
        self.assertIsInstance(runa_program, Program)
        self.assertGreater(len(runa_program.statements), 0)


class TestTypeScriptRoundTrip(unittest.TestCase):
    """Test round-trip conversion for TypeScript-specific patterns."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ts_to_runa = TSToRunaConverter()
        self.runa_to_ts = RunaToTSConverter()
    
    def test_roundtrip_interface(self):
        """Test round-trip conversion of interfaces."""
        original_ts = TSProgram([
            TSInterfaceDeclaration(
                name=TSIdentifier(name='User'),
                members=[
                    TSPropertySignature(
                        name=TSIdentifier(name='id'),
                        type=TSNumberKeyword()
                    ),
                    TSPropertySignature(
                        name=TSIdentifier(name='name'),
                        type=TSStringKeyword()
                    ),
                    TSPropertySignature(
                        name=TSIdentifier(name='email'),
                        type=TSStringKeyword(),
                        optional=True
                    )
                ]
            )
        ])
        
        # Round-trip conversion
        runa_program = self.ts_to_runa.convert(original_ts)
        converted_ts = self.runa_to_ts.convert(runa_program)
        
        # Verify interface structure is preserved
        self.assertIsInstance(converted_ts, TSProgram)
        stmt = converted_ts.body[0]
        self.assertIsInstance(stmt, TSInterfaceDeclaration)
        self.assertEqual(stmt.name.name, 'User')
        self.assertEqual(len(stmt.members), 3)
        
        # Check optional property is preserved
        email_prop = stmt.members[2]
        self.assertTrue(email_prop.optional)
    
    def test_roundtrip_generic_class(self):
        """Test round-trip conversion of generic classes."""
        original_ts = TSProgram([
            TSClassDeclaration(
                name=TSIdentifier(name='Container'),
                type_parameters=[
                    TSTypeParameter(name=TSIdentifier(name='T'))
                ],
                members=[
                    TSPropertyDeclaration(
                        name=TSIdentifier(name='value'),
                        type=TSTypeReference(name=TSIdentifier(name='T')),
                        access_modifier='private'
                    ),
                    TSConstructorDeclaration(
                        parameters=[
                            TSParameter(
                                name=TSIdentifier(name='value'),
                                type=TSTypeReference(name=TSIdentifier(name='T'))
                            )
                        ],
                        body=TSBlock([
                            TSExpressionStatement(
                                expression=TSBinaryExpression(
                                    left=TSPropertyAccessExpression(
                                        expression=TSThisKeyword(),
                                        name=TSIdentifier(name='value')
                                    ),
                                    operator='=',
                                    right=TSIdentifier(name='value')
                                )
                            )
                        ])
                    )
                ]
            )
        ])
        
        # Round-trip conversion
        runa_program = self.ts_to_runa.convert(original_ts)
        converted_ts = self.runa_to_ts.convert(runa_program)
        
        # Verify generic class structure is preserved
        self.assertIsInstance(converted_ts, TSProgram)
        stmt = converted_ts.body[0]
        self.assertIsInstance(stmt, TSClassDeclaration)
        self.assertEqual(stmt.name.name, 'Container')
        self.assertEqual(len(stmt.type_parameters), 1)
    
    def test_type_preservation_accuracy(self):
        """Test that type information is accurately preserved."""
        original_ts = TSProgram([
            TSFunctionDeclaration(
                name=TSIdentifier(name='process'),
                parameters=[
                    TSParameter(
                        name=TSIdentifier(name='items'),
                        type=TSArrayType(
                            element_type=TSUnionType([
                                TSStringKeyword(),
                                TSNumberKeyword()
                            ])
                        )
                    )
                ],
                return_type=TSArrayType(
                    element_type=TSStringKeyword()
                ),
                body=TSBlock([
                    TSReturnStatement(
                        expression=TSCallExpression(
                            expression=TSPropertyAccessExpression(
                                expression=TSIdentifier(name='items'),
                                name=TSIdentifier(name='map')
                            ),
                            arguments=[
                                TSArrowFunction(
                                    parameters=[TSIdentifier(name='item')],
                                    body=TSCallExpression(
                                        expression=TSPropertyAccessExpression(
                                            expression=TSIdentifier(name='String'),
                                            name=TSIdentifier(name='valueOf')
                                        ),
                                        arguments=[TSIdentifier(name='item')]
                                    )
                                )
                            ]
                        )
                    )
                ])
            )
        ])
        
        # Round-trip conversion
        runa_program = self.ts_to_runa.convert(original_ts)
        converted_ts = self.runa_to_ts.convert(runa_program)
        
        # Verify complex type structures are preserved
        self.assertIsInstance(converted_ts, TSProgram)
        func_def = converted_ts.body[0]
        self.assertIsInstance(func_def, TSFunctionDeclaration)
        
        # Check parameter type preservation
        param = func_def.parameters[0]
        self.assertIsInstance(param.type, TSArrayType)
        self.assertIsInstance(param.type.element_type, TSUnionType)


if __name__ == '__main__':
    unittest.main()