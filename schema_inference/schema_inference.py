import os
import sys
from multi_format_processing.extract_text import extract_text_from_pdf
from .schema_inference_logic import infer_schema
from logging import getLogger, Formatter, FileHandler, StreamHandler, INFO

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def process_dataset(file_path):
    schemas = {}
    logger = getLogger(__name__)
    logger.setLevel(INFO)
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = FileHandler('dataset_processing.log')
    file_handler.setFormatter(formatter)
    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.info(f"Processing: {file_path}")
    try:
        text = extract_text_from_pdf(file_path)
        schema = infer_schema(text)
        schemas[file_path] = schema
    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
    return schemas

if __name__ == "__main__":
    dataset_dir = "dataset_example"  # Change to your dataset directory
    schemas = process_dataset(dataset_dir)
    for doc, schema in schemas.items():
        print(f"Schema for {doc}:")
        print(schema)