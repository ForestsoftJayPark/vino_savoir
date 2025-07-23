from mcp.server.fastmcp import FastMCP
from langchain_community.tools import YouTubeSearchTool

mcp = FastMCP("Youtube Search")

@mcp.tool()
def search_youtube(query: str) -> str:
    """Return youtube link"""
    tool = YouTubeSearchTool()
    resp = tool.run(query)
    return "\n".join(resp)

if __name__ == "__main__":
    mcp.run(transport="stdio")