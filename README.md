<h1 align="center">
    <img src="https://i.imgur.com/bFiXBTa.png" width="50px" height="50px" style="border-radius: 20px;"></br> 
    <span style="font-size: 125px;">allow-agent</span>
  <br>
  <a href="https://github.com/EthicsGPT/allow-agent">
    <img src="https://img.shields.io/badge/%F0%9F%9B%A1%EF%B8%8F%20transparency-first-00ACD7.svg?style=flat-square">
  </a>
  <a href="https://github.com/EthicsGPT/allow-agent">
    <img src="https://img.shields.io/badge/%F0%9F%94%8D%20prompt-visibility-75C46B?style=flat-square">
  </a>
</h1>

<p align="center">
  <em>A lightweight framework to set allow policy for agents.</em>
</p>

---

```python
from allow_agent import *
```
```bash
pip install allow-agent
```
<br>

### compatibility

| Library | Status | Description |
|------------------|--------|-------------|
| ✅ browser-use       | Ready  | Direct browser usage via CDN/script |
| ✅ langchain     | Ready  | LangChain framework compatibility |
| ✅ openai        | Ready  | OpenAI API integration |
| ✅ anthropic     | Ready  | Anthropic Claude support |
| ✅ aisuite      | Ready  | Full AI framework compatibility |
| ✅ requests      | Ready  | Python HTTP library integration |

<br>

## Examples

### Request Filtering

```python
from allow_agent import *
import requests

@request # blocked example.com
def request(url, method, headers, body):
    if "example.com" in url:
        return False
    else:
        return True

# (requests, urllib, httpx, aiohttp) will be filtered through your function
print(requests.get('https://httpbin.org/get').text) # will print response from httpbin.org
print(requests.get("https://example.com").text) # requests.exceptions.RequestException: Request cancelled by allow-agent.
```
