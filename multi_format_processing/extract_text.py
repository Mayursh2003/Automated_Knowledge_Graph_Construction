import logging
from PyPDF2 import PdfReader
from pytesseract import image_to_string
from PIL import Image
from bs4 import BeautifulSoup
import requests

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file.

    Args:
        pdf_file (str): Path to the PDF file.

    Returns:
        str or None: Extracted text or None if extraction fails.
    """
    try:
        reader = PdfReader(pdf_file)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        if text:
            logging.info(f"Successfully extracted text from PDF: {pdf_file}")
            return text.strip()
        else:
            logging.warning(f"No text found in PDF: {pdf_file}")
            return None
    except Exception as e:
        logging.error(f"Error extracting text from PDF {pdf_file}: {e}")
        return None


def extract_text_from_image(image_file):
    """
    Extracts text from an image file using OCR.

    Args:
        image_file (str): Path to the image file.

    Returns:
        str or None: Extracted text or None if extraction fails.
    """
    try:
        img = Image.open(image_file)
        text = image_to_string(img)
        if text:
            logging.info(f"Successfully extracted text from image: {image_file}")
            return text.strip()
        else:
            logging.warning(f"No text found in image: {image_file}")
            return None
    except Exception as e:
        logging.error(f"Error extracting text from image {image_file}: {e}")
        return None


def extract_text_from_web(url):
    """
    Extracts text content from a web page.

    Args:
        url (str): URL of the webpage.

    Returns:
        str or None: Extracted text or None if extraction fails.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        if text:
            logging.info(f"Successfully extracted text from web page: {url}")
            return text.strip()
        else:
            logging.warning(f"No text found on the web page: {url}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error while accessing {url}: {e}")
        return None
    except Exception as e:
        logging.error(f"Error extracting text from web {url}: {e}")
        return None
