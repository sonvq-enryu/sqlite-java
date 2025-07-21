package dev.mini.sql;

/**
 * Token types understood by the SQL lexer.
 */
public enum TokenType {
    // Single-character tokens
    LEFT_PAREN, RIGHT_PAREN,
    COMMA, DOT, STAR, SEMICOLON,
    PLUS, MINUS, SLASH, PERCENT, // arithmetic not yet supported but reserved
    EQUAL, NOT_EQUAL, LESS, LESS_EQUAL, GREATER, GREATER_EQUAL,

    // Literals
    IDENTIFIER,
    STRING,
    NUMBER,

    // Keywords
    CREATE, TABLE, SELECT, FROM, WHERE, INSERT, INTO, VALUES,
    UPDATE, SET, DELETE,
    AND, OR,

    // End of input
    EOF
}