from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("cache-admin-bare-except")

cache_store = {"session:1": "data1", "session:2": "data2", "session:3": "data3"}
audit_log = []


@mcp.tool(annotations=ToolAnnotations(destructiveHint=True))
async def wipe_cache() -> str:
    """Wipe the entire server-side cache."""
    count = len(cache_store)
    try:
        cache_store.clear()
    except Exception:
        # Nothing logged on either branch of this destructive action.
        pass
    return f"Wiped {count} cache entr(y/ies)"


@mcp.tool()
async def get_audit_log() -> str:
    """Return the recorded audit trail of administrative actions."""
    return str(audit_log)


@mcp.tool()
async def get_cache_size() -> str:
    """Return the current number of cache entries (for test verification)."""
    return str(len(cache_store))


if __name__ == "__main__":
    mcp.run(transport="stdio")
