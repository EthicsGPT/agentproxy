import unittest
import agentproxy

class TestAgentProxy(unittest.TestCase):
    def test_import(self):
        """Test that the package can be imported"""
        self.assertIsNotNone(agentproxy)
    
    def test_version(self):
        """Test that the package has a version"""
        self.assertIsNotNone(agentproxy.__version__)
    
    def test_request_decorator(self):
        """Test that the request decorator can be used"""
        
        # Clear any existing request filter
        agentproxy._user_request_filter = None
        
        # Define a test filter function
        @agentproxy.request
        def test_filter(url, method, headers, body):
            if "example.com" in url:
                return False
            return True
        
        # Check that the filter function was registered
        self.assertIsNotNone(agentproxy._user_request_filter)
        self.assertEqual(agentproxy._user_request_filter, test_filter)
        
        # Test the filter function with a URL that should be allowed
        self.assertTrue(agentproxy.on_request(
            method="GET",
            url="https://allowed-site.com",
            headers={},
            body=None
        ))
        
        # Test the filter function with a URL that should be blocked
        self.assertFalse(agentproxy.on_request(
            method="GET",
            url="https://example.com/test",
            headers={},
            body=None
        ))

if __name__ == "__main__":
    unittest.main() 