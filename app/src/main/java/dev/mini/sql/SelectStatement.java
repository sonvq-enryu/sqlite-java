package dev.mini.sql;

import java.util.List;

public class SelectStatement implements SqlStatement {
    private final List<String> columns;
    private final String tableName;
    private final Expression where;

    public SelectStatement(List<String> columns, String tableName, Expression where) {
        this.columns = columns;
        this.tableName = tableName;
        this.where = where;
    }

    public List<String> getColumns() {
        return columns;
    }

    public String getTableName() {
        return tableName;
    }

    public Expression getWhere() {
        return where;
    }

    @Override
    public String toString() {
        return "SELECT " + String.join(",", columns) + " FROM " + tableName + (where != null ? " WHERE " + where : "");
    }
}