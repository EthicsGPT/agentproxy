from allow_agent import *

@request
def request(url, method, headers, body):
    if "France" in str(body):
        return False
    return True

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import asyncio
from dotenv import load_dotenv
load_dotenv()

async def main():
    # Initialize the language model
    llm = ChatOpenAI(model="gpt-4o")
    
    # Create a prompt template
    prompt = ChatPromptTemplate.from_template(
        "You are a helpful assistant. Answer the following question: {question}"
    )
    
    # Create a simple chain: prompt -> llm -> output parser
    chain = prompt | llm | StrOutputParser()
    
    # Run the chain
    response = await chain.ainvoke({"question": "What is the capital of France?"})
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
