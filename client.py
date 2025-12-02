from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os, asyncio

# Load environment variable
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

async def main():
    # Setup MCP Client
    client = MultiServerMCPClient({
        "math": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http",
        }
    })

    tools = await client.get_tools()

    # Use Gemini (Google Generative AI)
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",  # or "gemini-pro"
        google_api_key=api_key,
        temperature=0.7 
    )

    agent = create_react_agent(model, tools)

    response = await agent.ainvoke({
        "messages": [
            {"role": "user", "content": "What is 7 plus 5?"}
        ]
    })

    print("📊 AI response:", response['messages'][-1].content)

# Run async
asyncio.run(main())


