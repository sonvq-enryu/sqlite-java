package dev.mini.sql;

public class ColumnExpression implements Expression {
    private final String name;

    public ColumnExpression(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    @Override
    public String toString() {
        return name;
    }
}