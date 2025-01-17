import unittest
from unittest.mock import patch
from multi_format_processing.extract_text import extract_text_from_pdf, extract_text_from_image, extract_text_from_web

class TestMultiFormatProcessing(unittest.TestCase):

    # PDF Extraction Tests
    @patch('multi_format_processing.extract_text.extract_text_from_pdf')
    def test_pdf_extraction(self, mock_pdf):
        mock_pdf.return_value = "expected text"
        text = extract_text_from_pdf("example.pdf")
        self.assertEqual(text, "expected text")
        mock_pdf.assert_called_once_with("example.pdf")

    @patch('multi_format_processing.extract_text.extract_text_from_pdf')
    def test_pdf_extraction_empty_file(self, mock_pdf):
        mock_pdf.return_value = ""
        text = extract_text_from_pdf("empty_file.pdf")
        self.assertEqual(text, "")

    @patch('multi_format_processing.extract_text.extract_text_from_pdf')
    def test_pdf_extraction_failure(self, mock_pdf):
        mock_pdf.side_effect = FileNotFoundError("File not found")
        with self.assertRaises(FileNotFoundError):
            extract_text_from_pdf("non_existent_file.pdf")

    def test_pdf_extraction_type_error(self):
        with self.assertRaises(TypeError):
            extract_text_from_pdf(123)

    # Image Extraction Tests
    @patch('multi_format_processing.extract_text.extract_text_from_image')
    def test_image_extraction(self, mock_image):
        mock_image.return_value = "image text"
        text = extract_text_from_image("example.jpg")
        self.assertEqual(text, "image text")
        mock_image.assert_called_once_with("example.jpg")

    # Web Extraction Tests
    @patch('multi_format_processing.extract_text.extract_text_from_web')
    def test_web_extraction(self, mock_web):
        mock_web.return_value = "web page content"
        text = extract_text_from_web("http://example.com")
        self.assertEqual(text, "web page content")
        mock_web.assert_called_once_with("http://example.com")

if __name__ == "__main__":
    unittest.main()
