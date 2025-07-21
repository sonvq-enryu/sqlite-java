package dev.mini.sql;

import java.util.Map;

public class UpdateStatement implements SqlStatement {
    private final String tableName;
    private final Map<String, Expression> assignments;
    private final Expression where;

    public UpdateStatement(String tableName, Map<String, Expression> assignments, Expression where) {
        this.tableName = tableName;
        this.assignments = assignments;
        this.where = where;
    }

    public String getTableName() {
        return tableName;
    }

    public Map<String, Expression> getAssignments() {
        return assignments;
    }

    public Expression getWhere() {
        return where;
    }

    @Override
    public String toString() {
        return "UPDATE " + tableName + " SET " + assignments + (where != null ? " WHERE " + where : "");
    }
}