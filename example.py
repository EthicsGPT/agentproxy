import showprompt

# Example usage with OpenAI
from openai import OpenAI
client = OpenAI(api_key="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")
user_input = "This is a test prompt."
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_input}
    ]
)
print(response.choices[0].message.content)