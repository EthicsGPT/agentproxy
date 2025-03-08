import showprompt

# Example usage with OpenAI
from openai import OpenAI
client = OpenAI(api_key="your-api-key")
user_input = "This is a test prompt."
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_input}
    ]
)
# 📦 safeagent | Allow LLM to use this data? (y/n): 
print(response.choices[0].message.content)