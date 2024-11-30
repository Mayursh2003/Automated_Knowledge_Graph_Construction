def resolve_conflicts(schema, conflicting_entities):
    schema["entities"] = [entity for entity in schema["entities"] if entity not in conflicting_entities]
    return schema