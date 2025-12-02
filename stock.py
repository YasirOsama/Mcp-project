from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("stock_tools")

API_KEY = "EWDv9gcqGDecLXnia8FJ3QB8hPnGHDSi"  # Use your real API key

@mcp.tool()
def get_stock_price(symbol: str) -> str:
    """
    Get current stock price for a given symbol like AAPL, TSLA.
    """
    url = f"https://financialmodelingprep.com/api/v3/quote/{symbol.upper()}?apikey={API_KEY}"
    response = requests.get(url)

    print("✅ API Response:", response.status_code, response.text)  # Debug log

    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return (
            f"📊 {data['name']} ({data['symbol']})\n"
            f"💵 Price: ${data['price']}\n"
            f"📈 Change: {data['changesPercentage']}%\n"
            f"⏰ Last Updated: {data['timestamp']}"
        )
    else:
        return "❌ Symbol not found or API error."

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
