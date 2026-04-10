import asyncio
import os
from typing import Annotated
from pydantic import Field
from dotenv import load_dotenv
from agent_framework import AgentSession, tool
from agent_framework.openai import OpenAIChatCompletionClient

# Import raw functions from tool.py
import tool as tool_module

# ============================================================
# Azure OpenAI Configuration — loaded from .env file
# ============================================================
load_dotenv()
AZURE_KEY = os.getenv("AZURE_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
API_VERSION = os.getenv("API_VERSION", "2024-10-21")

# ============================================================
# Define tools using @tool decorator (Microsoft Agent Framework style)
# Each tool wraps the corresponding function from tool.py
# ============================================================

@tool(description="Add two numbers")
def add(
    a: Annotated[float, Field(description="First number")],
    b: Annotated[float, Field(description="Second number")],
) -> dict:
    return tool_module.add(a, b)

@tool(description="Subtract b from a")
def subtract(
    a: Annotated[float, Field(description="First number")],
    b: Annotated[float, Field(description="Second number")],
) -> dict:
    return tool_module.subtract(a, b)

@tool(description="Multiply two numbers")
def multiply(
    a: Annotated[float, Field(description="First number")],
    b: Annotated[float, Field(description="Second number")],
) -> dict:
    return tool_module.multiply(a, b)

@tool(description="Divide a by b")
def divide(
    a: Annotated[float, Field(description="First number")],
    b: Annotated[float, Field(description="Second number")],
) -> dict:
    return tool_module.divide(a, b)

@tool(description="Get current weather for a city")
def get_weather(
    city: Annotated[str, Field(description="City name")],
) -> dict:
    return tool_module.get_weather(city)

# ============================================================
# System prompt
# ============================================================
SYSTEM_PROMPT = (
    "You are a friendly assistant. "
    "Use the provided tools for math and weather questions. "
    "Never solve math manually — always call the math tools. "
    "If a request is ambiguous, ask a clarifying question."
)

# ============================================================
# Main chat loop
# ============================================================
async def main():
    # Create Azure OpenAI chat client using API key + azure_endpoint
    client = OpenAIChatCompletionClient(
        model=DEPLOYMENT_NAME,
        api_key=AZURE_KEY,
        azure_endpoint=AZURE_ENDPOINT,
        api_version=API_VERSION,
    )

    # Create the agent with tools registered
    agent = client.as_agent(
        name="MathWeatherBot",
        instructions=SYSTEM_PROMPT,
        tools=[add, subtract, multiply, divide, get_weather],
    )

    # Session keeps conversation history across turns
    session = AgentSession()

    print("Chatbot ready! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        if not user_input:
            continue

        try:
            # The framework handles the full tool-calling loop:
            # send → detect tool calls → execute tools → return final response
            response = await agent.run(user_input, session=session)
            print(f"\nAssistant: {response.text}\n")
        except Exception as e:
            print(f"\nError: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())
