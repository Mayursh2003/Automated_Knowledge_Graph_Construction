import sys
import os
import unittest
from schema_inference.schema_inference import infer_schema

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestSchemaInference(unittest.TestCase):
    def test_infer_schema(self):
        doc = "Paris is the capital of France."
        schema = infer_schema(doc)
        self.assertIn("GPE", schema["entities"])
        self.assertIsInstance(schema, dict)
        self.assertIn("entities", schema)

    def test_infer_schema_empty_doc(self):
        doc = ""
        schema = infer_schema(doc)
        self.assertEqual(schema, {})

    def test_infer_schema_invalid_doc(self):
        doc = None
        with self.assertRaises(TypeError):
            infer_schema(doc)

if __name__ == "__main__":
    unittest.main()