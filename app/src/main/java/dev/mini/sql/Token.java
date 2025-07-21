package dev.mini.sql;

/**
 * Represents a lexical token in an SQL statement.
 */
public class Token {
    public final TokenType type;
    public final String lexeme;
    public final Object literal;
    public final int position;

    public Token(TokenType type, String lexeme, Object literal, int position) {
        this.type = type;
        this.lexeme = lexeme;
        this.literal = literal;
        this.position = position;
    }

    @Override
    public String toString() {
        return type + " " + lexeme + (literal != null ? " " + literal : "");
    }
}