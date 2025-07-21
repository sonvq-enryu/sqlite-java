# SQLite Parser

A complete SQL parser implementation from scratch that supports basic SQL commands including CREATE TABLE, SELECT, INSERT, UPDATE, and DELETE statements.

## Features

- **Full Lexical Analysis**: Tokenizes SQL statements with proper handling of keywords, identifiers, operators, and literals
- **Comprehensive Parser**: Builds an Abstract Syntax Tree (AST) for SQL statements
- **SQL Command Support**:
  - `CREATE TABLE` with column definitions and constraints (PRIMARY KEY, NOT NULL)
  - `SELECT` with WHERE clauses and multiple conditions
  - `INSERT` with single or multiple rows
  - `UPDATE` with SET assignments and WHERE clauses
  - `DELETE` with WHERE clauses
- **Expression Support**:
  - Comparison operators: `=`, `!=`, `<>`, `<`, `>`, `<=`, `>=`
  - Logical operators: `AND`, `OR`, `NOT`
  - Parenthesized expressions
- **Data Types**: INTEGER, TEXT, REAL, BLOB
- **Error Handling**: Detailed syntax error messages with line and column information
- **Comment Support**: SQL single-line comments (`--`)

## Installation

No external dependencies required! The parser is implemented using only Python standard library.

```bash
# Clone or download the files
python sql_parser.py
```

## Quick Start

```python
from sql_parser import SQLParser

# Create parser instance
parser = SQLParser()

# Parse SQL statement
sql = "SELECT name, age FROM users WHERE age > 18"
ast = parser.parse(sql)

# Access parsed data
select_stmt = ast[0]
print(f"Table: {select_stmt.table_name}")
print(f"Columns: {select_stmt.columns}")
```

## Usage Examples

### Basic Parsing

```python
from sql_parser import SQLParser, print_ast

parser = SQLParser()

# Parse CREATE TABLE
sql = "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL)"
ast = parser.parse(sql)
print_ast(ast[0])

# Parse SELECT with WHERE
sql = "SELECT * FROM users WHERE age > 18 AND status = 'active'"
ast = parser.parse(sql)
print_ast(ast[0])
```

### Interactive Mode

Run the parser in interactive mode:

```bash
python test_sql_parser.py --interactive
```

### Batch Processing

Parse multiple SQL statements:

```python
parser = SQLParser()

sql_batch = """
CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL);
INSERT INTO products VALUES (1, 'Laptop', 999.99);
SELECT * FROM products WHERE price < 100;
"""

statements = parser.parse(sql_batch)
for stmt in statements:
    print(type(stmt).__name__)
```

## Supported SQL Syntax

### CREATE TABLE

```sql
CREATE TABLE table_name (
    column1 datatype [PRIMARY KEY] [NOT NULL],
    column2 datatype [NOT NULL],
    ...
)
```

### SELECT

```sql
SELECT column1, column2, ... FROM table_name
SELECT * FROM table_name
SELECT columns FROM table_name WHERE condition
SELECT columns FROM table_name WHERE condition1 AND/OR condition2
```

### INSERT

```sql
INSERT INTO table_name VALUES (value1, value2, ...)
INSERT INTO table_name (column1, column2) VALUES (value1, value2)
INSERT INTO table_name VALUES (row1_values), (row2_values), ...
```

### UPDATE

```sql
UPDATE table_name SET column1 = value1
UPDATE table_name SET column1 = value1, column2 = value2 WHERE condition
```

### DELETE

```sql
DELETE FROM table_name
DELETE FROM table_name WHERE condition
```

## AST Structure

The parser generates an Abstract Syntax Tree with the following node types:

- **Statement Nodes**:
  - `CreateTableStmt`: Contains table name and column definitions
  - `SelectStmt`: Contains column list, table name, and optional WHERE clause
  - `InsertStmt`: Contains table name, optional column list, and values
  - `UpdateStmt`: Contains table name, assignments, and optional WHERE clause
  - `DeleteStmt`: Contains table name and optional WHERE clause

- **Expression Nodes**:
  - `BinaryOp`: Binary operations (comparisons, AND/OR)
  - `UnaryOp`: Unary operations (NOT)
  - `Identifier`: Column or table names
  - `Literal`: String, number, or NULL values

## Error Handling

The parser provides detailed error messages:

```python
try:
    ast = parser.parse("SELECT FROM users")  # Missing columns
except SyntaxError as e:
    print(f"Error: {e}")
    # Output: Error: Expected identifier, got FROM at line 1, column 8
```

## Running Tests

Run the comprehensive test suite:

```bash
python test_sql_parser.py
```

Run specific examples:

```bash
python example_usage.py
```

## Architecture

The parser consists of three main components:

1. **Lexer** (`Lexer` class): Tokenizes the input SQL string into a stream of tokens
2. **Parser** (`Parser` class): Consumes tokens and builds the AST using recursive descent parsing
3. **AST Nodes**: Data classes representing different SQL constructs

## Extending the Parser

To add support for new SQL features:

1. Add new token types to `TokenType` enum
2. Update the lexer to recognize new tokens
3. Add new AST node classes
4. Implement parsing methods in the `Parser` class
5. Update the `print_ast` function for visualization

## Limitations

- No support for JOINs
- No support for subqueries
- No support for aggregate functions
- No support for ORDER BY, GROUP BY, HAVING
- No support for LIMIT/OFFSET
- Basic data type support only

## License

This is an educational implementation for learning purposes.

## Contributing

Feel free to extend the parser with additional SQL features!