import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        average_word_length = sum(len(word) for word in words) / len(words) if words else 0

        schema = {
            "word_count": len(words),
            "unique_entities": list(unique_words),
            "average_word_length": average_word_length,
            "sample_text": text[:100]  # Sample of the first 100 characters
        }

        logger.info("Schema inferred successfully.")
        return schema

    except Exception as e:
        logger.error(f"Error inferring schema: {e}")
        raise RuntimeError(f"Error inferring schema: {e}")
