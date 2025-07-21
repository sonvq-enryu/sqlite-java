package dev.mini.sql;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Very small hand-written SQL parser that supports a subset of SQLite DDL/DML.
 */
public class Parser {

    private final List<Token> tokens;
    private int current = 0;

    public Parser(List<Token> tokens) {
        this.tokens = tokens;
    }

    public SqlStatement parse() {
        if (match(TokenType.CREATE)) {
            return parseCreateTable();
        } else if (match(TokenType.SELECT)) {
            return parseSelect();
        } else if (match(TokenType.INSERT)) {
            return parseInsert();
        } else if (match(TokenType.UPDATE)) {
            return parseUpdate();
        } else if (match(TokenType.DELETE)) {
            return parseDelete();
        }
        throw error(peek(), "Unexpected statement start");
    }

    // --- CREATE TABLE ---
    private CreateTableStatement parseCreateTable() {
        consume(TokenType.TABLE, "Expect TABLE after CREATE");
        String tableName = consumeIdentifier("Expect table name");
        consume(TokenType.LEFT_PAREN, "Expect '(' after table name");
        List<ColumnDefinition> columns = new ArrayList<>();
        do {
            String columnName = consumeIdentifier("Expect column name");
            String type = null;
            if (check(TokenType.IDENTIFIER)) {
                type = consumeIdentifier("Expect column type");
            }
            columns.add(new ColumnDefinition(columnName, type));
        } while (match(TokenType.COMMA));
        consume(TokenType.RIGHT_PAREN, "Expect ')' after column list");
        optional(TokenType.SEMICOLON);
        return new CreateTableStatement(tableName, columns);
    }

    // --- SELECT ---
    private SelectStatement parseSelect() {
        List<String> columns = new ArrayList<>();
        if (match(TokenType.STAR)) {
            columns.add("*");
        } else {
            do {
                columns.add(consumeIdentifier("Expect column name"));
            } while (match(TokenType.COMMA));
        }
        consume(TokenType.FROM, "Expect FROM after column list");
        String tableName = consumeIdentifier("Expect table name");
        Expression where = null;
        if (match(TokenType.WHERE)) {
            where = parseExpression();
        }
        optional(TokenType.SEMICOLON);
        return new SelectStatement(columns, tableName, where);
    }

    // --- INSERT ---
    private InsertStatement parseInsert() {
        consume(TokenType.INTO, "Expect INTO after INSERT");
        String tableName = consumeIdentifier("Expect table name");
        consume(TokenType.LEFT_PAREN, "Expect '(' after table name");
        List<String> columns = new ArrayList<>();
        do {
            columns.add(consumeIdentifier("Expect column name"));
        } while (match(TokenType.COMMA));
        consume(TokenType.RIGHT_PAREN, "Expect ')' after column list");
        consume(TokenType.VALUES, "Expect VALUES keyword");
        consume(TokenType.LEFT_PAREN, "Expect '(' before values list");
        List<Expression> values = new ArrayList<>();
        do {
            values.add(parseLiteral());
        } while (match(TokenType.COMMA));
        consume(TokenType.RIGHT_PAREN, "Expect ')' after values list");
        optional(TokenType.SEMICOLON);
        return new InsertStatement(tableName, columns, values);
    }

    // --- UPDATE ---
    private UpdateStatement parseUpdate() {
        String tableName = consumeIdentifier("Expect table name");
        consume(TokenType.SET, "Expect SET keyword");
        Map<String, Expression> assignments = new HashMap<>();
        do {
            String column = consumeIdentifier("Expect column name in assignment");
            consume(TokenType.EQUAL, "Expect '=' in assignment");
            Expression value = parseLiteral();
            assignments.put(column, value);
        } while (match(TokenType.COMMA));
        Expression where = null;
        if (match(TokenType.WHERE)) {
            where = parseExpression();
        }
        optional(TokenType.SEMICOLON);
        return new UpdateStatement(tableName, assignments, where);
    }

    // --- DELETE ---
    private DeleteStatement parseDelete() {
        consume(TokenType.FROM, "Expect FROM after DELETE");
        String tableName = consumeIdentifier("Expect table name");
        Expression where = null;
        if (match(TokenType.WHERE)) {
            where = parseExpression();
        }
        optional(TokenType.SEMICOLON);
        return new DeleteStatement(tableName, where);
    }

    // --- Expressions (very limited) ---
    private Expression parseExpression() {
        // Only support column comparison literal (and optionally AND/OR chain)
        Expression expr = parseComparison();
        while (match(TokenType.AND, TokenType.OR)) {
            Token operator = previous();
            Expression right = parseComparison();
            expr = new BinaryExpression(expr, operator.lexeme.toUpperCase(), right);
        }
        return expr;
    }

    private Expression parseComparison() {
        Expression left = parsePrimary();
        if (match(TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL)) {
            Token operator = previous();
            Expression right = parsePrimary();
            return new BinaryExpression(left, operator.lexeme, right);
        }
        return left;
    }

    private Expression parsePrimary() {
        if (match(TokenType.IDENTIFIER)) {
            return new ColumnExpression(previous().lexeme);
        }
        return parseLiteral();
    }

    private Expression parseLiteral() {
        if (match(TokenType.STRING)) {
            return new LiteralExpression(previous().literal);
        }
        if (match(TokenType.NUMBER)) {
            return new LiteralExpression(previous().literal);
        }
        throw error(peek(), "Expect literal value");
    }

    // --- Helpers ---
    private boolean match(TokenType... types) {
        for (TokenType type : types) {
            if (check(type)) {
                advance();
                return true;
            }
        }
        return false;
    }

    private boolean optional(TokenType type) {
        if (check(type)) {
            advance();
            return true;
        }
        return false;
    }

    private Token consume(TokenType type, String message) {
        if (check(type)) return advance();
        throw error(peek(), message);
    }

    private String consumeIdentifier(String message) {
        if (check(TokenType.IDENTIFIER)) {
            return advance().lexeme;
        }
        throw error(peek(), message);
    }

    private boolean check(TokenType type) {
        if (isAtEnd()) return false;
        return peek().type == type;
    }

    private Token advance() {
        if (!isAtEnd()) current++;
        return previous();
    }

    private boolean isAtEnd() {
        return peek().type == TokenType.EOF;
    }

    private Token peek() {
        return tokens.get(current);
    }

    private Token previous() {
        return tokens.get(current - 1);
    }

    private ParseError error(Token token, String message) {
        return new ParseError("[Parser] Error at '" + token.lexeme + "': " + message);
    }

    private static class ParseError extends RuntimeException {
        ParseError(String msg) {super(msg);} }
}