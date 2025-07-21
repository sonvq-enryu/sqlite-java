package dev.mini.sql;

import java.util.List;

public class InsertStatement implements SqlStatement {
    private final String tableName;
    private final List<String> columns;
    private final List<Expression> values;

    public InsertStatement(String tableName, List<String> columns, List<Expression> values) {
        this.tableName = tableName;
        this.columns = columns;
        this.values = values;
    }

    public String getTableName() {
        return tableName;
    }

    public List<String> getColumns() {
        return columns;
    }

    public List<Expression> getValues() {
        return values;
    }

    @Override
    public String toString() {
        return "INSERT INTO " + tableName + "(" + String.join(",", columns) + ") VALUES(" + values + ")";
    }
}