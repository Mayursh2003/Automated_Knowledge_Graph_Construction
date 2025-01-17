import streamlit as st
from rdflib import Graph, URIRef, Literal, Namespace, RDF
import logging
import plotly.graph_objects as go
import networkx as nx
import pandas as pd
import json
from typing import Dict, List, Any
import PyPDF2
from PIL import Image
import pytesseract
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import docx
import spacy
import re
import tempfile
import os

# Load spaCy model for entity extraction
try:
    nlp = spacy.load("en_core_web_sm")
except:
    st.warning("Downloading spaCy model...")
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('knowledge_graph.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.supported_formats = {
            'pdf': self.process_pdf,
            'image': self.process_image,
            'url': self.process_url,
            'docx': self.process_docx
        }

    def process_pdf(self, file_content):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            return ""

    def process_image(self, file_content):
        """Extract text from image using OCR"""
        try:
            image = Image.open(BytesIO(file_content))
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            return ""

    def process_url(self, url):
        """Extract text from web page"""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text()
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            text = ' '.join(chunk for chunk in lines if chunk)
            return text
        except Exception as e:
            logger.error(f"Error processing URL: {e}")
            return ""

    def process_docx(self, file_content):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(BytesIO(file_content))
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            logger.error(f"Error processing DOCX: {e}")
            return ""

class EntityExtractor:
    def __init__(self):
        self.nlp = nlp
        self.entity_types = {
            'PERSON': 'Person',
            'ORG': 'Organization',
            'GPE': 'Location',
            'DATE': 'Date',
            'MONEY': 'Money',
            'PRODUCT': 'Product'
        }

    def extract_entities(self, text):
        """Extract entities from text using spaCy"""
        doc = self.nlp(text)
        entities = {}
        
        for ent in doc.ents:
            if ent.label_ in self.entity_types:
                entity_type = self.entity_types[ent.label_]
                if entity_type not in entities:
                    entities[entity_type] = set()
                entities[entity_type].add(ent.text)

        # Convert sets to lists for JSON serialization
        return {k: list(v) for k, v in entities.items()}

    def extract_relationships(self, text):
        """Extract basic relationships between entities"""
        doc = self.nlp(text)
        relationships = []

        for sent in doc.sents:
            doc_sent = self.nlp(sent.text)
            for token in doc_sent:
                if token.dep_ in ('nsubj', 'nsubjpass') and token.head.pos_ == 'VERB':
                    for obj in token.head.children:
                        if obj.dep_ in ('dobj', 'pobj'):
                            relationships.append({
                                'subject': token.text,
                                'predicate': token.head.text,
                                'object': obj.text
                            })

        return relationships

def build_knowledge_graph(entities, relationships):
    """Build knowledge graph from extracted entities and relationships"""
    g = Graph()
    ns = Namespace("http://example.org/")
    g.bind("ex", ns)

    # Add entities
    for entity_type, entity_list in entities.items():
        for entity in entity_list:
            entity_uri = URIRef(ns[re.sub(r'\s+', '_', entity)])
            g.add((entity_uri, RDF.type, ns[entity_type]))

    # Add relationships
    for rel in relationships:
        subj_uri = URIRef(ns[re.sub(r'\s+', '_', rel['subject'])])
        obj_uri = URIRef(ns[re.sub(r'\s+', '_', rel['object'])])
        pred_uri = URIRef(ns[re.sub(r'\s+', '_', rel['predicate'])])
        g.add((subj_uri, pred_uri, obj_uri))

    return g

def visualize_graph(graph):
    """Create interactive visualization of the knowledge graph"""
    G = nx.Graph()
    
    # Add nodes and edges
    for s, p, o in graph:
        s_label = str(s).split('/')[-1]
        o_label = str(o).split('/')[-1]
        p_label = str(p).split('/')[-1]
        
        G.add_node(s_label)
        G.add_node(o_label)
        G.add_edge(s_label, o_label, label=p_label)

    # Create layout
    pos = nx.spring_layout(G)
    
    # Create edge trace
    edge_x = []
    edge_y = []
    edge_text = []
    
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_text.append(edge[2].get('label', ''))

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='text',
        mode='lines',
        text=edge_text
    )

    # Create node trace
    node_x = []
    node_y = []
    node_text = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition='bottom center',
        marker=dict(
            size=20,
            color='#1f77b4',
            line_width=2
        )
    )

    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=0,l=0,r=0,t=0),
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                   ))
    
    return fig

def main():
    st.title("Automated Knowledge Graph Builder")
    
    # Initialize processors
    doc_processor = DocumentProcessor()
    entity_extractor = EntityExtractor()
    
    # Input method selection
    input_method = st.radio(
        "Choose input method",
        ["File Upload", "URL Input"]
    )
    
    extracted_text = ""
    
    if input_method == "File Upload":
        uploaded_file = st.file_uploader(
            "Choose a file", 
            type=['pdf', 'png', 'jpg', 'jpeg', 'docx']
        )
        
        if uploaded_file:
            file_content = uploaded_file.read()
            file_type = uploaded_file.type.split('/')[-1]
            
            with st.spinner('Processing file...'):
                if file_type in ['png', 'jpg', 'jpeg']:
                    extracted_text = doc_processor.process_image(file_content)
                elif file_type == 'pdf':
                    extracted_text = doc_processor.process_pdf(file_content)
                elif file_type == 'docx':
                    extracted_text = doc_processor.process_docx(file_content)
                
    else:
        url = st.text_input("Enter URL:")
        if url and st.button("Process URL"):
            with st.spinner('Processing URL...'):
                extracted_text = doc_processor.process_url(url)
    
    if extracted_text:
        st.subheader("Extracted Text")
        with st.expander("Show extracted text"):
            st.text(extracted_text)
        
        # Extract entities and relationships
        with st.spinner('Extracting entities and relationships...'):
            entities = entity_extractor.extract_entities(extracted_text)
            relationships = entity_extractor.extract_relationships(extracted_text)
        
        # Display extracted information
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Extracted Entities")
            st.write(entities)
        with col2:
            st.subheader("Extracted Relationships")
            st.write(relationships)
        
        # Build and visualize knowledge graph
        if st.button("Generate Knowledge Graph"):
            with st.spinner('Generating knowledge graph...'):
                graph = build_knowledge_graph(entities, relationships)
                
                st.subheader("Knowledge Graph Visualization")
                fig = visualize_graph(graph)
                st.plotly_chart(fig, use_container_width=True)
                
                # Download options
                st.download_button(
                    label="Download Graph (TTL)",
                    data=graph.serialize(format="turtle"),
                    file_name="knowledge_graph.ttl",
                    mime="text/turtle"
                )

if __name__ == "__main__":
    main()