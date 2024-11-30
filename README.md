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
To run the Streamlit app, navigate to the `deployment` directory and run:
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