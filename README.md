# Automated Knowledge Graph Construction

## Overview
This project extracts information from multiple formats (PDF, images, etc.), infers schemas, and builds knowledge graphs.

### Features
- Multi-format processing: Handles PDFs, images, and web text.
- Schema inference with dynamic refinement.
- Knowledge graph population and export.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure environment variables:
   ```bash
   export KG_CONSTRUCTION_DATA_DIR=/path/to/data
   export KG_CONSTRUCTION_OUTPUT_DIR=/path/to/output
   ```
3. Run the knowledge graph construction pipeline:
   ```bash
   python main.py
   ```

## Development
### Requirements
- Python 3.8+
- pip 20.0+
- Required libraries: listed in `requirements.txt`

### Code Structure
- `main.py`: Entry point for the knowledge graph construction pipeline
- `data/`: Directory for input data
- `output/`: Directory for output knowledge graphs
- `src/`: Directory for source code
  - `format_handlers/`: Format-specific processing modules
  - `schema_inference/`: Schema inference and refinement modules
  - `knowledge_graph/`: Knowledge graph population and export modules
  - `deployment/`: Streamlit app for deployment
  - `tests/`: Unit tests and integration tests
  - `utils/`: Utility functions for logging, configuration, etc.

### Contributing
Contributions are welcome! Please submit a pull request with a clear description of changes.

### Running the Streamlit App
To run on the Streamlit app, 
  https://automated-knowledge-graph-constructionms.streamlit.app/

```bash
streamlit run app.py
```
Alternatively, you can run the app from the root directory using:
```bash
PYTHONPATH=%cd% && streamlit run deployment/app.py
```

### Improvements
- **Error Handling**: Implement try-except blocks to handle potential errors during pipeline execution.
- **Logging**: Integrate a logging mechanism to track pipeline progress and errors.
- **Code Refactoring**: Refactor code to improve modularity and reusability.
- **Testing**: Develop comprehensive unit tests and integration tests to ensure pipeline reliability.
- **Documentation**: Maintain up-to-date documentation to facilitate collaboration and knowledge sharing.

### Error Handling Example
```python
try:
    # Code that may raise an exception
except Exception as e:
    # Handle the exception
    print(f"An error occurred: {e}")
```

### Logging Example
```python
import logging

# Create a logger
logger = logging.getLogger(__name__)

# Set the logging level
logger.setLevel(logging.INFO)

# Create a file handler
file_handler = logging.FileHandler('pipeline.log')
file_handler.setLevel(logging.INFO)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Log a message
logger.info('Pipeline started')
```

### Code Refactoring Example
```python
# Before refactoring
def process_data(data):
    # Code to process data
    return processed_data

def build_knowledge_graph(processed_data):
    # Code to build knowledge graph
    return knowledge_graph

# After refactoring
class DataProcessor:
    def __init__(self, data):
        self.data = data

    def process(self):
        # Code to process data
        return processed_data

class KnowledgeGraphBuilder:
    def __init__(self, processed_data):
        self.processed_data = processed_data

    def build(self):
        # Code to build knowledge graph
        return knowledge_graph

# Usage
data_processor = DataProcessor(data)
processed_data = data_processor.process()

knowledge_graph_builder = KnowledgeGraphBuilder(processed_data)
knowledge_graph = knowledge_graph_builder.build()
```

### Testing Example
```python
import unittest

class TestDataProcessor(unittest.TestCase):
    def test_process(self):
        # Test the process method
        data_processor = DataProcessor(data)
        processed_data = data_processor.process()
        self.assertEqual(processed_data, expected_processed_data)

class TestKnowledgeGraphBuilder(unittest.TestCase):
    def test_build(self):
        # Test the build method
        knowledge_graph_builder = KnowledgeGraphBuilder(processed_data)
        knowledge_graph = knowledge_graph_builder.build()
        self.assertEqual(knowledge_graph, expected_knowledge_graph)

if __name__ == '__main__':
    unittest.main()
```