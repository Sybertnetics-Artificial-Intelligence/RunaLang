#!/usr/bin/env python3
"""
Unit tests for SQL ↔ Runa Converter

Tests bidirectional conversion between SQL AST and Runa AST,
focusing on SQL queries, data manipulation, and database-specific constructs.
"""

import unittest
from unittest.mock import Mock, patch
from typing import List, Dict, Any
import sys
import os

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../src'))

from runa.languages.tier1.sql.sql_converter import SQLToRunaConverter, RunaToSQLConverter
from runa.languages.tier1.sql.sql_ast import *
from runa.core.runa_ast import *


class TestSQLToRunaConverter(unittest.TestCase):
    """Test SQL AST to Runa AST conversion."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.converter = SQLToRunaConverter()
    
    def test_select_statement(self):
        """Test conversion of SELECT statements."""
        # SQL: SELECT name, age FROM users WHERE age > 18;
        sql_ast = SQLScript([
            SQLSelectStatement(
                select_list=[
                    SQLColumn(name='name'),
                    SQLColumn(name='age')
                ],
                from_clause=SQLTable(name='users'),
                where_clause=SQLBinaryCondition(
                    left=SQLColumn(name='age'),
                    operator='>',
                    right=SQLLiteral(value=18)
                )
            )
        ])
        
        runa_program = self.converter.convert(sql_ast)
        
        self.assertIsInstance(runa_program, Program)
        self.assertEqual(len(runa_program.statements), 1)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, QueryStatement)
        self.assertEqual(stmt.operation, 'select')
        self.assertEqual(len(stmt.columns), 2)
        self.assertEqual(stmt.columns[0].name, 'name')
        self.assertEqual(stmt.columns[1].name, 'age')
        self.assertEqual(stmt.from_table.name, 'users')
        self.assertIsNotNone(stmt.where_condition)
    
    def test_select_with_join(self):
        """Test conversion of SELECT with JOIN."""
        # SQL: SELECT u.name, p.title FROM users u JOIN posts p ON u.id = p.user_id;
        sql_ast = SQLScript([
            SQLSelectStatement(
                select_list=[
                    SQLColumn(table='u', name='name'),
                    SQLColumn(table='p', name='title')
                ],
                from_clause=SQLJoin(
                    left=SQLTable(name='users', alias='u'),
                    join_type='JOIN',
                    right=SQLTable(name='posts', alias='p'),
                    condition=SQLBinaryCondition(
                        left=SQLColumn(table='u', name='id'),
                        operator='=',
                        right=SQLColumn(table='p', name='user_id')
                    )
                )
            )
        ])
        
        runa_program = self.converter.convert(sql_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, QueryStatement)
        self.assertIsInstance(stmt.from_table, JoinExpression)
        self.assertEqual(stmt.from_table.join_type, 'JOIN')
        self.assertEqual(stmt.from_table.left.name, 'users')
        self.assertEqual(stmt.from_table.right.name, 'posts')
    
    def test_insert_statement(self):
        """Test conversion of INSERT statements."""
        # SQL: INSERT INTO users (name, email) VALUES ('John', 'john@example.com');
        sql_ast = SQLScript([
            SQLInsertStatement(
                table=SQLTable(name='users'),
                columns=[
                    SQLColumn(name='name'),
                    SQLColumn(name='email')
                ],
                values=[
                    SQLLiteral(value='John'),
                    SQLLiteral(value='john@example.com')
                ]
            )
        ])
        
        runa_program = self.converter.convert(sql_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, InsertStatement)
        self.assertEqual(stmt.table.name, 'users')
        self.assertEqual(len(stmt.columns), 2)
        self.assertEqual(len(stmt.values), 2)
    
    def test_update_statement(self):
        """Test conversion of UPDATE statements."""
        # SQL: UPDATE users SET email = 'new@example.com' WHERE id = 1;
        sql_ast = SQLScript([
            SQLUpdateStatement(
                table=SQLTable(name='users'),
                set_clauses=[
                    SQLAssignment(
                        column=SQLColumn(name='email'),
                        value=SQLLiteral(value='new@example.com')
                    )
                ],
                where_clause=SQLBinaryCondition(
                    left=SQLColumn(name='id'),
                    operator='=',
                    right=SQLLiteral(value=1)
                )
            )
        ])
        
        runa_program = self.converter.convert(sql_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, UpdateStatement)
        self.assertEqual(stmt.table.name, 'users')
        self.assertEqual(len(stmt.assignments), 1)
        self.assertEqual(stmt.assignments[0].column.name, 'email')
    
    def test_delete_statement(self):
        """Test conversion of DELETE statements."""
        # SQL: DELETE FROM users WHERE age < 18;
        sql_ast = SQLScript([
            SQLDeleteStatement(
                table=SQLTable(name='users'),
                where_clause=SQLBinaryCondition(
                    left=SQLColumn(name='age'),
                    operator='<',
                    right=SQLLiteral(value=18)
                )
            )
        ])
        
        runa_program = self.converter.convert(sql_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, DeleteStatement)
        self.assertEqual(stmt.table.name, 'users')
        self.assertIsNotNone(stmt.where_condition)
    
    def test_create_table(self):
        """Test conversion of CREATE TABLE statements."""
        # SQL: CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100) NOT NULL, email VARCHAR(255));
        sql_ast = SQLScript([
            SQLCreateTableStatement(
                table_name='users',
                columns=[
                    SQLColumnDefinition(
                        name='id',
                        data_type=SQLDataType('INT'),
                        constraints=[SQLPrimaryKeyConstraint()]
                    ),
                    SQLColumnDefinition(
                        name='name',
                        data_type=SQLDataType('VARCHAR', [100]),
                        constraints=[SQLNotNullConstraint()]
                    ),
                    SQLColumnDefinition(
                        name='email',
                        data_type=SQLDataType('VARCHAR', [255])
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(sql_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, CreateTableStatement)
        self.assertEqual(stmt.table_name, 'users')
        self.assertEqual(len(stmt.columns), 3)
        
        # Check column definitions
        id_col = stmt.columns[0]
        self.assertEqual(id_col.name, 'id')
        self.assertEqual(id_col.data_type.name, 'INT')
        self.assertTrue(any(isinstance(c, PrimaryKeyConstraint) for c in id_col.constraints))
    
    def test_aggregate_functions(self):
        """Test conversion of aggregate functions."""
        # SQL: SELECT COUNT(*), AVG(age), MAX(salary) FROM employees GROUP BY department;
        sql_ast = SQLScript([
            SQLSelectStatement(
                select_list=[
                    SQLAggregateFunction(
                        function='COUNT',
                        arguments=[SQLWildcard()]
                    ),
                    SQLAggregateFunction(
                        function='AVG',
                        arguments=[SQLColumn(name='age')]
                    ),
                    SQLAggregateFunction(
                        function='MAX',
                        arguments=[SQLColumn(name='salary')]
                    )
                ],
                from_clause=SQLTable(name='employees'),
                group_by_clause=[
                    SQLColumn(name='department')
                ]
            )
        ])
        
        runa_program = self.converter.convert(sql_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, QueryStatement)
        
        # Check aggregate functions
        count_col = stmt.columns[0]
        self.assertIsInstance(count_col, AggregateFunctionCall)
        self.assertEqual(count_col.function_name, 'COUNT')
        
        avg_col = stmt.columns[1]
        self.assertIsInstance(avg_col, AggregateFunctionCall)
        self.assertEqual(avg_col.function_name, 'AVG')
        
        # Check GROUP BY
        self.assertEqual(len(stmt.group_by_columns), 1)
        self.assertEqual(stmt.group_by_columns[0].name, 'department')
    
    def test_subquery(self):
        """Test conversion of subqueries."""
        # SQL: SELECT name FROM users WHERE id IN (SELECT user_id FROM orders WHERE total > 100);
        sql_ast = SQLScript([
            SQLSelectStatement(
                select_list=[SQLColumn(name='name')],
                from_clause=SQLTable(name='users'),
                where_clause=SQLInCondition(
                    column=SQLColumn(name='id'),
                    subquery=SQLSelectStatement(
                        select_list=[SQLColumn(name='user_id')],
                        from_clause=SQLTable(name='orders'),
                        where_clause=SQLBinaryCondition(
                            left=SQLColumn(name='total'),
                            operator='>',
                            right=SQLLiteral(value=100)
                        )
                    )
                )
            )
        ])
        
        runa_program = self.converter.convert(sql_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, QueryStatement)
        self.assertIsInstance(stmt.where_condition, InCondition)
        self.assertIsInstance(stmt.where_condition.subquery, QueryStatement)
    
    def test_window_functions(self):
        """Test conversion of window functions."""
        # SQL: SELECT name, salary, ROW_NUMBER() OVER (ORDER BY salary DESC) as rank FROM employees;
        sql_ast = SQLScript([
            SQLSelectStatement(
                select_list=[
                    SQLColumn(name='name'),
                    SQLColumn(name='salary'),
                    SQLWindowFunction(
                        function='ROW_NUMBER',
                        arguments=[],
                        over_clause=SQLOverClause(
                            order_by=[
                                SQLOrderByColumn(
                                    column=SQLColumn(name='salary'),
                                    direction='DESC'
                                )
                            ]
                        ),
                        alias='rank'
                    )
                ],
                from_clause=SQLTable(name='employees')
            )
        ])
        
        runa_program = self.converter.convert(sql_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, QueryStatement)
        
        # Check window function
        rank_col = stmt.columns[2]
        self.assertIsInstance(rank_col, WindowFunctionCall)
        self.assertEqual(rank_col.function_name, 'ROW_NUMBER')
        self.assertIsNotNone(rank_col.over_clause)
    
    def test_cte_with_clause(self):
        """Test conversion of Common Table Expressions (WITH clause)."""
        # SQL: WITH dept_avg AS (SELECT department, AVG(salary) as avg_sal FROM employees GROUP BY department) SELECT * FROM dept_avg WHERE avg_sal > 50000;
        sql_ast = SQLScript([
            SQLWithClause(
                cte_definitions=[
                    SQLCTEDefinition(
                        name='dept_avg',
                        query=SQLSelectStatement(
                            select_list=[
                                SQLColumn(name='department'),
                                SQLAggregateFunction(
                                    function='AVG',
                                    arguments=[SQLColumn(name='salary')],
                                    alias='avg_sal'
                                )
                            ],
                            from_clause=SQLTable(name='employees'),
                            group_by_clause=[SQLColumn(name='department')]
                        )
                    )
                ],
                main_query=SQLSelectStatement(
                    select_list=[SQLWildcard()],
                    from_clause=SQLTable(name='dept_avg'),
                    where_clause=SQLBinaryCondition(
                        left=SQLColumn(name='avg_sal'),
                        operator='>',
                        right=SQLLiteral(value=50000)
                    )
                )
            )
        ])
        
        runa_program = self.converter.convert(sql_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, WithStatement)
        self.assertEqual(len(stmt.cte_definitions), 1)
        self.assertEqual(stmt.cte_definitions[0].name, 'dept_avg')
        self.assertIsInstance(stmt.main_query, QueryStatement)
    
    def test_stored_procedure(self):
        """Test conversion of stored procedures."""
        # SQL: CREATE PROCEDURE GetUserById(@UserId INT) AS BEGIN SELECT * FROM Users WHERE Id = @UserId END
        sql_ast = SQLScript([
            SQLCreateProcedureStatement(
                procedure_name='GetUserById',
                parameters=[
                    SQLParameter(
                        name='@UserId',
                        data_type=SQLDataType('INT')
                    )
                ],
                body=[
                    SQLSelectStatement(
                        select_list=[SQLWildcard()],
                        from_clause=SQLTable(name='Users'),
                        where_clause=SQLBinaryCondition(
                            left=SQLColumn(name='Id'),
                            operator='=',
                            right=SQLParameter(name='@UserId')
                        )
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(sql_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, CreateProcedureStatement)
        self.assertEqual(stmt.procedure_name, 'GetUserById')
        self.assertEqual(len(stmt.parameters), 1)
        self.assertEqual(stmt.parameters[0].name, '@UserId')
        self.assertEqual(len(stmt.body), 1)


class TestRunaToSQLConverter(unittest.TestCase):
    """Test Runa AST to SQL AST conversion."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.converter = RunaToSQLConverter()
    
    def test_query_conversion(self):
        """Test conversion of query statements."""
        # Runa: Query select name, age from users where age is greater than 18
        runa_program = Program([
            QueryStatement(
                operation='select',
                columns=[
                    ColumnReference(name='name'),
                    ColumnReference(name='age')
                ],
                from_table=TableReference(name='users'),
                where_condition=BinaryOperation(
                    left=ColumnReference(name='age'),
                    operator='is greater than',
                    right=NumericLiteral(value=18)
                )
            )
        ])
        
        sql_script = self.converter.convert(runa_program)
        
        self.assertIsInstance(sql_script, SQLScript)
        self.assertEqual(len(sql_script.statements), 1)
        
        stmt = sql_script.statements[0]
        self.assertIsInstance(stmt, SQLSelectStatement)
        self.assertEqual(len(stmt.select_list), 2)
        self.assertEqual(stmt.select_list[0].name, 'name')
        self.assertEqual(stmt.select_list[1].name, 'age')
        self.assertEqual(stmt.from_clause.name, 'users')
    
    def test_insert_conversion(self):
        """Test conversion of insert statements."""
        # Runa: Insert into users columns name, email values "John", "john@example.com"
        runa_program = Program([
            InsertStatement(
                table=TableReference(name='users'),
                columns=[
                    ColumnReference(name='name'),
                    ColumnReference(name='email')
                ],
                values=[
                    StringLiteral(value='John'),
                    StringLiteral(value='john@example.com')
                ]
            )
        ])
        
        sql_script = self.converter.convert(runa_program)
        
        stmt = sql_script.statements[0]
        self.assertIsInstance(stmt, SQLInsertStatement)
        self.assertEqual(stmt.table.name, 'users')
        self.assertEqual(len(stmt.columns), 2)
        self.assertEqual(len(stmt.values), 2)
    
    def test_table_creation_conversion(self):
        """Test conversion of table creation."""
        # Runa: Create table users with id as Integer primary key, name as String not null
        runa_program = Program([
            CreateTableStatement(
                table_name='users',
                columns=[
                    ColumnDefinition(
                        name='id',
                        data_type=TypeReference(name='Integer'),
                        constraints=[PrimaryKeyConstraint()]
                    ),
                    ColumnDefinition(
                        name='name',
                        data_type=TypeReference(name='String'),
                        constraints=[NotNullConstraint()]
                    )
                ]
            )
        ])
        
        sql_script = self.converter.convert(runa_program)
        
        stmt = sql_script.statements[0]
        self.assertIsInstance(stmt, SQLCreateTableStatement)
        self.assertEqual(stmt.table_name, 'users')
        self.assertEqual(len(stmt.columns), 2)
        
        # Check column mappings
        id_col = stmt.columns[0]
        self.assertEqual(id_col.name, 'id')
        self.assertEqual(id_col.data_type.name, 'INT')  # Integer -> INT mapping
        
        name_col = stmt.columns[1]
        self.assertEqual(name_col.name, 'name')
        self.assertEqual(name_col.data_type.name, 'VARCHAR')  # String -> VARCHAR mapping
    
    def test_join_conversion(self):
        """Test conversion of join expressions."""
        # Runa: Query select from users join posts on users.id equals posts.user_id
        runa_program = Program([
            QueryStatement(
                operation='select',
                columns=[WildcardColumn()],
                from_table=JoinExpression(
                    left=TableReference(name='users'),
                    join_type='JOIN',
                    right=TableReference(name='posts'),
                    condition=BinaryOperation(
                        left=ColumnReference(table='users', name='id'),
                        operator='equals',
                        right=ColumnReference(table='posts', name='user_id')
                    )
                )
            )
        ])
        
        sql_script = self.converter.convert(runa_program)
        
        stmt = sql_script.statements[0]
        self.assertIsInstance(stmt, SQLSelectStatement)
        self.assertIsInstance(stmt.from_clause, SQLJoin)
        self.assertEqual(stmt.from_clause.join_type, 'JOIN')
        self.assertEqual(stmt.from_clause.left.name, 'users')
        self.assertEqual(stmt.from_clause.right.name, 'posts')
    
    def test_aggregate_conversion(self):
        """Test conversion of aggregate functions."""
        # Runa: Query select count all, average age from employees group by department
        runa_program = Program([
            QueryStatement(
                operation='select',
                columns=[
                    AggregateFunctionCall(
                        function_name='count',
                        arguments=[WildcardColumn()]
                    ),
                    AggregateFunctionCall(
                        function_name='average',
                        arguments=[ColumnReference(name='age')]
                    )
                ],
                from_table=TableReference(name='employees'),
                group_by_columns=[
                    ColumnReference(name='department')
                ]
            )
        ])
        
        sql_script = self.converter.convert(runa_program)
        
        stmt = sql_script.statements[0]
        self.assertIsInstance(stmt, SQLSelectStatement)
        
        # Check aggregate function mappings
        count_func = stmt.select_list[0]
        self.assertIsInstance(count_func, SQLAggregateFunction)
        self.assertEqual(count_func.function, 'COUNT')  # count -> COUNT
        
        avg_func = stmt.select_list[1]
        self.assertIsInstance(avg_func, SQLAggregateFunction)
        self.assertEqual(avg_func.function, 'AVG')  # average -> AVG
    
    def test_procedure_conversion(self):
        """Test conversion of procedure definitions."""
        # Runa: Define procedure GetUserById with parameter UserId as Integer
        runa_program = Program([
            CreateProcedureStatement(
                procedure_name='GetUserById',
                parameters=[
                    Parameter(
                        name='UserId',
                        type_annotation=TypeReference(name='Integer')
                    )
                ],
                body=[
                    QueryStatement(
                        operation='select',
                        columns=[WildcardColumn()],
                        from_table=TableReference(name='Users'),
                        where_condition=BinaryOperation(
                            left=ColumnReference(name='Id'),
                            operator='equals',
                            right=ParameterReference(name='UserId')
                        )
                    )
                ]
            )
        ])
        
        sql_script = self.converter.convert(runa_program)
        
        stmt = sql_script.statements[0]
        self.assertIsInstance(stmt, SQLCreateProcedureStatement)
        self.assertEqual(stmt.procedure_name, 'GetUserById')
        self.assertEqual(len(stmt.parameters), 1)
        self.assertEqual(stmt.parameters[0].name, '@UserId')  # Add @ prefix
        self.assertEqual(len(stmt.body), 1)


class TestSQLSpecificFeatures(unittest.TestCase):
    """Test SQL-specific language features."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sql_to_runa = SQLToRunaConverter()
        self.runa_to_sql = RunaToSQLConverter()
    
    def test_database_specific_functions(self):
        """Test handling of database-specific functions."""
        # SQL: SELECT GETDATE(), NEWID() FROM dual;
        sql_ast = SQLScript([
            SQLSelectStatement(
                select_list=[
                    SQLFunction(
                        name='GETDATE',
                        arguments=[]
                    ),
                    SQLFunction(
                        name='NEWID',
                        arguments=[]
                    )
                ],
                from_clause=SQLTable(name='dual')
            )
        ])
        
        runa_program = self.sql_to_runa.convert(sql_ast)
        
        # Database functions should be converted to appropriate Runa functions
        stmt = runa_program.statements[0]
        getdate_col = stmt.columns[0]
        self.assertIsInstance(getdate_col, FunctionCall)
        self.assertEqual(getdate_col.function.name, 'current_timestamp')  # GETDATE -> current_timestamp
    
    def test_transaction_handling(self):
        """Test handling of transaction statements."""
        # SQL: BEGIN TRANSACTION; UPDATE accounts SET balance = balance - 100 WHERE id = 1; COMMIT;
        sql_ast = SQLScript([
            SQLBeginTransactionStatement(),
            SQLUpdateStatement(
                table=SQLTable(name='accounts'),
                set_clauses=[
                    SQLAssignment(
                        column=SQLColumn(name='balance'),
                        value=SQLBinaryExpression(
                            left=SQLColumn(name='balance'),
                            operator='-',
                            right=SQLLiteral(value=100)
                        )
                    )
                ],
                where_clause=SQLBinaryCondition(
                    left=SQLColumn(name='id'),
                    operator='=',
                    right=SQLLiteral(value=1)
                )
            ),
            SQLCommitStatement()
        ])
        
        runa_program = self.sql_to_runa.convert(sql_ast)
        
        # Transaction statements should be preserved
        self.assertEqual(len(runa_program.statements), 3)
        self.assertIsInstance(runa_program.statements[0], BeginTransactionStatement)
        self.assertIsInstance(runa_program.statements[1], UpdateStatement)
        self.assertIsInstance(runa_program.statements[2], CommitStatement)
    
    def test_index_operations(self):
        """Test handling of index operations."""
        # SQL: CREATE INDEX idx_user_email ON users(email);
        sql_ast = SQLScript([
            SQLCreateIndexStatement(
                index_name='idx_user_email',
                table_name='users',
                columns=[SQLColumn(name='email')]
            )
        ])
        
        runa_program = self.sql_to_runa.convert(sql_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, CreateIndexStatement)
        self.assertEqual(stmt.index_name, 'idx_user_email')
        self.assertEqual(stmt.table_name, 'users')
        self.assertEqual(len(stmt.columns), 1)


class TestSQLRoundTrip(unittest.TestCase):
    """Test round-trip conversion for SQL-specific patterns."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sql_to_runa = SQLToRunaConverter()
        self.runa_to_sql = RunaToSQLConverter()
    
    def test_roundtrip_complex_query(self):
        """Test round-trip conversion of complex queries."""
        original_sql = SQLScript([
            SQLSelectStatement(
                select_list=[
                    SQLColumn(name='department'),
                    SQLAggregateFunction(
                        function='COUNT',
                        arguments=[SQLWildcard()],
                        alias='employee_count'
                    ),
                    SQLAggregateFunction(
                        function='AVG',
                        arguments=[SQLColumn(name='salary')],
                        alias='avg_salary'
                    )
                ],
                from_clause=SQLTable(name='employees'),
                where_clause=SQLBinaryCondition(
                    left=SQLColumn(name='hire_date'),
                    operator='>',
                    right=SQLLiteral(value='2020-01-01')
                ),
                group_by_clause=[
                    SQLColumn(name='department')
                ],
                having_clause=SQLBinaryCondition(
                    left=SQLAggregateFunction(
                        function='COUNT',
                        arguments=[SQLWildcard()]
                    ),
                    operator='>',
                    right=SQLLiteral(value=5)
                ),
                order_by_clause=[
                    SQLOrderByColumn(
                        column=SQLColumn(name='avg_salary'),
                        direction='DESC'
                    )
                ]
            )
        ])
        
        # Round-trip conversion
        runa_program = self.sql_to_runa.convert(original_sql)
        converted_sql = self.runa_to_sql.convert(runa_program)
        
        # Verify query structure is preserved
        stmt = converted_sql.statements[0]
        self.assertIsInstance(stmt, SQLSelectStatement)
        self.assertEqual(len(stmt.select_list), 3)
        self.assertIsNotNone(stmt.where_clause)
        self.assertIsNotNone(stmt.group_by_clause)
        self.assertIsNotNone(stmt.having_clause)
        self.assertIsNotNone(stmt.order_by_clause)
    
    def test_data_type_preservation(self):
        """Test that SQL data types are preserved accurately."""
        original_sql = SQLScript([
            SQLCreateTableStatement(
                table_name='products',
                columns=[
                    SQLColumnDefinition(
                        name='id',
                        data_type=SQLDataType('BIGINT'),
                        constraints=[SQLPrimaryKeyConstraint(), SQLAutoIncrementConstraint()]
                    ),
                    SQLColumnDefinition(
                        name='name',
                        data_type=SQLDataType('NVARCHAR', [255]),
                        constraints=[SQLNotNullConstraint()]
                    ),
                    SQLColumnDefinition(
                        name='price',
                        data_type=SQLDataType('DECIMAL', [10, 2]),
                        constraints=[SQLCheckConstraint(condition="price > 0")]
                    ),
                    SQLColumnDefinition(
                        name='created_at',
                        data_type=SQLDataType('DATETIME2'),
                        constraints=[SQLDefaultConstraint(value='GETDATE()')]
                    )
                ]
            )
        ])
        
        # Round-trip conversion
        runa_program = self.sql_to_runa.convert(original_sql)
        converted_sql = self.runa_to_sql.convert(runa_program)
        
        # Verify data types and constraints are preserved
        stmt = converted_sql.statements[0]
        self.assertIsInstance(stmt, SQLCreateTableStatement)
        
        # Check BIGINT with constraints
        id_col = stmt.columns[0]
        self.assertEqual(id_col.data_type.name, 'BIGINT')
        self.assertTrue(any(isinstance(c, SQLPrimaryKeyConstraint) for c in id_col.constraints))
        
        # Check NVARCHAR with length
        name_col = stmt.columns[1]
        self.assertEqual(name_col.data_type.name, 'NVARCHAR')
        self.assertEqual(name_col.data_type.parameters, [255])
        
        # Check DECIMAL with precision and scale
        price_col = stmt.columns[2]
        self.assertEqual(price_col.data_type.name, 'DECIMAL')
        self.assertEqual(price_col.data_type.parameters, [10, 2])


if __name__ == '__main__':
    unittest.main()
