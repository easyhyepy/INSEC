DataField::DataField(PlannerDomValue fieldObject, int index) {
    if (fieldObject.hasKey("TABLE_NAME")) {
        fieldTableName = fieldObject.valueForKey("TABLE_NAME").asStr();
    }

    if (fieldObject.hasKey("COLUMN_NAME")) {
        fieldColumnName = fieldObject.valueForKey("COLUMN_NAME").asStr();
    } else {
        char defaultName[6];
        std::snprintf(defaultName, sizeof(defaultName), "F%d", index);
        defaultName[sizeof defaultName - 1] = '\0';
        fieldColumnName = std::string(defaultName);
    }

    if (fieldObject.hasKey("SIZE")) {
        fieldSize = fieldObject.valueForKey("SIZE").asInt();
    }

    fieldExpression = NULL;
    if (fieldObject.hasKey("EXPRESSION")) {
        PlannerDomValue expressionValue = fieldObject.valueForKey("EXPRESSION");

        fieldExpression = AbstractExpression::buildExpressionTree(expressionValue);
        vassert(fieldExpression);
    }
}
