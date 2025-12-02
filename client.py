# from langchain_mcp_adapters.client import MultiServerMCPClient
# from langgraph.prebuilt import create_react_agent
# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# import os, asyncio

# # Load API Key from .env
# load_dotenv()
# api_key = os.getenv("GOOGLE_API_KEY")

# async def main():
#     # Connect to MCP tool
#     client = MultiServerMCPClient({
#         "stock_tools": {  # MUST match the FastMCP name
#             "url": "http://localhost:8000/mcp",
#             "transport": "streamable_http",
#         }
#     })

#     tools = await client.get_tools()
#     print("🛠️ Tools Loaded:", tools)  # Debug

#     # Manually improve tool description (helps Gemini match it better)
#     tools[0].description = "Get current stock price by symbol like TSLA or AAPL."

#     # Load Gemini model
#     model = ChatGoogleGenerativeAI(
#         model="gemini-1.5-flash",
#         google_api_key=api_key,
#         temperature=0.7,
#     )

#     agent = create_react_agent(model, tools)

#     response = await agent.ainvoke({
#         "messages": [
#             {"role": "user", "content": "get stock price of Apple"}
#         ]
#     })

#     print("📊 AI response:", response['messages'][-1].content)

# # Run the async agent
# asyncio.run(main())


# from langchain_mcp_adapters.client import MultiServerMCPClient
# from langgraph.prebuilt import create_react_agent
# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# import os
# import asyncio

# # Load environment variable
# load_dotenv()
# api_key = os.getenv("GOOGLE_API_KEY")

# async def get_stock_agent():
#     # Step 1: Connect to MCP tool
#     client = MultiServerMCPClient({
#         "stock_tools": {  # Must match FastMCP("stock_tools")
#             "url": "http://localhost:8000/mcp",
#             "transport": "streamable_http",
#         }
#     })

#     # Step 2: Get tools
#     tools = await client.get_tools()

#     # Safety check: ensure tool exists
#     if not tools:
#         raise Exception("❌ No tools found. Make sure MCP server is running.")

#     # Step 3: Add strong description to improve Gemini matching
#     tools[0].name = "get_stock_price"
#     tools[0].description = (
#         "Get the current real-time stock price of a company by its stock symbol "
#         "(e.g., TSLA, AAPL, GOOGL). Returns price, change %, and last update timestamp."
#     )

#     # Step 4: Load Gemini model
#     model = ChatGoogleGenerativeAI(
#         model="gemini-1.5-flash",  # or gemini-pro
#         google_api_key=api_key,
#         temperature=0.7,
#     )

#     # Step 5: Return the React agent
#     return create_react_agent(model, tools)


# ya third clint ka test klea 

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_community.llms import HuggingFaceHub
from dotenv import load_dotenv
import os
import asyncio

# Load Hugging Face API key
load_dotenv()
hf_api_key = os.getenv("HUGGINGFACE_API_KEY")

async def get_stock_agent():
    client = MultiServerMCPClient({
        "stock_tools": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http",
        }
    })

    tools = await client.get_tools()
    if not tools:
        raise RuntimeError("❌ No tools found. Is the MCP server running?")

    tool = tools[0]
    tool.name = "get_stock_price"
    tool.description = "Get current stock price for a given symbol like TSLA, AAPL, etc."

    # ✅ Use a small public model
    model = HuggingFaceHub(
        repo_id="google/flan-t5-base",  # 🔄 You can try others too
        huggingfacehub_api_token=hf_api_key,
        model_kwargs={"temperature": 0.5, "max_new_tokens": 128}
    )

    return create_react_agent(model, [tool])
