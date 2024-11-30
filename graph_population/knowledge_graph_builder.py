from rdflib import Graph, URIRef, Literal, Namespace
from urllib.parse import quote

def build_knowledge_graph(schemas):
    g = Graph()
    EX = Namespace("http://example.org/")

    for doc, schema in schemas.items():
        doc_uri = URIRef(EX[quote(doc.replace(" ", "_"))])  # URL encode the document name
        g.add((doc_uri, EX.word_count, Literal(schema['word_count'])))
        for entity in schema['unique_entities']:
            entity_uri = URIRef(EX[quote(entity.replace(" ", "_"))])  # URL encode the entity name
            g.add((doc_uri, EX.has_entity, entity_uri))
            g.add((entity_uri, EX.entity_name, Literal(entity)))

    return g