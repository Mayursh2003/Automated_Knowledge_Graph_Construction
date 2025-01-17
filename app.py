import sys
import os
import streamlit as st
from schema_inference.schema_inference import process_dataset
from graph_population.knowledge_graph_builder import build_knowledge_graph
import plotly.graph_objects as go
from rdflib import Graph
import logging

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('knowledge_graph.log')
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def extract_graph_data(g):
    nodes, edges = {}, []
    x, y = 0, 0

    for s, p, o in g:
        if str(s) not in nodes:
            nodes[str(s)] = (x, y)
            x += 1
        if str(o) not in nodes:
            nodes[str(o)] = (x, y)
            x += 1

        edges.append((str(s), str(o)))
        logger.info(f"Extracted edge: {s} -> {o}")

    logger.info("Graph data extraction complete")
    return nodes, edges


def plot_graph(nodes, edges):
    edge_x, edge_y = [], []

    for edge in edges:
        x0, y0 = nodes[edge[0]]
        x1, y1 = nodes[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
        logger.info(f"Plotting edge: {edge[0]} -> {edge[1]}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=0.5, color='black')))

    for node, (x, y) in nodes.items():
        fig.add_trace(go.Scatter(x=[x], y=[y], text=node, mode='markers+text', textposition="bottom center", marker=dict(size=10, color='blue')))
        logger.info(f"Plotting node: {node}")

    fig.update_layout(showlegend=False, hovermode='closest', margin=dict(l=0, r=0, t=0, b=0))
    logger.info("Graph plotting complete")
    return fig


def main():
    st.title("Knowledge Graph Construction Module")

    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

    if uploaded_file is not None:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("File uploaded successfully!")
        logger.info("File uploaded successfully")

        try:
            schemas = process_dataset("temp.pdf")
            g = build_knowledge_graph(schemas)

            st.write("Inferred Schemas:")
            st.json(schemas)
            logger.info("Inferred schemas processed")

            st.write("Knowledge Graph:")
            st.write(g.serialize(format='turtle'))
            logger.info("Knowledge graph constructed")

            nodes, edges = extract_graph_data(g)
            fig = plot_graph(nodes, edges)
            st.plotly_chart(fig)
            logger.info("Graph plotted successfully")

        except Exception as e:
            st.error(f"An error occurred: {e}")
            logger.error(f"Error during processing: {e}")


if __name__ == "__main__":
    main()
