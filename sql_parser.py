import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Union, Dict, Any

# Token Types
class TokenType(Enum):
    # Keywords
    CREATE = auto()
    TABLE = auto()
    SELECT = auto()
    FROM = auto()
    WHERE = auto()
    INSERT = auto()
    INTO = auto()
    VALUES = auto()
    UPDATE = auto()
    SET = auto()
    DELETE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    NULL = auto()
    PRIMARY = auto()
    KEY = auto()
    INTEGER = auto()
    TEXT = auto()
    REAL = auto()
    BLOB = auto()
    
    # Operators
    EQUALS = auto()
    NOT_EQUALS = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_EQUALS = auto()
    GREATER_EQUALS = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    SEMICOLON = auto()
    DOT = auto()
    STAR = auto()
    
    # Literals
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    
    # Special
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int

class Lexer:
    def __init__(self, input_text: str):
        self.input = input_text
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        # Keywords mapping
        self.keywords = {
            'CREATE': TokenType.CREATE,
            'TABLE': TokenType.TABLE,
            'SELECT': TokenType.SELECT,
            'FROM': TokenType.FROM,
            'WHERE': TokenType.WHERE,
            'INSERT': TokenType.INSERT,
            'INTO': TokenType.INTO,
            'VALUES': TokenType.VALUES,
            'UPDATE': TokenType.UPDATE,
            'SET': TokenType.SET,
            'DELETE': TokenType.DELETE,
            'AND': TokenType.AND,
            'OR': TokenType.OR,
            'NOT': TokenType.NOT,
            'NULL': TokenType.NULL,
            'PRIMARY': TokenType.PRIMARY,
            'KEY': TokenType.KEY,
            'INTEGER': TokenType.INTEGER,
            'TEXT': TokenType.TEXT,
            'REAL': TokenType.REAL,
            'BLOB': TokenType.BLOB,
        }
    
    def current_char(self) -> Optional[str]:
        if self.position >= len(self.input):
            return None
        return self.input[self.position]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        pos = self.position + offset
        if pos >= len(self.input):
            return None
        return self.input[pos]
    
    def advance(self):
        if self.position < len(self.input):
            if self.input[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char().isspace():
            self.advance()
    
    def skip_comment(self):
        if self.current_char() == '-' and self.peek_char() == '-':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
    
    def read_string(self) -> str:
        quote_char = self.current_char()
        self.advance()  # Skip opening quote
        
        value = ''
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\' and self.peek_char() == quote_char:
                self.advance()
                value += quote_char
                self.advance()
            else:
                value += self.current_char()
                self.advance()
        
        if self.current_char() == quote_char:
            self.advance()  # Skip closing quote
        else:
            raise SyntaxError(f"Unterminated string at line {self.line}, column {self.column}")
        
        return value
    
    def read_number(self) -> Union[int, float]:
        num_str = ''
        has_dot = False
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if has_dot:
                    break
                has_dot = True
            num_str += self.current_char()
            self.advance()
        
        return float(num_str) if has_dot else int(num_str)
    
    def read_identifier(self) -> str:
        identifier = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            identifier += self.current_char()
            self.advance()
        
        return identifier
    
    def tokenize(self) -> List[Token]:
        while self.position < len(self.input):
            self.skip_whitespace()
            self.skip_comment()
            
            if self.position >= len(self.input):
                break
            
            line = self.line
            column = self.column
            char = self.current_char()
            
            # Single character tokens
            if char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', line, column))
                self.advance()
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', line, column))
                self.advance()
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', line, column))
                self.advance()
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ';', line, column))
                self.advance()
            elif char == '.':
                self.tokens.append(Token(TokenType.DOT, '.', line, column))
                self.advance()
            elif char == '*':
                self.tokens.append(Token(TokenType.STAR, '*', line, column))
                self.advance()
            
            # Operators
            elif char == '=':
                self.advance()
                self.tokens.append(Token(TokenType.EQUALS, '=', line, column))
            elif char == '!':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.NOT_EQUALS, '!=', line, column))
                else:
                    raise SyntaxError(f"Invalid character '!' at line {line}, column {column}")
            elif char == '<':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.LESS_EQUALS, '<=', line, column))
                elif self.current_char() == '>':
                    self.advance()
                    self.tokens.append(Token(TokenType.NOT_EQUALS, '<>', line, column))
                else:
                    self.tokens.append(Token(TokenType.LESS_THAN, '<', line, column))
            elif char == '>':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.GREATER_EQUALS, '>=', line, column))
                else:
                    self.tokens.append(Token(TokenType.GREATER_THAN, '>', line, column))
            
            # String literals
            elif char in ["'", '"']:
                value = self.read_string()
                self.tokens.append(Token(TokenType.STRING, value, line, column))
            
            # Numbers
            elif char.isdigit():
                value = self.read_number()
                self.tokens.append(Token(TokenType.NUMBER, value, line, column))
            
            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                identifier = self.read_identifier()
                token_type = self.keywords.get(identifier.upper(), TokenType.IDENTIFIER)
                value = identifier.upper() if token_type != TokenType.IDENTIFIER else identifier
                self.tokens.append(Token(token_type, value, line, column))
            
            else:
                raise SyntaxError(f"Unexpected character '{char}' at line {line}, column {column}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

# AST Node Classes
@dataclass
class ASTNode:
    pass

@dataclass
class ColumnDef:
    name: str
    data_type: str
    is_primary_key: bool = False
    is_not_null: bool = False

@dataclass
class CreateTableStmt(ASTNode):
    table_name: str
    columns: List[ColumnDef]

@dataclass
class SelectStmt(ASTNode):
    columns: List[str]  # ['*'] for SELECT *
    table_name: str
    where_clause: Optional['Expression'] = None

@dataclass
class InsertStmt(ASTNode):
    table_name: str
    columns: Optional[List[str]]
    values: List[List[Any]]

@dataclass
class UpdateStmt(ASTNode):
    table_name: str
    assignments: Dict[str, Any]
    where_clause: Optional['Expression'] = None

@dataclass
class DeleteStmt(ASTNode):
    table_name: str
    where_clause: Optional['Expression'] = None

@dataclass
class Expression(ASTNode):
    pass

@dataclass
class BinaryOp(Expression):
    left: Expression
    operator: str
    right: Expression

@dataclass
class UnaryOp(Expression):
    operator: str
    operand: Expression

@dataclass
class Literal(Expression):
    value: Any

@dataclass
class Identifier(Expression):
    name: str

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
    
    def current_token(self) -> Token:
        if self.position >= len(self.tokens):
            return self.tokens[-1]  # EOF token
        return self.tokens[self.position]
    
    def peek_token(self, offset: int = 1) -> Token:
        pos = self.position + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]  # EOF token
        return self.tokens[pos]
    
    def advance(self):
        if self.position < len(self.tokens) - 1:
            self.position += 1
    
    def expect(self, token_type: TokenType) -> Token:
        token = self.current_token()
        if token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {token.type} at line {token.line}, column {token.column}")
        self.advance()
        return token
    
    def parse(self) -> List[ASTNode]:
        statements = []
        
        while self.current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            
            # Optional semicolon
            if self.current_token().type == TokenType.SEMICOLON:
                self.advance()
        
        return statements
    
    def parse_statement(self) -> Optional[ASTNode]:
        token = self.current_token()
        
        if token.type == TokenType.CREATE:
            return self.parse_create_table()
        elif token.type == TokenType.SELECT:
            return self.parse_select()
        elif token.type == TokenType.INSERT:
            return self.parse_insert()
        elif token.type == TokenType.UPDATE:
            return self.parse_update()
        elif token.type == TokenType.DELETE:
            return self.parse_delete()
        else:
            raise SyntaxError(f"Unexpected token {token.type} at line {token.line}, column {token.column}")
    
    def parse_create_table(self) -> CreateTableStmt:
        self.expect(TokenType.CREATE)
        self.expect(TokenType.TABLE)
        
        table_name = self.expect(TokenType.IDENTIFIER).value
        
        self.expect(TokenType.LPAREN)
        
        columns = []
        while self.current_token().type != TokenType.RPAREN:
            column = self.parse_column_def()
            columns.append(column)
            
            if self.current_token().type == TokenType.COMMA:
                self.advance()
            elif self.current_token().type != TokenType.RPAREN:
                raise SyntaxError(f"Expected ',' or ')' at line {self.current_token().line}")
        
        self.expect(TokenType.RPAREN)
        
        return CreateTableStmt(table_name, columns)
    
    def parse_column_def(self) -> ColumnDef:
        name = self.expect(TokenType.IDENTIFIER).value
        
        # Parse data type
        data_type_token = self.current_token()
        if data_type_token.type in [TokenType.INTEGER, TokenType.TEXT, TokenType.REAL, TokenType.BLOB]:
            data_type = data_type_token.value
            self.advance()
        else:
            raise SyntaxError(f"Expected data type at line {data_type_token.line}")
        
        is_primary_key = False
        is_not_null = False
        
        # Parse constraints
        while self.current_token().type in [TokenType.PRIMARY, TokenType.NOT]:
            if self.current_token().type == TokenType.PRIMARY:
                self.advance()
                self.expect(TokenType.KEY)
                is_primary_key = True
            elif self.current_token().type == TokenType.NOT:
                self.advance()
                self.expect(TokenType.NULL)
                is_not_null = True
        
        return ColumnDef(name, data_type, is_primary_key, is_not_null)
    
    def parse_select(self) -> SelectStmt:
        self.expect(TokenType.SELECT)
        
        columns = []
        if self.current_token().type == TokenType.STAR:
            columns.append('*')
            self.advance()
        else:
            while True:
                column = self.expect(TokenType.IDENTIFIER).value
                columns.append(column)
                
                if self.current_token().type != TokenType.COMMA:
                    break
                self.advance()
        
        self.expect(TokenType.FROM)
        table_name = self.expect(TokenType.IDENTIFIER).value
        
        where_clause = None
        if self.current_token().type == TokenType.WHERE:
            self.advance()
            where_clause = self.parse_expression()
        
        return SelectStmt(columns, table_name, where_clause)
    
    def parse_insert(self) -> InsertStmt:
        self.expect(TokenType.INSERT)
        self.expect(TokenType.INTO)
        
        table_name = self.expect(TokenType.IDENTIFIER).value
        
        columns = None
        if self.current_token().type == TokenType.LPAREN:
            self.advance()
            columns = []
            while self.current_token().type != TokenType.RPAREN:
                column = self.expect(TokenType.IDENTIFIER).value
                columns.append(column)
                
                if self.current_token().type == TokenType.COMMA:
                    self.advance()
            self.expect(TokenType.RPAREN)
        
        self.expect(TokenType.VALUES)
        
        values = []
        while True:
            self.expect(TokenType.LPAREN)
            row_values = []
            
            while self.current_token().type != TokenType.RPAREN:
                value = self.parse_literal()
                row_values.append(value)
                
                if self.current_token().type == TokenType.COMMA:
                    self.advance()
            
            self.expect(TokenType.RPAREN)
            values.append(row_values)
            
            if self.current_token().type != TokenType.COMMA:
                break
            self.advance()
        
        return InsertStmt(table_name, columns, values)
    
    def parse_update(self) -> UpdateStmt:
        self.expect(TokenType.UPDATE)
        
        table_name = self.expect(TokenType.IDENTIFIER).value
        
        self.expect(TokenType.SET)
        
        assignments = {}
        while True:
            column = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.EQUALS)
            value = self.parse_literal()
            assignments[column] = value
            
            if self.current_token().type != TokenType.COMMA:
                break
            self.advance()
        
        where_clause = None
        if self.current_token().type == TokenType.WHERE:
            self.advance()
            where_clause = self.parse_expression()
        
        return UpdateStmt(table_name, assignments, where_clause)
    
    def parse_delete(self) -> DeleteStmt:
        self.expect(TokenType.DELETE)
        self.expect(TokenType.FROM)
        
        table_name = self.expect(TokenType.IDENTIFIER).value
        
        where_clause = None
        if self.current_token().type == TokenType.WHERE:
            self.advance()
            where_clause = self.parse_expression()
        
        return DeleteStmt(table_name, where_clause)
    
    def parse_expression(self) -> Expression:
        return self.parse_or()
    
    def parse_or(self) -> Expression:
        left = self.parse_and()
        
        while self.current_token().type == TokenType.OR:
            self.advance()
            right = self.parse_and()
            left = BinaryOp(left, 'OR', right)
        
        return left
    
    def parse_and(self) -> Expression:
        left = self.parse_not()
        
        while self.current_token().type == TokenType.AND:
            self.advance()
            right = self.parse_not()
            left = BinaryOp(left, 'AND', right)
        
        return left
    
    def parse_not(self) -> Expression:
        if self.current_token().type == TokenType.NOT:
            self.advance()
            operand = self.parse_comparison()
            return UnaryOp('NOT', operand)
        
        return self.parse_comparison()
    
    def parse_comparison(self) -> Expression:
        left = self.parse_primary()
        
        token = self.current_token()
        if token.type in [TokenType.EQUALS, TokenType.NOT_EQUALS, TokenType.LESS_THAN,
                         TokenType.GREATER_THAN, TokenType.LESS_EQUALS, TokenType.GREATER_EQUALS]:
            operator = token.value
            self.advance()
            right = self.parse_primary()
            return BinaryOp(left, operator, right)
        
        return left
    
    def parse_primary(self) -> Expression:
        token = self.current_token()
        
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        elif token.type == TokenType.IDENTIFIER:
            self.advance()
            return Identifier(token.value)
        else:
            return Literal(self.parse_literal())
    
    def parse_literal(self) -> Any:
        token = self.current_token()
        
        if token.type == TokenType.NUMBER:
            self.advance()
            return token.value
        elif token.type == TokenType.STRING:
            self.advance()
            return token.value
        elif token.type == TokenType.NULL:
            self.advance()
            return None
        else:
            raise SyntaxError(f"Expected literal at line {token.line}, column {token.column}")

class SQLParser:
    def __init__(self):
        pass
    
    def parse(self, sql: str) -> List[ASTNode]:
        lexer = Lexer(sql)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse()

# Helper function to pretty print AST
def print_ast(node: ASTNode, indent: int = 0):
    prefix = "  " * indent
    
    if isinstance(node, CreateTableStmt):
        print(f"{prefix}CREATE TABLE {node.table_name}")
        for col in node.columns:
            constraints = []
            if col.is_primary_key:
                constraints.append("PRIMARY KEY")
            if col.is_not_null:
                constraints.append("NOT NULL")
            constraint_str = f" ({', '.join(constraints)})" if constraints else ""
            print(f"{prefix}  - {col.name}: {col.data_type}{constraint_str}")
    
    elif isinstance(node, SelectStmt):
        columns = ", ".join(node.columns)
        print(f"{prefix}SELECT {columns} FROM {node.table_name}")
        if node.where_clause:
            print(f"{prefix}  WHERE:")
            print_expression(node.where_clause, indent + 2)
    
    elif isinstance(node, InsertStmt):
        columns_str = f"({', '.join(node.columns)})" if node.columns else ""
        print(f"{prefix}INSERT INTO {node.table_name}{columns_str}")
        for i, values in enumerate(node.values):
            values_str = ", ".join(repr(v) for v in values)
            print(f"{prefix}  VALUES ({values_str})")
    
    elif isinstance(node, UpdateStmt):
        print(f"{prefix}UPDATE {node.table_name}")
        print(f"{prefix}  SET:")
        for col, val in node.assignments.items():
            print(f"{prefix}    {col} = {repr(val)}")
        if node.where_clause:
            print(f"{prefix}  WHERE:")
            print_expression(node.where_clause, indent + 2)
    
    elif isinstance(node, DeleteStmt):
        print(f"{prefix}DELETE FROM {node.table_name}")
        if node.where_clause:
            print(f"{prefix}  WHERE:")
            print_expression(node.where_clause, indent + 2)

def print_expression(expr: Expression, indent: int = 0):
    prefix = "  " * indent
    
    if isinstance(expr, BinaryOp):
        print(f"{prefix}{expr.operator}")
        print_expression(expr.left, indent + 1)
        print_expression(expr.right, indent + 1)
    elif isinstance(expr, UnaryOp):
        print(f"{prefix}{expr.operator}")
        print_expression(expr.operand, indent + 1)
    elif isinstance(expr, Identifier):
        print(f"{prefix}ID: {expr.name}")
    elif isinstance(expr, Literal):
        print(f"{prefix}LITERAL: {repr(expr.value)}")

if __name__ == "__main__":
    # Test the parser with example SQL statements
    test_queries = [
        "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, age INTEGER)",
        "SELECT * FROM users",
        "SELECT name, age FROM users WHERE age > 18",
        "INSERT INTO users (name, age) VALUES ('John', 25), ('Jane', 30)",
        "UPDATE users SET age = 26 WHERE name = 'John'",
        "DELETE FROM users WHERE age < 18",
        "SELECT name FROM users WHERE age > 20 AND name != 'Admin'",
    ]
    
    parser = SQLParser()
    
    for query in test_queries:
        print(f"\nParsing: {query}")
        print("-" * 50)
        try:
            ast = parser.parse(query)
            for stmt in ast:
                print_ast(stmt)
        except Exception as e:
            print(f"Error: {e}")