import unittest
import allow_agent

class Testallow_agent(unittest.TestCase):
    def test_import(self):
        """Test that the package can be imported"""
        self.assertIsNotNone(allow_agent)
    
    def test_version(self):
        """Test that the package has a version"""
        self.assertIsNotNone(allow_agent.__version__)
    
    def test_request_decorator(self):
        """Test that the request decorator can be used"""
        
        # Clear any existing request filter
        allow_agent._user_request_filter = None
        
        # Define a test filter function
        @allow_agent.request
        def test_filter(url, method, headers, body):
            if "example.com" in url:
                return False
            return True
        
        # Check that the filter function was registered
        self.assertIsNotNone(allow_agent._user_request_filter)
        self.assertEqual(allow_agent._user_request_filter, test_filter)
        
        # Test the filter function with a URL that should be allowed
        self.assertTrue(allow_agent.on_request(
            method="GET",
            url="https://allowed-site.com",
            headers={},
            body=None
        ))
        
        # Test the filter function with a URL that should be blocked
        self.assertFalse(allow_agent.on_request(
            method="GET",
            url="https://example.com/test",
            headers={},
            body=None
        ))

if __name__ == "__main__":
    unittest.main() 