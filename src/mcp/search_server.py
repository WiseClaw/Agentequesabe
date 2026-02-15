from mcp.server.fastmcp import FastMCP
from duckduckgo_search import DDGS

mcp = FastMCP("WiseClaw Search")

@mcp.tool()
def web_search(query: str, max_results: int = 5) -> list:
    """Realiza uma pesquisa na web via DuckDuckGo."""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=max_results)]
            return results
    except Exception as e:
        return [{"error": str(e)}]

if __name__ == "__main__":
    mcp.run()
