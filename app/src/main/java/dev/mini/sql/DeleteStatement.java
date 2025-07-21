package dev.mini.sql;

public class DeleteStatement implements SqlStatement {
    private final String tableName;
    private final Expression where;

    public DeleteStatement(String tableName, Expression where) {
        this.tableName = tableName;
        this.where = where;
    }

    public String getTableName() {
        return tableName;
    }

    public Expression getWhere() {
        return where;
    }

    @Override
    public String toString() {
        return "DELETE FROM " + tableName + (where != null ? " WHERE " + where : "");
    }
}