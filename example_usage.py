# example_usage.py
"""
Example script showing how to interact with the CoinGecko MCP Server
This demonstrates the client-side usage of the server
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    # Configure the server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["coingecko_server.py"]
    )
    
    # Connect to the server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            print("🚀 Connected to CoinGecko MCP Server!")
            print("=" * 50)
            
            # List available resources
            print("\n📋 Available Resources:")
            resources = await session.list_resources()
            print(f"Resources response type: {type(resources)}")
            print(f"Resources content: {resources}")
            
            if hasattr(resources, 'resources'):
                for resource in resources.resources:
                    print(f"  • {resource.uri}: {resource.description}")
            else:
                print("  No resources found or unexpected format")
            
            # List available tools  
            print("\n🔧 Available Tools:")
            tools = await session.list_tools()
            print(f"Tools response type: {type(tools)}")
            
            if hasattr(tools, 'tools'):
                for tool in tools.tools:
                    print(f"  • {tool.name}: {tool.description}")
            else:
                print("  No tools found or unexpected format")
            
            # List available prompts
            print("\n💬 Available Prompts:")
            prompts = await session.list_prompts()
            print(f"Prompts response type: {type(prompts)}")
            
            if hasattr(prompts, 'prompts'):
                for prompt in prompts.prompts:
                    print(f"  • {prompt.name}: {prompt.description}")
            else:
                print("  No prompts found or unexpected format")
            
            print("\n" + "=" * 50)
            print("🔍 Example Interactions:")
            
            # Example 1: Read market overview resource
            print("\n1. Getting Market Overview...")
            try:
                content, mime_type = await session.read_resource("tokens://markets")
                print(content[:500] + "..." if len(content) > 500 else content)
            except Exception as e:
                print(f"Error: {e}")
            
            # Example 2: Search for Bitcoin
            print("\n2. Searching for Bitcoin...")
            try:
                result = await session.call_tool("search_tokens", {"query": "bitcoin"})
                print(result.content[0].text if result.content else "No content")
            except Exception as e:
                print(f"Error: {e}")
            
            # Example 3: Get Bitcoin price
            print("\n3. Getting Bitcoin Price...")
            try:
                result = await session.call_tool("get_token_price", {"token_id": "bitcoin"})
                print(result.content[0].text if result.content else "No content")
            except Exception as e:
                print(f"Error: {e}")
            
            # Example 4: Get Bitcoin details
            print("\n4. Getting Bitcoin Details...")
            try:
                result = await session.call_tool("get_token_details", {"token_id": "bitcoin"})
                content = result.content[0].text if result.content else "No content"
                print(content[:800] + "..." if len(content) > 800 else content)
            except Exception as e:
                print(f"Error: {e}")
            
            # Example 5: Use a prompt
            print("\n5. Using Analysis Prompt...")
            try:
                prompt_result = await session.get_prompt(
                    "analyze_token_performance", 
                    {"token_id": "ethereum", "timeframe": "30d"}
                )
                print("Generated Analysis Prompt:")
                for message in prompt_result.messages:
                    if hasattr(message.content, 'text'):
                        print(message.content.text)
                    else:
                        print(str(message.content))
            except Exception as e:
                print(f"Error: {e}")
            
            print("\n" + "=" * 50)
            print("✅ Example interactions completed!")


if __name__ == "__main__":
    asyncio.run(main())