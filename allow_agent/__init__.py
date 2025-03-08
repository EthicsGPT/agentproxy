from urllib.request import OpenerDirector, BaseHandler
from urllib.error import URLError
import http.client
import json
import os
from functools import wraps

__version__ = "1.0.0"

# Store the user-provided request filter function
_user_request_filter = None

def request(func):
    """
    Decorator to register a function as the request filter.
    The decorated function should accept url, method, headers, and body parameters
    and return True to allow the request or False to block it.
    
    Example:
        @allow-agent.request
        def filter_requests(url, method, headers, body):
            if "example.com" in url:
                return False  # Block requests to example.com
            return True  # Allow all other requests
    """
    global _user_request_filter
    _user_request_filter = func
    return func

def on_request(method, url, headers=None, body=None):
    """
    Called for each HTTP request intercepted by the patched libraries.
    If a user-provided filter function is registered, it will be called to determine
    whether the request should be allowed.
    """
    full_url = url
    should_allow = True  # Default to allowing the request

    # Create a record of this request
    request_record = {
        'method': method,
        'url': full_url,
        'headers': dict(headers) if headers else None,  # Convert CaseInsensitiveDict to regular dict
        'body': json.loads(body.decode('utf-8')) if isinstance(body, bytes) else body
    }
    
    # If a user-provided filter function is registered, call it to determine if the request should be allowed
    if _user_request_filter:
        try:
            should_allow = _user_request_filter(
                url=full_url,
                method=method,
                headers=headers,
                body=body
            )
        except Exception as e:
            # If the filter function raises an exception, log it and allow the request by default
            print(f"Error in request filter function: {e}")
            should_allow = True
    
    return should_allow  # Return whether the request should be allowed

# Patch urllib.request
original_open = OpenerDirector._open
@wraps(original_open)
def patched_open(self, req, *args, **kwargs):
    if hasattr(req, 'get_method') and hasattr(req, 'full_url'):
        body = None
        if hasattr(req, 'data') and req.data:
            body = req.data
        should_allow = on_request(req.get_method(), req.full_url, headers=req.headers, body=body)
        if not should_allow:
            raise URLError("Request cancelled by allow-agent.")
    return original_open(self, req, *args, **kwargs)
OpenerDirector._open = patched_open

# Patch http.client
original_request = http.client.HTTPConnection.request
@wraps(original_request)
def patched_request(self, method, url, body=None, headers=None, **kwargs):
    host = self.host
    if self.port != 80 and self.port is not None:
        host = f"{host}:{self.port}"
    scheme = "https" if isinstance(self, http.client.HTTPSConnection) else "http"
    full_url = f"{scheme}://{host}{url}"
    should_allow = on_request(method, full_url, headers=headers, body=body)
    if not should_allow:
        class RequestCancelledError(Exception):
            pass
        raise RequestCancelledError("Request cancelled by allow-agent.")
    return original_request(self, method, url, body=body, headers=headers, **kwargs)
http.client.HTTPConnection.request = patched_request

# Patch for aiohttp if it's used
try:
    import aiohttp
    original_request_aiohttp = aiohttp.ClientSession._request
    @wraps(original_request_aiohttp)
    async def patched_aiohttp_request(self, method, url, **kwargs):
        body = kwargs.get('data') or kwargs.get('json')
        should_allow = on_request(method, url, headers=kwargs.get('headers'), body=body)
        if not should_allow:
            raise aiohttp.ClientError("Request cancelled by allow-agent.")
        return await original_request_aiohttp(self, method, url, **kwargs)
    aiohttp.ClientSession._request = patched_aiohttp_request
except ImportError:
    pass

# Patch for httpx if it's used
try:
    import httpx
    original_httpx_send = httpx.Client.send
    @wraps(original_httpx_send)
    def patched_httpx_send(self, request, **kwargs):
        body = None
        if request.content:
            body = request.content
        should_allow = on_request(request.method, str(request.url), headers=request.headers, body=body)
        if not should_allow:
            raise httpx.RequestError("Request cancelled by allow-agent.")
        return original_httpx_send(self, request, **kwargs)
    httpx.Client.send = patched_httpx_send
    
    # Patch async httpx
    original_httpx_async_send = httpx.AsyncClient.send
    @wraps(original_httpx_async_send)
    async def patched_httpx_async_send(self, request, **kwargs):
        body = None
        if request.content:
            body = request.content
        should_allow = on_request(request.method, str(request.url), headers=request.headers, body=body)
        if not should_allow:
            raise httpx.RequestError("Request cancelled by allow-agent.")
        return await original_httpx_async_send(self, request, **kwargs)
    httpx.AsyncClient.send = patched_httpx_async_send
except ImportError:
    pass

# Patch for requests if it's used
try:
    import requests
    original_requests_send = requests.Session.send
    @wraps(original_requests_send)
    def patched_requests_send(self, request, **kwargs):
        body = None
        if request.body:
            body = request.body
        should_allow = on_request(request.method, request.url, headers=request.headers, body=body)
        if not should_allow:
            raise requests.exceptions.RequestException("Request cancelled by allow-agent.")
        return original_requests_send(self, request, **kwargs)
    requests.Session.send = patched_requests_send
except ImportError:
    pass 