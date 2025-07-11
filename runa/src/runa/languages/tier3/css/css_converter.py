#!/usr/bin/env python3
"""
CSS to Runa AST Converter

Bidirectional converter between CSS AST and Runa AST for the universal
translation system.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
import logging

from ....core.runa_ast import *
from .css_ast import *


class CssToRunaConverter:
    """Converts CSS AST to Runa AST."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def convert(self, css_node: CssNode) -> ASTNode:
        """Convert CSS AST node to Runa AST."""
        try:
            if isinstance(css_node, CssStylesheet):
                return self._convert_stylesheet(css_node)
            elif isinstance(css_node, CssRule):
                return self._convert_rule(css_node)
            elif isinstance(css_node, CssDeclaration):
                return self._convert_declaration(css_node)
            else:
                # Create a simple variable for other node types
                return Variable(identifier="css_node", type_hint=StringType())
        except Exception as e:
            self.logger.error(f"CSS to Runa conversion failed: {e}")
            raise RuntimeError(f"Failed to convert CSS to Runa: {e}")
    
    def _convert_stylesheet(self, stylesheet: CssStylesheet) -> Program:
        """Convert CSS stylesheet to Runa program."""
        statements = []
        
        # Create stylesheet metadata
        if stylesheet.charset:
            charset_stmt = VariableDeclaration(
                identifier="stylesheet charset",
                expression=StringLiteral(stylesheet.charset),
                type_hint=StringType()
            )
            statements.append(charset_stmt)
        
        # Convert rules to dictionary structures
        if stylesheet.rules:
            rules_list = []
            for rule in stylesheet.rules:
                rule_dict = self._rule_to_expression(rule)
                rules_list.append(rule_dict)
            
            rules_stmt = VariableDeclaration(
                identifier="css rules",
                expression=ListLiteral(elements=rules_list),
                type_hint=ListType(DictionaryType(StringType(), StringType()))
            )
            statements.append(rules_stmt)
        
        # Convert at-rules
        if stylesheet.at_rules:
            at_rules_list = []
            for at_rule in stylesheet.at_rules:
                at_rule_dict = self._at_rule_to_expression(at_rule)
                at_rules_list.append(at_rule_dict)
            
            at_rules_stmt = VariableDeclaration(
                identifier="css at rules",
                expression=ListLiteral(elements=at_rules_list),
                type_hint=ListType(DictionaryType(StringType(), StringType()))
            )
            statements.append(at_rules_stmt)
        
        # Add demonstration operations
        demo_stmts = self._create_demo_operations(stylesheet)
        statements.extend(demo_stmts)
        
        return Program(statements=statements)
    
    def _convert_rule(self, rule: CssRule) -> Expression:
        """Convert CSS rule to Runa expression."""
        return self._rule_to_expression(rule)
    
    def _rule_to_expression(self, rule: CssRule) -> Expression:
        """Convert CSS rule to dictionary expression."""
        items = []
        
        # Add selectors
        if rule.selectors:
            selector_list = []
            for selector in rule.selectors:
                selector_dict = DictionaryLiteral(items=[
                    DictionaryItem(
                        key=StringLiteral("text"),
                        value=StringLiteral(selector.text)
                    ),
                    DictionaryItem(
                        key=StringLiteral("specificity"),
                        value=StringLiteral(str(selector.calculate_specificity()))
                    )
                ])
                selector_list.append(selector_dict)
            
            items.append(DictionaryItem(
                key=StringLiteral("selectors"),
                value=ListLiteral(elements=selector_list)
            ))
        
        # Add declarations
        if rule.declarations:
            decl_list = []
            for decl in rule.declarations:
                decl_dict = self._declaration_to_expression(decl)
                decl_list.append(decl_dict)
            
            items.append(DictionaryItem(
                key=StringLiteral("declarations"),
                value=ListLiteral(elements=decl_list)
            ))
        
        return DictionaryLiteral(items=items)
    
    def _declaration_to_expression(self, declaration: CssDeclaration) -> Expression:
        """Convert CSS declaration to dictionary expression."""
        items = [
            DictionaryItem(
                key=StringLiteral("property"),
                value=StringLiteral(declaration.property)
            ),
            DictionaryItem(
                key=StringLiteral("value"),
                value=StringLiteral(declaration.value)
            )
        ]
        
        if declaration.important:
            items.append(DictionaryItem(
                key=StringLiteral("important"),
                value=BooleanLiteral(True)
            ))
        
        # Add property category
        category = get_css_property_category(declaration.property)
        items.append(DictionaryItem(
            key=StringLiteral("category"),
            value=StringLiteral(category)
        ))
        
        # Parse value for additional information
        css_value = parse_css_value(declaration.value)
        if css_value.type != "string":
            items.append(DictionaryItem(
                key=StringLiteral("value_type"),
                value=StringLiteral(css_value.type)
            ))
            
            if css_value.unit:
                items.append(DictionaryItem(
                    key=StringLiteral("unit"),
                    value=StringLiteral(css_value.unit)
                ))
        
        return DictionaryLiteral(items=items)
    
    def _at_rule_to_expression(self, at_rule: CssAtRule) -> Expression:
        """Convert CSS at-rule to dictionary expression."""
        items = [
            DictionaryItem(
                key=StringLiteral("name"),
                value=StringLiteral(at_rule.name)
            ),
            DictionaryItem(
                key=StringLiteral("params"),
                value=StringLiteral(at_rule.params)
            )
        ]
        
        # Add nested rules if present
        if at_rule.rules:
            rule_list = []
            for rule in at_rule.rules:
                rule_dict = self._rule_to_expression(rule)
                rule_list.append(rule_dict)
            
            items.append(DictionaryItem(
                key=StringLiteral("rules"),
                value=ListLiteral(elements=rule_list)
            ))
        
        return DictionaryLiteral(items=items)
    
    def _convert_declaration(self, declaration: CssDeclaration) -> VariableDeclaration:
        """Convert CSS declaration to Runa variable declaration."""
        return VariableDeclaration(
            identifier=f"css property {declaration.property}",
            expression=StringLiteral(declaration.value),
            type_hint=StringType()
        )
    
    def _create_demo_operations(self, stylesheet: CssStylesheet) -> List[Statement]:
        """Create demonstration operations for CSS processing."""
        statements = []
        
        # Add selector targeting operation
        if stylesheet.rules:
            selector_stmt = VariableDeclaration(
                identifier="element targeting",
                expression=FunctionCall(
                    function_name="apply styles to elements",
                    arguments=[
                        StringLiteral("body"),
                        Variable(identifier="css rules")
                    ]
                ),
                type_hint=StringType()
            )
            statements.append(selector_stmt)
        
        # Add property extraction
        if any(rule.declarations for rule in stylesheet.rules):
            props_stmt = VariableDeclaration(
                identifier="all css properties",
                expression=FunctionCall(
                    function_name="extract all properties",
                    arguments=[Variable(identifier="css rules")]
                ),
                type_hint=ListType(StringType())
            )
            statements.append(props_stmt)
        
        # Add specificity calculation
        if stylesheet.rules and stylesheet.rules[0].selectors:
            spec_stmt = VariableDeclaration(
                identifier="selector specificity",
                expression=FunctionCall(
                    function_name="calculate specificity",
                    arguments=[
                        StringLiteral(stylesheet.rules[0].selectors[0].text)
                    ]
                ),
                type_hint=StringType()
            )
            statements.append(spec_stmt)
        
        # Add media query processing for responsive design
        if stylesheet.at_rules:
            media_rules = [rule for rule in stylesheet.at_rules if rule.is_media_query]
            if media_rules:
                media_stmt = VariableDeclaration(
                    identifier="responsive breakpoints",
                    expression=FunctionCall(
                        function_name="extract media queries",
                        arguments=[Variable(identifier="css at rules")]
                    ),
                    type_hint=ListType(StringType())
                )
                statements.append(media_stmt)
        
        # Add color extraction
        color_stmt = VariableDeclaration(
            identifier="stylesheet colors",
            expression=FunctionCall(
                function_name="extract all colors",
                arguments=[Variable(identifier="css rules")]
            ),
            type_hint=ListType(StringType())
        )
        statements.append(color_stmt)
        
        return statements


class RunaToCssConverter:
    """Converts Runa AST to CSS AST."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def convert(self, runa_node: ASTNode) -> CssNode:
        """Convert Runa AST node to CSS AST."""
        try:
            if isinstance(runa_node, Program):
                return self._convert_program(runa_node)
            elif isinstance(runa_node, DictionaryLiteral):
                return self._convert_dictionary_to_rule(runa_node)
            elif isinstance(runa_node, ListLiteral):
                return self._convert_list_to_stylesheet(runa_node)
            else:
                # Create a simple CSS comment for other types
                return CssComment(text=str(runa_node))
        except Exception as e:
            self.logger.error(f"Runa to CSS conversion failed: {e}")
            raise RuntimeError(f"Failed to convert Runa to CSS: {e}")
    
    def _convert_program(self, program: Program) -> CssStylesheet:
        """Convert Runa program to CSS stylesheet."""
        stylesheet = CssStylesheet()
        
        for stmt in program.statements:
            if isinstance(stmt, VariableDeclaration):
                if stmt.identifier == "stylesheet charset" and isinstance(stmt.expression, StringLiteral):
                    stylesheet.charset = stmt.expression.value
                elif stmt.identifier == "css rules" and isinstance(stmt.expression, ListLiteral):
                    for rule_expr in stmt.expression.elements:
                        if isinstance(rule_expr, DictionaryLiteral):
                            css_rule = self._convert_dictionary_to_rule(rule_expr)
                            if isinstance(css_rule, CssRule):
                                stylesheet.add_rule(css_rule)
                elif stmt.identifier == "css at rules" and isinstance(stmt.expression, ListLiteral):
                    for at_rule_expr in stmt.expression.elements:
                        if isinstance(at_rule_expr, DictionaryLiteral):
                            css_at_rule = self._convert_dictionary_to_at_rule(at_rule_expr)
                            if css_at_rule:
                                stylesheet.add_at_rule(css_at_rule)
        
        # If no rules found, create a basic structure
        if not stylesheet.rules and not stylesheet.at_rules:
            # Create a basic body rule
            body_rule = create_css_rule(
                selectors=["body"],
                declarations={"margin": "0", "padding": "0", "font-family": "Arial, sans-serif"}
            )
            stylesheet.add_rule(body_rule)
        
        return stylesheet
    
    def _convert_dictionary_to_rule(self, dict_literal: DictionaryLiteral) -> Union[CssRule, CssComment]:
        """Convert dictionary literal to CSS rule."""
        rule = CssRule()
        
        for item in dict_literal.items:
            if isinstance(item.key, StringLiteral):
                key = item.key.value
                
                if key == "selectors" and isinstance(item.value, ListLiteral):
                    for sel_expr in item.value.elements:
                        if isinstance(sel_expr, DictionaryLiteral):
                            # Extract selector text from dictionary
                            for sel_item in sel_expr.items:
                                if (isinstance(sel_item.key, StringLiteral) and 
                                    sel_item.key.value == "text" and 
                                    isinstance(sel_item.value, StringLiteral)):
                                    selector = CssSelector(text=sel_item.value.value)
                                    rule.add_selector(selector)
                                    break
                        elif isinstance(sel_expr, StringLiteral):
                            selector = CssSelector(text=sel_expr.value)
                            rule.add_selector(selector)
                
                elif key == "declarations" and isinstance(item.value, ListLiteral):
                    for decl_expr in item.value.elements:
                        if isinstance(decl_expr, DictionaryLiteral):
                            declaration = self._convert_dictionary_to_declaration(decl_expr)
                            if declaration:
                                rule.add_declaration(declaration)
        
        return rule if rule.selectors and rule.declarations else CssComment(text="Empty rule")
    
    def _convert_dictionary_to_declaration(self, dict_literal: DictionaryLiteral) -> Optional[CssDeclaration]:
        """Convert dictionary to CSS declaration."""
        property_name = ""
        value = ""
        important = False
        
        for item in dict_literal.items:
            if isinstance(item.key, StringLiteral):
                key = item.key.value
                
                if key == "property" and isinstance(item.value, StringLiteral):
                    property_name = item.value.value
                elif key == "value" and isinstance(item.value, StringLiteral):
                    value = item.value.value
                elif key == "important" and isinstance(item.value, BooleanLiteral):
                    important = item.value.value
        
        if property_name and value:
            return CssDeclaration(property=property_name, value=value, important=important)
        
        return None
    
    def _convert_dictionary_to_at_rule(self, dict_literal: DictionaryLiteral) -> Optional[CssAtRule]:
        """Convert dictionary to CSS at-rule."""
        name = ""
        params = ""
        rules = []
        
        for item in dict_literal.items:
            if isinstance(item.key, StringLiteral):
                key = item.key.value
                
                if key == "name" and isinstance(item.value, StringLiteral):
                    name = item.value.value
                elif key == "params" and isinstance(item.value, StringLiteral):
                    params = item.value.value
                elif key == "rules" and isinstance(item.value, ListLiteral):
                    for rule_expr in item.value.elements:
                        if isinstance(rule_expr, DictionaryLiteral):
                            css_rule = self._convert_dictionary_to_rule(rule_expr)
                            if isinstance(css_rule, CssRule):
                                rules.append(css_rule)
        
        if name:
            return CssAtRule(name=name, params=params, rules=rules)
        
        return None
    
    def _convert_list_to_stylesheet(self, list_literal: ListLiteral) -> CssStylesheet:
        """Convert list literal to CSS stylesheet."""
        stylesheet = CssStylesheet()
        
        for expr in list_literal.elements:
            if isinstance(expr, DictionaryLiteral):
                css_rule = self._convert_dictionary_to_rule(expr)
                if isinstance(css_rule, CssRule):
                    stylesheet.add_rule(css_rule)
            elif isinstance(expr, StringLiteral):
                # Treat as selector with basic styling
                rule = create_css_rule(
                    selectors=[expr.value],
                    declarations={"display": "block"}
                )
                stylesheet.add_rule(rule)
        
        return stylesheet


# Convenience functions
def css_to_runa(css_node: CssNode) -> ASTNode:
    """Convert CSS AST to Runa AST."""
    converter = CssToRunaConverter()
    return converter.convert(css_node)


def runa_to_css(runa_node: ASTNode) -> CssNode:
    """Convert Runa AST to CSS AST."""
    converter = RunaToCssConverter()
    return converter.convert(runa_node)


def css_stylesheet_to_runa_program(stylesheet: CssStylesheet) -> Program:
    """Convert CSS stylesheet to Runa program."""
    converter = CssToRunaConverter()
    return converter.convert(stylesheet)


def runa_program_to_css_stylesheet(program: Program) -> CssStylesheet:
    """Convert Runa program to CSS stylesheet."""
    converter = RunaToCssConverter()
    result = converter.convert(program)
    if isinstance(result, CssStylesheet):
        return result
    else:
        # Wrap in stylesheet
        stylesheet = CssStylesheet()
        if isinstance(result, CssRule):
            stylesheet.add_rule(result)
        elif isinstance(result, CssComment):
            stylesheet.add_comment(result)
        return stylesheet