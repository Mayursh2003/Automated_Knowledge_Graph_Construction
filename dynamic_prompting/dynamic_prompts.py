def refine_schema(inferred_schema):
    st.title("Schema Refinement Tool")
    st.write("Please review the inferred schema below:")
    
    # Display inferred entities
    entities = inferred_schema["entities"]
    entity_form = {}
    for entity in entities:
        entity_form[entity] = {}
        with st.expander(f"Edit {entity}"):
            entity_form[entity]["new_name"] = st.text_input("Update entity name:", value=entity)
            if st.button("Update Entity", key=entity):
                entities[entities.index(entity)] = entity_form[entity]["new_name"]
                st.success(f"Updated entity: {entity_form[entity]['new_name']}")
            if st.button("Delete Entity", key=f"{entity}_delete"):
                entities.remove(entity)
                st.success(f"Deleted entity: {entity}")
                del entity_form[entity]

    # Add new entity
    new_entity = st.text_input("Add a new entity:")
    if st.button("Add Entity"):
        entities.append(new_entity)
        entity_form[new_entity] = {}
        st.success(f"Added entity: {new_entity}")

    return inferred_schema