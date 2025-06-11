from typing import Dict, Any
from mcp.server.fastmcp import FastMCP
import httpx


# Constants
FLOW_AI_API_URL = "http://127.0.0.1:8080"
FLOW_AI_CHAT_URL = "http://127.0.0.1:8081"
HTTP_TIMEOUT = 3000.0  # seconds

# Initialize the MCP server
mcp = FastMCP("FlowAI Server")

async def get_request(url: str) -> Dict[str, Any]:
  headers = {
    "Content-Type": "application/json"
  }

  async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
    try:
      response = await client.get(url, headers=headers)
      response.raise_for_status()
      return response.json()
    except httpx.TimeoutException:
      raise Exception(f"Request timed out after {HTTP_TIMEOUT} seconds: {url}")
    except httpx.HTTPError as e:
      raise Exception(f"HTTP error occurred during request to {url}: {str(e)}")

async def post_request(url: str, data: Dict[str, Any]) -> Dict[str, Any]:
  headers = {
    "Content-Type": "application/json"
  }

  async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
    try:
      response = await client.post(url, headers=headers, json=data)
      response.raise_for_status()
      return response.json()
    except httpx.TimeoutException:
      raise Exception(f"Request timed out after {HTTP_TIMEOUT} seconds: {url}")
    except httpx.HTTPError as e:
      raise Exception(f"HTTP error occurred during request to {url}: {str(e)}")


# RESOURCES
@mcp.resource("flowai://agents")
async def get_agents() -> Dict[str, Any] | str:
  """
  Get all agents from the FlowAI server.
  """
  try:
    return await get_request(f"{FLOW_AI_API_URL}/agents")
  except Exception as e:
    return f"Failed to get agents: {str(e)}"


# TOOLS
@mcp.tool("flowai://send-message")
async def send_message(message: str, agent_id: str = "apecoin") -> Dict[str, Any]:
  chat_data = {
    "name": "new-chat",
    "agent_id": agent_id,
    "message": message
  }

  try:
    return await post_request(f"{FLOW_AI_CHAT_URL}/chat-mcp", chat_data)
  except Exception as e:
    return f"Failed to send message: {str(e)}"

if __name__ == "__main__":
  mcp.run()
