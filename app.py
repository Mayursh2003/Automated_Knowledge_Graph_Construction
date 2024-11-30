import sys
import os
import streamlit as st
from schema_inference.schema_inference import process_dataset
from graph_population.knowledge_graph_builder import build_knowledge_graph
import plotly.graph_objects as go
import streamlit as st
from rdflib import Graph

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def extract_graph_data(g):
    nodes = {}
    edges = []
    
    # Example coordinates for nodes (you can modify this logic as needed)
    x, y = 0, 0
    for s, p, o in g:
        # Add nodes with some coordinates (you can implement your own logic)
        if str(s) not in nodes:
            nodes[str(s)] = (x, y)
            x += 1  # Increment x for next node (simple layout logic)
        if str(o) not in nodes:
            nodes[str(o)] = (x, y)
            x += 1  # Increment x for next node (simple layout logic)
        
        edges.append((str(s), str(o)))

    return nodes, edges

def plot_graph(nodes, edges):
    edge_x = []
    edge_y = []
    
    for edge in edges:
        x0, y0 = nodes[edge[0]]  # Accessing coordinates from the nodes dictionary
        x1, y1 = nodes[edge[1]]  # Accessing coordinates from the nodes dictionary
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)  # None to break the line
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)  # None to break the line

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=0.5, color='black')))
    
    # Add nodes
    for node, (x, y) in nodes.items():  # Iterate through the nodes dictionary
        fig.add_trace(go.Scatter(x=[x], y=[y], text=node, mode='markers+text', textposition="bottom center", marker=dict(size=10, color='blue')))

    fig.update_layout(showlegend=False, hovermode='closest', margin=dict(l=0, r=0, t=0, b=0))
    return fig

def main():
    st.title("Knowledge Graph Construction Module")
    
    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
    
    if uploaded_file is not None:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success("File uploaded successfully!")

        # Process the uploaded file
        schemas = process_dataset("temp.pdf")
        g = build_knowledge_graph(schemas)

        st.write("Inferred Schemas:")
        st.json(schemas)

        st.write("Knowledge Graph:")
        st.write(g.serialize(format='turtle'))

        # Extract graph data
        nodes, edges = extract_graph_data(g)

        # Plot the graph
        fig = plot_graph(nodes, edges)
        st.plotly_chart(fig)

def main():
    st.title("Knowledge Graph Construction Module")
    
    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
    
    if uploaded_file is not None:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success("File uploaded successfully!")

        # Process the uploaded file
        schemas = process_dataset("temp.pdf")
        g = build_knowledge_graph(schemas)

        st.write("Inferred Schemas:")
        st.json(schemas)

        st.write("Knowledge Graph:")
        st.write(g.serialize(format='turtle'))

        # Extract graph data
        nodes, edges = extract_graph_data(g)

        # Plot the graph
        fig = plot_graph(nodes, edges)
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()