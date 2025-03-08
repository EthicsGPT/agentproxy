import allow_agent
import requests

@allow_agent.request # blocked example.com
def request_filter(url, method, headers, body):
    return "example.com" not in url

print(requests.get('https://httpbin.org/get').text) # will print response from httpbin.org
print(requests.get("https://example.com").text) # requests.exceptions.RequestException: Request cancelled by allow-agent.