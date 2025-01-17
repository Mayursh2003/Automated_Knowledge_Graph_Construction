import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def resolve_conflicts(schema, conflicting_entities):
    """
    Removes conflicting entities from the schema.

    Args:
        schema (dict): The extracted schema containing entities.
        conflicting_entities (list): A list of entities to remove.

    Returns:
        dict: Updated schema with conflicts resolved.
    """
    if "entities" not in schema:
        logging.warning("Schema does not contain 'entities' key.")
        return schema

    original_entities = set(schema["entities"])
    updated_entities = [entity for entity in schema["entities"] if entity not in conflicting_entities]
    removed_entities = original_entities - set(updated_entities)

    schema["entities"] = updated_entities

    if removed_entities:
        logging.info(f"Removed conflicting entities: {removed_entities}")
    else:
        logging.info("No conflicting entities found.")

    return schema
