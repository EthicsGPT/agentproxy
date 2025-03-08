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
import allow-agent
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
import allow_agent

# Register a request filter function using the decorator
@allow_agent.request
def request_filter(url, method, headers, body):
    """
    Filter HTTP requests based on your own criteria
    Returns:
        - False to block the request
        - True to allow the request
    """
    # Block requests to specific domains
    if "domain.com" in url:
        return False
    
    # Allow all other requests
    return True

# Now all HTTP requests made using standard Python libraries
# (requests, urllib, httpx, aiohttp) will be filtered through your function
```

### OpenAI

```python
import allow_agent

# Basic usage with OpenAI
from openai import OpenAI
client = OpenAI(api_key="your-api-key")
response = client.chat.completions.create(
    model="gpt-o1",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "This is a test prompt."}
    ]
)
print(response.choices[0].message.content)
