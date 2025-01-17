import sys
import os
import unittest
from schema_inference.schema_inference_logic import infer_schema

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestSchemaInference(unittest.TestCase):

    def test_infer_schema_basic_text(self):
        doc = "Paris is the capital of France."
        schema = infer_schema(doc)
        self.assertIsInstance(schema, dict)
        self.assertIn("word_count", schema)
        self.assertIn("unique_entities", schema)
        self.assertEqual(schema["word_count"], 6)
        self.assertIn("Paris", schema["unique_entities"])

    def test_infer_schema_empty_doc(self):
        doc = ""
        with self.assertRaises(RuntimeError):
            infer_schema(doc)

    def test_infer_schema_invalid_input(self):
        doc = None
        with self.assertRaises(RuntimeError):
            infer_schema(doc)

    def test_infer_schema_large_text(self):
        doc = "word " * 1000  # Simulating a large document
        schema = infer_schema(doc)
        self.assertEqual(schema["word_count"], 1000)
        self.assertEqual(len(schema["unique_entities"]), 1)

    def test_infer_schema_special_characters(self):
        doc = "@#$%^&*()_+=-[]{}|;':,.<>/?"
        schema = infer_schema(doc)
        self.assertGreaterEqual(schema["word_count"], 1)

if __name__ == "__main__":
    unittest.main()
