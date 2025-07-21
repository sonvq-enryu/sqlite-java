#!/usr/bin/env python3

from sql_parser import (
    SQLParser, 
    CreateTableStmt, 
    SelectStmt, 
    InsertStmt, 
    UpdateStmt, 
    DeleteStmt,
    BinaryOp,
    Identifier,
    Literal
)

def example_basic_usage():
    """Basic usage example"""
    print("=== Basic Usage Example ===\n")
    
    parser = SQLParser()
    
    # Parse a CREATE TABLE statement
    sql = "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT)"
    ast = parser.parse(sql)
    
    print(f"SQL: {sql}")
    print(f"Parsed AST: {ast[0]}")
    print()
    
    # Access the parsed data
    create_stmt = ast[0]
    print(f"Table name: {create_stmt.table_name}")
    print("Columns:")
    for col in create_stmt.columns:
        print(f"  - {col.name}: {col.data_type}", end="")
        if col.is_primary_key:
            print(" [PRIMARY KEY]", end="")
        if col.is_not_null:
            print(" [NOT NULL]", end="")
        print()

def example_query_analysis():
    """Example of analyzing SELECT queries"""
    print("\n=== Query Analysis Example ===\n")
    
    parser = SQLParser()
    
    queries = [
        "SELECT * FROM users",
        "SELECT name, email FROM users WHERE age > 18",
        "SELECT id FROM orders WHERE status = 'pending' AND total > 100"
    ]
    
    for sql in queries:
        print(f"SQL: {sql}")
        ast = parser.parse(sql)
        select_stmt = ast[0]
        
        print(f"  Table: {select_stmt.table_name}")
        print(f"  Columns: {', '.join(select_stmt.columns)}")
        
        if select_stmt.where_clause:
            print(f"  Has WHERE clause: Yes")
            print(f"  WHERE clause type: {type(select_stmt.where_clause).__name__}")
        else:
            print(f"  Has WHERE clause: No")
        print()

def example_ast_traversal():
    """Example of traversing the AST"""
    print("\n=== AST Traversal Example ===\n")
    
    def extract_literals(expr):
        """Recursively extract all literals from an expression"""
        literals = []
        
        if isinstance(expr, Literal):
            literals.append(expr.value)
        elif isinstance(expr, BinaryOp):
            literals.extend(extract_literals(expr.left))
            literals.extend(extract_literals(expr.right))
        elif isinstance(expr, Identifier):
            # Identifiers are not literals
            pass
        
        return literals
    
    parser = SQLParser()
    
    sql = "SELECT * FROM users WHERE age > 18 AND name = 'John' AND status != 'inactive'"
    ast = parser.parse(sql)
    select_stmt = ast[0]
    
    print(f"SQL: {sql}")
    
    if select_stmt.where_clause:
        literals = extract_literals(select_stmt.where_clause)
        print(f"Literals found in WHERE clause: {literals}")

def example_sql_validation():
    """Example of using the parser for SQL validation"""
    print("\n=== SQL Validation Example ===\n")
    
    parser = SQLParser()
    
    # List of SQL statements to validate
    sql_statements = [
        ("Valid SELECT", "SELECT * FROM users WHERE id = 1"),
        ("Invalid SELECT", "SELECT FROM users"),
        ("Valid INSERT", "INSERT INTO users (name) VALUES ('John')"),
        ("Invalid INSERT", "INSERT INTO users VALUES"),
        ("Valid UPDATE", "UPDATE users SET name = 'Jane' WHERE id = 1"),
        ("Invalid syntax", "UPDATE users WHERE id = 1"),
    ]
    
    for description, sql in sql_statements:
        print(f"{description}: {sql}")
        try:
            ast = parser.parse(sql)
            print("  ✓ Valid SQL")
        except Exception as e:
            print(f"  ✗ Invalid SQL: {e}")
        print()

def example_batch_processing():
    """Example of processing multiple SQL statements"""
    print("\n=== Batch Processing Example ===\n")
    
    parser = SQLParser()
    
    # Multiple SQL statements separated by semicolons
    sql_batch = """
    CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL);
    INSERT INTO products VALUES (1, 'Laptop', 999.99);
    INSERT INTO products VALUES (2, 'Mouse', 29.99);
    SELECT * FROM products WHERE price < 100;
    UPDATE products SET price = 899.99 WHERE id = 1;
    DELETE FROM products WHERE price < 20;
    """
    
    # Parse all statements
    statements = parser.parse(sql_batch)
    
    print(f"Parsed {len(statements)} statements:\n")
    
    # Categorize statements
    statement_types = {}
    for stmt in statements:
        stmt_type = type(stmt).__name__
        statement_types[stmt_type] = statement_types.get(stmt_type, 0) + 1
    
    for stmt_type, count in statement_types.items():
        print(f"  {stmt_type}: {count}")
    
    # Process each statement
    print("\nStatement details:")
    for i, stmt in enumerate(statements, 1):
        print(f"\n{i}. {type(stmt).__name__}:")
        
        if isinstance(stmt, CreateTableStmt):
            print(f"   Table: {stmt.table_name}")
            print(f"   Columns: {len(stmt.columns)}")
        elif isinstance(stmt, SelectStmt):
            print(f"   Table: {stmt.table_name}")
            print(f"   Selecting: {', '.join(stmt.columns)}")
        elif isinstance(stmt, InsertStmt):
            print(f"   Table: {stmt.table_name}")
            print(f"   Rows: {len(stmt.values)}")
        elif isinstance(stmt, UpdateStmt):
            print(f"   Table: {stmt.table_name}")
            print(f"   Updates: {len(stmt.assignments)} column(s)")
        elif isinstance(stmt, DeleteStmt):
            print(f"   Table: {stmt.table_name}")
            print(f"   Has WHERE: {'Yes' if stmt.where_clause else 'No'}")

def example_custom_visitor():
    """Example of implementing a visitor pattern for the AST"""
    print("\n=== Custom Visitor Example ===\n")
    
    class TableExtractor:
        """Extract all table names from SQL statements"""
        
        def __init__(self):
            self.tables = set()
        
        def visit(self, node):
            method_name = f'visit_{type(node).__name__}'
            visitor = getattr(self, method_name, self.generic_visit)
            return visitor(node)
        
        def generic_visit(self, node):
            pass
        
        def visit_CreateTableStmt(self, node):
            self.tables.add(node.table_name)
        
        def visit_SelectStmt(self, node):
            self.tables.add(node.table_name)
        
        def visit_InsertStmt(self, node):
            self.tables.add(node.table_name)
        
        def visit_UpdateStmt(self, node):
            self.tables.add(node.table_name)
        
        def visit_DeleteStmt(self, node):
            self.tables.add(node.table_name)
    
    parser = SQLParser()
    
    sql_script = """
    CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER);
    INSERT INTO users VALUES (1, 'John');
    SELECT * FROM users;
    SELECT * FROM orders WHERE user_id = 1;
    UPDATE users SET name = 'Jane' WHERE id = 1;
    DELETE FROM orders WHERE id > 100;
    """
    
    statements = parser.parse(sql_script)
    
    # Extract all table names
    extractor = TableExtractor()
    for stmt in statements:
        extractor.visit(stmt)
    
    print("Tables referenced in the SQL script:")
    for table in sorted(extractor.tables):
        print(f"  - {table}")

if __name__ == "__main__":
    # Run all examples
    example_basic_usage()
    example_query_analysis()
    example_ast_traversal()
    example_sql_validation()
    example_batch_processing()
    example_custom_visitor()