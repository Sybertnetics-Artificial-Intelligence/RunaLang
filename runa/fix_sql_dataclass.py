#!/usr/bin/env python3
"""
Fix SQL AST dataclass inheritance issues.

The problem is that base classes like SQLNode have default fields,
but child classes add required fields, which violates dataclass rules.
"""

import re
import sys
from pathlib import Path

def fix_sql_ast_dataclass_issues():
    """Fix dataclass inheritance issues in SQL AST."""
    sql_ast_file = Path("src/runa/languages/tier1/sql/sql_ast.py")
    
    if not sql_ast_file.exists():
        print(f"File not found: {sql_ast_file}")
        return False
    
    # Read the file
    with open(sql_ast_file, 'r') as f:
        content = f.read()
    
    # Define patterns to fix - convert required fields to optional with defaults
    patterns = [
        # Basic types with sensible defaults
        (r'(\s+)name: str(\s*\n)', r'\1name: str = ""\2'),
        (r'(\s+)table: str(\s*\n)', r'\1table: str = ""\2'),
        (r'(\s+)column: str(\s*\n)', r'\1column: str = ""\2'),
        (r'(\s+)schema: str(\s*\n)', r'\1schema: str = ""\2'),
        (r'(\s+)alias: str(\s*\n)', r'\1alias: str = ""\2'),
        (r'(\s+)value: str(\s*\n)', r'\1value: str = ""\2'),
        (r'(\s+)pattern: str(\s*\n)', r'\1pattern: str = ""\2'),
        (r'(\s+)language: str(\s*\n)', r'\1language: str = "SQL"\2'),
        (r'(\s+)message: str(\s*\n)', r'\1message: str = ""\2'),
        
        # Numeric types
        (r'(\s+)value: int(\s*\n)', r'\1value: int = 0\2'),
        (r'(\s+)value: float(\s*\n)', r'\1value: float = 0.0\2'),
        (r'(\s+)precision: int(\s*\n)', r'\1precision: int = 0\2'),
        (r'(\s+)scale: int(\s*\n)', r'\1scale: int = 0\2'),
        (r'(\s+)size: int(\s*\n)', r'\1size: int = 0\2'),
        
        # Boolean types
        (r'(\s+)ascending: bool(\s*\n)', r'\1ascending: bool = True\2'),
        (r'(\s+)distinct: bool(\s*\n)', r'\1distinct: bool = False\2'),
        (r'(\s+)negated: bool(\s*\n)', r'\1negated: bool = False\2'),
        (r'(\s+)recursive: bool(\s*\n)', r'\1recursive: bool = False\2'),
        (r'(\s+)temporary: bool(\s*\n)', r'\1temporary: bool = False\2'),
        (r'(\s+)if_exists: bool(\s*\n)', r'\1if_exists: bool = False\2'),
        (r'(\s+)if_not_exists: bool(\s*\n)', r'\1if_not_exists: bool = False\2'),
        (r'(\s+)cascade: bool(\s*\n)', r'\1cascade: bool = False\2'),
        
        # SQL-specific types that need defaults
        (r'(\s+)operator: SQLOperator(\s*\n)', r'\1operator: SQLOperator = SQLOperator.EQUAL\2'),
        (r'(\s+)join_type: JoinType(\s*\n)', r'\1join_type: JoinType = JoinType.INNER\2'),
        (r'(\s+)operation: str(\s*\n)', r'\1operation: str = "UNION"\2'),
        (r'(\s+)element_type: SQLDataType(\s*\n)', r'\1element_type: Optional[SQLDataType] = None\2'),
        (r'(\s+)timing: str(\s*\n)', r'\1timing: str = "AFTER"\2'),
        (r'(\s+)events: List\[str\](\s*\n)', r'\1events: List[str] = field(default_factory=list)\2'),
        (r'(\s+)table_name: SQLIdentifier(\s*\n)', r'\1table_name: Optional[SQLIdentifier] = None\2'),
        (r'(\s+)values: List\[SQLExpression\](\s*\n)', r'\1values: List[SQLExpression] = field(default_factory=list)\2'),
        (r'(\s+)lower_bound: SQLExpression(\s*\n)', r'\1lower_bound: Optional[SQLExpression] = None\2'),
        (r'(\s+)upper_bound: SQLExpression(\s*\n)', r'\1upper_bound: Optional[SQLExpression] = None\2'),
        (r'(\s+)pattern: SQLExpression(\s*\n)', r'\1pattern: Optional[SQLExpression] = None\2'),
        (r'(\s+)query: \'?SQLSelectStatement\'?(\s*\n)', r'\1query: Optional[SQLSelectStatement] = None\2'),
        (r'(\s+)left: SQLSelectStatement(\s*\n)', r'\1left: Optional[SQLSelectStatement] = None\2'),
        (r'(\s+)right: SQLSelectStatement(\s*\n)', r'\1right: Optional[SQLSelectStatement] = None\2'),
        (r'(\s+)left: SQLTableReference(\s*\n)', r'\1left: Optional[SQLTableReference] = None\2'),
        (r'(\s+)right: SQLTableReference(\s*\n)', r'\1right: Optional[SQLTableReference] = None\2'),
        (r'(\s+)table: SQLIdentifier(\s*\n)', r'\1table: Optional[SQLIdentifier] = None\2'),
        (r'(\s+)table: SQLTableReference(\s*\n)', r'\1table: Optional[SQLTableReference] = None\2'),
        (r'(\s+)subquery: SQLSubquery(\s*\n)', r'\1subquery: Optional[SQLSubquery] = None\2'),
        (r'(\s+)subquery: \'?SQLSubquery\'?(\s*\n)', r'\1subquery: Optional[SQLSubquery] = None\2'),
        (r'(\s+)set_clauses: List\[.*\](\s*\n)', r'\1set_clauses: List[Tuple[SQLExpression, SQLExpression]] = field(default_factory=list)\2'),
        
        # Required expressions/nodes that should be optional
        (r'(\s+)left: SQLExpression(\s*\n)', r'\1left: Optional[SQLExpression] = None\2'),
        (r'(\s+)right: SQLExpression(\s*\n)', r'\1right: Optional[SQLExpression] = None\2'),
        (r'(\s+)operand: SQLExpression(\s*\n)', r'\1operand: Optional[SQLExpression] = None\2'),
        (r'(\s+)expression: SQLExpression(\s*\n)', r'\1expression: Optional[SQLExpression] = None\2'),
        (r'(\s+)condition: SQLExpression(\s*\n)', r'\1condition: Optional[SQLExpression] = None\2'),
        (r'(\s+)target_type: SQLDataType(\s*\n)', r'\1target_type: Optional[SQLDataType] = None\2'),
        (r'(\s+)query: SQLSelectStatement(\s*\n)', r'\1query: Optional[SQLSelectStatement] = None\2'),
        (r'(\s+)subquery: SQLSelectStatement(\s*\n)', r'\1subquery: Optional[SQLSelectStatement] = None\2'),
        (r'(\s+)table: SQLTableReference(\s*\n)', r'\1table: Optional[SQLTableReference] = None\2'),
        (r'(\s+)name: SQLIdentifier(\s*\n)', r'\1name: Optional[SQLIdentifier] = None\2'),
        (r'(\s+)data_type: SQLDataType(\s*\n)', r'\1data_type: Optional[SQLDataType] = None\2'),
    ]
    
    # Apply patterns
    original_content = content
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    # Check if changes were made
    if content != original_content:
        # Backup original file
        backup_file = sql_ast_file.with_suffix('.py.backup')
        with open(backup_file, 'w') as f:
            f.write(original_content)
        print(f"Backup created: {backup_file}")
        
        # Write fixed content
        with open(sql_ast_file, 'w') as f:
            f.write(content)
        print(f"Fixed dataclass issues in {sql_ast_file}")
        return True
    else:
        print("No changes needed")
        return False

if __name__ == "__main__":
    success = fix_sql_ast_dataclass_issues()
    sys.exit(0 if success else 1)