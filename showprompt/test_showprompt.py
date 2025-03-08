import unittest
import showprompt

class TestShowPrompt(unittest.TestCase):
    def test_import(self):
        """Test that the package can be imported"""
        self.assertIsNotNone(showprompt)
    
    def test_version(self):
        """Test that the package has a version"""
        self.assertIsNotNone(showprompt.__version__)

if __name__ == "__main__":
    unittest.main() 