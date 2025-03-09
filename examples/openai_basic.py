from allow_agent import *
from allow_agent import safety
import openai


# allow-agent handler, logs all LLM requests
@request
def request(url, method, headers, body):
    # Log the LLM request, then return True to allow
    if url == "https://api.openai.com/v1/chat/completions":
        print("logged request:", body["messages"][0])
        return True


# Initialize the OpenAI client
client = openai.OpenAI()

# Example user input
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": input("Enter a message to gpt-4o-mini: ")
        }
    ]
)

# Print the response
print(response)

print("This should get reached.")