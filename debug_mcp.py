# debug_mcp.py
"""
Debug script to inspect MCP server responses and structure
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def debug_server():
    # Configure the server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["coingecko_server.py"]
    )
    
    try:
        # Connect to the server
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                print("🔄 Initializing connection...")
                init_result = await session.initialize()
                print(f"✅ Initialization result: {init_result}")
                print(f"   Type: {type(init_result)}")
                print(f"   Attributes: {dir(init_result)}")
                
                print("\n" + "="*60)
                
                # Debug resources
                print("🔍 Debugging Resources...")
                try:
                    resources = await session.list_resources()
                    print(f"Resources type: {type(resources)}")
                    print(f"Resources dir: {[attr for attr in dir(resources) if not attr.startswith('_')]}")
                    print(f"Resources content: {resources}")
                    
                    if hasattr(resources, 'resources'):
                        print(f"Found resources attribute with {len(resources.resources)} items")
                        for i, resource in enumerate(resources.resources):
                            print(f"  Resource {i}: {type(resource)}")
                            print(f"    Attributes: {[attr for attr in dir(resource) if not attr.startswith('_')]}")
                            if hasattr(resource, 'uri'):
                                print(f"    URI: {resource.uri}")
                            if hasattr(resource, 'description'):
                                print(f"    Description: {resource.description}")
                    else:
                        print("No 'resources' attribute found")
                        
                except Exception as e:
                    print(f"❌ Error listing resources: {e}")
                    import traceback
                    traceback.print_exc()
                
                print("\n" + "="*60)
                
                # Debug tools
                print("🔍 Debugging Tools...")
                try:
                    tools = await session.list_tools()
                    print(f"Tools type: {type(tools)}")
                    print(f"Tools dir: {[attr for attr in dir(tools) if not attr.startswith('_')]}")
                    print(f"Tools content: {tools}")
                    
                    if hasattr(tools, 'tools'):
                        print(f"Found tools attribute with {len(tools.tools)} items")
                        for i, tool in enumerate(tools.tools):
                            print(f"  Tool {i}: {type(tool)}")
                            print(f"    Attributes: {[attr for attr in dir(tool) if not attr.startswith('_')]}")
                            if hasattr(tool, 'name'):
                                print(f"    Name: {tool.name}")
                            if hasattr(tool, 'description'):
                                print(f"    Description: {tool.description}")
                    else:
                        print("No 'tools' attribute found")
                        
                except Exception as e:
                    print(f"❌ Error listing tools: {e}")
                    import traceback
                    traceback.print_exc()
                
                print("\n" + "="*60)
                
                # Debug prompts
                print("🔍 Debugging Prompts...")
                try:
                    prompts = await session.list_prompts()
                    print(f"Prompts type: {type(prompts)}")
                    print(f"Prompts dir: {[attr for attr in dir(prompts) if not attr.startswith('_')]}")
                    print(f"Prompts content: {prompts}")
                    
                    if hasattr(prompts, 'prompts'):
                        print(f"Found prompts attribute with {len(prompts.prompts)} items")
                        for i, prompt in enumerate(prompts.prompts):
                            print(f"  Prompt {i}: {type(prompt)}")
                            print(f"    Attributes: {[attr for attr in dir(prompt) if not attr.startswith('_')]}")
                            if hasattr(prompt, 'name'):
                                print(f"    Name: {prompt.name}")
                            if hasattr(prompt, 'description'):
                                print(f"    Description: {prompt.description}")
                    else:
                        print("No 'prompts' attribute found")
                        
                except Exception as e:
                    print(f"❌ Error listing prompts: {e}")
                    import traceback
                    traceback.print_exc()
                
                print("\n" + "="*60)
                
                # Test a simple tool call
                print("🔍 Testing Tool Call...")
                try:
                    result = await session.call_tool("search_tokens", {"query": "bitcoin"})
                    print(f"Tool result type: {type(result)}")
                    print(f"Tool result dir: {[attr for attr in dir(result) if not attr.startswith('_')]}")
                    print(f"Tool result: {result}")
                    
                    if hasattr(result, 'content'):
                        print(f"Content type: {type(result.content)}")
                        print(f"Content: {result.content}")
                        if result.content:
                            print(f"First content item: {result.content[0]}")
                            if hasattr(result.content[0], 'text'):
                                print(f"Text: {result.content[0].text[:200]}...")
                                
                except Exception as e:
                    print(f"❌ Error calling tool: {e}")
                    import traceback
                    traceback.print_exc()
                
    except Exception as e:
        print(f"❌ Connection error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(debug_server())