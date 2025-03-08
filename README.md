<h1 align="center">
    <span style="font-size: 125px;">📦</span></br>
    <span style="font-size: 125px;">agentproxy</span>
  <br>
  <a href="https://github.com/yourusername/showprompt">
    <img src="https://img.shields.io/badge/%F0%9F%9B%A1%EF%B8%8F%20transparency-first-00ACD7.svg?style=flat-square">
  </a>
  <a href="https://github.com/yourusername/showprompt">
    <img src="https://img.shields.io/badge/%F0%9F%94%8D%20prompt-visibility-75C46B?style=flat-square">
  </a>
</h1>

<p align="center">
  <em>A simple HTTP proxy for AI agents.</em>
</p>

---

```python
import agentproxy
```
```bash
pip install agentproxy
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

### OpenAI

```python
import agentproxy

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
