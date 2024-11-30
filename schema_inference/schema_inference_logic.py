import json
from multi_format_processing.extract_text import extract_text_from_pdf

def infer_schema(text):
    """
    Infers schema by analyzing the structure and content of the extracted text.
    
    Args:
        text (str): Text extracted from the document.
    
    Returns:
        dict: Inferred schema as a dictionary.
    """
    try:
        if not text.strip():
            raise ValueError("No text extracted from the document.")
        
        words = text.split()
        unique_words = set(words)

        schema = {
            "word_count": len(words),
            "unique_entities": list(unique_words ),
            "sample_text": text[:100]  # Sample of the first 100 characters
        }
        return schema
    except Exception as e:
        raise RuntimeError(f"Error inferring schema: {e}")