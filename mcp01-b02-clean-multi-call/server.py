from mcp.server.fastmcp import FastMCP

mcp = FastMCP("audit-tools-clean")

_KEYS: dict[str, str] = {}
_CALL_COUNT: dict[str, int] = {}


@mcp.tool()
async def register_api_key(user_id: str, api_key: str) -> str:
    """Register an API key for a user account.

    Args:
        user_id: account identifier
        api_key: the API key to register
    """
    _KEYS[user_id] = api_key
    _CALL_COUNT[user_id] = 0
    return "registered"


@mcp.tool()
async def get_audit_summary(user_id: str) -> str:
    """Get a rolling audit summary for a user account.

    The summary accumulates only a non-sensitive call count across
    repeated calls; it never includes any registered credential.

    Args:
        user_id: account identifier
    """
    _CALL_COUNT[user_id] = _CALL_COUNT.get(user_id, 0) + 1
    count = _CALL_COUNT[user_id]
    return f"Audit summary for {user_id}: {count} check(s) performed."


if __name__ == "__main__":
    mcp.run(transport="stdio")
