
import unittest
from unittest.mock import patch
from multi_format_processing.extract_text import extract_text_from_pdf

class TestMultiFormatProcessing(unittest.TestCase):
    @patch('multi_format_processing.extract_text.extract_text_from_pdf')
    def test_pdf_extraction(self, mock_extract_text_from_pdf):
        mock_extract_text_from_pdf.return_value = "expected text"
        text = extract_text_from_pdf("example.pdf")
        self.assertEqual(text, "expected text")
        mock_extract_text_from_pdf.assert_called_once_with("example.pdf")

    @patch('multi_format_processing.extract_text.extract_text_from_pdf')
    def test_pdf_extraction_empty_file(self, mock_extract_text_from_pdf):
        mock_extract_text_from_pdf.return_value = ""
        text = extract_text_from_pdf("empty_file.pdf")
        self.assertEqual(text, "")

    @patch('multi_format_processing.extract_text.extract_text_from_pdf')
    def test_pdf_extraction_failure(self, mock_extract_text_from_pdf):
        mock_extract_text_from_pdf.side_effect = FileNotFoundError("File not found")
        with self.assertRaises(FileNotFoundError):
            extract_text_from_pdf("non_existent_file.pdf")

    def test_pdf_extraction_type_error(self):
        with self.assertRaises(TypeError):
            extract_text_from_pdf(123)

if __name__ == "__main__":
    unittest.main()