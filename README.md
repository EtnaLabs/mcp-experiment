# CoinGecko MCP Server

A comprehensive Model Context Protocol (MCP) server that integrates with the CoinGecko API to provide real-time cryptocurrency data, market analysis, and research tools for LLM applications like Claude Desktop.

<div align="center">

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-compatible-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## 🚀 Features

### 📊 Resources (Data Access)
- **Complete Token Database**: Access to 10,000+ cryptocurrencies from CoinGecko
- **Market Overview**: Real-time market data for top cryptocurrencies  
- **Trending Analysis**: Currently trending tokens and market movements

### 🛠️ Tools (Interactive Functions)
- **Price Lookup**: Get current prices, market caps, and 24h changes
- **Token Search**: Find cryptocurrencies by name or symbol
- **Detailed Analysis**: Comprehensive token information and fundamentals
- **Historical Data**: Price history and performance tracking

### 💭 Prompts (AI Analysis Templates)
- **Performance Analysis**: Deep-dive token performance evaluation
- **Comparative Research**: Side-by-side cryptocurrency comparisons  
- **Market Intelligence**: Overall market trend analysis
- **Investment Research**: Structured research conversation flows

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- MCP Python SDK

### Quick Start

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd coingecko-mcp-server
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Test the server:**
```bash
mcp dev coingecko_server.py
```

4. **Install in Claude Desktop:**
```bash
mcp install coingecko_server.py --name "CoinGecko Crypto Server"
```

## 🔧 Usage

### In Claude Desktop

Once installed, interact with the server through natural language:

```
🗣️ "Show me the current cryptocurrency market overview"
🗣️ "What's Bitcoin's price and how has it performed this week?"
🗣️ "Compare Ethereum and Solana across multiple metrics"
🗣️ "Which cryptocurrencies are trending right now?"
🗣️ "Give me a detailed analysis of Cardano"
```

### Available Resources

| Resource | URI | Description |
|----------|-----|-------------|
| Token List | `tokens://list` | Complete cryptocurrency database |
| Market Data | `tokens://markets` | Top tokens by market cap |
| Trending | `tokens://trending` | Currently trending cryptocurrencies |

### Available Tools

| Tool | Parameters | Description |
|------|------------|-------------|
| `get_token_price` | `token_id`, `vs_currency` | Current price and market data |
| `get_token_details` | `token_id` | Comprehensive token information |
| `search_tokens` | `query` | Search by name or symbol |
| `get_token_history` | `token_id`, `days`, `vs_currency` | Historical price data |

### Available Prompts

| Prompt | Parameters | Use Case |
|--------|------------|----------|
| `analyze_token_performance` | `token_id`, `timeframe` | Performance analysis |
| `compare_tokens` | `token1`, `token2` | Comparative research |
| `market_overview_analysis` | None | Market intelligence |
| `token_research_deep_dive` | `token_id` | Investment research |

## 📈 Example Use Cases

### 1. Market Research
```python
# Get market overview
resource_data = await read_resource("tokens://markets")

# Search for specific tokens
search_results = await call_tool("search_tokens", {"query": "ethereum"})
```

### 2. Price Analysis
```python
# Get current Bitcoin price
btc_price = await call_tool("get_token_price", {"token_id": "bitcoin"})

# Get 30-day price history
btc_history = await call_tool("get_token_history", {
    "token_id": "bitcoin", 
    "days": 30
})
```

### 3. Comparative Analysis
```python
# Use prompt for structured comparison
comparison = await get_prompt("compare_tokens", {
    "token1": "bitcoin",
    "token2": "ethereum"
})
```

## 🏗️ Development

### Project Structure
```
├── coingecko_server.py     # Main MCP server implementation
├── example_usage.py        # Client usage examples
├── debug_mcp.py           # Debug and testing utilities
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

### Running Examples

**Test client interaction:**
```bash
python example_usage.py
```

**Debug server responses:**
```bash
python debug_mcp.py
```

**Development mode with hot reload:**
```bash
mcp dev coingecko_server.py
```

### Adding Custom Features

Extend the server with custom tools:

```python
@mcp.tool()
async def your_custom_analysis(token_id: str) -> str:
    """Your custom cryptocurrency analysis"""
    # Your implementation here
    return analysis_result
```

Add new resources:

```python
@mcp.resource("tokens://your-endpoint")
async def your_custom_resource() -> str:
    """Your custom data endpoint"""
    # Your implementation here
    return data
```

## 🔑 API Information

### CoinGecko API Details
- **Rate Limits**: 10-30 requests/minute (free tier)
- **No API Key Required**: Uses public endpoints
- **Data Coverage**: 10,000+ cryptocurrencies
- **Update Frequency**: Real-time to 5-minute delays

### Common Token IDs
| Cryptocurrency | Token ID |
|----------------|----------|
| Bitcoin | `bitcoin` |
| Ethereum | `ethereum` |
| Binance Coin | `binancecoin` |
| Cardano | `cardano` |
| Solana | `solana` |
| Polkadot | `polkadot` |
| Dogecoin | `dogecoin` |

*Use the search tool to find IDs for other tokens*

## 🛡️ Error Handling

The server includes comprehensive error handling for:

- ✅ API rate limiting and network failures
- ✅ Invalid token IDs and malformed requests  
- ✅ CoinGecko API outages and timeouts
- ✅ Data parsing and formatting errors

## 📊 Performance Features

- **Intelligent Caching**: Reduces API calls for frequently accessed data
- **Async Operations**: Non-blocking HTTP requests for better performance
- **Rate Limit Awareness**: Built-in handling of API constraints
- **Efficient Data Formatting**: Optimized response formatting

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Test thoroughly**: `mcp dev coingecko_server.py`
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Guidelines

- Follow Python PEP 8 style guidelines
- Add docstrings to all functions
- Include error handling for API calls
- Test with both `mcp dev` and example clients
- Update documentation for new features

## 📋 Requirements

### System Requirements
- Python 3.8+
- Internet connection for CoinGecko API
- 50MB+ available memory for token caching

### Python Dependencies
```
mcp[cli]>=1.0.0
httpx>=0.24.0
pandas>=1.5.0  # Optional, for advanced data processing
```

## 🚨 Limitations

- **Free API Tier**: Rate limited to 10-30 requests/minute
- **Public Data Only**: No access to premium CoinGecko features
- **No Real-time Streaming**: Polling-based data updates only
- **Historical Data**: Limited to what CoinGecko provides in free tier

## 🔍 Troubleshooting

### Common Issues

**"Resources showing as tuple with 'Meta'"**
- Run `debug_mcp.py` to inspect server responses
- Ensure you're using the latest MCP SDK version

**"API request failed" errors**
- Check your internet connection
- Verify CoinGecko API status
- Reduce request frequency if rate limited

**"Token not found"**
- Use the search tool to find correct token IDs
- Check spelling and use lowercase IDs (e.g., 'bitcoin', not 'Bitcoin')

**Server won't start**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (must be 3.8+)

### Getting Help

1. Check the [CoinGecko API documentation](https://docs.coingecko.com/reference/introduction)
2. Review [MCP specification](https://modelcontextprotocol.io/)
3. Run `debug_mcp.py` for detailed debugging information
4. Open an issue with error logs and system details

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CoinGecko](https://coingecko.com/) for providing comprehensive cryptocurrency data
- [Anthropic](https://anthropic.com/) for the MCP specification and SDK
- The open-source community for continuous improvements and feedback

## 🔗 Links

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [CoinGecko API Documentation](https://docs.coingecko.com/)
- [Claude Desktop](https://claude.ai/download)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

<div align="center">

**Built with ❤️ for the crypto community**

[Report Bug](../../issues) · [Request Feature](../../issues) · [Contribute](../../pulls)

</div>