#!/usr/bin/env python3

from sql_parser import SQLParser, print_ast
import sys

def test_parser():
    """Test the SQL parser with various SQL statements"""
    
    parser = SQLParser()
    
    # Test cases organized by SQL command type
    test_cases = {
        "CREATE TABLE": [
            "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT)",
            "CREATE TABLE products (product_id INTEGER PRIMARY KEY, name TEXT NOT NULL, price REAL, description TEXT)",
            "CREATE TABLE orders (order_id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, total REAL, created_at TEXT)",
            "CREATE TABLE inventory (id INTEGER, product_id INTEGER, quantity INTEGER, warehouse TEXT)"
        ],
        
        "SELECT": [
            "SELECT * FROM users",
            "SELECT name, email FROM users",
            "SELECT id, name FROM users WHERE id = 1",
            "SELECT * FROM products WHERE price > 100.50",
            "SELECT name, price FROM products WHERE price >= 50 AND price <= 200",
            "SELECT * FROM users WHERE name = 'John Doe' OR email = 'john@example.com'",
            "SELECT * FROM products WHERE NOT price > 1000",
            "SELECT id, name FROM users WHERE age > 18 AND name != 'Admin'",
            "SELECT * FROM orders WHERE total > 100 AND (status = 'pending' OR status = 'processing')"
        ],
        
        "INSERT": [
            "INSERT INTO users VALUES (1, 'John Doe', 'john@example.com')",
            "INSERT INTO users (name, email) VALUES ('Jane Smith', 'jane@example.com')",
            "INSERT INTO products (name, price, description) VALUES ('Laptop', 999.99, 'High-performance laptop')",
            "INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com'), ('Bob', 'bob@example.com')",
            "INSERT INTO inventory VALUES (1, 101, 50, 'Warehouse A'), (2, 102, 30, 'Warehouse B')"
        ],
        
        "UPDATE": [
            "UPDATE users SET email = 'newemail@example.com' WHERE id = 1",
            "UPDATE products SET price = 899.99 WHERE product_id = 101",
            "UPDATE users SET name = 'John Smith', email = 'johnsmith@example.com' WHERE id = 1",
            "UPDATE inventory SET quantity = 100 WHERE product_id = 101 AND warehouse = 'Warehouse A'",
            "UPDATE products SET price = price * 0.9 WHERE category = 'Electronics'"
        ],
        
        "DELETE": [
            "DELETE FROM users WHERE id = 1",
            "DELETE FROM products WHERE price < 10",
            "DELETE FROM orders WHERE created_at < '2023-01-01'",
            "DELETE FROM users WHERE email = 'test@example.com' AND status = 'inactive'",
            "DELETE FROM inventory WHERE quantity = 0"
        ],
        
        "Complex Examples": [
            # Multiple statements with semicolons
            "CREATE TABLE temp (id INTEGER); SELECT * FROM temp; DELETE FROM temp",
            # Case insensitive keywords
            "select * from users where id = 1",
            "SELECT * FROM users WHERE id = 1",
            # Comments
            "-- This is a comment\nSELECT * FROM users",
            "SELECT * FROM users -- inline comment",
            # String with special characters
            "INSERT INTO users (name) VALUES ('O''Brien')",
            "SELECT * FROM users WHERE name = 'It''s a test'",
            # Numeric comparisons
            "SELECT * FROM products WHERE price <> 100",
            "SELECT * FROM products WHERE price != 100"
        ]
    }
    
    # Run all test cases
    for category, queries in test_cases.items():
        print(f"\n{'=' * 60}")
        print(f"Testing {category}")
        print(f"{'=' * 60}")
        
        for query in queries:
            print(f"\nSQL: {query}")
            print("-" * 40)
            
            try:
                ast = parser.parse(query)
                for stmt in ast:
                    print_ast(stmt)
            except Exception as e:
                print(f"ERROR: {type(e).__name__}: {e}")
    
    # Test error cases
    print(f"\n{'=' * 60}")
    print("Testing Error Cases")
    print(f"{'=' * 60}")
    
    error_cases = [
        ("Missing table name", "CREATE TABLE (id INTEGER)"),
        ("Invalid syntax", "SELECT FROM users"),
        ("Unclosed string", "SELECT * FROM users WHERE name = 'unclosed"),
        ("Invalid operator", "SELECT * FROM users WHERE id @ 1"),
        ("Missing values", "INSERT INTO users VALUES"),
        ("Invalid token", "SELECT * FROM users WHERE id = $1"),
        ("Missing WHERE expression", "SELECT * FROM users WHERE"),
        ("Invalid column definition", "CREATE TABLE test (id)"),
    ]
    
    for description, query in error_cases:
        print(f"\n{description}: {query}")
        print("-" * 40)
        try:
            ast = parser.parse(query)
            print("ERROR: Should have raised an exception!")
        except Exception as e:
            print(f"✓ Expected error: {type(e).__name__}: {e}")

def interactive_mode():
    """Run the parser in interactive mode"""
    parser = SQLParser()
    
    print("SQL Parser Interactive Mode")
    print("Type 'exit' or 'quit' to exit")
    print("-" * 40)
    
    while True:
        try:
            # Get input
            sql = input("\nSQL> ").strip()
            
            # Check for exit
            if sql.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            if not sql:
                continue
            
            # Parse and display AST
            ast = parser.parse(sql)
            print("\nParsed AST:")
            print("-" * 20)
            for stmt in ast:
                print_ast(stmt)
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        test_parser()
        print("\n\nTo run in interactive mode, use: python test_sql_parser.py --interactive")