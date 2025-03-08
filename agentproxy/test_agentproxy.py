import unittest
import agentproxy

class TestAgentProxy(unittest.TestCase):
    def test_import(self):
        """Test that the package can be imported"""
        self.assertIsNotNone(agentproxy)
    
    def test_version(self):
        """Test that the package has a version"""
        self.assertIsNotNone(agentproxy.__version__)

if __name__ == "__main__":
    unittest.main() 