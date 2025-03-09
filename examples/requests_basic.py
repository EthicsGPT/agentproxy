from allow_agent import *
import requests

@request
def request(url, method, headers, body):
    print("LOG: ", url, body)

response = requests.get("https://www.example.com")
print(response)