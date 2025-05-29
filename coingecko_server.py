# coingecko_server.py
import httpx
from typing import Optional, List, Dict, Any
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

# Create the MCP server
mcp = FastMCP("CoinGecko Crypto Server")

# Base URL for CoinGecko API
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

# Cache for tokens list to avoid repeated API calls
_tokens_cache = None


async def get_coingecko_data(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Helper function to fetch data from CoinGecko API"""
    print(f"[DEBUG] Calling get_coingecko_data with endpoint: {endpoint}, params: {params}")
    url = f"{COINGECKO_BASE_URL}/{endpoint}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params or {})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"API request failed: {str(e)}")


# RESOURCES - Expose token data

@mcp.resource("tokens://list")
async def get_tokens_list() -> str:
    """Get the complete list of all cryptocurrencies available on CoinGecko"""
    print("[DEBUG] get_tokens_list called")
    global _tokens_cache
    
    if _tokens_cache is None:
        data = await get_coingecko_data("coins/list")
        _tokens_cache = data
    
    # Format the data nicely
    formatted_tokens = []
    for token in _tokens_cache[:50]:  # Limit to first 50 for readability
        formatted_tokens.append(f"• {token['name']} ({token['symbol'].upper()}) - ID: {token['id']}")
    
    result = "Top 50 Cryptocurrencies:\n\n" + "\n".join(formatted_tokens)
    result += f"\n\n... and {len(_tokens_cache) - 50} more tokens available"
    
    return result


@mcp.resource("tokens://trending")
async def get_trending_tokens() -> str:
    """Get currently trending cryptocurrencies"""
    print("[DEBUG] get_trending_tokens called")
    data = await get_coingecko_data("search/trending")
    
    trending_coins = data.get('coins', [])
    formatted_trending = []
    
    for coin_data in trending_coins:
        coin = coin_data['item']
        formatted_trending.append(
            f"• {coin['name']} ({coin['symbol']}) - Market Cap Rank: {coin.get('market_cap_rank', 'N/A')}"
        )
    
    return "Currently Trending Cryptocurrencies:\n\n" + "\n".join(formatted_trending)


@mcp.resource("tokens://markets")
async def get_market_overview() -> str:
    """Get market overview with top cryptocurrencies by market cap"""
    print("[DEBUG] get_market_overview called")
    data = await get_coingecko_data("coins/markets", {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 20,
        "page": 1,
        "sparkline": False
    })
    
    formatted_markets = []
    for coin in data:
        price = f"${coin['current_price']:,.2f}" if coin['current_price'] else "N/A"
        market_cap = f"${coin['market_cap']:,.0f}" if coin['market_cap'] else "N/A"
        change_24h = f"{coin['price_change_percentage_24h']:.2f}%" if coin['price_change_percentage_24h'] else "N/A"
        
        formatted_markets.append(
            f"• {coin['name']} ({coin['symbol'].upper()})\n"
            f"  Price: {price} | 24h Change: {change_24h} | Market Cap: {market_cap}"
        )
    
    return "Top 20 Cryptocurrencies by Market Cap:\n\n" + "\n\n".join(formatted_markets)


# TOOLS - Provide functionality to interact with token data

@mcp.tool()
async def get_token_price(token_id: str, vs_currency: str = "usd") -> str:
    """
    Get current price and basic market data for a specific cryptocurrency
    
    Args:
        token_id: The CoinGecko ID of the token (e.g., 'bitcoin', 'ethereum')
        vs_currency: Currency to show price in (default: 'usd')
    """
    print(f"[DEBUG] get_token_price called with token_id: {token_id}, vs_currency: {vs_currency}")
    try:
        data = await get_coingecko_data("simple/price", {
            "ids": token_id,
            "vs_currencies": vs_currency,
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true"
        })
        
        if token_id not in data:
            return f"Token '{token_id}' not found. Please check the token ID."
        
        token_data = data[token_id]
        price = token_data.get(vs_currency, "N/A")
        market_cap = token_data.get(f"{vs_currency}_market_cap", "N/A")
        volume_24h = token_data.get(f"{vs_currency}_24h_vol", "N/A")
        change_24h = token_data.get(f"{vs_currency}_24h_change", "N/A")
        
        return (
            f"Token: {token_id.upper()}\n"
            f"Price: {price} {vs_currency.upper()}\n"
            f"24h Change: {change_24h:.2f}%" if isinstance(change_24h, (int, float)) else f"24h Change: {change_24h}\n"
            f"Market Cap: {market_cap}\n"
            f"24h Volume: {volume_24h}"
        )
        
    except Exception as e:
        return f"Error fetching token price: {str(e)}"


@mcp.tool()
async def get_token_details(token_id: str) -> str:
    """
    Get detailed information about a specific cryptocurrency
    
    Args:
        token_id: The CoinGecko ID of the token (e.g., 'bitcoin', 'ethereum')
    """
    print(f"[DEBUG] get_token_details called with token_id: {token_id}")
    try:
        data = await get_coingecko_data(f"coins/{token_id}")
        
        name = data.get('name', 'N/A')
        symbol = data.get('symbol', 'N/A').upper()
        description = data.get('description', {}).get('en', 'No description available')[:500]
        
        market_data = data.get('market_data', {})
        current_price = market_data.get('current_price', {}).get('usd', 'N/A')
        market_cap_rank = data.get('market_cap_rank', 'N/A')
        total_supply = market_data.get('total_supply', 'N/A')
        circulating_supply = market_data.get('circulating_supply', 'N/A')
        
        links = data.get('links', {})
        homepage = links.get('homepage', ['N/A'])[0] if links.get('homepage') else 'N/A'
        
        return (
            f"Name: {name} ({symbol})\n"
            f"Market Cap Rank: {market_cap_rank}\n"
            f"Current Price: ${current_price}\n"
            f"Circulating Supply: {circulating_supply:,.0f}" if isinstance(circulating_supply, (int, float)) else f"Circulating Supply: {circulating_supply}\n"
            f"Total Supply: {total_supply:,.0f}" if isinstance(total_supply, (int, float)) else f"Total Supply: {total_supply}\n"
            f"Homepage: {homepage}\n\n"
            f"Description: {description}..."
        )
        
    except Exception as e:
        return f"Error fetching token details: {str(e)}"


@mcp.tool()
async def search_tokens(query: str) -> str:
    """
    Search for cryptocurrencies by name or symbol
    
    Args:
        query: Search term (token name or symbol)
    """
    print(f"[DEBUG] search_tokens called with query: {query}")
    try:
        data = await get_coingecko_data("search", {"query": query})
        
        coins = data.get('coins', [])
        if not coins:
            return f"No tokens found matching '{query}'"
        
        results = []
        for coin in coins[:10]:  # Limit to top 10 results
            results.append(
                f"• {coin['name']} ({coin['symbol'].upper()}) - ID: {coin['id']}\n"
                f"  Market Cap Rank: {coin.get('market_cap_rank', 'N/A')}"
            )
        
        return f"Search results for '{query}':\n\n" + "\n\n".join(results)
        
    except Exception as e:
        return f"Error searching tokens: {str(e)}"


@mcp.tool()
async def get_token_history(token_id: str, days: int = 7, vs_currency: str = "usd") -> str:
    """
    Get price history for a specific cryptocurrency
    
    Args:
        token_id: The CoinGecko ID of the token
        days: Number of days of history (1, 7, 14, 30, 90, 180, 365)
        vs_currency: Currency to show price in (default: 'usd')
    """
    print(f"[DEBUG] get_token_history called with token_id: {token_id}, days: {days}, vs_currency: {vs_currency}")
    try:
        data = await get_coingecko_data(f"coins/{token_id}/market_chart", {
            "vs_currency": vs_currency,
            "days": days
        })
        
        prices = data.get('prices', [])
        if not prices:
            return f"No price history available for {token_id}"
        
        # Get first and last prices
        first_price = prices[0][1]
        last_price = prices[-1][1]
        change_percent = ((last_price - first_price) / first_price) * 100
        
        # Sample some price points
        sample_size = min(5, len(prices))
        step = len(prices) // sample_size if sample_size > 0 else 1
        
        price_samples = []
        for i in range(0, len(prices), step)[:sample_size]:
            timestamp = prices[i][0]
            price = prices[i][1]
            date = str(pd.to_datetime(timestamp, unit='ms').date()) if 'pd' in globals() else "Date N/A"
            price_samples.append(f"  {date}: ${price:.4f}")
        
        return (
            f"Price History for {token_id.upper()} (Last {days} days):\n\n"
            f"Starting Price: ${first_price:.4f}\n"
            f"Current Price: ${last_price:.4f}\n"
            f"Change: {change_percent:+.2f}%\n\n"
            f"Sample Price Points:\n" + "\n".join(price_samples)
        )
        
    except Exception as e:
        return f"Error fetching token history: {str(e)}"


# PROMPTS - Interactive templates for token analysis

@mcp.prompt()
def analyze_token_performance(token_id: str, timeframe: str = "7d") -> str:
    """
    Generate a prompt to analyze token performance
    
    Args:
        token_id: The CoinGecko ID of the token to analyze
        timeframe: Time period for analysis (7d, 30d, 90d, etc.)
    """
    return f"""Please provide a comprehensive analysis of {token_id} cryptocurrency performance over the {timeframe} timeframe. 

Please use the available tools to gather information about:
1. Current price and market data
2. Detailed token information
3. Price history for the specified timeframe

Based on this data, provide insights on:
- Price trends and volatility
- Market position and ranking
- Key fundamentals (supply, market cap, etc.)
- Notable recent developments

Token to analyze: {token_id}
Timeframe: {timeframe}"""


@mcp.prompt()
def compare_tokens(token1: str, token2: str) -> str:
    """
    Generate a prompt to compare two cryptocurrencies
    
    Args:
        token1: First token ID to compare
        token2: Second token ID to compare
    """
    return f"""Please compare {token1} and {token2} cryptocurrencies across multiple dimensions.

Use the available tools to gather current data for both tokens including:
1. Current prices and market metrics
2. Detailed information for both tokens
3. Recent price performance

Provide a comparison covering:
- Price and market cap comparison
- Technology and use case differences
- Market performance and volatility
- Community and development activity
- Investment considerations

Tokens to compare:
- Token 1: {token1}
- Token 2: {token2}"""


@mcp.prompt()
def market_overview_analysis() -> str:
    """Generate a prompt for overall cryptocurrency market analysis"""
    return """Please provide a comprehensive analysis of the current cryptocurrency market.

Use the available resources and tools to gather:
1. Market overview with top cryptocurrencies
2. Currently trending tokens
3. Price data for major cryptocurrencies (Bitcoin, Ethereum, etc.)

Based on this information, provide insights on:
- Overall market sentiment and trends
- Top performers and underperformers
- Market cap distribution
- Notable trends or patterns
- Key market drivers

Focus on actionable insights and current market dynamics."""


@mcp.prompt()
def token_research_deep_dive(token_id: str) -> list[base.Message]:
    """
    Generate a structured conversation for deep token research
    
    Args:
        token_id: Token ID to research
    """
    return [
        base.UserMessage(f"I want to do a deep research dive on {token_id}. Can you help me understand this cryptocurrency comprehensively?"),
        base.AssistantMessage(f"I'd be happy to help you research {token_id}! Let me gather comprehensive information using multiple data points."),
        base.UserMessage("Please start by getting the basic token details and current market data."),
        base.AssistantMessage("I'll collect the fundamental data first, then we can dive deeper into specific aspects like price history, market trends, and comparative analysis. What particular aspects are you most interested in - technical fundamentals, market performance, or competitive positioning?")
    ]


if __name__ == "__main__":
    # Run the server
    mcp.run()