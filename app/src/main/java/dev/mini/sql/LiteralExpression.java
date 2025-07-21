package dev.mini.sql;

public class LiteralExpression implements Expression {
    private final Object value;

    public LiteralExpression(Object value) {
        this.value = value;
    }

    public Object getValue() {
        return value;
    }

    @Override
    public String toString() {
        if (value instanceof String) {
            return "'" + value + "'";
        }
        return String.valueOf(value);
    }
}