import os
import logging
from PyPDF2 import PdfReader
from pytesseract import image_to_string
from PIL import Image
from bs4 import BeautifulSoup
import requests

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_text_from_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text.strip() if text else None
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        return None

def extract_text_from_image(image_file):
    try:
        img = Image.open(image_file)
        text = image_to_string(img)
        return text.strip() if text else None
    except Exception as e:
        logging.error(f"Error extracting text from image: {e}")
        return None

def extract_text_from_web(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        return text.strip() if text else None
    except Exception as e:
        logging.error(f"Error extracting text from web: {e}")
        return None