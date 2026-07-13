from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-demo")

THREADS = [
    {"id": 1, "title": "Welcome to MCP"},
    {"id": 2, "title": "Getting Started with Servers"},
    {"id": 3, "title": "Building Custom Tools"},
]


@mcp.tool()
def list_threads() -> list[dict]:
    """Return the list of available threads."""
    return THREADS


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
