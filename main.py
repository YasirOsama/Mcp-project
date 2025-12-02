import streamlit as st
import asyncio
from client import get_stock_agent  # Your get_stock_agent() with Claude setup

# Page config
st.set_page_config(page_title="📈 Claude Stock Chatbot", page_icon="🤖")
st.title("💬 Ask Stock Prices (Claude + MCP Tool)")

# Load agent once into session state
if "stock_agent" not in st.session_state:
    with st.spinner("🔄 Initializing Claude agent..."):
        st.session_state.stock_agent = asyncio.run(get_stock_agent())

# User input
query = st.text_input("Enter company name or stock symbol (e.g., TSLA, AAPL):")

# Button action
if st.button("Get Stock Price") and query:
    with st.spinner("🧠 Thinking..."):
        try:
            async def ask_agent():
                response = await st.session_state.stock_agent.ainvoke({
                    "messages": [{"role": "user", "content": query}]
                })
                return response["messages"][-1].content

            result = asyncio.run(ask_agent())
            st.success(result)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
