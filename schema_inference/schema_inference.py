import os
import sys
from multi_format_processing.extract_text import extract_text_from_pdf
from .schema_inference_logic import infer_schema
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_dataset(file_path):
    """
    Processes a file or directory of files to infer schemas.

    Args:
        file_path (str): Path to the file or directory.

    Returns:
        dict: Inferred schemas for each document.
    """
    schemas = {}

    logger.info(f"Processing: {file_path}")
    try:
        if os.path.isfile(file_path):
            text = extract_text_from_pdf(file_path)
            if text:
                schema = infer_schema(text)
                schemas[file_path] = schema
            else:
                logger.warning(f"No text extracted from {file_path}. Skipping.")
        elif os.path.isdir(file_path):
            for filename in os.listdir(file_path):
                file_ext = filename.lower().split('.')[-1]
                if file_ext == "pdf":
                    full_path = os.path.join(file_path, filename)
                    text = extract_text_from_pdf(full_path)
                    if text:
                        schema = infer_schema(text)
                        schemas[full_path] = schema
                    else:
                        logger.warning(f"No text extracted from {full_path}. Skipping.")
        else:
            logger.error(f"Invalid path: {file_path}")

    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")

    return schemas


if __name__ == "__main__":
    dataset_dir = "dataset_example"  # Change to your dataset directory
    schemas = process_dataset(dataset_dir)

    if schemas:
        for doc, schema in schemas.items():
            print(f"Schema for {doc}:")
            print(schema)
    else:
        logger.info("No schemas generated.")
